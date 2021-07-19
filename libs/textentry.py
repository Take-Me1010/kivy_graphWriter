from kivy.uix.textinput import TextInput

class TextEntry(TextInput):
    '''
        single line text input.
        its height is 30 by default.
        if you want to change it, call like this; TextEntry(height=35)
    '''
    def __init__(self, **kwargs):
        super().__init__(multiline=False, **kwargs)
        self.size_hint_y = kwargs.get("size_hint_y", None)
        self.height = kwargs.get("height", 30)
    
    def on_enter(self):
        pass