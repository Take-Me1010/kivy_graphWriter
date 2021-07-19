from typing import Dict, List, Tuple, Union
from kivy.properties import ListProperty
from core.exceptions import *
from core.window import WindowBase

from formulawindow.rvcells import FormulaCell, CSVDataCell

from kivy.lang.builder import Builder
Builder.load_string('''
#<KvLang>
<FormulaWindow>:
    rv_csv: rv_csv
    rv_csv_layout: rv_csv_layout
    rv_formula: rv_formula
    rv_formula_layout: rv_formula_layout
    mode: 'Scatter'
    plus_btn_src: repath('./data/image/button/plus.png')
    TabbedPanel:
        do_default_tab: False
        size_hint: 0.95, 0.75
        pos_hint: {'x':0.025, 'y':0.25}
        TabbedPanelItem:
            text: 'CSVList'
            RecycleView:
                id: rv_csv
                scroll_type: ['bars', 'content']
                scroll_wheel_distance: sp(30) #スクロール速度
                bar_width: sp(10)
                viewclass: 'CSVDataCell'
                RecycleBoxLayout:
                    id: rv_csv_layout
                    default_size: None, sp(70)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'
                    spacing: dp(8)

        TabbedPanelItem:
            text: 'Formula'
            FloatLayout:
                FloatLayout:
                    size_hint: 1, 0.05
                    pos_hint: {'x':0, 'y':0.95}
                    ImageButton:
                        size_hint: 0.1, 1
                        pos_hint: {'x':0, 'y':0}
                        source: root.plus_btn_src
                        src_normal: root.plus_btn_src
                        src_down: root.plus_btn_src
                        on_release: app.cont.add_formula()
                    Label:
                        size_hint: 0.1, 1
                        pos_hint: {'x':0.2, 'y':0}
                        text: '数式追加'
                        
                RecycleView:
                    id: rv_formula
                    size_hint: 1, 0.95
                    pos_hint: {'x':0, 'y':0}
                    scroll_type: ['bars', 'content']
                    scroll_wheel_distance: sp(30) #スクロール速度
                    bar_width: sp(10)
                    viewclass: 'FormulaCell'
                    RecycleBoxLayout:
                        id: rv_formula_layout
                        default_size: None, sp(60)
                        default_size_hint: 1, None
                        size_hint_y: None
                        height: self.minimum_height
                        orientation: 'vertical'
                        spacing: dp(8)
    # TabbedPanel //
    FloatLayout:
        size_hint: 0.95, 0.25
        pos_hint: {'x':0.025, 'y':0}
        # 保存設定部分
        FloatLayout:
            size_hint: 1, 0.6
            pos_hint: {'x':0, 'y':0.4}
            # 保存先
            BoxLayout:
                size_hint: 1, 0.33
                pos_hint: {'x':0, 'y':0.66}
                Label:
                    size_hint_x: 0.3
                    text: '保存先'
                
                TextInput:
                    size_hint_x: 0.7
                    line_height: 1
                    id: savedir
                    multiline: False
                    #TODO デフォルト設定から読み込むようにする
                    text: 'C:/Users/taketo/Desktop/大学関係/電気電子工学実験'

            # 保存名
            BoxLayout:
                size_hint: 1, 0.33
                pos_hint: {'x':0, 'y':0.33}
                Label:
                    size_hint_x: 0.3
                    text: '保存名'
                
                TextInput:
                    size_hint_x: 0.7
                    line_height: 1
                    id: savename
                    multiline: False
                    #TODO デフォルト設定から読み込むようにする
                    text: 'image.png'

            # 保存ボタン
            BasicButton:
                size_hint: 0.8, 0.27
                pos_hint: {'x':0.1, 'y':0.03}
                text: 'save plot'
                on_release: app.cont.save_plot(savedir.text+'/'+savename.text)
        
        
        FloatLayout:
            size_hint: 1, 0.4
            pos_hint: {'x':0, 'y':0}
            
            # モード切替スピンボックス
            Spinner:
                id: modespin
                size_hint: 1, 0.5
                pos_hint: {'x':0, 'y':0.5}
                text: 'Scatter'
                values: root.MODES
                on_text: root.mode = self.text
            # プロット実行ボタン
            BasicButton:
                text: 'Plot'
                on_release: app.cont.plot()
                size_hint: 1, 0.4
                pos_hint: {'x':0, 'y':0.05}

#</KvLang>
''')

