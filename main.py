from ui import FuzzingMenu
from items_extractor import StubTargetsExtractor # TODO

if __name__ == '__main__':
    extractor = StubTargetsExtractor()

    app = FuzzingMenu(extractor)
    app.run()
