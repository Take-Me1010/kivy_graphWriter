
from formulawindow.rvbase import RVCellBase

from kivy.lang.builder import Builder
Builder.load_string('''
#<KvLang>
#: import BasicButton core.button.BasicButton
#: import ImageButton libs.imagebutton.ImageButton
#: import repath libs.utils.resource_path

<CSVDataCell>:
    label: ''
    path: ''
    index: -1
    # del_btn_src は親クラスで定義
    ImageButton:
        size_hint: 0.048, 0.98
        pos_hint: {'x':0.01, 'y':0.01}
        source: root.del_btn_src
        src_normal: root.del_btn_src
        src_down: root.del_btn_src
        on_release: app.cont.delete_csv(root.path)

    Label:
        text: 'Label :'
        size_hint: 0.25, 0.5
        pos_hint: {'x':0.05, 'y':0.5}
    TextInput:
        text: root.label
        line_height: 1
        multiline: False
        size_hint: 0.7, 0.5
        pos_hint: {'x':0.3, 'y':0.5}
        on_text_validate:
            root.label = self.text
            root.parent.parent.data[root.index]['label'] = self.text
    Label:
        text: 'Path :'
        size_hint: 0.25, 0.5
        pos_hint: {'x':0.05, 'y':0}
    TextInput:
        text: root.path
        line_height: 1
        multiline: False
        size_hint: 0.7, 0.5
        pos_hint: {'x':0.3, 'y':0}
        on_text_validate:
            root.path = self.text
            root.parent.parent.data[root.index]['path'] = self.text
#</KvLang>
''')

class CSVDataCell(RVCellBase):
    pass

Builder.load_string('''
#<KvLang>
#: import repath libs.utils.resource_path
<ValidButton@Label+ButtonBehavior>:
    isvalid: True
    back_c: (1, 1, 1, 1)
    canvas.before:
        Color:
            rgba: root.back_c
        Rectangle:
            size: self.size
            pos: self.pos
    
    text: '無効化'

    on_release:
        self.text = ['無効化', '有効化'][self.isvalid]
        self.back_c =[(1, 1, 1, 1), (0, 0, 0, 1)][self.isvalid]
        self.isvalid = not self.isvalid
    
<FormulaCell>:
    formula: ''
    index: -1
    isvalid: True
    up_btn_src: repath('./data/image/button/up_btn.png')
    down_btn_src: repath('./data/image/button/down_btn.png')
    # del_btn_src は親クラスで定義
    ImageButton:
        size_hint: 0.048, 0.98
        pos_hint: {'x':0.01, 'y':0.01}
        source: root.del_btn_src
        src_normal: root.del_btn_src
        src_down: root.del_btn_src
        on_release: app.cont.delete_formula(root.formula)

    TextInput:
        text: root.formula
        line_height: 1
        multiline: False
        font_size: 25
        size_hint: 0.85, 0.98
        pos_hint: {'x':0.055, 'y':0.01}
        on_text_validate:
            root.formula = self.text
            root.parent.parent.data[root.index]['formula'] = self.text
    
    ImageButton:
        size_hint: 0.05, 0.5
        pos_hint: {'x':0.925, 'y':0.5}
        source: root.up_btn_src
        src_normal: root.up_btn_src
        src_down: root.up_btn_src
        on_release:
            app.cont.tranpose_formula(root.index, root.index-1)

    ImageButton:
        size_hint: 0.05, 0.5
        pos_hint: {'x':0.925, 'y':0}
        source: root.down_btn_src
        src_normal: root.down_btn_src
        src_down: root.down_btn_src
        on_release:
            app.cont.tranpose_formula(root.index, root.index+1)


    #TODO: 順番入れ替え処理の追加

#</KvLang>
''')

class FormulaCell(RVCellBase):
    pass