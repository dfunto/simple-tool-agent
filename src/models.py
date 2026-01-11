from pydantic import Field, BaseModel


class Observation(BaseModel):
    prompt: str
    tools: list[str] = Field(default_factory=lambda: ["calculator", "file_reader"])
