from gpt_finetune_trainer import MovieGenreTrainer
import pandas as pd
import json
import openai
import time


api_key = "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"
df = pd.read_csv("../Dataset/genre_counts.csv") # Dataset
prompt = "A model that takes in a complex paragraph of a movie synopsis and classifies it into one of the following genres: 'action,' 'adventure,' 'crime,' 'family,' 'fantasy,' 'horror,' 'mystery,' 'romance,' 'scifi,' or 'thriller.' The model will output one of these genres based on the given movie synopsis."

trainer = MovieGenreTrainer(api_key)
trainer.generate_system_message(prompt)

df_train = df.sample(frac=0.8, random_state=42)
df_test = df.drop(df_train.index)

training_examples = trainer.create_training_examples(df_train)
inference_examples = trainer.create_inference_examples(df_test)

with open('out/training_examples.jsonl', 'w') as f:
    for example in training_examples:
        f.write(json.dumps(example) + '\n')

with open('out/inference_examples.jsonl', 'w') as f:
    for example in inference_examples:
        f.write(json.dumps(example) + '\n')

# Fine-tune the model
job_id = trainer.fine_tune_model('out/training_examples.jsonl')

# Check the status
events = trainer.check_fine_tuning_status(job_id)
print(events)
model_name_pre_object = openai.FineTuningJob.retrieve(job_id)
model_name = model_name_pre_object.fine_tuned_model
print(model_name)

status = openai.FineTuningJob.retrieve(job_id)
while status["status"] != "succeeded":
    print(f"Job status: {status['status']}")
    time.sleep(30) 
    status = openai.FineTuningJob.retrieve(job_id)

model_name = status.fine_tuned_model
print(f"Fine-tuned model name: {model_name}")


