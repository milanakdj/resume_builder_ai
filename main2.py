import yaml
import argparse
from extract_skills import extract_skills_from_job, extract_experiences_from_job, extract_summary_from_job
from generate_resume import generate_compact_resume
from docx_utils import update_resume_with_skills, update_resume_with_experience, update_resume_with_summary

def load_resume_skeleton(file_path="resume_skeleton.yaml"):
    """Load the resume skeleton from a YAML file."""
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

def main():

    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    args = Namespace(
        job_description=""" 
            The Warehouse Associate will understand and complete the goals set by the operations Supervisor and/or Lead. The Associate must also be able to communicate clearly and effectively to ensure they remain on task, especially with other departments in order to ensure constant order flow.
            What You'll Do

            Effectively use systems and processes applicable to the functional department
            Prepare and complete orders for receipt, delivery or pickup according to schedule
            Maintain quality service by accurately and diligently following set processes and company standards
            Be able to work individually but also within small groups
            Maintain a safe working environment by following procedures, rules, and regulations including motor vehicle maintenance 
            Ensure the proper hand off is given to the following shift(s)
            Follow departmental SLA’s
            Performs other incidental and related duties as required
            Working at or above established productivity standards
            Proactively contributes to creating a team environment that is enjoyable, shares suggestions, ideas, and concerns while upholding Crocs Inc. values

            What You'll Bring to the Table 

            Must be 16 years old or older
            High school diploma or equivalent experience
            Good oral and written communication skills
            Good problem-solving skills
            Flexible work schedule (which may include nights, weekends, holidays, and long hours) and regular attendance is necessary 
            The work environment and physical demands described here are representative of those that an employee will encounter while performing the essential functions of this job. Reasonable accommodations may be made to enable individuals with disabilities to perform the essential functions.
            Ability to move merchandise across the warehouse floor
            Ability to place and arrange items on all shelves and racks daily
            Ability to climb and descend ladders carrying merchandise daily
            Ability to lift 30 pounds or more with assistance daily
            Ability to be on your feet for at least 8 hours per shift and to continuously move around all areas of the warehouse daily
            Ability to also be required to stand, walk, kneel, or balance for a duration of time daily
            Ability to read instructions, reports, and information on computer/register screens and to key information into computer daily
            The Company is an Equal Opportunity Employer committed to a diverse and inclusive work environment.

            All qualified applicants will receive consideration for employment without regard to race, color, religion, sex, sexual orientation, gender identity, national origin, or disability, or any other classification protected by law.

            Job Category: Retail    
        """,
        output='./outputs/enhanced_resume2_the_new4.docx',
        generate_pdf=True
        )

    # Step 1: Load Resume Skeleton
    resume_skeleton = load_resume_skeleton()

    # Step 2: Extract and Enhance Skills
    current_skills = resume_skeleton["skills"]
    current_experiences = resume_skeleton["experience"]
    current_summary= resume_skeleton['summary']


    enhanced_skills = extract_skills_from_job(args.job_description, current_skills)
    enhanced_experiences = extract_experiences_from_job(args.job_description, current_experiences)
    enhanced_summary = extract_summary_from_job(args.job_description, current_skills ,current_experiences, current_summary)

    # Step 3: Update Resume Skeleton with Enhanced Skills
    updated_resume = update_resume_with_skills(resume_skeleton, enhanced_skills)
    updated_resume = update_resume_with_experience(resume_skeleton, enhanced_experiences)
    updated_resume = update_resume_with_summary(resume_skeleton, enhanced_summary)

    # Step 4: Generate Resume
    generate_compact_resume(updated_resume, output_file=args.output, generate_pdf=args.generate_pdf)

if __name__ == "__main__":
    main()
