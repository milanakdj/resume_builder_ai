import yaml
from datetime import datetime
from zoneinfo import ZoneInfo

import os
import argparse
from src.extract_skills import (
    extract_skills_from_job,
    extract_experiences_from_job,
    extract_summary_from_job,
    extract_projects_from_job
)
from src.generate_resume import generate_compact_resume
from src.docx_utils import (
    update_resume_with_skills,
    update_resume_with_experience,
    update_resume_with_summary,
    update_resume_with_project
)


def load_resume_skeleton(file_path="resume_skeleton.yaml"):
    """Load the resume skeleton from a YAML file."""
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def main(job_description="", job_name="", it_check:bool = False):
    os.makedirs("./outputs", exist_ok=True)
    file_name = (
        f"{job_name}_" + str(datetime.now(ZoneInfo("Canada/Central")).strftime("%d-%m-%Y_%H-%M-%S")) + ".docx"
    )

    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    args = Namespace(
        job_description=job_description,
        output=f"./outputs/{file_name}",
        generate_pdf=True,
    )

    # Step 1: Load Resume Skeleton
    resume_skeleton = load_resume_skeleton()

    # Step 2: Extract and Enhance Skills
    current_skills = resume_skeleton["skills"]
    if it_check:
        current_projects = resume_skeleton["projects"]
        enhanced_projects = extract_projects_from_job(args.job_description, current_projects)
        print("enhanced projects: ", enhanced_projects, "\n\n")
        updated_resume = update_resume_with_project(resume_skeleton, enhanced_projects)
        updated_resume = update_resume_with_experience(resume_skeleton, {})
        enhanced_experiences = ""
    else:
        current_experiences = resume_skeleton["experience"]
        enhanced_experiences = extract_experiences_from_job(args.job_description, current_experiences)
        print("enhanced experiences: ", enhanced_experiences, "\n\n")
        updated_resume = update_resume_with_experience(resume_skeleton, enhanced_experiences)
        updated_resume = update_resume_with_project(resume_skeleton, {})
        enhanced_projects = ""

    current_summary = resume_skeleton["summary"]

    enhanced_skills = extract_skills_from_job(args.job_description, current_skills)
    print("enhanced skills: ", enhanced_skills, "\n\n")

    enhanced_summary = extract_summary_from_job(args.job_description, enhanced_skills, enhanced_projects, enhanced_experiences,current_summary)
    print("enhanced summary: ", enhanced_summary, "\n\n")

    # Step 3: Update Resume Skeleton with Enhanced Skills
    updated_resume = update_resume_with_skills(resume_skeleton, enhanced_skills)
    updated_resume = update_resume_with_summary(resume_skeleton, enhanced_summary)

    # Step 4: Generate Resume
    generate_compact_resume(
        updated_resume, output_file=args.output, generate_pdf=args.generate_pdf
    )

    return os.path.abspath(args.output)


if __name__ == "__main__":
    main()
