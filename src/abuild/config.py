from pathlib import Path
import yaml
from pydantic import BaseModel


class BuildStep(BaseModel):
    name: str | None
    cmd: str
    break_on_error: bool = True


class Component(BaseModel):
    path: Path
    steps: list[BuildStep]


class Config(BaseModel):
    components: list[Component]
    state_file: Path = Path('.abuild_state')

    @classmethod
    def from_file(cls, path: Path):
        with path.open('r') as f:
            return cls(**yaml.safe_load(f))
