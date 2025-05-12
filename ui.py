from dataclasses import dataclass

from textual.app import App, ComposeResult
from textual.events import Key
from textual.widget import Widget
from textual.widgets import ListView, Label, ListItem, Footer, Header
from textual.containers import Vertical

from items_extractor import ItemsProvider
from command_generator import CommandGenerator

@dataclass
class FuzzingCommand:
    prepare: None | str
    cmd: str

@dataclass
class UserExit :
    pass

class FuzzingMenu(App[UserExit | FuzzingCommand]):
    __items_provider: ItemsProvider
    __command_generator: CommandGenerator
    __main_widget: Widget
    __list_view: ListView
    __selected: dict[str, int]

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
            command_generator: CommandGenerator,
        ) -> None:
        self.__items_provider = items_provider
        self.__command_generator = command_generator
        self.__list_view = self._fill_view()
        self.__selected = {}
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

    # TODO: refactor
    # Maybe State 1 -> end OR State 1 -> State 2 -> State 3 -> end
    async def on_list_view_selected(self, event) -> None:
        item: ListItem = event.item
        text = FuzzingMenu.extract_text(
            FuzzingMenu.extract_label(item)
        )
        # State 3: end selection
        if self.__selected:
            target = self.__list_view.get_title()
            index = self.__selected[text]

            prepare = self.__command_generator.prepare_command_create(target)
            cmd = self.__command_generator.run_command_create(target, index)
            self._end_ui(FuzzingCommand(prepare, cmd))
            return
        
        runs = self.__command_generator.extract_runs(text)
        
        # State 2: target sub-selection 
        if len(runs) > 1:
            self.__selected = runs
            items = runs.keys()
            list_items = [
                ListItem(Label(item)) for item in items
            ]
            
            lv = ListView(*list_items)
            sv = SwitchableView(text, lv)
            
            self.__list_view.display = False
            self.__main_widget.mount(sv)
            return

        # State 1: default selection
        index = 0
        prepare = self.__command_generator.prepare_command_create(text)
        cmd = self.__command_generator.run_command_create(text, index)
        self._end_ui(FuzzingCommand(prepare, cmd))

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


class SwitchableView(Vertical):
    def __init__(self, title: str, initial_list: ListView) -> None:
        self._label = Label(title)
        self._list_view = initial_list
        super().__init__()

    async def on_mount(self) -> None:
        await self.mount(self._label)
        await self.mount(self._list_view)
        self.call_after_refresh(self._list_view.focus)
    
    def get_title(self) -> str:
        return self.extract_text(self._label)

    # TODO
    @staticmethod
    def extract_text(label: Label) -> str:
        return label.renderable
