
from typing import Callable, Dict, List
from itertools import zip_longest

import sympy
import numpy as np
from scipy.optimize import curve_fit

from plotwindow.formulaparser import VariableFactory
from libs.utils import load_csv

class Plotter:
    use_defferent_markers : bool
    # 散布図に異なるマーカーを用いるか
    def __init__(self, ax) -> None:
        self.ax = ax
        self.markers = [
            '.',
            's',
            'v',
            '*',
            'p',
            'h'
        ]
        self.use_defferent_markers = False
        self.range_x = [-10, 10]        #TODO: デフォルト設定ロード

    def set_axis(self, **kwargs):
        """軸に関する設定をする
            kwargs : 
                xmin, xmax, ymin, ymax : それぞれの軸のグラフの最大最小
                xlabel, ylabel : 軸のラベル
        """        
        xmin = kwargs.pop('xmin', None)
        xmax = kwargs.pop('xmax', None)
        if xmin and xmax:
            self.range_x = [xmin, xmax]
            self.ax.set_xlim([xmin, xmax])

        ymin = kwargs.pop('ymin', None)
        ymax = kwargs.pop('ymax', None)
        if ymin and ymax:
            # self.range_y = [ymin, ymax]
            self.ax.set_ylim([ymin, ymax])
        
        xlabel = kwargs.pop('xlabel', None)
        ylabel = kwargs.pop('ylabel', None)
        if xlabel:
            # self.ax.set_xlabel("$"+ xlabel + "$", size = 14, weight = "light")
            self.ax.set_xlabel(self._format_label(xlabel), size = 14, weight = "light")
        
        if ylabel:
            # self.ax.set_xlabel("$"+ ylabel + "$", size = 14, weight = "light")
            self.ax.set_ylabel(self._format_label(ylabel), size = 10, weight = "light")
    
    def _format_label(self, label:str) -> str:
        """labelを$$で囲んで返す

        Args:
            label (str): ラベル文字列

        Returns:
            str: $に挟まれた文字列
        """
        return '$' + label + '$'

    def set_title(self, title=None):
        """グラフタイトルを設定する

        Args:
            title (str, optional): グラフタイトル. Defaults to None.
        """        
        if title:
            self.ax.set_title("$"+title+"$", fontsize=16)
    
    def set_options(self, **kwargs):
        """オプション設定をする
            kwargs : 
                grid : 補助線を引くか
                log_x, log_y : 対数スケールにするか
                markers : 散布図のマーカーを変更するか
        """
        grid = kwargs.pop('grid', False)
        if grid:
            self.ax.grid(which="major", axis="both")
        else:
            self.ax.grid(b=False)
        
        log_x = kwargs.pop('log_x', False)
        if log_x:
            self.ax.set_xscale("log")
        log_y = kwargs.pop('log_y', False)
        if log_y:
            self.ax.set_yscale("log")
        
        self.use_defferent_markers = kwargs.pop('markers', False)
    
    def set_advanced_config(self, **kwargs):
        xpad = kwargs.pop('xpad', (0, 0))
        self.range_x = [self.range_x[0]+xpad[0], self.range_x[1]-xpad[1]]

        self.xinterval = kwargs.pop('xinterval', 0.01)

    def clear_plots(self):
        self.ax.clear()

    def _get_plot_kwargs(self, label:str, i:int) -> Dict[str, any]:
        """plotする際のキーワード引数を得る

        Args:
            label (str): ラベル名
            i (int): 何番目のプロットか

        Returns:
            Dict[str, any]: キーワード引数のための辞書
        """
        kw = {}
        if label:
            kw['label'] = "$" + label + "$"
        if self.use_defferent_markers:
            try:
                kw['marker'] = self.markers[i]
            except IndexError:
                print(f'[Warning\t] [Plotter\t\t] default marker used due to too many csvs.')
        
        return kw
    
    def _set_legend(self):
        """legendを実行する

        Returns:
            Legend: Legendオブジェクト
        """
        return self.ax.legend(
            bbox_to_anchor=[1, 1],
            loc="upper right",
            borderaxespad=0
        )

    def csv_plot_base(self, paths:List[str], labels:List[str], plotfunc:callable):
        """csvを利用するplotの基本骨格を実行し、plotfuncを実行する

        Args:
            plotfunc (callable): scatter, plotなどを行う関数。xdata, ydata. **kwを受け取り、何らかのインスタンスを返す
        """
        ret = []
        for i, (path, label) in enumerate(zip(paths, labels)):
            xdata, ydata = load_csv(path)
            kw = self._get_plot_kwargs(label, i)

            ret.append(plotfunc(xdata, ydata, **kw))
        
        if any(labels):
            self._set_legend()

        return ret

    def scatter(self, paths:List[str], labels:List[str]) -> list:
        """散布図を描画する

        Args:
            paths (List[str]): csvのパスリスト
            labels (List[str]): ラベルのリスト

        Returns:
            list: PathCollectionsが返却される
        """
        def func(xdata, ydata, **kw):
            return self.ax.scatter(xdata, ydata, **kw)

        ret = self.csv_plot_base(paths, labels, func)

        return ret
    
    def line(self, paths:List[str], labels:List[str]) -> list:
        """折れ線を描画する

        Args:
            paths (List[str]): csvのパスリスト
            labels (List[str]): ラベルのリスト
        
        Returns:
            list: Line2Dインスタンスのリストが返却される
        """
        def func(xdata, ydata, **kw):
            return self.ax.plot(xdata, ydata, **kw)
        
        lines = self.csv_plot_base(paths, labels, func)
        return lines
    
    def scatter_and_line(self, paths:List[str], labels:List[str]) -> list:
        """折れ線と散布図を描画する

        Args:
            paths (List[str]): csvのパスリスト
            labels (List[str]): ラベルのリスト
        
        Returns:
            list: Line2Dインスタンスのリストが返却される
        """
        def func(xdata, ydata, **kw):
            line = self.ax.plot(xdata, ydata, **kw)
            kw.pop('label', None)
            self.ax.scatter(xdata, ydata, **kw)
            return line
        
        lines = self.csv_plot_base(paths, labels, func)

        return lines
    
    def histgram(self, paths:List[str], labels:List[str]) -> list:
        """ヒストグラムを描画する

        Args:
            paths (List[str]): csvのパスリスト
            labels (List[str]): ラベルのリスト

        """
        def func(xdata, ydata, **kwargs):
            hist = self.ax.hist(xdata, ydata, **kwargs)
            return hist
        
        hists = self.csv_plot_base(paths, labels, func)
        return hists

    def func_plot(self, funcs:List[callable], labels:List[str]) -> list:
        lines = []
        x = np.arange(self.range_x[0], self.range_x[1], self.xinterval)
        for i, (func, label) in enumerate(zip_longest(funcs, labels)):
            y = func(x)
            kw = self._get_plot_kwargs(label, i)
            line = self.ax.plot(x, y, **kw)

            lines.append(line)
        if labels:
            self._set_legend()

        return lines

    def approx_plot(self, paths:List[str], labels:List[str], approx:sympy.Poly):
        x = sympy.Symbol('x')
        args = VariableFactory.estimate_variables
        args.insert(0, x)
        target = sympy.lambdify(args, approx.as_expr(), ['numpy'])

        lines = []
        for i, (path, label) in enumerate(zip(paths, labels)):
            xdata, ydata = load_csv(path)
            param, _ = curve_fit(target, xdata, ydata)

            print(f'[INFO\t] [plotter.approx_plot] label : {label} param : {param}')

            X = np.arange(self.range_x[0], self.range_x[1], self.xinterval)
            Y = target(X, *param)

            # 散布図
            kw = self._get_plot_kwargs(label, i)
            self.ax.scatter(xdata, ydata, **kw)

            kw.pop('label', None)
            # 近似曲線
            line = self.ax.plot(X, Y, **kw)
            lines.append(line)

        if any(labels):
            self._set_legend()
        
        return lines