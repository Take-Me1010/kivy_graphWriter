
from core.exceptions import *
from core.window import WindowBase

from kivy.lang.builder import Builder
Builder.load_string('''
#<KvLang>
#: import BasicButton core.button.BasicButton
#: import ImageButton libs.imagebutton.ImageButton
#: import repath libs.utils.resource_path
<FileChooserWindow>:
    btn_left: repath('./data/image/button/left.png')
    btn_right: repath('./data/image/button/right.png')
    path: 'C:/Users'
    ImageButton:
        id: arrow_btn
        size_hint_x: 0.5
        size_hint_y: 0.1
        pos_hint: {'x':0.5, 'y':0.95}
        source: root.btn_left
        src_normal: root.btn_left
        src_down: root.btn_left
        on_release: root.arrow_btn_clicked(self)

    BasicButton:
        size_hint_x: 0.8
        size_hint_y: 0.04
        pos_hint: {'x':0.1, 'y':0.905}
        text: 'Append'
        on_release: app.cont.append_csv()
    
    BasicButton:
        size_hint: 0.8, 0.04
        pos_hint: {'x':0.1, 'y':0.855}
        text: 'Set Save Dir'
        on_release: app.cont.set_save_dir()

    FileChooserListView:
        id: fc
        size_hint_x: 1.0
        size_hint_y: 0.8
        pos_hint: {'x':0, 'y':0}
        filters: ['*.csv', '*.json']
        # multiselect: True
        path: root.path
#</KvLang>
''')

class FileChooserWindow(WindowBase):
    maximize : bool
    # 最大化状態ならTrueにする。
    def __init__(self, **kwargs):
        super(FileChooserWindow, self).__init__(**kwargs)
        
        self.maximize = True

    def get_selected_files(self) -> list:
        return self.ids['fc'].selection
    
    def get_selected_dir(self) -> str:
        return self.ids['fc'].path

    def set_filechooser_path(self, path:str):
        self.ids['fc'].path = path

    def arrow_btn_clicked(self, instance, *args):
        if self.maximize:
            # 最小化する
            instance.src_normal = instance.src_down = self.btn_right
        else:
            # 最大化する
            instance.src_normal = instance.src_down = self.btn_left
        
        self.cont.chenge_window_sizex(self.maximize)

        self.maximize = not self.maximize