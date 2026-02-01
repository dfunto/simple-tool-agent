import textwrap
from enum import Enum
from pydantic import Field, BaseModel


class AgentTool(Enum):
    CALCULATOR = "calculator"
    FILE_READER = "file_reader"


class AgentObservation(BaseModel):
    prompt: str
    tools: list[AgentTool] = Field(default_factory=lambda: list(AgentTool))

    @property
    def plan_prompt(self) -> str:
        tools = ','.join([tool.value for tool in self.tools])
        return textwrap.dedent(f"""
        You are a tool-selection engine.
        Rules:
            - Respond with VALID JSON ONLY
            - No explanations
            - No markdown
            - No extra text

        User input: "{self.prompt}"
        Available tools: "{tools}"
        
        Task: Decide which tool to use and what input to provide.
        Output Example: {{"tool": "selected tool", "input": "user input for the tool"}}
        """)


class AgentPlan(BaseModel):
    tool: AgentTool
    input: str


class AgentResult(BaseModel):
    input: str
    output: str

    @property
    def reflect_prompt(self) -> str:
        return textwrap.dedent(f"""
        Is the 
        Rules:
            - Respond with VALID JSON ONLY
            - No explanations
            - No markdown
            - No extra text

        User input: "{self.prompt}"
        Available tools: "{tools}"

        Task: Decide which tool to use and what input to provide.
        Output Example: {{"tool": "selected tool", "input": "user input for the tool"}}
        """)