""" 
      Step 2: upload offlines docs to the model. (They are stored in 'data/docs')
"""

import os
from scripts.prepare_vectordb import PrepareVectorDB
from scripts.load_configuration import LoadConfiguration


YML = LoadConfiguration() # We gain access to the .yml by instantating the class that processes them

def upload_data_manually() -> None:

      instance = PrepareVectorDB(data_directory=YML.data_directory, persist_directory=YML.persist_directory,
                                 embedding_model_2=YML.embedding_model_2,
                                 chunk_size=YML.chunk_size, chunk_overlap=YML.chunk_overlap)
      
      if not len(os.listdir(YML.persist_directory)) != 0: #If the vectorDB is not created, create one
        instance.create_vectordb()
      else:
        print(f"VectorDB already exists in {YML.persist_directory}, could not create a new one.")

      return None

if __name__ == "__main__":
    upload_data_manually()
