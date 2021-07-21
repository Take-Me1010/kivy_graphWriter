
from typing import Dict, List, Tuple
from pathlib import Path

from kivy.uix.floatlayout import FloatLayout

from core.exceptions import AlreadySetWindowsError
from header import Header
from filechooserwindow import FileChooserWindow
from plotwindow import PlotWindow
from formulawindow import FormulaWindow
from statemanager import StateManager
from libs.explorepopup import ExplorePopup
from libs.yesnopopup import YesNoPopup
from libs.utils import resource_path, Logger

class AppController:
    header : Header
    filechooserwindow : FileChooserWindow
    plotwindow : PlotWindow
    formulawindow : FormulaWindow
    wins : Dict[str, FloatLayout]
    '''アプリが保有する4つのwindow全てのリスト
    '''
    _has_wins : bool
    explore : ExplorePopup
    def __init__(self, app) -> None:
        self.app = app
        self.statemanager = StateManager(app)
        self._has_wins = False
        self.explore = ExplorePopup(
            filters=['*.json'],
            multiselect=False
        )
        self.explore.set_callback(
            on_canceled=self._fbrowser_canceled
        )
        self.logger = Logger(self)
        
    def _fbrowser_canceled(self, instance):
        self.explore.dismiss()
    
    def print_info(self, mes:str):
        self.logger.print_info(mes)
    
    def print_warn(self, mes:str):
        self.logger.print_warn(mes)

    def set_windows(self):
        """windowインスタンスを取得する

        Raises:
            AlreadySetWindowsError: 二回目にcallしたとき
        """        
        if self._has_wins:
            raise AlreadySetWindowsError('既にwinsを取得しています')

        self.wins = {
            'header' : self.app.root.ids['header'],
            'filechooserwindow' : self.app.root.ids['filechooserwindow'],
            'plotwindow' : self.app.root.ids['plotwindow'],
            'formulawindow' : self.app.root.ids['formulawindow']
        }
        self.header = self.wins['header']
        self.filechooserwindow = self.wins['filechooserwindow']
        self.plotwindow = self.wins['plotwindow']
        self.formulawindow = self.wins['formulawindow']
        self._has_wins = True
    
    def init_state_set(self):
        state = self.statemanager.load_state(path='./cache/previous.json')
        # self.print_info(f'[init_state_set] state : {state}')
        if state:
            self.load_state(state)

    def chenge_window_sizex(self, state:bool):
        """windowのサイズを変更する。

        Args:
            state (bool): True(=最大状態)なら最小化する。False(=最小状態)なら最大化する。
        """
        if state:
            self._minimize_filechooser()
        else:
            self._maximize_filechooser()
    
    def _minimize_filechooser(self):
        """ファイル選択ウィンドウを最小化する
        """        
        self.filechooserwindow.size_hint_x = 0.1
        self.plotwindow.size_hint_x = 0.6
        self.plotwindow.pos_hint['x'] = 0.1

        self.formulawindow.size_hint_x = 0.3
        self.formulawindow.pos_hint['x'] = 0.7
    
    def _maximize_filechooser(self):
        """ファイル選択ウィンドウを最大化する
        """        
        self.filechooserwindow.size_hint_x = 0.3
        self.plotwindow.size_hint_x = 0.5
        self.plotwindow.pos_hint['x'] = 0.3

        self.formulawindow.size_hint_x = 0.2
        self.formulawindow.pos_hint['x'] = 0.8

    def set_save_dir(self):
        """保存先ディレクトリをセットする。
        """        
        dir = self.filechooserwindow.get_selected_dir()
        self.formulawindow.set_save_dir(dir)
    
    def _setup_plot(self) -> Tuple[List[str], List[str]]:
        """setup plot. call ax.clear and set axis and options config

        Returns:
            Tuple[List[str], List[str]]: paths, labels
        """        
        self.plotwindow.clear_plots()
        axis = self.plotwindow.get_axis_configs()
        self.plotwindow.set_axis_configs(axis)
        options = self.plotwindow.get_plot_configs()
        self.plotwindow.set_plot_configs(options)
        advanced = self.plotwindow.get_advanced_configs()
        self.plotwindow.set_advanced_configs(advanced)

        paths = self.formulawindow.get_csv_paths()
        labels = self.formulawindow.get_csv_labels()

        return paths, labels

    def plot(self):
        """現在設定された設定でグラフを描画する.、具体的な各処理は委譲。
        """
        paths, labels = self._setup_plot()
        fs = self.formulawindow.get_formulas()
        mode : str = self.formulawindow.mode

        if mode == 'Scatter':
            self.plotwindow.scatter(paths, labels)
        
        elif mode == 'Scatter+Line':
            self.plotwindow.scatter_and_line(paths, labels)
        
        elif mode == 'Line':
            self.plotwindow.line(paths, labels)
            
        elif mode == 'Function':
            self.plotwindow.function_plot(fs)
        
        elif mode == 'Approx':
            self.plotwindow.approx_plot(paths, labels, fs)
        
        elif mode == 'Histgram':
            self.plotwindow.histgram(paths, labels)

    def save_plot(self, name='image.png'):
        """現在描画中のpltを画像として保存する

        Args:
            name (str, optional): 保存名。ディレクトリまで含む。. Defaults to 'image.png'.
        """
        self.plotwindow.save(name)
    
    def append_csv(self):
        """現在選択中のcsvファイルをリストに追加する
        """
        paths = self.filechooserwindow.get_selected_files()
        for p in paths:
            self.formulawindow.append_csv_list('Label', p)

    def delete_csv(self, path:str):
        """pathのCSVファイルをリストから消去する

        Args:
            path (str): 消去したいパス名
        """
        self.formulawindow.delete_csv_list_by_path(path)

    def add_formula(self):
        """空白の数式を追加する
        """
        self.formulawindow.add_formula_cell()

    def delete_formula(self, formula:str):
        """数式を削除する

        Args:
            formula (str): 削除したい数式
        """
        self.formulawindow.delete_formula(formula)
    
    def tranpose_formula(self, i:int, j:int):
        """数式を入れ替える

        Args:
            i (int): 対象1
            j (int): 対象2
        """
        self.formulawindow.transpose_formula(i, j)
    
    def load_state(self, state:dict):
        """stateに基づいてデータをセットする

        Args:
            state (dict): state
        """
        try:
            path = state.get('FileChooserWindow')['path']
            self.filechooserwindow.set_filechooser_path(path)
        except (KeyError, TypeError, FileNotFoundError) as e:
            self.print_warn(f'failed to load {state} in FileChooserWindow due to {e}')

        try:
            plotconfigs = state.get('PlotWindow')
            self.plotwindow.set_axis_configs_display(plotconfigs['axisconfig'])
            self.plotwindow.set_plot_configs_displey(plotconfigs['plotconfig'])
            self.plotwindow.set_advanced_configs_display(plotconfigs['advancedconfig'])
        except (KeyError, TypeError) as e:
            self.print_warn(f'failed to load {state} in PlotWindow due to {e}')

        try:
            formulaconfig = state.get('FormulaWindow')
            self.formulawindow.set_mode(formulaconfig['mode'])
            self.formulawindow.set_rv_csv_data(formulaconfig['rv_csv.data'])
            self.formulawindow.set_rv_formula_data(formulaconfig['rv_formula.data'])
            self.formulawindow.set_save_dir(formulaconfig['savedir'])
            self.formulawindow.set_save_name(formulaconfig['savename'])

        except (KeyError, TypeError) as e:
            self.print_warn(f'failed to load {state} in FormulaWindow due to {e}')
    
    def load_state_from_file(self, path:str):
        state = self.get_state_from_file(path)
        if state:
            self.load_state(state)
        
        else:
            self.print_warn(f'[file_load\t] {path} is invalid.')

    def get_state(self) -> dict:
        """現在のデータをstateにして返す

        Returns:
            dict: state
        """
        state = {}
        state['FileChooserWindow'] = {'path' : self.filechooserwindow.path}
        axisconfig     = self.plotwindow.get_axis_configs()
        plotconfig     = self.plotwindow.get_plot_configs()
        advancedconfig = self.plotwindow.get_advanced_configs()
        state['PlotWindow'] = {'axisconfig':axisconfig,'plotconfig':plotconfig, 'advancedconfig':advancedconfig}
        fw = self.formulawindow
        state['FormulaWindow'] = {
            'mode' : fw.mode,
            'rv_csv.data' : fw.get_csv_rvdata(),
            'rv_formula.data' : fw.get_formulas_rvdata(),
            'savedir' : fw.get_save_dir(),
            'savename' : fw.get_save_name()
        }
        return state
    
    def get_state_from_file(self, path:str) -> dict:
        return self.statemanager.load_state(path)
    
    def write_state_to_file(self, path:str, state:dict=None):
        if state is None:
            state = self.get_state()
        
        # self.print_info(f'[self.write_state_to_file] write {state} in {path}')
        self.statemanager.write_state(path, state)

    def on_stop(self, *args):
        ''' called when application stops. '''
        state = self.get_state()
        previous = resource_path('./cache/previous.json')
        self.write_state_to_file(path=previous, state=state)
    
    def end(self):
        """アプリ終了確認を行い、Yesなら終了する。
        """        
        def yes(instance):
            p.dismiss()
            self.app.stop()
        
        def no(instance):
            p.dismiss()

        p = YesNoPopup(
            title='confirm',
            message='close this app ?',
            size_hint=(0.4, 0.3),
            pos_hint={'x':0.3, 'y':0.35}
        )
        p.bind(
            on_yes=yes,
            on_no=no
        )
        p.open()

    def file_load(self):
        def _fbrowser_success(instance):
            try:
                path = instance.selection[0]
            except IndexError:
                self.print_warn('failed to get the selected file.')
                return
            
            self.load_state_from_file(path)
            self.explore.dismiss()
        
        self.explore.set_mode(mode='file')
        self.explore.set_callback(
            on_success=_fbrowser_success,
            on_submit=_fbrowser_success
        )
        self.explore.open()
    
    def file_save(self):
        def _fbrowser_success(instance):
            try:
                path = instance.selection[0]
            except IndexError:
                self.print_warn('failed to get the selected file.')
                return
            
            p = Path(path)
            if p.is_dir():
                p /= 'state.json'
            
            elif p.suffix != '.json':
                self.print_warn(f'the suffix must be json, not {p.suffix}')
                return

            self.write_state_to_file(path)
            self.explore.dismiss()

        self.explore.set_mode(mode='dir')
        self.explore.set_callback(
            on_success=_fbrowser_success,
            on_submit=_fbrowser_success
        )
        self.explore.open()
