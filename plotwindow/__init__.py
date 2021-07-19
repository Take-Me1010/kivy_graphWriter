
from typing import Dict, List, Tuple, Union

import sympy
import matplotlib
matplotlib.use('module://libs.garden.matplotlib.backend_kivy')
import matplotlib.pyplot as plt

from kivy.uix.floatlayout import FloatLayout

from core.exceptions import *
from core.window import WindowBase
from plotwindow.plotter import Plotter
from plotwindow.formulaparser import FormulaFormatter, FormulaParser, VariableFactory

from kivy.lang.builder import Builder
Builder.load_string('''
#<KvLang>
<OptionCheck@FloatLayout>:
    active: ch.active
    text: ''
    CheckBox:
        id: ch
        size_hint: 0.1, 0.9
        pos_hint: {'x':0, 'y':0.05}
    
    Label:
        size_hint: 0.9, 0.9
        pos_hint: {'x':0.1, 'y':0.05}
        text_size: self.size
        halign: 'left'
        text: root.text

<PlotConfigFrame@FloatLayout>:
    grid: grid.active
    log_x: log_x.active
    log_y: log_y.active
    markers: markers.active
    OptionCheck:
        id: grid
        size_hint: 1, 0.25
        pos_hint: {'x':0, 'y':0.75}
        text: "グリッド線を表示する"
    OptionCheck:
        id: log_x
        size_hint: 1, 0.25
        pos_hint: {'x':0, 'y':0.5}
        text: "x軸を対数スケールにする"
    OptionCheck:
        id: log_y
        size_hint: 1, 0.25
        pos_hint: {'x':0, 'y':0.25}
        text: "y軸を対数スケールにする"
    OptionCheck:
        id: markers
        size_hint: 1, 0.25
        pos_hint: {'x':0, 'y':0}
        text: "散布図に異なるマーカーを使用する"

<AxisConfigFrame@TabbedPanel>:
    do_default_tab: False
    tab_height: 20
    xmin: xmin.text
    xmax: xmax.text
    ymin: ymin.text
    ymax: ymax.text
    title: title.text
    xlabel: xlabel.text
    ylabel: ylabel.text

    xpad: (xpadleft.text, xpadright.text)
    xinterval: xinterval.text
    TabbedPanelItem:
        text: 'Normal'
        FloatLayout:
            # x軸範囲設定
            BoxLayout:
                size_hint: 1, 0.2
                pos_hint: {'x':0, 'y':0.8}
                TextInput:
                    id: xmin
                    size_hint_x: 0.4
                    multiline: False
                    hint_text: 'min for x'
                Label:
                    size_hint_x: 0.2
                    text: ' <= x <= '
                TextInput:
                    id: xmax
                    size_hint_x: 0.4
                    multiline: False
                    hint_text: 'max for x'

            # y軸範囲設定
            BoxLayout:
                size_hint: 1, 0.2
                pos_hint: {'x':0, 'y':0.6}
                TextInput:
                    id: ymin
                    size_hint_x: 0.4
                    multiline: False
                    hint_text: 'min for y'
                Label:
                    size_hint_x: 0.2
                    text: ' <= y <= '
                TextInput:
                    id: ymax
                    size_hint_x: 0.4
                    multiline: False
                    hint_text: 'max for y'
            # 軸・タイトル文字列設定
            BoxLayout:
                size_hint: 1, 0.6
                pos_hint: {'x':0, 'y':0}
                orientation: 'vertical'
                BoxLayout:
                    size_hint_y: 0.33
                    Label:
                        size_hint_x: 0.4
                        text: 'Graph Title'
                    TextInput:
                        id: title
                        size_hint_x: 0.6
                        multiline: False
                        hint_text: 'Graph Title'
                
                BoxLayout:
                    size_hint_y: 0.33
                    Label:
                        size_hint_x: 0.4
                        text: 'x-axis label'
                    TextInput:
                        id: xlabel
                        size_hint_x: 0.6
                        multiline: False
                        hint_text: 'x-axis label'
                
                BoxLayout:
                    size_hint_y: 0.33
                    Label:
                        size_hint_x: 0.4
                        text: 'y-axis label'
                    TextInput:
                        id: ylabel
                        size_hint_x: 0.6
                        multiline: False
                        hint_text: 'y-axis label'

            

    TabbedPanelItem:
        text: 'Advanced'
        FloatLayout:
            # padding設定
            FloatLayout:
                size_hint: 1, 0.2
                pos_hint: {'x':0, 'y':0.8}
                TextInput:
                    id: xpadleft
                    size_hint: 0.3, 1
                    pos_hint: {'x':0.05, 'y':0}
                    multiline: False
                    hint_text: 'left : 0'

                Label:
                    size_hint: 0.3, 1
                    pos_hint: {'x':0.35, 'y':0}
                    text: 'x-axis-padding'

                TextInput:
                    id: xpadright
                    size_hint: 0.3, 1
                    pos_hint: {'x':0.65, 'y':0}
                    multiline: False
                    hint_text: 'right : 0'
            # 関数プロットの時のサンプルの幅設定
            FloatLayout:
                size_hint: 1, 0.2
                pos_hint: {'x':0, 'y':0.6}
                Label:
                    size_hint: 0.3, 1
                    pos_hint: {'x':0.05, 'y':0}
                    text: 'x_interval'
                
                TextInput:
                    id: xinterval
                    size_hint: 0.3, 1
                    pos_hint: {'x':0.35, 'y':0}
                    multiline: False

<PlotWindow>:
    AxisConfigFrame:
        id: axisconfig
        size_hint: 0.6, 0.3
        pos_hint: {'x':0, 'y':0}
    PlotConfigFrame:
        id: plotconfig
        size_hint: 0.4, 0.3
        pos_hint: {'x':0.6, 'y':0}
#</KvLang>
''')

