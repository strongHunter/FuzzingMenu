import pytest
import yaml
from command_generator import CommandGenerator

def example_config():
    with open("tests/targets_config_example.yaml") as f:
        config = yaml.safe_load(f)
        return config


@pytest.fixture
def dummy_config():
    command_generator = CommandGenerator(example_config())
    yield command_generator


def test_CommandGenerator_getTarget(dummy_config):
    from config_validation import Target
    def is_equal(target: Target, data: dict) -> bool:
        return target.model_dump(exclude_none=True) == data

    config = example_config()
    fuzzers = config['fuzzers']
    assert is_equal(dummy_config._get_target('target_1-afl'), fuzzers['afl']['target_1'])
    assert is_equal(dummy_config._get_target('target_2-afl'), fuzzers['afl']['target_2'])
    assert is_equal(dummy_config._get_target('target_3-afl'), fuzzers['afl']['target_3'])

    assert is_equal(dummy_config._get_target('target_1-lf'), fuzzers['libfuzzer']['target_1'])
    assert is_equal(dummy_config._get_target('target_2-lf'), fuzzers['libfuzzer']['target_2'])

def test_CommandGenerator_GlobalShouldBeReplaced(dummy_config):
    cmd = dummy_config.run_command_create('target_2-lf', 0)
    assert cmd == '/fuzzer/targets/target_2-lf.elf /fuzzer/artifacts/target_2 /fuzzer/corpus/target_2'

def test_CommandGenerator_ArgsShouldBeReplaced(dummy_config):
    cmd = dummy_config.run_command_create('target_1-lf', 0)
    assert cmd == '/fuzzer/targets/target_1-lf.elf /fuzzer/artifacts/target_1 /fuzzer/corpus/target_1 -timeout 60'

def test_CommandGenerator_EnvShouldBeInsertedIntoCommand(dummy_config):
    cmd = dummy_config.run_command_create('target_3-afl', 0)
    assert cmd == 'TMPDIR=/tmp/fuzzing afl-fuzz -i /fuzzer/corpus/target_3 -o /fuzzer/artifacts/target_3 -t 60000 -- /fuzzer/targets/target_3-afl.elf'

def test_CommandGenerator_EmptyPrepareShouldReturnsNone(dummy_config):
    cmd = dummy_config.prepare_command_create('target_1-afl')
    assert cmd is None

def test_CommandGenerator_PrepareShouldBeConcatenated(dummy_config):
    cmd = dummy_config.prepare_command_create('target_3-afl')
    assert cmd == 'mkdir /tmp/fuzzing && mount -t tmpfs -o size=10G tmpfs /tmp/fuzzing'

def test_CommandGenerator_ShouldHaveOneItem(dummy_config):
    rd = dummy_config.extract_runs('target_1-afl')
    assert len(rd) == 1

def test_CommandGenerator_ItemShouldHaveCorrectIndices(dummy_config):
    rd = dummy_config.extract_runs('target_2-afl')
    assert len(rd) == 2

    assert rd['generation'] == 0
    assert rd['mutation'] == 1

def test_CommandGenerator_CheckSecondIndex(dummy_config):
    cmd = dummy_config.run_command_create('target_2-afl', 1)
    assert cmd == 'AFL_CUSTOM_MUTATOR_ONLY=1 AFL_CUSTOM_MUTATOR_LIBRARY=$MUTATORS_PATH/mutator-target_2.so afl-fuzz -i /fuzzer/corpus/target_2 -o /fuzzer/artifacts/target_2 -- /fuzzer/targets/target_2-afl.elf'

def test_CommandGenerator_ShouldRaiseForInvalidIndex(dummy_config):
    invalid_index = 2
    with pytest.raises(IndexError):
        dummy_config.run_command_create('target_2-afl', invalid_index)
    

@pytest.fixture
def dummy_config_missing_args():
    incorrect_config = example_config()

    # Remove `args` from `target_1`
    # But `$ARGS` still inside `cmd` 
    incorrect_config['fuzzers']['libfuzzer']['target_1']['run'][0].pop('args')

    command_generator = CommandGenerator(incorrect_config)
    yield command_generator

def test_CommandGenerator_ShouldRaiseForNonexistentArgs(dummy_config_missing_args):
    with pytest.raises(ValueError):
        dummy_config_missing_args.run_command_create('target_1-lf', 0)


@pytest.fixture
def dummy_config_unexpected_args():
    incorrect_config = example_config()

    # Add `args` into `target_2`
    # But `$ARGS` not inside `cmd`
    incorrect_config['fuzzers']['libfuzzer']['target_2']['run'][0]['args'] = 'something args'

    command_generator = CommandGenerator(incorrect_config)
    yield command_generator

def test_CommandGenerator_ShouldRaiseForUnexpectedArgs(dummy_config_unexpected_args):
    with pytest.raises(KeyError):
        dummy_config_unexpected_args.run_command_create('target_2-lf', 0)


@pytest.fixture
def dummy_config_extended_env():
    extended_config = example_config()

    # Add another into `env` list
    extended_config['fuzzers']['afl']['target_3']['run'][0]['env'].append('ADDITIONAL_ENV=anything')

    command_generator = CommandGenerator(extended_config)
    yield command_generator

def test_CommandGenerator_ManyEnvShouldBeInsertedIntoCommand(dummy_config_extended_env):
    cmd = dummy_config_extended_env.run_command_create('target_3-afl', 0)
    assert cmd == 'TMPDIR=/tmp/fuzzing ADDITIONAL_ENV=anything afl-fuzz -i /fuzzer/corpus/target_3 -o /fuzzer/artifacts/target_3 -t 60000 -- /fuzzer/targets/target_3-afl.elf'
