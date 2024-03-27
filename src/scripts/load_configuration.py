"""
       Step 0: get the configurations to be able to be referenced all throughout the project. Load them from "app_config.yml"

    Called in: 
      - upload_offline_docs.py
      
"""



import openai, os # Used to get API's credential 
from dotenv import load_dotenv # Same as above
import yaml # Module to work with app_config
from langchain.embeddings.openai import OpenAIEmbeddings 
from pyprojroot import here 
import shutil

load_dotenv()

class LoadConfiguration:
      """ Go over the .yml document (configurations vales ) and create attributes with each of them. 
      
      Motive: used to reference the configurations all throughout the project with """
      def __init__(self) -> None: # The arrow directed to None says the output of the function is None (there is no return statement)


            """ 
            Attributes:
                  - llm_model = which model will power the prompt processing
                  - llm_template = prompt template for the model
                  - persist_directory = directory for offline docs
                  - 
            
            
            Methods:
                  - load_openai_configuration: extract API key from system variable
                  - create/remove_directory = each time instantiated (running the script) create a directory for the vectordb. If already existing create a new one. """





            with open(here("/Users/javierdominguezsegura/Programming/Python/Side projects/RAG 4/configs/app_config.yml")) as cfg: # Uploading .yml with project configurations; the here function return the path 
                  app_config = yaml.load(cfg, Loader=yaml.FullLoader) #This functions has as parameter the path to the file and specifies a type of loader

            # 1. LLM configs
            self.llm_model = app_config["llm_config"]["model"] 
            self.llm_template = app_config["llm_config"]["llm_template"]
            self.persist_directory = str(here( app_config["directories"]["persist_directory"]))  
            self.custom_persist_directory = str(here(app_config["directories"]["custom_persist_directory"]))
            self.embedding_model = OpenAIEmbeddings() # Why are we calling this one here

            # 2. Retrieval configs
            self.data_directory = app_config["directories"]["data_directory"]
            self.k = app_config["retrieval_config"]["k"]
            self.embedding_model_2 = app_config["embedding_model_config"]["model"]
            self.chunk_size = app_config["splitter_config"]["chunk_size"]
            self.chunk_overlap = app_config["splitter_config"]["chunk_overlap"]

            # 3. Summarizer config
            self.max_final_token = app_config["summarizer_config"]["max_final_token"]
            self.token_threshold = app_config["summarizer_config"]["token_threshold"]
            self.summarizer_llm_template = app_config["summarizer_config"]["summarizer_llm_template"]
            self.character_overlap = app_config["summarizer_config"]["character_overlap"]
            self.final_summarizer_llm_template = app_config[
                  "summarizer_config"]["final_summarizer_llm_template"]
            self.temperature = app_config["llm_config"]["temperature"]

            # 4. Memory
            self.number_of_q_a_pairs = app_config["memory"]["number_of_q_a_pairs"]

            # 5. Load OpenAI credentials
            self.load_openai_configuration()

            # Clean up the upload doc vectordb if it exists
            self.create_directory(self.persist_directory)
            self.remove_directory(self.custom_persist_directory)

      def load_openai_configuration(self) -> None:
            openai.api_key = os.getenv("OPENAI_API_KEY")

      def create_directory(self, path) -> None: # Create directory for offline docs; are all uploaded files (online or offline) being redirected from here
        """ 
        Parameters: 
            - path = value from yml 'persist_directory'
        """
        if not os.path.exists(path):
            os.makedirs(path)
            os.system("clear")
            print(f"\nVectordb for offlines docs created in {path}")

      def remove_directory(self, path): # Remove directory for online docs (from prior uses); Question is, where is the directory being created for online docs? - WARNING 2
        """ 
        Parameters: 
            - path = value from yml 'custom_persist_directory'
        """
        
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                print(f"The directory '{path}' has been successfully removed.")
            except OSError as e:
                print(f"Error: {e}")
        else:
            print(f"\nThe directory '{path}' did not exist. The vectorstore folder for offline docs was already emptied.")