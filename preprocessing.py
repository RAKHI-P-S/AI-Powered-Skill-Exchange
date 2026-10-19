import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib

df=pd.read_csv("dataset\skill_exchange_dataset_1000.csv")
print("Dataset loaded successfully.....")
print(df.head())
print(df.tail())
print(df.info())
print(df.shape)
print(df.describe())
print(df.isnull().sum())
print(df.duplicated())
print(df.columns)


preprocessed_df=df.copy()

features=['gender','city','teach_skill','learn_skill','proficiency_level','preferred_language',
       'learning_mode','availability']
encoders={}

for colum in features:
 encoder=LabelEncoder()
 preprocessed_df[colum]=encoder.fit_transform(preprocessed_df[colum])
 encoders[colum]=encoder

#check the encoder
print("\nOriginal Dataset")
print(df.head())

print("\nEncoded Dataset")
print(preprocessed_df.head())
preprocessed_df.to_csv("dataset/processed_skill_exchange_dataset.csv",index=False)

#check DataType 
print("\nData Types After Encoding")
print(preprocessed_df.dtypes)

for colums,my_encoder in encoders.items():
 print(f"/n[{colums}]")
 mapping=dict(zip(my_encoder.classes_,my_encoder.transform(my_encoder.classes_)))
 print(mapping)

#save model
joblib.dump(encoders, "models/encoders.pkl")
print("\nProcessed dataset saved successfully!")