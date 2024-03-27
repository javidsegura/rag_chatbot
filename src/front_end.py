import gradio as gr
from scripts.upload_online_docs import UploadFile
from scripts.backend import ChatBot
from scripts.ui_settings import UISettings


js_func = """
function refresh() {
    const url = new URL(window.location);

    if (url.searchParams.get('__theme') !== 'white') {
        url.searchParams.set('__theme', 'white');
        window.location.href = url.href;
    }
}
"""


with gr.Blocks(theme = gr.themes.Base( 
    primary_hue= "neutral",
      secondary_hue="gray"

), js = js_func) as demo:
    with gr.Tabs():
        with gr.TabItem("Socrates"):
            ##############
            # First ROW:
            ##############
            with gr.Row() as row_one:
                with gr.Column(visible=False) as reference_bar: # Reference panel
                    #ref_output = gr.Markdown() # Second alternative
                    ref_output = gr.Textbox(
                     lines=22,
                       max_lines=22,
                        interactive=False,
                         type="text",
                         label="References",
                         show_copy_button=True
                    )

                with gr.Column() as chatbot_output:
                    chatbot = gr.Chatbot(
                        [],
                        elem_id="chatbot",
                        bubble_full_width=False,
                        height=400,
                        container=True,
                        show_copy_button=True,
                        avatar_images=(
                            "/Users/javierdominguezsegura/Programming/Python/Side projects/RAG 4/other/images/user.png", # User picture
                              "/Users/javierdominguezsegura/Programming/Python/Side projects/RAG 4/other/images/system.png"), # LLM picture
                        
                    )
                    # **Adding like/dislike icons
                    chatbot.like(UISettings.feedback, None, None)

            ##############
            # SECOND ROW:
            ##############
            with gr.Row():
                input_txt = gr.Textbox(
                    lines=2,
                    scale=3,
                    placeholder="Message Socrates...",
                    container=False,
                    autofocus=True,
                    autoscroll=True, show_copy_button=True
                )

            ##############
            # Third ROW:
            ##############
            with gr.Row() as row_two:
                #1st button
                text_submit_btn = gr.Button(value="Submit text", size = "sm", scale = 1)

                #2nd button
                upload_btn = gr.UploadButton(
                    "Upload files", file_types=['.pdf'],file_count="multiple", size = "sm", scale = 1)

                #3rd button
                sidebar_state = gr.State(False)
                btn_toggle_sidebar = gr.Button(value="References", size = "sm", scale=1)
                btn_toggle_sidebar.click(UISettings.toggle_sidebar, [sidebar_state], [reference_bar, sidebar_state]) # Activate references when clicking button
                
                #4th element 
                rag_with_dropdown = gr.Dropdown(
                    label="RAG with", choices=["Built-in files Q&A", "Upload file Q&A", "Upload file: Summary"], value="Built-in files Q&A")
                #5th chat
                clear_button = gr.ClearButton([input_txt, chatbot], size="sm", scale = 1, value = "Clear chat") #Clear chat





            ##############
            # Process:
            ##############
            file_msg = upload_btn.upload(fn=UploadFile.process_uploaded_files, inputs=[
                upload_btn, chatbot, rag_with_dropdown], outputs=[input_txt, chatbot], queue=False)

            txt_msg = input_txt.submit(fn=ChatBot.respond,
                                       inputs=[chatbot, input_txt,
                                               rag_with_dropdown],
                                       outputs=[input_txt,
                                                chatbot, ref_output],
                                       queue=False).then(lambda: gr.Textbox(interactive=True),
                                                         None, [input_txt], queue=False)

            txt_msg = text_submit_btn.click(fn=ChatBot.respond,
                                            inputs=[chatbot, input_txt,
                                                    rag_with_dropdown],
                                            outputs=[input_txt,
                                                     chatbot, ref_output],
                                            queue=False).then(lambda: gr.Textbox(interactive=True),
                                                              None, [input_txt], queue=False)


if __name__ == "__main__":

    demo.launch(favicon_path="/Users/javierdominguezsegura/Programming/Python/Side projects/RAG 4/other/images/system.png")
