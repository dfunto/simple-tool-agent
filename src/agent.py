import requests
import textwrap

from models import AgentObservation
from logs import LoggingMixin
from src.models import AgentPlan


class Agent(LoggingMixin):

    def observe(self) -> AgentObservation:
        print("How can I help you today? (Hit CTRL + C to exit)")
        prompt = input()
        return AgentObservation(prompt=prompt)

    def plan(self, observation: AgentObservation) -> AgentPlan:
        plan_prompt = textwrap.dedent(f"""
        You are a tool-selection engine.
        Rules:
            - Respond with VALID JSON ONLY
            - No explanations
            - No markdown
            - No extra text

        User input: "{observation.prompt}"
        Available tools: "{','.join(observation.tools)}"
        
        Task: Decide which tool to use and what input to provide.
        Output Example: {{"tool": "selected tool", "input": "user input for the tool"}}
        """)
        self.log.info(f"Plan Prompt:{plan_prompt}")
        response = requests.post(
            url="http://llm:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": plan_prompt,
                "format": "json",
                "stream": False
            },
        )
        response.raise_for_status()
        plan_output = response.json().get("response")
        self.log.info(f"Plan Output:\n{plan_output}")
        return AgentPlan(**plan_output)

    def act(self, plan: AgentPlan):
        print("Acting")

    def reflect(self):
        print("Reflecting")

    def run(self):
        while True:
            observation = self.observe()
            plan = self.plan(observation=observation)
            self.act()
            self.reflect()
