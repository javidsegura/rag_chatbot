"""
    Particular functionalities for reference's hidden bar and feedback system.

    Called in: 'front_end.py'



"""


import gradio as gr
import csv


with open("/Users/javierdominguezsegura/Programming/Python/Side projects/RAG 4/other/user_feedback/feedback.csv", "w") as file:
                 writer = csv.writer(file,delimiter=",")
                 writer.writerow([0,1,"User_message", "System_message"])



class UISettings:
  
    @staticmethod
    def toggle_sidebar(state):
     
        state = not state
        return gr.update(visible=state), state

    @staticmethod
    def feedback(data: gr.LikeData):
      if data.liked:
            print("You upvoted this response: " + f"'{data.value}'")
            with open("/Users/javierdominguezsegura/Programming/Python/Side projects/RAG 4/other/user_feedback/feedback.csv", "a") as file:
                 writer = csv.writer(file,delimiter=",")
                 writer.writerow([1,0," ",f"{data.value}"])
                
      else:
            print("You downvoted this response: " + f"'{data.value}'")
            with open("/Users/javierdominguezsegura/Programming/Python/Side projects/RAG 4/other/user_feedback/feedback.csv", "a") as file:
                 writer = csv.writer(file,delimiter=",")
                 writer.writerow([0,1," ",f"{data.value}"])
