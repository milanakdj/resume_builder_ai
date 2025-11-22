from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai_like import OpenAILike
from llama_index.llms.google_genai import GoogleGenAI
from pydantic import Field, model_validator

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)
from typing import Optional, Tuple, Type, Any

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

    return llm

def chat_completion(input, system_message=None, schema_cls=None) -> str:
    llm = get_llm()

    chat_list: list[ChatMessage] = []

    if system_message:
        chat_list.append(ChatMessage(role=MessageRole.SYSTEM, content=system_message))

    chat_list.append(ChatMessage(role=MessageRole.USER, content=input))

    response = llm.chat(chat_list)
    return str(
        response.message.content if hasattr(response, "message") else response.content
    )


if __name__ == "__main__":
    print(chat_completion(input = "what is the capital of Nepal?"))