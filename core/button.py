
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex as hex

from kivy.lang.builder import Builder
Builder.load_string('''
#<KvLang>
<BasicButton>:
    canvas.before:
        Color:
            rgba: root.inner_line_color
        Line:
            width: 2
            rectangle: self.x, self.y, self.width, self.height
        
        Color:
            rgba: root.outer_line_color
        Line:
            width: 1
            rectangle: self.x-4, self.y-4, self.width+8, self.height+8

#</KvLang>
''')

class BasicButton(Button):
    inner_line_color = ObjectProperty(hex('#26c7e5'))
    outer_line_color = ObjectProperty(hex('#26c7e5'))
