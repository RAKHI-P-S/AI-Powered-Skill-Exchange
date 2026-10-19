import pandas as pd
import joblib
from sklearn.neighbors import NearestNeighbors

#load dataset
df=pd.read_csv("dataset\processed_skill_exchange_dataset.csv")
print("Dataset loaded successfully.....")

#feature selection
features=['age', 'gender', 'city', 'teach_skill','learn_skill', 'proficiency_level', 'preferred_language',
       'learning_mode', 'availability', 'rating', 'completed_exchanges']

x=df[features]

#create model
knn=NearestNeighbors(n_neighbors=5,metric="euclidean")
knn.fit(x)

#save model 
joblib.dump(knn,"models\knn_model.pkl")

print("Model Trained Successfully!")
print("KNN Model Saved Successfully!")