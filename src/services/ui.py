import gradio as gr
import os
from src.services.core import main

INDEX_DIR = "json_files"

def generate_resume(job_name, job_description, input_file_name, it_check:bool):
    final_path = main(job_description=job_description, job_name=job_name, input_file_name = input_file_name, it_check= it_check)
    if it_check:
        return "Hello your new IT Resume has been created in " + final_path
    else:
        return "Hello your new Resume has been created in " + final_path
    
def list_folders():
    """List folders inside INDEX_DIR for dropdown."""
    try:
        global INDEX_DIR
        return [
            f
            for f in os.listdir(INDEX_DIR)
            if os.path.isfile(os.path.join(INDEX_DIR, f))
        ]
    except Exception as e:
        return [f"Error: Unable to list folders {str(e)}"]

folder_dropdown = gr.Dropdown(choices=list_folders(), label="Select Folder", value=None)



def ui():
    with gr.Blocks(title="CSAM demo application") as demo:
        gr.Markdown("## Resume Generator")

        with gr.Row():
            job_name_input = gr.Textbox(label="Job Name")
            job_description_input = gr.Textbox(label="Job Description")
        
        with gr.Row():
            folder_dropdown = gr.Dropdown(choices=list_folders(), label="Select Folder", value=None)
            it_checkbox = gr.Checkbox(label="IT job", info="Is it a job related to the field of IT?")
        
        output_text = gr.Textbox(label="Output")
        
        generate_button = gr.Button("Generate Resume")
        generate_button.click(
            fn=generate_resume,
            inputs=[job_name_input, job_description_input, folder_dropdown, it_checkbox],
            outputs=output_text
        )
        def update_items():
            folders = list_folders()
            return gr.update(choices=folders, value=None)
        
        # Dynamically populate the dropdown when the app loads
        demo.load(
            fn=update_items,
            inputs=None,
            outputs=[folder_dropdown]
        )
        
        return demo


def return_gradio_ui(app, auth_dependency):
    demo = ui()
    app = gr.mount_gradio_app(app= app, path = "/gradio_ui", blocks= demo, auth_dependency= auth_dependency)
    return app


if __name__ == "__main__":
    demo = ui()
    demo.launch()
