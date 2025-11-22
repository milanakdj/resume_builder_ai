import time
import json
import re
import openai
import os
from src.services.utils import retry_with_backoff
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai_like import OpenAILike
from pydantic import Field, model_validator
from llama_index.llms.google_genai import GoogleGenAI
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
    BaseModel
)
from typing import Optional, Tuple, Type, Any
import outlines
import ollama


# openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LLMSettings(BaseSettings):
    api_base: str = Field(description="Base URL for LLM API")
    model_name: str = Field(description="LLM model name")
    api_key: Optional[str] = Field(default=None, description="API key for LLM (set via environment)")
    context_length: int = Field(default=8192, description="Context length for LLM")
    max_new_tokens: int = Field(default=4098, description="Maximum tokens for LLM response")
    temperature : float = Field(default=0.1, description="Temperature")
    timeout : float = Field(default=300, description="Request timeout for api calls")
    enable_embeddings: bool = Field(False, description="Enable embeddings (default: False)")
    embedding_api_base: Optional[str] = Field(default=None, description="Base URL for embedding API")
    embedding_model_name: Optional[str] = Field(default=None, description="Embedding model name")
    embedding_api_key: Optional[str] = Field(default=None, description="API key for embedding")
    tokenizer_path: Optional[str] = Field(default=None, description="Path to custom tokenizer.")
    tokenizer_model: Optional[str] = Field(default="gpt-4o", description="Name of the models supported by tiktoken.")
    extra_arguments: Optional[dict[str, Any]] = Field(default={}, description="Additional API call arguments.")


    @model_validator(mode="after")
    def check_embedding_requirements(self):
        if self.enable_embeddings:
            if not self.embedding_api_base:
                raise ValueError("embedding_api_base is required when enable_embeddings=True")
            if not self.embedding_model_name:
                raise ValueError("embedding_model_name is required when enable_embeddings=True")
        return self


class AppConfig(BaseSettings):
    llm: LLMSettings
    
    
    model_config = SettingsConfigDict(toml_file="settings.toml", extra="allow")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),init_settings)
    
_settings = None

def get_settings() -> AppConfig:
    global _settings
    if _settings is None:
        _settings = AppConfig()
    return _settings


def get_llm():
    settings = get_settings()
    llm_settings = settings.llm

    if llm_settings:
        api_base = llm_settings.api_base or settings.llm.api_base
        api_key = llm_settings.api_key or api_key
        model = llm_settings.model_name or settings.llm.model_name
        temperature = llm_settings.temperature or settings.llm.temperature
        timeout = llm_settings.timeout or settings.llm.timeout
        context_length = llm_settings.context_length or settings.llm.context_length
        max_new_tokens = llm_settings.max_new_tokens or settings.llm.max_new_tokens
        extra_arguments = (
            llm_settings.extra_arguments or settings.llm.extra_arguments or {}
        )

    if "gemini" in model: 
        llm = GoogleGenAI(
            # api_base=api_base,
            api_key=api_key,
            model=model,
            temperature=temperature,
            timeout=timeout,
            context_window=context_length,
            max_tokens=max_new_tokens,
            is_chat_model=True,
            reuse_client=False,
            max_retries=3,
            additional_kwargs={"extra_body": extra_arguments},
        )
    else:
        llm = OpenAILike(
            api_base=api_base,
            api_key=api_key,
            model=model,
            temperature=temperature,
            timeout=timeout,
            context_window=context_length,
            max_tokens=max_new_tokens,
            is_chat_model=True,
            reuse_client=False,
            max_retries=3,
            additional_kwargs={"extra_body": extra_arguments},
        )

    return llm

llm = get_llm()
settings = get_settings()
client = ollama.Client()
model = outlines.from_ollama(
    client,
    settings.llm.model_name,
)

def chat_completion(input, system_message=None, schema_cls=None) -> str:
    llm = get_llm()

    chat_list: list[ChatMessage] = []

    if system_message:
        chat_list.append(ChatMessage(role=MessageRole.SYSTEM, content=system_message))

    chat_list.append(ChatMessage(role=MessageRole.USER, content=input))

    if schema_cls:
        # schema = schema_cls.model_json_schema()
        # response_format = {
        #     "type": "json_schema",
        #     "json_schema": {"name": "json_structured_response", "schema": schema},
        # }
        # response = llm.chat(chat_list, response_format=response_format)

        response = model(chat_list, schema_cls)

        result = schema_cls.model_validate_json(response)

        return result

    response = llm.chat(chat_list)

    return str(
        response.message.content if hasattr(response, "message") else response.content
    )


