from typing import Dict, Optional
from pydantic import BaseModel, Field, model_validator

class GlobalConfig(BaseModel):
    targets_path: str
    artifacts_path: str
    inputs_path: str
    mutators_path: Optional[str] = None

class Fuzzer(BaseModel):
    # TODO
    pass

class ConfigValidation(BaseModel):
    global_conf: GlobalConfig = Field(alias="global")
    fuzzers: Dict[str, Fuzzer]

    @model_validator(mode="after")
    def check_fuzzers_not_empty(cls, model):
        if not model.fuzzers:
            raise ValueError("The 'fuzzers' section must not be empty.")
        return model
