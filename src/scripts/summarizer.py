

from langchain.document_loaders import PyPDFLoader
from scripts.count_tokens import count_num_tokens
import openai
from openai import OpenAI

client = OpenAI()

class Summarizer:
    """
    Summarize PDFs. Summarize each page and then total pages.
    """

    @staticmethod
    def summarize_the_pdf(
        file_dir,
        max_final_token,
        token_threshold,
        gpt_model,
        temperature,
        summarizer_llm_template,
        final_summarizer_llm_template,
        character_overlap
    ):
        
        docs = []
        docs.extend(PyPDFLoader(file_dir).load())
        print(f"Document length: {len(docs)}")
        max_summarizer_output_token = int(max_final_token/len(docs)) - token_threshold
        full_summary = ""
        counter = 1
        print("Generating the summary..")
        
        if len(docs) > 1: # If the document has more than one pages
            for i in range(len(docs)):

                if i == 0:  # For the first page
                    prompt = docs[i].page_content + \
                        docs[i+1].page_content[:character_overlap]
                # For pages except the fist and the last one.
                elif i < len(docs)-1:
                    prompt = docs[i-1].page_content[-character_overlap:] + \
                        docs[i].page_content + \
                        docs[i+1].page_content[:character_overlap]
                else:  # For the last page
                    prompt = docs[i-1].page_content[-character_overlap:] + \
                        docs[i].page_content
                summarizer_llm_template = summarizer_llm_template.format(
                    max_summarizer_output_token)
                
            full_summary += Summarizer.get_llm_response(
                gpt_model,
                temperature,
                summarizer_llm_template,
                prompt=prompt
            )
        else:  # if the document has only one page
            full_summary = docs[0].page_content

            print(f"Page {counter} was summarized. ", end="")
            counter += 1
        print("\nFull summary token length:", count_num_tokens(
            full_summary, model=gpt_model))
        final_summary = Summarizer.get_llm_response( gpt_model, temperature, final_summarizer_llm_template,
            prompt=full_summary
        )
        return final_summary

    @staticmethod
    def get_llm_response(gpt_model, temperature, llm_template, prompt):

        response = client.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": llm_template},
                {"role": "user", "content": prompt}],
            stream=False
            )
        choice = response.choices[0]
        message = choice.message
        content = message.content
        return content