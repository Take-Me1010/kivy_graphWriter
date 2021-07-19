
from kivy.uix.image import Image
from kivy.uix.behaviors.button import ButtonBehavior

from libs.utils import resource_path

class ImageButton(ButtonBehavior, Image):
    def __init__(self, src_normal:str='', src_down:str='', **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.src_normal = src_normal
        self.src_down = src_down

        self.source = self.src_normal
        
        # レスポンシブデザイン
        self.allow_stretch = True
        self.keep_ratio = True
        self.height = self.width / self.image_ratio

    def on_press(self):
        self.source = self.src_down
    
    def on_release(self):
        self.source = self.src_normal



def main():
    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout
    from kivy.config import Config
    Config.set('modules', 'inspector', '')
    Config.set('modules', 'showborder', '')

    class TestApp(App):
        def __init__(self, **kwargs):
            super(TestApp, self).__init__(**kwargs)
        
        def build(self):
            self.root = root = FloatLayout()
            root.add_widget(ImageButton(
                src_normal=resource_path("../data/image/close_button_test_min.png"),
                src_down=resource_path("../data/image/close_button_test_min_down.png"),
                pos_hint={'x':0.5, 'y':0.5},
                size_hint=(1, None),
            ))
            return root

    TestApp().run()


if __name__ == '__main__':
    main()