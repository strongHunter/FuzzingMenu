from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field, RootModel, model_validator

class GlobalConfig(BaseModel):
    targets_path: str
    artifacts_path: str
    inputs_path: str
    mutators_path: Optional[str] = None

class Fuzzer(RootModel[Dict[str, Any]]): # TODO: Target
    def __getitem__(self, key: str) -> Any: # TODO: Target
        return self.root[key]

class ConfigValidation(BaseModel):
    global_conf: GlobalConfig = Field(alias="global")
    fuzzers: Dict[str, Fuzzer]

    @model_validator(mode="after")
    def check_fuzzers_not_empty(cls, model):
        if not model.fuzzers:
            raise ValueError("The 'fuzzers' section must not be empty.")
        return model
