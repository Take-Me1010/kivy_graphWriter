

from kivy.uix.button import Button
from kivy.lang.builder import Builder
Builder.load_string('''
#<KvLang>

<HeaderButton>:

#</KvLang>
''')


class HeaderButton(Button):
    pass