import pytest

from config_validation import GlobalConfig
from pydantic import ValidationError


def test_GlobalConfig_RequiredOnly():
    gc = GlobalConfig(
        targets_path='/path',
        artifacts_path='/path',
        inputs_path='/path',
    )
    assert gc

def test_GlobalConfig_All():
    gc = GlobalConfig(
        targets_path='/path',
        artifacts_path='/path',
        inputs_path='/path',
        mutators_path='/path',
    )
    assert gc
    assert gc.mutators_path is not None

def test_GlobalConfig_MissingRequired():
    with pytest.raises(ValidationError):
        GlobalConfig(
            artifacts_path='/path',
            inputs_path='/path',
        )

def test_GlobalConfig_MissingRequired_WrongType():
    with pytest.raises(ValidationError):
        GlobalConfig(
            targets_path=123,
            artifacts_path='/path',
            inputs_path='/path',
        )
