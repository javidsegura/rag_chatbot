
""" 
      MAIN BACKEND MODULE:

      All prior functions intersect in this module.
       
     Called in: 'front-end'
         
          
           
             """

import gradio as gr
import time
import openai
import os
from langchain.vectorstores import Chroma
from typing import List, Tuple
import re
import ast
import html
from scripts.load_configuration import LoadConfiguration
from openai import OpenAI

client = OpenAI()

YML = LoadConfiguration()



class ChatBot:
    """
    Class representing a chatbot with document retrieval and response generation capabilities.

    This class provides static methods for responding to user queries, handling feedback, and
    cleaning references from retrieved documents.
    """
    @staticmethod
    def respond(chatbot # Conversation history
                , message, # User's query 
                data_type = "Built-in files Q&A", # Mode selected. Could also be "Upload a new file"
                temperature= 0.2) -> Tuple:
        if data_type == "Built-in files Q&A": 
            if os.path.exists(YML.persist_directory): # Why would you create a new vectordb if it already uploads them in 'prepare_vectordb.py'
                vectordb = Chroma(persist_directory=YML.persist_directory,
                                  embedding_function=YML.embedding_model)
            else:
                chatbot.append(
                    (message, f"VectorDB does not exist. Please first execute the 'upload_data_manually.py' module."))
                return "", chatbot, None
        elif data_type == "Upload file Q&A":
            if os.path.exists(YML.custom_persist_directory):
                vectordb = Chroma(persist_directory=YML.custom_persist_directory,
                                  embedding_function=YML.embedding_model)
            else:
                chatbot.append(
                    (message, f"No file was uploaded. Make sure you have clicked the 'upload' button."))
                return "", chatbot, None

        docs = vectordb.similarity_search(message, k=YML.k) #Searching in the vectorstore based on the query 
        print(docs)

        question = "# User new question:\n" + message
        retrieved_content = ChatBot.clean_references(docs) # Call function ahead of time. Clean content from retriever to guarantee better results 
        
        # Memory: previous two Q&A pairs
        chat_history = f"Chat history:\n {str(chatbot[-YML.number_of_q_a_pairs:])}\n\n" # Memory keeps 4 (current value for 'number_of_q_a_pairs') of the last messages from ...
        prompt = f"{chat_history}{retrieved_content}{question}"
        print("========================")
        print(prompt)
        response = client.chat.completions.create(
        model=YML.llm_model,
        messages=[
            {"role": "system", "content": YML.llm_template},
            {"role": "user", "content": prompt}],
        stream=False, temperature = temperature
        )
        choice = response.choices[0]
        _message = choice.message
        content = _message.content

        chatbot.append(
            (message, content)) # Message is user's query and content is LLM's answer 
        time.sleep(2)

        return "", chatbot, retrieved_content

    @staticmethod
    def clean_references(documents: List) -> str:
        server_url = "http://localhost:8000"
        documents = [str(x)+"\n\n" for x in documents]
        markdown_documents = ""
        counter = 1
        for doc in documents:
            # Extract content and metadata
            content, metadata = re.match(
                r"page_content=(.*?)( metadata=\{.*\})", doc).groups()
            metadata = metadata.split('=', 1)[1]
            metadata_dict = ast.literal_eval(metadata)

            # Decode newlines and other escape sequences
            content = bytes(content, "utf-8").decode("unicode_escape")

            # Replace escaped newlines with actual newlines
            content = re.sub(r'\\n', '\n', content)
            # Remove special tokens
            content = re.sub(r'\s*<EOS>\s*<pad>\s*', ' ', content)
            # Remove any remaining multiple spaces
            content = re.sub(r'\s+', ' ', content).strip()

            # Decode HTML entities
            content = html.unescape(content)

            # Replace incorrect unicode characters with correct ones
            content = content.encode('latin1').decode('utf-8', 'ignore')

            # Remove or replace special characters and mathematical symbols
            # This step may need to be customized based on the specific symbols in your documents
            content = re.sub(r'â', '-', content)
            content = re.sub(r'â', '∈', content)
            content = re.sub(r'Ã', '×', content)
            content = re.sub(r'ï¬', 'fi', content)
            content = re.sub(r'â', '∈', content)
            content = re.sub(r'Â·', '·', content)
            content = re.sub(r'ï¬', 'fl', content)

            pdf_url = f"{server_url}/{os.path.basename(metadata_dict['source'])}"

            # Append cleaned content to the markdown string with two newlines between documents
            markdown_documents += f"# Retrieved content {counter}:\n" + content + "\n\n" + \
                f"Source: {os.path.basename(metadata_dict['source'])}" + " | " +\
                f"Page number: {str(metadata_dict['page'])}" + " | " +\
                f"[View PDF]({pdf_url})" "\n\n"
            counter += 1

        return markdown_documents