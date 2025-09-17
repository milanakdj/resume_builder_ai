import yaml
from datetime import datetime
from zoneinfo import ZoneInfo


def load_resume_skeleton(file_path="resume_skeleton.yaml"):
    """Load the resume skeleton from a YAML file."""
    with open(file_path, "r") as file:
        return yaml.safe_load(file)



if __name__ == "__main__":
    resume_yaml = load_resume_skeleton("../yaml_files/milan_2025-09-17_19-22-49.yaml")
    print(resume_yaml)
    print(resume_yaml["skills"])