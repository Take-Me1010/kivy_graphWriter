
from kivy.uix.floatlayout import FloatLayout
from kivy.lang.builder import Builder

Builder.load_string('''
#<KvLang>
#: import hex kivy.utils.get_color_from_hex
#: import repath libs.utils.resource_path
<RVCellBase>:
    del_btn_src: repath('./data/image/button/del.png')
    canvas.before:
        Color:
            rgba: hex('#26c7e5')
        Line:
            width: 1
            rectangle: self.x, self.y, self.width, self.height
#</KvLang>
''')
class RVCellBase(FloatLayout):
    pass