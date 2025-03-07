from flask import Flask, render_template, request
from gpt_finetune_inference import MovieGenrePredictor
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../.env.example")

api_key=os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

#Model Setup
model_name = "ft:gpt---"  # change the model name
system_message = "Given a synopsis of a movie, determine its genre as either 'action,' 'adventure,' 'crime,' 'family,' 'fantasy,' 'horror,' 'mystery,' 'romance,' 'scifi,' or 'thriller.'"

predictor = MovieGenrePredictor(api_key=api_key, model=model_name, system_message=system_message)

@app.route('/', methods=['GET', 'POST'])
def index():
    genre = None
    if request.method == 'POST':
        movie_synopsis = request.form['synopsis']
        genre = "horror"
        # genre = predictor.generate_response(movie_synopsis)
    return render_template('index.html', genre=genre)

if __name__ == '__main__':
    app.run(debug=True)
