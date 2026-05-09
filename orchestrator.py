from agents.input_agent import InputAgent
from agents.model_agent import ModelAgent
from agents.output_agent import OutputAgent

class Orchestrator:
    def __init__(self):
        self.input_agent = InputAgent()
        self.model_agent = ModelAgent("models/trained_model.pkl")
        self.output_agent = OutputAgent()

    def run(self, user_input: str):
        processed = self.input_agent.process(user_input)
        prediction = self.model_agent.predict(processed)
        result = self.output_agent.format(prediction)
        return result

if __name__ == "__main__":
    orchestrator = Orchestrator()
    print(orchestrator.run("Hola mundo"))
