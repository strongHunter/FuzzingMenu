from ui import FuzzingMenu, FuzzingCommand, UserExit
from items_extractor import BinaryExecutableExtractor
from command_generator import CommandGenerator

if __name__ == '__main__':
    directory = '.' # TODO: directory
    extractor = BinaryExecutableExtractor(directory)

    from tests.test_command_generator import config # TODO
    command_generator = CommandGenerator(config)

    app = FuzzingMenu(extractor, command_generator)
    result = app.run()
    match result:
        case FuzzingCommand():
            if result.prepare:
                print(f'Prepare: {result.prepare}')
            print(f'Command: {result.cmd}')
        case UserExit():
            exit(0)
        case _:
            raise TypeError(f'Unexpected return type: {type(result)}')    
