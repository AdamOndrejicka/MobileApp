import kivy
kivy.require('2.1.0') 
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.garden.matplotlib import FigureCanvasKivyAgg
import requests
import matplotlib.pyplot as plt
plt.rcParams['axes.facecolor'] = 'none'
plt.rcParams['text.color'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

URL = 'http://127.0.0.1:5000'

class Request():
    def get_data(self):
        return requests.get(f'{URL}/data').json()
    def add_data(self, data):
        return requests.post(f'{URL}/data/add', json=data)
    def delete_data(data, button):
        return requests.delete(f'{URL}/data/{button.id}')

class LoadingPage(Screen):
    def on_enter(self):
        Clock.schedule_once(self.load_home_page, 5)
    def load_home_page(self, *args):
        self.manager.current = 'HomePage'
        self.manager.transition.direction = 'left'

class RecordPage(Screen):
    def load_home_page(self):
        self.reset_form()
        self.manager.current = 'HomePage'
        self.manager.transition.direction = 'down'
    def reset_text(self):
        self.ids.date.text = ""
        self.ids.time.text = ""
        self.ids.pressure.text = ""
    def reset_background_color(self):
        self.ids.date.background_color = (1,1,1,1)
        self.ids.time.background_color = (1,1,1,1)
        self.ids.pressure.background_color = (1,1,1,1)
    def reset_form(self):
        self.reset_text()
        self.reset_background_color()
    def save_data(self, date, time, pressure):
        if not date and not time and not pressure: return
        self.reset_background_color()
        data = {
            'date': date,
            'time': time,
            'pressure': pressure
        }
        response = Request().add_data(data)
        if response.ok:
            self.load_home_page()
            return
        if response.text.upper() == 'PRESSURE'.upper():
            self.ids.pressure.background_color = (1,0.28,0.2,1)
        else:
            self.ids.date.background_color = (1,0.28,0.2,1)
            self.ids.time.background_color = (1,0.28,0.2,1)
        
class SummaryPage(Screen):
    def avg_pressure(self):
        data = Request().get_data()
        systolic = [x[1] for x in data]
        avg_systolic = sum(systolic)/len(systolic)
        diastolic = [x[2] for x in data]
        avg_diastolic = sum(diastolic)/len(diastolic)
        if avg_systolic >= 180 or avg_diastolic >= 110:
            self.ids.pressure_value.color = (1,0.28,0.2,1)
        elif avg_systolic >= 120 or avg_diastolic >= 80:
            self.ids.pressure_value.color = (0.8,0.8,0,1)
        else:
            self.ids.pressure_value.color = (0.28,1,0.2,1)
        self.plot_graph()
        return f'{int(avg_systolic)}/{int(avg_diastolic)}'
    def plot_graph(self):
        data = Request().get_data()
        systolic = [x[1] for x in data]
        diastolic = [x[2] for x in data]
        date = [x[3].split()[0] for x in data]
        figure = plt.figure(edgecolor='white')
        figure.patch.set_facecolor('black')
        axes = plt.axes()
        axes.spines['top'].set_color('white')
        axes.spines['bottom'].set_color('white')
        axes.spines['left'].set_color('white')
        axes.spines['right'].set_color('white')
        axes.plot(date, systolic, label='Systolic')
        axes.plot(date, diastolic, label='Diastolic')
        axes.legend()
        self.ids.graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))

class HomePage(Screen):
    def on_pre_enter(self):
        self.remove_children_widgets()
        records = Request().get_data()
        for record in records:
            local_datetime = record[3].split()
            local_date = local_datetime[0]
            local_time = local_datetime[1]
            label_date = Label(text=local_date)
            label_time = Label(text=local_time)
            label_pressure = Label(text=f"{record[1]}/{record[2]}")
            boxlayout = BoxLayout()
            boxlayout.add_widget(label_date)
            boxlayout.add_widget(label_time)
            boxlayout.add_widget(label_pressure)
            delete = Button(text='ZMAZAŤ', color=(1,1,1,1), background_color=(1,0.28,0.2,1), background_normal="")
            delete.id = record[0]
            delete.bind(on_press=self.callback_for_delete)
            boxlayout.add_widget(delete)
            self.ids.scroll_box.add_widget(boxlayout)    
    def callback_for_delete(self, button):
        request = Request().delete_data(button)
        if request.ok:
            self.on_pre_enter()
    def remove_children_widgets(self):
        childrens = [i for i in self.ids.scroll_box.children]
        for children in childrens:
            if isinstance(children, BoxLayout):
                self.ids.scroll_box.remove_widget(children)

class Application(App):
    pass

if __name__ == '__main__':
    Application().run()