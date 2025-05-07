from dataclasses import dataclass

from textual.app import App, ComposeResult
from textual.events import Key
from textual.widget import Widget
from textual.widgets import ListView, Label, ListItem, Footer, Header

from items_extractor import ItemsProvider
from command_generator import CommandGenerator

@dataclass
class FuzzingCommand:
    cmd: str

@dataclass
class UserExit :
    pass

class FuzzingMenu(App[UserExit | FuzzingCommand]):
    __items_provider: ItemsProvider
    __command_generator: CommandGenerator
    __main_widget: Widget
    __list_view: ListView

    TITLE = 'Fuzzing menu'
    BINDINGS = [
        ('q', '', 'Выйти'),
        ('d', 'toggle_dark', 'Переключение светлой/темной темы'),
    ]
    ENABLE_COMMAND_PALETTE = False

    CSS = '''
    Screen {
        align: center middle;
    }

    #main_widget {
        width: 80;
        height: 10;
        border: round #666;
    }
    '''

    def __init__(
            self,
            items_provider: ItemsProvider,
        ) -> None:
        self.__items_provider = items_provider
        self.__command_generator = CommandGenerator()
        self.__list_view = self._fill_view()
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        with Widget(id='main_widget') as self.__main_widget:
            yield self.__list_view
        yield Footer()

    async def on_key(self, event: Key) -> None:
        if event.key == 'ctrl+q':
            event.prevent_default()
            event.stop()
        elif event.key == 'q':
            self.exit(UserExit())

    def action_toggle_dark(self) -> None:
        self.theme = (
            'textual-dark' if self.theme == 'textual-light' else 'textual-light'
        )

    # async def on_mount(self) -> None:
    #     pass

    async def on_list_view_selected(self, event) -> None:
        item: ListItem = event.item
        text = FuzzingMenu.extract_text(
            FuzzingMenu.extract_label(item)
        )
        cmd = self.__command_generator.create_command(text)
        self._end_ui(FuzzingCommand(cmd))

    def _end_ui(self, retval) -> None:
        self.exit(retval)

    def _fill_view(self) -> ListView:
        items = self.__items_provider.items()
        list_items = [
            ListItem(Label(item)) for item in items
        ]
        return ListView(*list_items)
        
    @staticmethod
    def extract_label(item: ListItem) -> Label:
        return item.get_child_by_type(Label)
    
    @staticmethod
    def extract_text(label: Label) -> str:
        return label.renderable
