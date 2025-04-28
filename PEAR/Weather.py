from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# maybe i shoulda webscraped the date and time lol
# some of the daily details are messed up



# the paths are as detailed as needed to get the correct results
attributes = {'.weather-current':{'temp':' .current','feels like':' .value','condition':' .phrase','high':' .high','low':' .low'},\
              '.weather-hourly' :{'temp':' .temp.hour','feels like':' .card .top .left .feels-like .value','condition':' .bottom .phrase'},\
              '.weather-daily'  :{'desc':' .daily .card .bottom .phrase'}}#{'high':' .daily .high','low':' .daily .low','desc':' .daily .card .bottom .phrase'}}

details = {'.weather-current':['uv','air quality','wind','rain'], '.weather-hourly':['wind','pressure','humidity','uv','visiblity','cloud cover'], '.weather-daily':['high feels like','wind','humidity','uv','sunrise','sunset']}

def remove_whitespace(string):
    return "".join(string.split())


class Weather:
    def __init__(s, storage=('sorry-causing','storage')):
        s.storage = storage

        s.root = Tk()
        s.root.title('Weather')

        # loc setting area
        s.locF = ttk.Frame(s.root)
        s.locF.pack()
        ttk.Label(s.locF, text='City:').pack(side='left')
        s.cityE = ttk.Entry(s.locF)
        s.cityE.pack(side='left')
        ttk.Label(s.locF, text='State:').pack(side='left')
        s.stateE = ttk.Entry(s.locF)
        s.stateE.pack(side='left')
        ttk.Button(s.locF, text='Set', command=s.set_location).pack()

        # label for where the location is currently set
        s.locL = ttk.Label(s.root, text = f'')
        s.locL.pack()

        # tabs
        notebook = ttk.Notebook(s.root)
        s.tabs = {'Current': ttk.Frame(notebook), 'Hourly':ttk.Frame(notebook), 'Daily':ttk.Frame(notebook)}
        for text, tab in s.tabs.items():
            notebook.add(tab, text=text)
        notebook.pack()


        s.texts = []
        s.set_location(*s.storage)
        s.root.mainloop()



    def set_location(s, city=None, state=None):
        # this if statement is working
        if not city or not state:
            city  = s.cityE.get().lower()
            s.cityE.delete(0, END)
            state = s.stateE.get().lower()
            s.stateE.delete(0, END)
        else:
            city = city.lower()
            state = state.lower()

        html = requests.get(f'https://www.foxweather.com/local-weather/{state}/{city}').text
        if 'SORRY' in html:
            # runs when set for the first time without storage
            return

        # now we've confirmed this is a legit location
        s.fox = BeautifulSoup(html, "html.parser")
        s.state = state
        s.city = city
        s.storage = (s.city,s.state)
        s.update_data()
        s.locL.config(text=f'Location is currently set to {s.city}, {s.state}.')

    
    def update_data(s):
        paths = {'Current':'.weather-current','Hourly':'.weather-hourly','Daily':'.weather-daily'}
        s.data = {'Current':[],'Hourly':[],'Daily':[]}
        for cat in s.data.keys():
            attributes = s.get_attributes(paths[cat])
            details = s.get_details(paths[cat])
            for i in range(len(attributes)):
                s.data[cat].append({**attributes[i], **details[i]})

        def get_prefix(i, name):
            if name == 'Current':
                return ''
            elif name == 'Hourly':
                return (datetime.now() + timedelta(hours=i+1)).strftime('%I%p') + ': '
            else:
                return (datetime.now() + timedelta(days=i)).strftime('%m/%d') + ': '


        for label in s.texts:
            label.destroy()
        
        for name, frame in s.tabs.items():
            for i, sec in enumerate(s.data[name]):
                s.texts.append(ttk.Label(frame, text=get_prefix(i,name)+str(sec)))
                s.texts[-1].pack()


    
    def get_attributes(s, start):
        result = []
        data = {key:s.fox.select(val) for key, val in attributes[start].items()} # attribute : listish of data for every day or whatever
        n = len(list(data.values())[0])

        for i in range(n): # for each day or whatever we are getting attributes for
            result.append({})
            for attribute, sub_data in data.items():
                result[i][attribute] = remove_whitespace(sub_data[i].text)
        return result
    
    def get_details(s, start):
        data = s.fox.select(start+' .weather-details .value')
        result = []
        n = len(data)//len(details[start]) # num sections (ex. how many hours)
        #print(n)
        for i in range(n):
            result.append({})
            for j, detail in enumerate(details[start]):
                result[i][detail] = remove_whitespace(data[i*len(details)+j].text)
        return result



'''
today = fox.select_one('.card-today .phrase').text.strip()
tonight = fox.select_one('.card-tonight .phrase').text.strip()
tomorrow = fox.select_one('.card-tomorrow .phrase').text.strip()
'''