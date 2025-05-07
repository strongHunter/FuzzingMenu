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

# def test_CommandGenerator_GlobalShouldBeReplaced(dummy_config):
#     cmd = dummy_config.create_command('')
