"""

ADDITIONAL SCRIPT: 

      Interact with the RAG system via the terminal (scope limited to offline docs )
"""

import openai
import yaml
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from typing import List, Tuple
from scripts.load_configuration import LoadConfiguration
from openai import OpenAI
import time

client = OpenAI()

# For loading openai credentials
YML = LoadConfiguration()

with open("configs/app_config.yml") as cfg:
    app_config = yaml.load(cfg, Loader=yaml.FullLoader)

# Load the embedding function
embedding = OpenAIEmbeddings()
# Load the vector database
vectordb = Chroma(persist_directory=YML.persist_directory,
                  embedding_function=embedding)

print("Number of vectors in vectordb:", vectordb._collection.count())

# Prepare the RAG with openai in terminal
print("-"*60)
while True:
    question = input("\n \n ==> Enter your question or press 'q' to exit: ")
    if question.lower() =='q':
        break
    question = "\t# User's prompt: " + f"'{question}'" + "\n"
    docs = vectordb.similarity_search(question, k=YML.k) # Activate retriever 
    retrieved_docs_page_content: List[Tuple] = [
        str(x.page_content)+"\n\n" for x in docs] # Get content from metatada of the retriever  
    retrived_docs_str = "\t# Retrieved content:\n\n" + str(retrieved_docs_page_content)
    prompt = retrived_docs_str + "\n\n" + question  
    print(f"\n\n ~ COMPLETE PROMPT \n[{prompt}]\n ")
    print("**LLM response: ")
    stream = client.chat.completions.create(
        model=YML.llm_model,
        messages=[
            {"role": "system", "content": YML.llm_template},
            {"role": "user", "content": prompt}],
        stream=True,
        )
    for i in stream:
      if i.choices[0].delta.content is not None:
        time.sleep(0.05)
        print(i.choices[0].delta.content, end="", flush= True)

  
