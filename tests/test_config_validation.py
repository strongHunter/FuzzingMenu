import pytest

from config_validation import GlobalConfig, ConfigValidation
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


### ConfigValidation

def test_ConfigValidation_ShouldBeOk():
    cfg = ConfigValidation.model_construct(
        global_conf=GlobalConfig(
            targets_path='/a',
            artifacts_path='/b',
            inputs_path='/c',
        ),
        fuzzers={
            'afl': {}
        }
    )
    assert cfg.global_conf.targets_path == "/a"
    assert 'afl' in cfg.fuzzers

# TODO
def testConfigValidation_MissingFuzzers():
    pass
