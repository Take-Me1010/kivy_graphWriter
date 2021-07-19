
from pathlib import Path
import json
from core.exceptions import *

class StateManager:
    def __init__(self, app) -> None:
        self.app = app
    
    def get_state(self) -> dict:
        """現在のstateを取得する

        Returns:
            dict: 現在保持しているstate
        """
        if hasattr(self, "state"):
            return self.state
        else:
            print(f'[WARNING\t] [StateManager\t] [get_data\t] no state attribute.')
            return None
        
    def set_state(self, state:dict):
        """stateデータをセットする

        Args:
            state (dict): 状態を表す辞書
        """
        self.state = state


        """前回終了時のデータを読み込む
        """
        self.load_state(path='./cache/previous.json')
        return True

    def save_state(self, state:dict=None, name:str="./cache/previous.json",):
        """stateを保存する

        Args:
            state (dict, optional): ths state you want to save. if None, the state becomes one the instance has. Defaults to None.
            name (str, optional): tha path to save. Defaults to "./cache/previous.pikcle".

        Returns:
            dict: the state saved by this method.
        """
        if state:
            self.set_state(state)
        self.write_state(name)
        return state or self.state

    def load_state(self, path:str) -> dict:
        """pathのデータを読み込む

        Args:
            path (str): 読み込む対象のファイル
        """
        p = Path(path)
        if not p.exists():
            self.state = {}
            print(f'[WARNING\t] [StateManager\t] {path} does not exist.')
            return {}

        s = p.suffix

        if s == '.json':
            with open(path, "r", encoding="utf-8") as jf:
                try:
                    self.state = json.load(jf)
                except json.decoder.JSONDecodeError:
                    print(f'[WARNING\t] [StateManager] Invalid data {path}')
                    self.state = {}
        else:
            raise FailedToLoadData(f'{path} is unvalid data file. must be .json')
        
        return self.state

    def write_state(self, path:str, state:dict=None):
        """stateを保存する

        Args:
            path (str): 保存先
            state (dict, optional): 保存したいstate. Noneなら現在保持するstateを保存する. Defaults to None.
        """
        state = state or self.state
        # print(f'[INFO\t] [StateManager\t] [self.write_state] state : type={type(state)}, value={state}')
        with open(path, 'w', encoding='utf-8') as jf:
            json.dump(state, jf, indent=4, ensure_ascii=False)
