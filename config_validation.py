from typing import Dict, Optional, List
from pydantic import BaseModel, Field, RootModel, model_validator

class ValidationBase(BaseModel):
    # throws `ValidationError` when encountering unexpected field
    model_config = {
        "extra": "forbid"
    }

class GlobalConfig(ValidationBase):
    targets_path: str
    artifacts_path: str
    inputs_path: str
    mutators_path: Optional[str] = None

class RunStatement(ValidationBase):
    type: Optional[str] = None
    cmd: str
    args: Optional[str] = None
    env: Optional[List[str]] = None

class Target(ValidationBase):
    run: List[RunStatement]
    prepare: Optional[List[str]] = None

class Fuzzer(RootModel[Dict[str, Target]]):
    def __getitem__(self, key: str) -> Target:
        return self.root[key]

class ConfigValidation(ValidationBase):
    global_conf: GlobalConfig = Field(alias="global")
    fuzzers: Dict[str, Fuzzer]

    @model_validator(mode="after")
    def check_fuzzers_not_empty(cls, model):
        if not model.fuzzers:
            raise ValueError("The 'fuzzers' section must not be empty.")
        return model
