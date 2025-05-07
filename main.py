from ui import FuzzingMenu, FuzzingCommand
from items_extractor import StubTargetsExtractor # TODO

if __name__ == '__main__':
    extractor = StubTargetsExtractor()

    app = FuzzingMenu(extractor)
    result: FuzzingCommand = app.run()
    print(f'Command: {result.cmd}')