@retry_with_backoff()
def extract_skills_from_job(job_description, current_skills,):
    """
    Extract skills from a job description with a retry mechanism to handle API failures.
    
    Args:
        job_description (str): The job description.
        current_skills (dict): Current skills data to be passed to the model.
        max_retries (int): Maximum number of retries in case of failure.
        retry_delay (int): Time in seconds to wait before retrying.

    Returns:
        dict: Enhanced skills in structured format or an empty dictionary on failure.
    """
    prompt = f"""
        Below is a list of skills grouped by categories. 

        Example format:
        {{
            "skills": [
                {{
                "name": "Customer-focused service and engagement",
                "description": [
                    "Ability to understand and respond to customer needs",
                    "Friendly and helpful demeanor",
                    "Efficient handling of customer inquiries"
                ]
                }},
                {{
                "name": "Strong communication and teamwork",
                "description": [
                    "Clearly communicates with team members",
                    "Listens actively and respectfully",
                    "Contributes ideas and supports team goals"
                ]
                }}
            ]
            }}


        Current Skills:
        {json.dumps(current_skills)}

        Based on the following job description, extract both the original and any additional relevant technical and soft skills and selected the best 5 skills only.

        Job Description:
        {job_description}

        Return the result strictly in JSON, using the format shown above.
        """

    class skill(BaseModel):
        name: str
        description: list[str]

    class skills(BaseModel):
        skills: list[skill]

    try:
        response = chat_completion(
            input = prompt,
            schema_cls= skills
        )
            
        response = str(
            response.message.content if hasattr(response, "message") else response.content
        )
        
        # Extract raw content and JSON
        match = re.search(r"```json\n(.*?)\n```", response, re.DOTALL)
        if match:
            json_content = match.group(1).strip()
        return json.loads(json_content)  # Parse JSON response into Python dictionary
        
    except Exception as e:
        print(str(e))         
        return {"Skills": {}}  # Return an empty structure on failure
            

@retry_with_backoff()
def extract_experiences_from_job(job_description, current_experiences, ):
    """
    Extract skills from a job description with a retry mechanism to handle API failures.
    
    Args:
        job_description (str): The job description.
        current_experiences (dict): Current experiences data to be passed to the model.
        max_retries (int): Maximum number of retries in case of failure.
        retry_delay (int): Time in seconds to wait before retrying.

    Returns:
        dict: Enhanced skills in structured format or an empty dictionary on failure.
    """
    
    prompt = f"""
        Below is a list of skills grouped by categories. 

        Example format:
        {{
            "experience": [
                {{
                    "title": "Team Member",
                    "company": "Value Village, Toronto, Canada",
                    "duration": "Jul 2024",
                    "responsibilities": [
                        "Delivered excellent service by assisting customers with product selection and addressing inquiries.",
                        "Maintained visually appealing displays and organized merchandise for easy navigation."
                    ]
                }},
                {{
                    "title": "Team Member",
                    "company": "Wendy's, Toronto, ON",
                    "duration": "Dec 2022 - Jun 2023",
                    "responsibilities": [
                        "Provided friendly and efficient service at the counter, managing orders with accuracy and speed.",
                        "Operated POS system, processed payments, and ensured correct change was given."
                    ]
                }}
            ]
        }}

        Current Experience:
        {json.dumps(current_experiences)}

        Based on the following job description, extract both the original and any additional relevant technical and soft experiences and selected the best 3 experiences only.

        Job Description:
        {job_description}

        Return the result strictly in JSON, using the format shown above.
        """

    class Experience(BaseModel):
        title: str
        company: str
        duration: str
        responsibilities: list[str]

    class Experiences(BaseModel):
        experiences: list[Experience]

    try:
        
        response = chat_completion(
            input = prompt,
            schema_cls= Experiences
        )
        # Extract raw content and JSON
        response = str(
            response.message.content if hasattr(response, "message") else response.content
        )
        match = re.search(r"```json\n(.*?)\n```", response, re.DOTALL)
        if match:
            json_content = match.group(1).strip()
            
        return json.loads(json_content)  # Parse JSON response into Python dictionary
        
    except Exception as e:
        print(str(e))         
        return {"Skills": {}}  # Return an empty structure on failure

