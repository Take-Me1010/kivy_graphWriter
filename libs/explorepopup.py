
from kivy.uix.popup import Popup

from libs.garden.filebrowser import FileBrowser

from kivy.lang.builder import Builder

Builder.load_string('''
#<KvLang>
<ExplorePopup>:
    FileBrowser:
        id: fb

#</KvLang>
''')

class ExplorePopup(Popup):
    filebrowser: FileBrowser
    def __init__(self, **kwargs) -> None:
        filters = kwargs.pop('filters', None)
        multiselect = kwargs.pop('multiselect', None)
        favorites = kwargs.pop('favorites', None)
        super(ExplorePopup, self).__init__(**kwargs)
        self.filebrowser = self.ids['fb']
        if filters:
            self.filebrowser.filters = filters
        if multiselect:
            self.filebrowser.multiselect = multiselect
        if favorites:
            self.filebrowser.favorites = favorites
    
    def set_mode(self, mode:str):
        """set wether filebrowser can select directory.

        Args:
            mode (str): only accept 'dir' or 'file'.
        """
        if mode == 'dir':
            self.filebrowser.dirselect = True
        
        elif mode == 'file':
            self.filebrowser.dirselect = False

        else:
            print(f'[WARNING\t] [ExplorePopup] invalid mode : {mode}')
    
    def set_callback(self, **kwargs):
        self.filebrowser.bind(**kwargs)

    def get_selected_selection(self) -> list:
        return self.filebrowser.selection
    
    def get_selected_path(self) -> str:
        return self.filebrowser.path.decode('utf-8')
