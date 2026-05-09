import os
import pickle
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

df = pd.read_csv("data/dataset fisikapp - Hoja 1 (2).csv")

df = df.dropna(subset=["categoria", "palabras-clave"])

X_texto = df["palabras-clave"]
y = df["categoria"]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X_texto)

model = MultinomialNB()
model.fit(X, y)

os.makedirs("models", exist_ok=True)

with open("models/trained_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("Modelo entrenado y guardado en models/trained_model.pkl")