class FormulaWindow(WindowBase):
    '''数式などを調整するWindow

        rv_csv : {RecycleView} csvデータ表示テーブル。
    
    '''
    MODES = ListProperty(['Scatter', 'Scatter+Line', 'Line', 'Approx', 'Function', 'Histgram'])
    def __init__(self, **kwargs):
        super(FormulaWindow, self).__init__(**kwargs)
        self.registered_values = {}
    
    def get_csv_paths(self) -> List[str]:
        ds : List[Dict[str, str]] = self.rv_csv.data
        return [d['path'] for d in ds]
    
    def get_csv_labels(self) -> List[str]:
        ds : List[Dict[str, str]] = self.rv_csv.data
        return [d['label'] for d in ds]
    
    def get_csv_rvdata(self) -> List[Dict[str, str]]:
        """csvセルの辞書データを得る

        Returns:
            List[Dict[str, str]]: 数式セルのデータのリスト
        """
        return self.rv_csv.data

    def append_csv_list(self, label:str, path:str):
        i = len(self.rv_csv.data)
        self.rv_csv.data.append({'label':label, 'path':path, 'index':i})
    
    def delete_csv_list_by_path(self, path:str):
        """pathのCSVを消去する

        Args:
            path (str): 消去したいcsvファイルのパス

        Raises:
            NoCSVPathFound: pathが存在しなかった場合
        """        
        ds = self.rv_csv.data
        index = -1
        for i, d in enumerate(ds):
            if d['path'] == path:
                index = i;
                break
        
        if index == -1:
            raise NoCSVPathFound(f'couldn\'t find the target file; {path}')
        
        else:
            self.delete_csv_list_by_index(index)
    
    def delete_csv_list_by_index(self, index:int):
        """indexで指定したCSVを消去する

        Args:
            index (int): 消去対象のindex
        """        
        ds = self.rv_csv.data
        del ds[index]
        for d in ds:
            if index < d['index']:
                d['index'] -= 1
        self.rv_csv.data = ds

    def get_formulas(self) -> List[str]:
        """数式のみを取り出す

        Returns:
            List[str]: 数式のリスト
        """
        return [d['formula'] for d in self.rv_formula.data]
    
    def get_formulas_rvdata(self) -> List[Dict[str, str]]:
        """数式セルの辞書データを得る

        Returns:
            List[Dict[str, str]]: セルのデータ
        """
        return self.rv_formula.data

    def add_formula_cell(self):
        i = len(self.rv_formula.data)
        d = self.rv_formula.data
        d.append({'formula' : '', 'index' : i})

    def delete_formula(self, formula:str):
        index = -1
        for i, d in enumerate(self.rv_formula.data):
            if d['formula'] == formula:
                index = i;
                break
        
        if index == -1:
            raise NoCSVPathFound(f'couldn\'t find the target file; {formula}')
        
        else:
            self.delete_formula_by_index(index)
    
    def delete_formula_by_index(self, index:int):
        ds = self.rv_formula.data
        del ds[index]
        for d in ds:
            if index < d['index']:
                d['index'] -= 1

        if not ds:
            ds.append({'formula' : '', 'index':0})
        self.rv_formula.data = ds

    def transpose_formula(self, i:int, j:int):
        """数式の順番を入れ替える

        Args:
            i (int): index
            j (int): index
        """
        if i <= -1 or j <= -1:
            print(f'[WARNING\t] [FormulaWindow\t] failed to transpose({i}, {j})')
            return
        
        ds = self.rv_formula.data
        try:
            ds[i]['index'] = j
            ds[j]['index'] = i
        except IndexError:
            print(f'[WARNING\t] [FormulaWindow\t] failed to transpose({i}, {j})')
            return

        ds[i], ds[j] = ds[j], ds[i]
        
        self.rv_formula.data = ds

    def set_save_dir(self, dir:str):
        """保存ディレクトリをセットする

        Args:
            dir (str): 保存先ディレクトリ
        """
        self.ids['savedir'].text = dir
    
    def get_save_dir(self) -> str:
        """保存ディレクトリを得る

        Returns:
            str: 保存ディレクトリ
        """
        return self.ids["savedir"].text
    
    def set_save_name(self, name:str):
        """保存名をセットする

        Args:
            name (str): 保存名
        """
        self.ids['savename'].text = name
    
    def get_save_name(self) -> str:
        return self.ids['savename'].text

    def set_mode(self, mode:str):
        if mode not in self.MODES:
            raise ValueError(f'{mode} is not proper.')

        self.mode = mode
        self.ids['modespin'].text = mode
    
    def set_rv_csv_data(self, data:List[Dict[str, str]]):
        self.rv_csv.data = data
    
    def set_rv_formula_data(self, data:List[Dict[str, str]]):
        self.rv_formula.data = data