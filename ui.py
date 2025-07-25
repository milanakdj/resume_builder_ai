import gradio as gr
from core import main


def generate_resume(job_description, job_name, it_check:bool):
    final_path = main(job_description=job_description, job_name=job_name, it_check= it_check)
    if it_check:
        return "Hello ujjwal your new IT Resume has been created in " + final_path
    else:
        return "Hello ujjwal your new Resume has been created in " + final_path


demo = gr.Interface(
    fn=generate_resume,
    inputs=["textbox", "textbox",gr.Checkbox(label="IT job", info="Is it a job related to the field of IT?"),],
    outputs="textbox",
    title="Resume generator",
)

if __name__ == "__main__":
    demo.launch()
