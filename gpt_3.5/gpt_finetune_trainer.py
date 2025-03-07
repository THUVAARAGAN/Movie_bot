import pandas as pd
import json
import openai

class MovieGenreTrainer:
    def __init__(self, api_key, model="gpt-3.5-turbo", temperature=0.4):
        openai.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.system_message = None

    def generate_system_message(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You will be given a high-level description of the model we are training, and from that, you will generate a simple system prompt for that model to use. Remember, you are not generating the system message for data generation -- you are generating the system message to use for inference. A good format to follow is `Given WHAT_THE_MODEL_SHOULD_DO.`.\n\nMake it as concise as possible. Include nothing but the system prompt in your response.\n\nFor example, never write: `\" SYSTEM_PROMPT_HERE`."
                },
                {
                    "role": "user",
                    "content": prompt.strip(),
                }
            ],
            temperature=self.temperature,
            max_tokens=700,
        )

        self.system_message = response.choices[0].message['content']
        return self.system_message

    def create_training_examples(self, df_train):
        training_examples = []
        for index, row in df_train.iterrows():
            training_example = {
                "messages": [
                    {"role": "system", "content": self.system_message.strip()},
                    {"role": "user", "content": row['synopsis']},    
                    {"role": "assistant", "content": row['genre']}
                ]
            }
            training_examples.append(training_example)
        return training_examples

    def create_inference_examples(self, df_test):
        inference_examples = []
        for index, row in df_test.iterrows():
            inference_example = {
                "messages": [
                    {"role": "system", "content": self.system_message.strip()},
                    {"role": "user", "content": row['synopsis']},
                    {"role": "assistant", "content": row['genre']}
                ]
            }
            inference_examples.append(inference_example)
        return inference_examples

    def fine_tune_model(self, training_file_path):
        file_id = openai.File.create(
            file=open(training_file_path, "rb"),
            purpose='fine-tune'
        ).id

        job = openai.FineTuningJob.create(training_file=file_id, model=self.model)
        job_id = job.id
        return job_id

    def check_fine_tuning_status(self, job_id):
        events = openai.FineTuningJob.list_events(id=job_id, limit=5)
        return events
