import faster_whisper as whisper
import time

class Transcribe:
      # @staticmethod
      def __init__(self) -> None:
            pass
      def process_mp3(files_dir, language = "english", model = "medium.en"):
            print("Starting transcription...")
            print(files_dir, language, model, sep = "\n")
            if language == "en" and model != "distil-medium.en":
                  model += ".en"
            print(model)
            trasncriber = whisper.WhisperModel(
                  model_size_or_path=model, 
                  device="cpu",
                  compute_type="int8", cpu_threads=8
            )

            segments, info = trasncriber.transcribe(files_dir, beam_size=5, language=language)

            # print(f"Detected language is '{('english' if info.language == "en" else info.language)}' with probability {info.language_probability}") # Detecting language based on first 30seconds 
            print("Starting to transcribe...")
            with open("/Users...other/transcription/transcribed.txt", "w") as f:
                  for segment in segments: # Looping through segments (small chunks of the transcription); Transcription starts here
                        f.write(f"{segment.text} \n") # Writing to file
                        time.sleep(.4)
                        
 
            print("Transcription saved succesfully in 'transcription.txt' file .")  
