import openai

class MovieGenrePredictor:
    def __init__(self, api_key, model, system_message, temperature=0.4):
        openai.api_key = api_key
        self.model = model
        self.system_message = system_message
        self.temperature = temperature

    def generate_response(self, question):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": question},
            ],
        )
        return response.choices[0].message['content']
