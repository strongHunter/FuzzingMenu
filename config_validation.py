from typing import Optional
from pydantic import BaseModel

class GlobalConfig(BaseModel):
    targets_path: str
    artifacts_path: str
    inputs_path: str
    mutators_path: Optional[str] = None
