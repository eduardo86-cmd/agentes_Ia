import pickle

class ModelAgent:
    def __init__(self, model_path: str):
        with open(model_path, "rb") as f:
            self.model, self.vectorizer = pickle.load(f)

    def predict(self, text: str):
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]
