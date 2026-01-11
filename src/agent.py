import requests

from models import Observation


class Agent:

    def observe(self) -> Observation:
        print("How can I help you today? (Hit CTRL + C to exit)")
        prompt = input()
        return Observation(prompt=prompt)

    def plan(self, observation: Observation):
        plan_prompt = f"""
        User input: "{observation.prompt}"
        Available tools: "{','.join(observation.tools)}"
        
        Task: Decide which tool to use and what input to provide.
        Return JSON: {{"tool": "file_reader", "input": "notes.txt"}}
        """
        response = requests.post(
            url="http://llm:11434/api/generate",
            json={
                "model": "llama3.1",
                "prompt": plan_prompt
            }
        )
        response.raise_for_status()
        plan_output = response.text
        print(f"Plan: {plan_output}")


    def act(self):
        print("Acting")

    def reflect(self):
        print("Reflecting")

    def run(self):
        while True:
            observation = self.observe()
            self.plan(observation=observation)
            self.act()
            self.reflect()
