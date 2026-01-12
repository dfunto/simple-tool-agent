from pydantic import Field, BaseModel


class AgentObservation(BaseModel):
    prompt: str
    tools: list[str] = Field(default_factory=lambda: ["calculator", "file_reader"])


class AgentPlan(BaseModel):
    tool: str
    input: str
