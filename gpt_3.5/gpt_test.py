from gpt_finetune_inference import MovieGenrePredictor
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../.env.example")

api_key=os.getenv("OPENAI_API_KEY")

model_name = "ft:########:personal::######"  
system_message = "Given a synopsis of a movie, determine its genre as either 'action,' 'adventure,' 'crime,' 'family,' 'fantasy,' 'horror,' 'mystery,' 'romance,' 'scifi,' or 'thriller.'"

predictor = MovieGenrePredictor(api_key=api_key, model=model_name, system_message=system_message)

# prediction
movie_synopsis = "A young scriptwriter starts bringing valuable objects back from his short nightmares of being chased by a demon. Selling them makes him rich."
predicted_genre = predictor.generate_response(movie_synopsis)
print(f"Predicted Genre: {predicted_genre}")