@retry_with_backoff()
def extract_projects_from_job(job_description, current_projects):
    """
    Extract skills from a job description with a retry mechanism to handle API failures.
    
    Args:
        job_description (str): The job description.
        current_projects (dict): Current projects data to be passed to the model.
        max_retries (int): Maximum number of retries in case of failure.
        retry_delay (int): Time in seconds to wait before retrying.

    Returns:
        dict: Enhanced skills in structured format or an empty dictionary on failure.
    """
    prompt = f"""
        Below is a list of projects grouped by categories. 

        Example format:
        {{
            "projects": [
                {{
                    "name": "Team Member",
                    "description": "Delivered excellent service by assisting customers with product selection and addressing inquiries. Maintained visually appealing displays and organized merchandise for easy navigation."
                }},
                {{
                    "name": "Team Member",
                    "description": "Delivered excellent service by assisting customers with product selection and addressing inquiries. Maintained visually appealing displays and organized merchandise for easy navigation."
                }}
            ]
        }}

        Current Experience:
        {json.dumps(current_projects)}

        Based on the following job description, extract both the original and any additional relevant technical and soft projects and selected the best 3 projects only.

        Job Description:
        {job_description}

        Return the result strictly in JSON, using the format shown above.
        """
    
    class project(BaseModel):
        name:str
        description:str

    class projects(BaseModel):
        projects: list[project]
    

    
    try:
        response = chat_completion(
        input = prompt,
        schema_cls= projects
        )

        # Extract raw content and JSON
        response = str(
            response.message.content if hasattr(response, "message") else response.content
        )
        match = re.search(r"```json\n(.*?)\n```", response, re.DOTALL)
        if match:
            json_content = match.group(1).strip()
            
        return json.dumps(json_content)  # Parse JSON response into Python dictionary

    
    except Exception as e:
        print(str(e))         
        return {"projects": []}  # Return an empty structure on failure
            
      

@retry_with_backoff()
def extract_summary_from_job(job_description, enhanced_skills, enhanced_projects, enhanced_experiences, current_summary):
    """
    Extract skills from a job description with a retry mechanism to handle API failures.
    
    Args:
        job_description (str): The job description.
        current_experiences (dict): Current skills data to be passed to the model.
        max_retries (int): Maximum number of retries in case of failure.
        retry_delay (int): Time in seconds to wait before retrying.

    Returns:
        dict: Enhanced skills in structured format or an empty dictionary on failure.
    """
    prompt = f"""
        Below is a list of skills grouped by categories. 

        Example format:
            "Friendly and engaging team member with strong experience in retail and food service environments, known for delivering exceptional customer experiences. Adept at handling transactions, assisting with product inquiries, and creating welcoming, clean, and organized spaces. Passionate about retail, with a positive attitude and a focus on building customer loyalty through helpful service and effective communication. Quick to adapt, eager to learn, and committed to supporting a collaborative team environment."
        


        Current Skills:
        {json.dumps(enhanced_skills)}

        Current Experience:
        {json.dumps(enhanced_experiences)}

        Current Projects:
        {json.dumps(enhanced_projects)}


        Based on the following job description, extract a suitable summary that is short ans sweet with a maximum of 3 sentences. availability: Monday to Friday (Weekdays) 5 pm to Closing ; Sunday, Saturday (Weekends) 8am to 11 pm

        Job Description:
        {job_description}

        Return the result strictly in String, using the format shown above.
        """

    response = chat_completion(
        input = prompt,
    )

    try:
        # Extract raw content and JSON
        response = str(
            response.message.content if hasattr(response, "message") else response.content
        )
            
        return {"summary": response}  # Parse JSON response into Python dictionary


    except Exception as e:
        print(str(e))         
        return {"summary": ""}  # Return an empty structure on failure
            

