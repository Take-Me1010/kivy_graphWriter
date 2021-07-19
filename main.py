
from kivy.config import Config
# Config.set('modules', 'inspector', '')
# Config.set('modules', 'showBorder', '')
from libs.splash import Splash

with Splash('Waiting...', '(c) Take-Me1010'):
    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout

    import japanize_kivy

    from appcontroller import AppController

class RootWidget(FloatLayout):
    pass

class GraphGUI(App):
    def __init__(self, **kwargs):
        super(GraphGUI, self).__init__(**kwargs)

    def build(self):
        self.cont = AppController(self)
        self.root = RootWidget()

        self.cont.set_windows()
        self.cont.init_state_set()

        return self.root

    def on_stop(self, *args):
        self.cont.on_stop(*args)

        return super(GraphGUI, self).on_stop(*args)

def main():
    GraphGUI().run()

if __name__ == '__main__':
    main()