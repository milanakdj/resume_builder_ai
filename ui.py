import gradio as gr
from core import main


def generate_resume(job_description, job_name):
    final_path = main(job_description=job_description, job_name=job_name)
    return "Hello ujjwal your new Resume has been created in " + final_path


demo = gr.Interface(
    fn=generate_resume,
    inputs=["textbox", "textbox"],
    outputs="textbox",
    title="Resume generator",
)

if __name__ == "__main__":
    demo.launch()
