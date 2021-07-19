
import os, sys, csv
from typing import Tuple
import numpy as np

def resource_path(relative:str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)

    return os.path.join(relative)

def load_csv(path) -> Tuple[np.ndarray, np.ndarray]:
    xdata = []      # CSVデータ(x)
    ydata = []      # CSVデータ(y)
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            _ = next(reader)        # ヘッダーをスキップ
        except UnicodeDecodeError:      # ヘッダに全角文字などがあった場合
            print(f'[WARNING\t] [load_csv\t] invalid character found in {path}. correct it.')
            reader = [0, 0]

        for row in reader:
            xdata.append(float(row[0]))
            ydata.append(float(row[1]))

    xdata = np.array(xdata, dtype='float64')
    ydata = np.array(ydata, dtype='float64')

    return xdata, ydata


class Logger:
    def __init__(self, c) -> None:
        self.c = c
    
    def print_info(self, mes:str):
        print(f'[INFO\t] [{self.__class__.__name__}] {mes}')
    
    def print_warn(self, mes:str):
        print(f'[WARNING\t] [{self.__class__.__name__}] {mes}')

