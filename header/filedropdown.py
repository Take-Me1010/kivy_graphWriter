
from kivy.uix.dropdown import DropDown

from kivy.lang.builder import Builder
Builder.load_string('''
#<KvLang>
<FileDropDown>:
    Button:
        text: 'Load State'
        size_hint_y: None
        height: 44
        on_release: app.cont.file_load()

    Button:
        text: 'Save State'
        size_hint_y: None
        height: 44
        on_release: app.cont.file_save()

#</KvLang>
''')

class FileDropDown(DropDown):
    pass
