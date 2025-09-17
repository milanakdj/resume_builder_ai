from fastapi import FastAPI
import gradio as gr
app = FastAPI()
@app.get("/")
def read_main():
    return {"message": "This is your main app"}
io = gr.Interface(lambda x: "Hello, " + x + "!", "textbox", "textbox")
app = gr.mount_gradio_app(app, io, path="/gradio")