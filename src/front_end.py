import gradio as gr
from scripts.upload_online_docs import UploadFile
from scripts.backend import ChatBot
from scripts.ui_settings import UISettings
from scripts.transcription import Transcribe


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
      secondary_hue="gray"), 
      js = js_func) as demo:
    with gr.Tab("Model"):
            ##############
            # First ROW:
            ##############
            with gr.Row() as main_row:
                with gr.Column(scale=11, variant="compact") as col1:
                    with gr.Row() as row_one:
                        with gr.Column(visible=False) as reference_bar: # Reference panel
                            ref_output = gr.Markdown() # Second alternative
                            # ref_output = gr.Textbox(
                            # lines=30,
                            # max_lines=30,
                            #     interactive=False,
                            #     type="text",
                            #     label="References",
                            #     show_copy_button=True
                            # )

                        with gr.Column() as chatbot_output:
                            chatbot = gr.Chatbot(
                                [],
                                elem_id="chatbot",
                                bubble_full_width=False,
                                height=500,
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
                    
                    with gr.Row() as row_two:
                        with gr.Column(): 
                            input_txt = gr.Textbox(
                                lines=2,
                                scale=1,
                                placeholder="Message Socrates...",
                                container=False,
                                autofocus=True,
                                autoscroll=True, show_copy_button=True, min_width=800
                            )
                        
                                


                with gr.Column(scale = 1) as col2:
                        rag_with_dropdown = gr.Dropdown(
                            label="What do you want to do?", choices=["Built-in files: Q&A", "Upload file: Q&A", "Upload file: Summary"], value="Upload file: Q&A")
                        gr.Markdown()

                        #4th element 
                                #2nd button+
                        # upload_btn = gr.UploadButton(
                                    # "Upload files", file_types=['.pdf'],file_count="multiple", size = "sm")
                        upload_btn = gr.File(file_count="multiple", file_types=[".pdf"], label="Upload files")
                        
                        

                                #3rd butto
                        gr.Markdown()
                        gr.Markdown()
                        gr.Markdown()
                        gr.Markdown()
                        gr.Markdown()
                        gr.Markdown()
                

                        with gr.Row():
                                sidebar_state = gr.State(False)
                                btn_toggle_sidebar = gr.Button(value="Response references", size = "sm", scale = 1)
                                btn_toggle_sidebar.click(UISettings.toggle_sidebar, [sidebar_state], [reference_bar, sidebar_state]) # Activate references when clicking button 
                                clear_button = gr.ClearButton([input_txt, chatbot],scale=3, size="sm", value = "Clear chat") #Clear chat  


        
    with gr.Tab("Transcription"):
         
         audio_file = gr.File(file_types=[".mp3", ".mp4", ".wav", ".m4a"], label="Uplaod your audios here (mp3 or mp4)" )

         language = gr.Radio(choices=["en", "es", "fa", "de"], info = "Select the language the audio contains", label ="Language", value = "en", interactive=True)

         transcription_model = gr.Radio(choices=["tiny", "base", "small","distil-small.en", "medium", "distil-medium.en", "large", "distil-large-v2"], 
                          label = "Select your model", info = "The larger the more accurate but the slower it transcribes (distilled version perfom faster with small decrese in perfomance)", value = "medium",interactive=True)
         

         gr.Button("Click here to transcribe")


    with gr.Tab("Settings") as Settings:

        temperature = gr.Slider(minimum=0, maximum=1, step=.1, info = "The closer to 1 the more creative the output", label="Temperature", value = 0, interactive=True)

        model = gr.Radio(choices=["gpt-3.5-turbo", "gpt-4", "gpt-4-0125-preview"], label="Select your model", info="Increasing order of capability", value = "gpt-3.5-turbo", interactive=True)

        k_retrieval = gr.Slider(minimum=0, maximum=5, step=1, info = "The higher k the more accurate results, but the more processing time required", label="K retrieval", value=3, interactive=True)

        chat_history_k = gr.Slider(minimum=0, maximum=6, step=1, info = "The higher k the more accurate results, but the more processing time required", label="K chat history", value = 3, interactive=True)

        gr.Button("Save changes")

         

            ##############
            # Process:
            ##############
    file_msg = upload_btn.upload(fn=UploadFile.process_uploaded_files, inputs=[upload_btn, chatbot, rag_with_dropdown], outputs=[input_txt, chatbot], queue=False)

    txt_msg = input_txt.submit(fn=ChatBot.respond,
                                       inputs=[chatbot, input_txt,
                                               rag_with_dropdown, 
                                               temperature, model, k_retrieval, chat_history_k],
                                       outputs=[input_txt,
                                                chatbot, ref_output],
                                       queue=False).then(lambda: gr.Textbox(interactive=True),
                                                         None, [input_txt], queue=False)
    transcription = audio_file.upload(fn=Transcribe.process_mp3, 
                                      inputs=[audio_file, language, transcription_model], outputs=None, queue=False)
    

if __name__ == "__main__":

    demo.launch(favicon_path="/Users/javierdominguezsegura/Programming/Python/Side projects/RAG 4/other/images/system.png")
