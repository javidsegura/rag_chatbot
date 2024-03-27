"""
      Step 1: Get the vectordatabase
      
       Called in: 
      - upload_offline_docs.py

"""

from langchain.document_loaders import PyPDFLoader # 1. Load documents 
from langchain.text_splitter import RecursiveCharacterTextSplitter # 2. Chuking on the loaded documents 
from langchain.embeddings.openai import OpenAIEmbeddings # 3. Transform the chunks 
from langchain.vectorstores import Chroma # 4. Store the transformed chunks into a vector db

import os


class PrepareVectorDB:
      """ In this class all the steps for the retriever will be executed.

      That is, this class contains the following chain: load - chunk - transform - store      
      """

      def __init__(self, 
                  data_directory, # Offline docs path 
                  persist_directory, # Vector db for path 
                  embedding_model_2, # Tranforming chunks
                  chunk_size,  chunk_overlap # Parameters for chunking
                  ) -> None:
            
            self.embedding_model_2 = embedding_model_2
            self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap,separators=["\n\n", "\n", " ", ""])
            self.data_directory = data_directory
            self.persist_directory = persist_directory
            self.embedding = OpenAIEmbeddings()

      def __load_all_documents(self) -> list:
            """
                  Use: load all offline docs (have to be in .pdf)

            """

            doc_counter = 0

            if isinstance(self.data_directory, list): 
                  print("\nLoading the uploaded documents...")
                  docs = []
                  for doc_dir in self.data_directory:
                        docs.extend(PyPDFLoader(doc_dir).load())
                        doc_counter += 1
                  print("Number of loaded documents:", doc_counter)
                  print("Number of pages:", len(docs), "\n\n")
            else: 
                  print("\nLoading documents manually...") 
                  document_list = os.listdir(self.data_directory)
                  docs = []
                  for doc_name in document_list:
                        docs.extend(PyPDFLoader(os.path.join(
                              self.data_directory, doc_name)).load())
                        doc_counter += 1
                  print("Number of loaded documents:", doc_counter)
                  print("Number of pages:", len(docs), "\n\n")
            
            return docs
      
      def __chunk_documents(self, docs) -> list:
        
        print("Chunking documents...")
        chunked_documents = self.text_splitter.split_documents(docs)
        print("Number of chunks:", len(chunked_documents), "\n\n")
        return chunked_documents
      
      def create_vectordb(self):
            """ Execute chain based on prior functions"""

            docs = self.__load_all_documents() # 1st step
            chunked_docs = self.__chunk_documents(docs) # 2nd step
            print("Docs have been loaded and chunked. \n \nStarting to prepare vectordb...")
 
            vectordb = Chroma.from_documents(documents = chunked_docs, # Use the prior chunked docs
                                              embedding= self.embedding, # Use OpenAIEmbeddings()
                                                persist_directory = self.persist_directory #Store them in a new directory 
                                                )
            print(f"Vectordb created succesfully ({vectordb._collection.count()} vectors in it). \n\n It has been stored at {self.persist_directory}")
            print()


