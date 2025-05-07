from ui import FuzzingMenu, FuzzingCommand, UserExit
from items_extractor import StubTargetsExtractor # TODO

if __name__ == '__main__':
    extractor = StubTargetsExtractor()

    app = FuzzingMenu(extractor)
    result = app.run()
    match result:
        case FuzzingCommand():
            print(f'Command: {result.cmd}')
        case UserExit():
            exit(0)
        case _:
            raise TypeError(f'Unexpected return type: {type(result)}')    
