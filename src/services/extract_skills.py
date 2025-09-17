import time
import yaml
import re
import openai
import os

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_skills_from_job(job_description, current_skills, max_retries=3, retry_delay=2):
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
    attempt = 0
    while attempt < max_retries:
        try:
            prompt = f"""
                Below is a list of skills grouped by categories. 

                Example format:
                skills:
                    Customer-focused service and engagement:
                        - "Ability to understand and respond to customer needs"
                        - "Friendly and helpful demeanor"
                        - "Efficient handling of customer inquiries"
                    
                    Strong communication and teamwork:
                        - "Clearly communicates with team members"
                        - "Listens actively and respectfully"
                        - "Contributes ideas and supports team goals"

                Current Skills:
                {yaml.dump(current_skills)}

                Based on the following job description, extract both the original and any additional relevant technical and soft skills and selected the best 5 skills only.

                Job Description:
                {job_description}

                Return the result strictly in YAML, using the format shown above.
                """

            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract raw content and YAML
            raw_content = response.choices[0].message.content
            match = re.search(r"```yaml\n(.*?)\n```", raw_content, re.DOTALL)
            if match:
                yaml_content = match.group(1).strip()
                return yaml.safe_load(yaml_content)  # Parse YAML response into Python dictionary
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(retry_delay)  # Wait before retrying
            attempt += 1
    
    print(f"All {max_retries} attempts failed. Proceeding with default or empty skills.")
    return {"Skills": {}}  # Return an empty structure on failure



def extract_experiences_from_job(job_description, current_experiences, max_retries=3, retry_delay=2):
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
    attempt = 0
    while attempt < max_retries:
        try:
            prompt = f"""
                Below is a list of skills grouped by categories. 

                Example format:
                experience:
                    - title: "Team Member"
                        company: "Value Village, Toronto, Canada"
                        duration: "Jul 2024"
                        responsibilities:
                        - "Delivered excellent service by assisting customers with product selection and addressing inquiries."
                        - "Maintained visually appealing displays and organized merchandise for easy navigation. "
                    - title: "Team Member "
                        company: "Wendy's, Toronto, ON "
                        duration: "Dec 2022 - Jun 2023 "
                        responsibilities:
                        - "Provided friendly and efficient service at the counter, managing orders with accuracy and speed. "
                        - "Operated POS system, processed payments, and ensured correct change was given. "

                Current Experience:
                {yaml.dump(current_experiences)}

                Based on the following job description, extract both the original and any additional relevant technical and soft experiences and selected the best 3 experiences only.

                Job Description:
                {job_description}

                Return the result strictly in YAML, using the format shown above.
                """

            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract raw content and YAML
            raw_content = response.choices[0].message.content
            match = re.search(r"```yaml\n(.*?)\n```", raw_content, re.DOTALL)
            if match:
                yaml_content = match.group(1).strip()
                
                return yaml.safe_load(yaml_content)  # Parse YAML response into Python dictionary
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(retry_delay)  # Wait before retrying
            attempt += 1
    
    print(f"All {max_retries} attempts failed. Proceeding with default or empty skills.")
    return {"Skills": {}}  # Return an empty structure on failure


def extract_projects_from_job(job_description, current_projects, max_retries=3, retry_delay=2):
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
    attempt = 0
    while attempt < max_retries:
        try:
            prompt = f"""
                Below is a list of projects grouped by categories. 

                Example format:
                projects:
                    - name: "Team Member"
                      responsibilities:
                        - "Delivered excellent service by assisting customers with product selection and addressing inquiries."
                        - "Maintained visually appealing displays and organized merchandise for easy navigation. "
                    - name: "Team Member"
                      responsibilities:
                        - "Delivered excellent service by assisting customers with product selection and addressing inquiries."
                        - "Maintained visually appealing displays and organized merchandise for easy navigation. "
                    

                Current Experience:
                {yaml.dump(current_projects)}

                Based on the following job description, extract both the original and any additional relevant technical and soft projects and selected the best 3 projects only.

                Job Description:
                {job_description}

                Return the result strictly in YAML, using the format shown above.
                """

            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract raw content and YAML
            raw_content = response.choices[0].message.content
            match = re.search(r"```yaml\n(.*?)\n```", raw_content, re.DOTALL)
            if match:
                yaml_content = match.group(1).strip()
                
                return yaml.safe_load(yaml_content)  # Parse YAML response into Python dictionary
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(retry_delay)  # Wait before retrying
            attempt += 1
    
    print(f"All {max_retries} attempts failed. Proceeding with default or empty skills.")
    return {"Projects": {}}  # Return an empty structure on failure



def extract_summary_from_job(job_description, enhanced_skills, enhanced_projects, enhanced_experiences,current_summary ,max_retries=3, retry_delay=2):
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
    attempt = 0
    while attempt < max_retries:
        try:
            prompt = f"""
                Below is a list of skills grouped by categories. 

                Example format:
                summary: >
                    Friendly and engaging team member with strong experience in retail and food service environments, known for delivering exceptional customer experiences. Adept at handling transactions, assisting with product inquiries, and creating welcoming, clean, and organized spaces. Passionate about retail, with a positive attitude and a focus on building customer loyalty through helpful service and effective communication. Quick to adapt, eager to learn, and committed to supporting a collaborative team environment.


                Current Skills:
                {yaml.dump(enhanced_skills)}

                Current Experience:
                {yaml.dump(enhanced_experiences)}

                Current Projects:
                {yaml.dump(enhanced_projects)}


                Based on the following job description, extract a suitable summary that is short ans sweet with a maximum of 3 sentences. availability: Monday to Friday (Weekdays) 5 pm to Closing ; Sunday, Saturday (Weekends) 8am to 11 pm

                Job Description:
                {job_description}

                Return the result strictly in YAML, using the format shown above.
                """

            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract raw content and YAML
            raw_content = response.choices[0].message.content
            match = re.search(r"```yaml\n(.*?)\n```", raw_content, re.DOTALL)
            if match:
                yaml_content = match.group(1).strip()
                
                return yaml.safe_load(yaml_content)  # Parse YAML response into Python dictionary
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(retry_delay)  # Wait before retrying
            attempt += 1
    
    print(f"All {max_retries} attempts failed. Proceeding with default or empty skills.")
    return {"Skills": {}}  # Return an empty structure on failure
