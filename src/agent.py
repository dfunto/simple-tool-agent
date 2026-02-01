import json
from pathlib import Path

import requests

from models import AgentObservation
from logs import LoggingMixin
from models import AgentPlan, AgentTool
from models import AgentResult


class Agent(LoggingMixin):

    @staticmethod
    def _query_llm(prompt: str) -> str:
        response = requests.post(
            url="http://llm:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "format": "json",
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response")

    def observe(self) -> AgentObservation:
        print("How can I help you today? (Hit CTRL + C to exit)")
        prompt = input()
        self.log.debug(f"Prompt received {prompt}")
        return AgentObservation(prompt=prompt)

    def plan(self, observation: AgentObservation) -> AgentPlan:
        self.log.debug(f"Plan Prompt:{observation.plan_prompt}")
        output = self._query_llm(prompt=observation.plan_prompt)
        self.log.info(f"Plan Output:\n{output}")
        return AgentPlan(**json.loads(output))

    def act(self, plan: AgentPlan) -> AgentResult:
        if plan.tool == AgentTool.CALCULATOR:
            self.log.info(f"Calculating {plan.input}")
            output = str(eval(plan.input))
        elif plan.tool == AgentTool.FILE_READER:
            self.log.info(f"Reading file {plan.input}")
            file = Path("./input") / plan.input
            lines = open(file).readlines()
            output = "\n".join(lines)
        else:
            raise NotImplemented(f"Tool {plan.tool} not implemented")

        result = AgentResult(input=plan.input, output=output)
        return result

    def reflect(self, result: AgentResult) -> bool:
        self.log.debug(f"Result: {result}")
        print(f"Output: {result.output}")
        return True

    def run(self):
        while True:
            observation = self.observe()
            plan = self.plan(observation=observation)
            result = self.act(plan=plan)
            if not self.reflect(result=result):
                raise ValueError("Failed to achieve result")
