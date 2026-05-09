class InputAgent:
    def process(self, raw_input: str) -> str:
        return raw_input.lower().strip()
