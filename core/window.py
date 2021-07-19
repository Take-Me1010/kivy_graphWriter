
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App


class WindowBase(FloatLayout):
    ''' 全てのwindowの基底クラス '''
    def __init__(self, **kwargs):
        super(WindowBase, self).__init__(**kwargs)
        self.cont = App.get_running_app().cont