import pandas as pd


df = pd.read_csv("Dataset\movie_genre_kaggle.csv")
# print(df.head()) 
# print(df.info())  
# print(df.describe())  

genre_counts = df['genre'].value_counts()
total_samples = 80
proportional_samples = (genre_counts / genre_counts.sum() * total_samples).round().astype(int)
sampled_df = df.groupby('genre', group_keys=False).apply(lambda x: x.sample(min(len(x), proportional_samples[x.name]), random_state=42))
sampled_df.drop(columns=['id', 'movie_name'], inplace=True)

unique_genres = df['genre'].unique()
genre_counts = sampled_df['genre'].value_counts()
print(unique_genres)
print(genre_counts)
sampled_df.to_csv("Dataset/genre_counts.csv", index=True)

# conda create -n cardezzdev python==3.10
# conda activate
# pip install pandas
# pip install openai==0.28
# pip install flask