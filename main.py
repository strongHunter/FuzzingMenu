import os
import shlex
import yaml
import subprocess

from ui import FuzzingMenu, FuzzingCommand, UserExit
from items_extractor import BinaryExecutableExtractor
from command_generator import CommandGenerator

def exec_and_exit(cmd: str):
    args = shlex.split(cmd)
    os.execvp(args[0], args)

if __name__ == '__main__':
    directory = '.' # TODO: directory
    config_path = 'targets_config.yaml' # TODO

    extractor = BinaryExecutableExtractor(directory)
    with open(config_path) as f:
        config = yaml.safe_load(f)

    command_generator = CommandGenerator(config)

    app = FuzzingMenu(extractor, command_generator)
    result = app.run()
    match result:
        case FuzzingCommand():
            if result.prepare:
                subprocess.run(result.prepare, shell=True)
            exec_and_exit(result.cmd)
        case UserExit():
            exit(0)
        case _:
            raise TypeError(f'Unexpected return type: {type(result)}')    
