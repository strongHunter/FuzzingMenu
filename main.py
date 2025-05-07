from ui import FuzzingMenu, FuzzingCommand, UserExit
from items_extractor import StubTargetsExtractor # TODO
from command_generator import CommandGenerator

if __name__ == '__main__':
    extractor = StubTargetsExtractor()
    command_generator = CommandGenerator({}) # TODO

    app = FuzzingMenu(extractor, command_generator)
    result = app.run()
    match result:
        case FuzzingCommand():
            print(f'Command: {result.cmd}')
        case UserExit():
            exit(0)
        case _:
            raise TypeError(f'Unexpected return type: {type(result)}')    
