""" 

      Step 2: Upload new (online) files    

      Called in: 'front_end.py'   
      
"""

from scripts.prepare_vectordb import PrepareVectorDB # This class creates a vectordb ready for the retrieval
from scripts.load_configuration import LoadConfiguration #Provides access to configuration values in a .yml file
from scripts.summarizer import Summarizer # Second features of this app; summarizing any file

YML = LoadConfiguration() #Access to loaded configuration

class UploadFile: # Triggered when uploaded a file
    @staticmethod # No self attribute
    def process_uploaded_files(files_dir, chatbot, rag_with_dropdown):

        """ 
            Def: this functions allows the users to upload the file and create a vectordb out of them. Requires "serve.py" to be running at the moment of upload.

            Params:
                - files_dir = files path (comes from the corresponding gradio button)
                - chatbot = tuple with user and system conversation
                - rag_with_dropdown = type of interactions with the model (options: [Upload file: Summary, Upload file: Q&A, Built-in files: Q&A])
        
        """

        if rag_with_dropdown == "Upload file: Q&A":
            prepare_vectordb_instance = PrepareVectorDB(data_directory=files_dir,
                                                        persist_directory=YML.custom_persist_directory,
                                                        embedding_model_2=YML.embedding_model_2,
                                                        chunk_size=YML.chunk_size,
                                                        chunk_overlap=YML.chunk_overlap)
            prepare_vectordb_instance.create_vectordb()
            chatbot.append(
                ("I just uploaded the file.", "Indeed, files added to the knowledge base succesfully. Please ask your question"))
        elif rag_with_dropdown == "Upload file: Summary":
            final_summary = Summarizer.summarize_the_pdf(file_dir=files_dir[0],
                                                         max_final_token=YML.max_final_token,
                                                         token_threshold=YML.token_threshold,
                                                         gpt_model=YML.llm_model,
                                                         temperature=YML.temperature,
                                                         summarizer_llm_template=YML.summarizer_llm_template,
                                                         final_summarizer_llm_template=YML.final_summarizer_llm_template,
                                                         character_overlap=YML.character_overlap)
            chatbot.append(
                ("I just uploaded the file for summary", f"Here is the summary:\n\n{final_summary}"))
        else:
            chatbot.append(
                (" ", "It seems you have uploaded a new file, but you are interacting with the built-in files. If you want to query your own docs change it in the dropdown to the right. "))
        return "", chatbot