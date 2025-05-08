import pytest
from command_generator import CommandGenerator

config = {
    "global": {
        "targets_path": "/fuzzer/targets",
        "artifacts_path": "/fuzzer/artifacts",
        "inputs_path": "/fuzzer/corpus",
        "mutators_path": "/fuzzer/mutators"
    },

    "fuzzers": {
        "afl": {
            "target_1": {
                "run": [
                    {
                        "cmd": "afl-fuzz -i $INPUTS_PATH/target_1 -o $ARTIFACTS_PATH/target_1 $ARGS -- $TARGETS_PATH/target_1-afl.elf",
                        "args": "-t 60000"
                    }
                ]
            },
            "target_2": {
                "run": [
                    {
                        "type": "generation",
                        "cmd": "afl-fuzz -i $INPUTS_PATH/target_2 -o $ARTIFACTS_PATH/target_2 $ARGS -- $TARGETS_PATH/target_2-afl.elf"
                    },
                    {
                        "type": "mutation",
                        "env": [
                            "AFL_CUSTOM_MUTATOR_ONLY=1",
                            "AFL_CUSTOM_MUTATOR_LIBRARY=$MUTATORS_PATH/mutator-target_2.so"
                        ],
                        "cmd": "afl-fuzz -i $INPUTS_PATH/target_2 -o $ARTIFACTS_PATH/target_2 $ARGS -- $TARGETS_PATH/target_2-afl.elf"
                    }
                ]
            },
            "target_3": {
                "prepare": [
                    "mkdir /tmp/fuzzing",
                    "mount -t tmpfs -o size=10G tmpfs /tmp/fuzzing"
                ],
                "run": [
                    {
                        "env": [
                            "TMPDIR=/tmp/fuzzing"
                        ],
                        "cmd": "afl-fuzz -i $INPUTS_PATH/target_3 -o $ARTIFACTS_PATH/target_3 $ARGS -- $TARGETS_PATH/target_3-afl.elf",
                        "args": "-t 60000"
                    }
                ]
            }
        },
        "libfuzzer": {
            "target_1": {
                "run": [
                    {
                        "cmd": "$TARGETS_PATH/target_1-lf.elf $ARTIFACTS_PATH/target_1 $INPUTS_PATH/target_1 $ARGS",
                        "args": "-timeout 60"
                    }
                ]
            },
            "target_2": {
                "run": [
                    {
                        "cmd": "$TARGETS_PATH/target_2-lf.elf $ARTIFACTS_PATH/target_2 $INPUTS_PATH/target_2"
                    }
                ]
            }
        }
    }
}

@pytest.fixture
def dummy_config():
    command_generator = CommandGenerator(config)
    yield command_generator


def test_CommandGenerator_ShouldSplitConfit_ToGlobalAndFuzzers(dummy_config):
    assert dummy_config._CommandGenerator__global == config['global']
    assert dummy_config._CommandGenerator__fuzzers == config['fuzzers']

def test_CommandGenerator_getTarget(dummy_config):
    fuzzers = config['fuzzers']
    assert dummy_config._get_target('target_1-afl') == fuzzers['afl']['target_1']
    assert dummy_config._get_target('target_2-afl') == fuzzers['afl']['target_2']
    assert dummy_config._get_target('target_3-afl') == fuzzers['afl']['target_3']

    assert dummy_config._get_target('target_1-lf') == fuzzers['libfuzzer']['target_1']
    assert dummy_config._get_target('target_2-lf') == fuzzers['libfuzzer']['target_2']

def test_CommandGenerator_GlobalShouldBeReplaced(dummy_config):
    cmd = dummy_config.run_command_create('target_2-lf')
    assert cmd == '/fuzzer/targets/target_2-lf.elf /fuzzer/artifacts/target_2 /fuzzer/corpus/target_2'

def test_CommandGenerator_ArgsShouldBeReplaced(dummy_config):
    cmd = dummy_config.run_command_create('target_1-lf')
    assert cmd == '/fuzzer/targets/target_1-lf.elf /fuzzer/artifacts/target_1 /fuzzer/corpus/target_1 -timeout 60'

def test_CommandGenerator_EnvShouldBeInsertedIntoCommand(dummy_config):
    cmd = dummy_config.run_command_create('target_3-afl')
    assert cmd == 'TMPDIR=/tmp/fuzzing afl-fuzz -i /fuzzer/corpus/target_3 -o /fuzzer/artifacts/target_3 -t 60000 -- /fuzzer/targets/target_3-afl.elf'

def test_CommandGenerator_EmptyPrepareShouldReturnsNone(dummy_config):
    cmd = dummy_config.prepare_command_create('target_1-afl')
    assert cmd is None

def test_CommandGenerator_PrepareShouldBeConcatenated(dummy_config):
    cmd = dummy_config.prepare_command_create('target_3-afl')
    assert cmd == 'mkdir /tmp/fuzzing && mount -t tmpfs -o size=10G tmpfs /tmp/fuzzing'


@pytest.fixture
def dummy_config_missing_args():
    incorrect_config = config

    # Remove `args` from `target_1`
    # But `$ARGS` still inside `cmd` 
    incorrect_config['fuzzers']['libfuzzer']['target_1']['run'][0].pop('args')

    command_generator = CommandGenerator(incorrect_config)
    yield command_generator

def test_CommandGenerator_ShouldRaiseForNonexistentArgs(dummy_config_missing_args):
    with pytest.raises(ValueError):
        dummy_config_missing_args.run_command_create('target_1-lf')


@pytest.fixture
def dummy_config_unexpected_args():
    incorrect_config = config

    # Add `args` into `target_2`
    # But `$ARGS` not inside `cmd`
    incorrect_config['fuzzers']['libfuzzer']['target_2']['run'][0]['args'] = 'something args'

    command_generator = CommandGenerator(incorrect_config)
    yield command_generator

def test_CommandGenerator_ShouldRaiseForUnexpectedArgs(dummy_config_unexpected_args):
    with pytest.raises(KeyError):
        dummy_config_unexpected_args.run_command_create('target_2-lf')


@pytest.fixture
def dummy_config_extended_env():
    extended_config = config

    # Add another into `env` list
    extended_config['fuzzers']['afl']['target_3']['run'][0]['env'].append('ADDITIONAL_ENV=anything')

    command_generator = CommandGenerator(extended_config)
    yield command_generator

def test_CommandGenerator_ManyEnvShouldBeInsertedIntoCommand(dummy_config_extended_env):
    cmd = dummy_config_extended_env.run_command_create('target_3-afl')
    assert cmd == 'TMPDIR=/tmp/fuzzing ADDITIONAL_ENV=anything afl-fuzz -i /fuzzer/corpus/target_3 -o /fuzzer/artifacts/target_3 -t 60000 -- /fuzzer/targets/target_3-afl.elf'