class PlotWindow(WindowBase):
    fig : plt.figure
    ax : plt.axes
    def __init__(self, **kwargs):
        super(PlotWindow, self).__init__(**kwargs)

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.size_hint= (1, 0.7)
        self.fig.canvas.pos_hint = {'x':0, 'y':0.3}
        self.add_widget(self.fig.canvas)

        self.plotter = Plotter(self.ax)
    
    def clear_plots(self):
        self.plotter.clear_plots()

    def get_plot_configs(self) -> Dict[str, bool]:
        con : List[FloatLayout] = self.ids['plotconfig']

        kw = {
            'grid' : con.grid,
            'log_x' : con.log_x,
            'log_y' : con.log_y,
            'markers' : con.markers
        }
        return kw

    def set_plot_configs(self, kw:dict):
        self.plotter.set_options(**kw)
    
    def set_plot_configs_displey(self, kw:dict):
        c = self.ids['plotconfig'].ids
        c['grid'].active = kw['grid']
        c['log_x'].active = kw['log_x']
        c['log_y'].active = kw['log_y']
        c['markers'].active = kw['markers']

    def get_axis_configs(self) -> Dict[str, Union[float, None]]:
        c = self.ids['axisconfig']
        kw = {}
        for key, val in zip(['xmin', 'xmax', 'ymin', 'ymax'], [c.xmin, c.xmax, c.ymin, c.ymax]):
            try:
                num = float(val)
            except:
                num = None
            kw[key] = num
        
        for key, val in zip(['title', 'xlabel', 'ylabel'], [c.title, c.xlabel, c.ylabel]):
            if val:
                kw[key] = val
            
            else:
                kw[key] = None

        return kw
    
    def set_axis_configs(self, kw:dict):
        self.plotter.set_axis(**kw)
        self.plotter.set_title(title=kw.pop('title', None))
    
    def set_axis_configs_display(self, kw:dict):
        c = self.ids['axisconfig'].ids
        for key in kw.keys():
            if kw[key]:
                if key in ['title', 'xlabel', 'ylabel']:
                    pass
                else:
                    kw[key] = str(kw[key])
            else:
                kw[key] = ''

        c['xmin'].text = kw['xmin']
        c['xmax'].text = kw['xmax']
        c['ymin'].text = kw['ymin']
        c['ymax'].text = kw['ymax']
        c['title'].text = kw['title']
        c['xlabel'].text = kw['xlabel']
        c['ylabel'].text = kw['ylabel']
    
    def get_advanced_configs(self) -> Dict[str, Union[float, Tuple[float]]]:
        c = self.ids['axisconfig']
        xpad = c.xpad
        try:
            xpad_left = float(xpad[0])
        except ValueError:
            xpad_left = 0
        
        try:
            xpad_right = float(xpad[1])
        except ValueError:
            xpad_right = 0
        
        try:
            xinterval = float(c.xinterval)
        except ValueError:
            xinterval = 0.01
        
        return {
            'xpad' : (xpad_left, xpad_right),
            'xinterval' : xinterval
        }

    def set_advanced_configs(self, kw:dict):
        self.plotter.set_advanced_config(**kw)
    
    def set_advanced_configs_display(self, kw:dict):
        c = self.ids['axisconfig'].ids
        c['xpadleft'].text = str(kw['xpad'][0])
        c['xpadright'].text = str(kw['xpad'][1])
        c['xinterval'].text = str(kw['xinterval'])

    def plot(self, x, y, clear:bool=False, **kwargs):
        if clear:
            self.clear_plots()

        self.plotter.plot(x, y, **kwargs)

        self.fig.canvas.draw()
    
    def scatter(self, paths, labels):
        self.plotter.scatter(paths, labels)
        self.fig.canvas.draw()
    
    def scatter_and_line(self, paths, labels):
        self.plotter.scatter_and_line(paths, labels)
        self.fig.canvas.draw()
    
    def line(self, paths, labels):
        self.plotter.line(paths, labels)
        self.fig.canvas.draw()
    
    def histgram(self, paths, labels):
        self.plotter.histgram(paths, labels)
        self.fig.canvas.draw()

    def function_plot(self, formulas:List[str]):
        polys = []
        labels = []
        # 登録を初期化
        VariableFactory.init()
        for formula in formulas:
            res = FormulaParser.parse(formula)

            if isinstance(res, dict):
                labels.append(res.pop('label', ''))

            elif isinstance(res, sympy.Poly):
                if len(res.atoms(sympy.Symbol)) > 1:
                    raise ValueError('undefined variables exist')
                
                poly = FormulaFormatter.poly2numpy(res, args=[sympy.symbols('x')])
                polys.append(poly)

        # print(f'[INFO\t] [plotWindow\t] [function_plot\t] polys : {polys}')

        self.plotter.func_plot(polys, labels)
        self.fig.canvas.draw()
    
    def approx_plot(self, paths:List[str], labels:List[str], formulas:List[str]):
        get_flag = False
        approx_formula = None
        # 登録を初期化
        VariableFactory.init()
        for formula in formulas:
            res = FormulaParser.parse(formula)

            if isinstance(res, dict):
                if res.get('estimate', False):
                    get_flag = True
                    # print(f'[INFO\t] [PlotWindow] [approx_plot] estimate : {res}')

            elif isinstance(res, sympy.Poly):
                if get_flag:
                    approx_formula = res
                    get_flag = False

        
        if approx_formula is None:
            raise FormulaParseError('No estimate set.')

        self.plotter.approx_plot(paths, labels, approx_formula)
        self.fig.canvas.draw()
    
    def save(self, name:str):
        if '.png' not in name:
            name += '.png'

        plt.savefig(name)