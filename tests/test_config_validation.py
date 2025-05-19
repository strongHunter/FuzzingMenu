import pytest

from config_validation import *
from pydantic import ValidationError

### ValidationBase
def test_ValidationBase_ShouldThrowsForUnexpected():
    class Test(ValidationBase):
        required: str
    
    with pytest.raises(ValidationError):
        Test.model_validate({
            'required': 'text',
            'unexpected': 'something'
        })

### GlobalConfig
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


### RunStatement
def test_RunStatement_RequiredOnly():
    stmt = RunStatement.model_validate({
        'cmd': 'echo'
    })
    assert stmt.cmd == "echo"
    assert stmt.type is None
    assert stmt.args is None
    assert stmt.env is None

def test_RunStatement_AllFields():
    stmt = RunStatement.model_validate({
        'type': 'shell',
        'cmd': 'python',
        'args': 'script.py',
        'env': ['KEY=VALUE', 'DEBUG=1']
    })
    assert stmt.type == "shell"
    assert stmt.cmd == "python"
    assert stmt.args == "script.py"
    assert stmt.env == ["KEY=VALUE", "DEBUG=1"]


### Target
def test_Target_NeedRequiredRun():
    Target.model_validate({
        'run': []
    })

def test_Target_RequiredWithOptional():
    Target.model_validate({
        'prepare': [],
        'run': []
    })

def test_Target_ShouldRaisesForInvalidType():
    with pytest.raises(ValueError):
        Target.model_validate({
        'run': {}
    })

def test_Target_ShouldRaisesForOptionalInvalidType():
    with pytest.raises(ValueError):
        Target.model_validate({
        'prepare': {},
        'run': []
    })


### Fuzzer
def test_Fuzzer_SquareBraces():
    fuzzer = Fuzzer.model_validate({
        'some target': {
            'run': []
        }
    })
    assert isinstance(fuzzer['some target'], Target)


### ConfigValidation
def test_ConfigValidation_ShouldBeOk():
    cfg = ConfigValidation.model_validate({
        'global': {
            'targets_path': '/a',
            'artifacts_path': '/b',
            'inputs_path': '/c',
        },
        'fuzzers': {
            'afl': {}
        }
    })
    assert cfg.global_conf.targets_path == "/a"
    assert 'afl' in cfg.fuzzers

def test_ConfigValidation_MissingFuzzers():
    with pytest.raises(ValueError):
        ConfigValidation.model_validate({
            'global': {
                'targets_path': '/a',
                'artifacts_path': '/b',
                'inputs_path': '/c',
            },
            'fuzzers': {}
        })
