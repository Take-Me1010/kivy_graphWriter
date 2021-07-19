
from core.exceptions import *
from core.window import WindowBase

from header.headerbutton import HeaderButton
from header.filedropdown import FileDropDown

from kivy.lang.builder import Builder
Builder.load_string('''
#<KvLang>

<Header>:
    FileButton:
        size_hint: (0.1, 0.9)
        pos_hint: {'x':0, 'y':0.05}
        text: 'File'

    # HeaderButton:
    #     size_hint: (0.1, 0.9)
    #     pos_hint: {'x':0.1, 'y':0.05}
    #     text: 'Edit'
    
    HeaderButton:
        size_hint: 0.1, 0.9
        pos_hint: {'x':0.8, 'y':0.05}
        text: 'end'
        on_release: app.cont.end()

#</KvLang>
''')

class FileButton(HeaderButton):
    def __init__(self, **kwargs) -> None:
        super(FileButton, self).__init__(**kwargs)
        self.dropdown = FileDropDown()
        self.bind(on_release=self.dropdown.open)


class Header(WindowBase):
    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)
