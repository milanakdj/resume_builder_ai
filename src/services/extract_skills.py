import time
import json
import re
import openai
import os
from src.services.utils import retry_with_backoff

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract raw content and JSON
    raw_content = response.choices[0].message.content
    match = re.search(r"```json\n(.*?)\n```", raw_content, re.DOTALL)
    if match:
        json_content = match.group(1).strip()
        return json.loads(json_content)  # Parse JSON response into Python dictionary
            

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


    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract raw content and JSON
    raw_content = response.choices[0].message.content
    match = re.search(r"```json\n(.*?)\n```", raw_content, re.DOTALL)
    if match:
        json_content = match.group(1).strip()
        
        return json.loads(json_content)  # Parse JSON response into Python dictionary
            

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


    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract raw content and JSON
    raw_content = response.choices[0].message.content
    match = re.search(r"```json\n(.*?)\n```", raw_content, re.DOTALL)
    if match:
        json_content = match.group(1).strip()
        
        return json.dumps(json_content)  # Parse JSON response into Python dictionary
            
      

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
        {{
            "summary": 
            "Friendly and engaging team member with strong experience in retail and food service environments, known for delivering exceptional customer experiences. Adept at handling transactions, assisting with product inquiries, and creating welcoming, clean, and organized spaces. Passionate about retail, with a positive attitude and a focus on building customer loyalty through helpful service and effective communication. Quick to adapt, eager to learn, and committed to supporting a collaborative team environment."
        }}


        Current Skills:
        {json.dumps(enhanced_skills)}

        Current Experience:
        {json.dumps(enhanced_experiences)}

        Current Projects:
        {json.dumps(enhanced_projects)}


        Based on the following job description, extract a suitable summary that is short ans sweet with a maximum of 3 sentences. availability: Monday to Friday (Weekdays) 5 pm to Closing ; Sunday, Saturday (Weekends) 8am to 11 pm

        Job Description:
        {job_description}

        Return the result strictly in JSON, using the format shown above.
        """

    

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract raw content and JSON
    raw_content = response.choices[0].message.content
    match = re.search(r"```json\n(.*?)\n```", raw_content, re.DOTALL)
    if match:
        json_content = match.group(1).strip()
        
        return json.loads(json_content)  # Parse JSON response into Python dictionary
            

