# RAG CHATBOT 

### Retrieved augment generation, query LLMs with supplemented knowledge base from your own files
<p> <b> Description: </b> Enhance LLMs capabilities by suppleting your own files to the knowledge base and query them. Includes option to upload audios (.mp4, .m4a etc) for their transcription. Additionally modify the models parameters in the settings page.</p>



<p>Stack:</p> 

<ul> 
<li>Programming languages: Python, YAML </li>
<li> Libraries/APIs: langchain, OpenAI, faster whisper, chromaDB</li> 
</ul>
<p>  </p>
<hr>

https://github.com/javidsegura/rag_chatbot/assets/129964070/f5506237-cebc-468b-8254-49b6f3a7a738


<hr>

<p> <b> Features, described: </b> </p>
<ul>
      <li> Memory</li>
      <li> Built-in knowledge base</li>
      <li> Speech to text feature </li>
      <li> LLM's responses references </li>
      <li> Files summarizer</li>
      <li> Feedback on LLM's responses </li>
      <li> Modify retrieval chain parameters (temperature, model, k-retrievals etc) </li>
</ul>



<p> <b> Complete walkthrough: </b> </p>
<ol>
      <li> Select to query internal knowledge base or uplaod your own files</li>
      <li> Load the files (if external),chunk them, transform them with an embedding model and store them with ChromaDB  </li>
      <li> Query the LLM</li>
      <li> Start retriever: vector search (similarity search algorithm)</li>
      <li> Clean results from retriever</li>
      <li> Pass a prompt to the LLM with the original user's question, retrieved results and memory from the conversation</li>
      <li> Get response from LLM</li>
      <li> See response references</li>
      <li> Repeat from 3 or upload new files and repeat from 1</li>

</ol>
<p> <i> Note: if mode is 'Upload file: Summary', the process is the same up to 2 and then it provides a summary directly. </p> </i>
