
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

class LatexView(BoxLayout):
    def __init__(self, **kwargs):
        super(LatexView, self).__init__(orientation='vertical', **kwargs)
        self.widgets()
    
    def widgets(self):
        self.fig, self.ax = plt.subplots()
        
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.text(0.1, 0.5, "No input", fontsize=10)

        self.add_widget(self.fig.canvas)
    
    def set_expression(self, expr):
        if expr:
            expr = "$" + expr + "$"
            expr = expr.replace("\ee", "e")
            expr = expr.replace("\ppi", "\pi")
        else:
            expr = "No input"
        self.ax.clear()
        self.ax.text(0.1, 0.5, expr, fontsize=10)
        self.fig.canvas.draw()

class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)

    def build(self):
        return LatexView()

def main():
    TestApp().run()


if __name__ == '__main__':
    main()