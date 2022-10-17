from bs4 import BeautifulSoup
import requests
import numpy as np
import ast
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
import pandas as pd


ALL_EVENTS = ['practice-1', 'practice-2', 'practice-3', 'qualifying', 'sprint-results', 'race-result']


def convert(time):
    if time==None or time==np.nan or time[0]=='D' or time=='' or time[0]==' ':
        return np.nan
    minutes = int(time[0])
    secs = float(time[2::])
    return minutes*60+secs
    

def convert_loss(time):
    if time[0]==' ':
        return 0.
    else:
        return float(time[1::])
    

def convert_dict_to_df(Drivers,Weekends,Results):
    D = {'driver':[], 'year':[], 'GP':[], 'fp1':[], 'fp1+':[], 'fp2':[], 'fp2+':[], 'fp3':[], 'fp3+':[], 'q1':[], 'q1+':[], 'q2':[], 'q2+':[], 'q3':[], 'q3+':[], 'r':[]}
    ALL_EVENTS = ['practice-1', 'practice-2', 'practice-3', 'qualifying', 'race-result']

    for year in Results.keys():
        for wknd in Weekends[year]:
            for driver in Drivers[year]:
                D['driver'].append(driver)
                D['year'].append(year)
                D['GP'].append(wknd)
                for event in ALL_EVENTS:
                    if event in Results[year][wknd].keys():
                        #print(year,wknd,event,driver)
                        r = Results[year][wknd][event][driver]
                        if r==None:
                            if event[0]=='p':
                                D['fp'+event[-1]].append(np.nan)
                                D['fp'+event[-1]+'+'].append(np.nan)
                            elif event[0]=='q':
                                for j in range(3):
                                    D['q'+str(j+1)].append(np.nan)
                                    D['q'+str(j+1)+'+'].append(np.nan)
                            elif event[0]=='r':
                                D['r'].append(np.nan)
                        elif event[0]=='r':
                            r = Results[year][wknd][event][driver]['pos']
                            D['r'].append(r)
                        else:
                            r = Results[year][wknd][event][driver]['times']
                            l = Results[year][wknd][event][driver]['loss']
                            if r==None:
                                if event[0]=='p':
                                    D['fp'+event[-1]].append(np.nan)
                                    D['fp'+event[-1]+'+'].append(np.nan)
                                elif event[0]=='q':
                                    for j in range(3):
                                        D['q'+str(j+1)].append(np.nan)
                                        D['q'+str(j+1)+'+'].append(np.nan)
                                elif event[0]=='r':
                                    D['r'].append(np.nan)
                            else:
                                if event[0]=='p':
                                    D['fp'+event[-1]].append(r)
                                    D['fp'+event[-1]+'+'].append(l)
                                elif event[0]=='q':
                                    for j in range(3):
                                        D['q'+str(j+1)].append(r[j])
                                        D['q'+str(j+1)+'+'].append(l[j])
                                elif event[0]=='r':
                                    D['r'].append(r)
                    else:
                        if event[0]=='p':
                            D['fp'+str(event[-1])].append(np.nan)
                            D['fp'+str(event[-1])+'+'].append(np.nan)
                        elif event[0]=='q':
                            for j in range(3):
                                D['q'+str(j+1)].append(np.nan)
                                D['q'+str(j+1)+'+'].append(np.nan)
                        else:
                            D['r'].append(np.nan)

    data = pd.DataFrame(D)
    #for e in ['fp1','fp2','fp3','q1','q2','q3']:
     #   for j in range(data.shape[0]):
      #      data.at[j,e] = convert(data.at[j,e])
    
    return data
    

def get_drivers(year):
    #return the list of drivers participating in the season
    url = 'https://www.formula1.com/en/results.html/' + str(year) + '/drivers.html'
    result = requests.get(url).text
    doc = BeautifulSoup(result, 'html.parser')

    Drivers = [thing.string for thing in doc.tbody.find_all('span',class_='hide-for-mobile')]
    
    return Drivers
    
    
def get_weekends(year):
    #return the list of Grand Prix's organised during the given season and the dictionary of links
    url = 'https://www.formula1.com/en/results.html/' + str(year) + '/races.html'
    result = requests.get(url).text
    doc = BeautifulSoup(result, 'html.parser')

    things = doc.tbody.find_all('a')
    Links = {thing.string.strip():thing['href'][21:-16:] for thing in things}
    Weekends = list(Links.keys())
    
    return Weekends, Links
    
    
def get_gp(year,wknd):
    Drivers = get_drivers(year)
    Weekends, Links = get_weekends(year)
    
    results = {}
    
    url = 'https://www.formula1.com/en/results.html/' + str(year) + Links[wknd] + 'practice-1.html'
    result = requests.get(url).text
    doc = BeautifulSoup(result, 'html.parser')
    selects = doc.find_all('select')
    
    for select in selects:
        if select['name']=='resultType':
            CURRENT_EVENTS = [thing['value'] for thing in select.contents[1::2]]
   
    EVENTS = list(set(ALL_EVENTS) & set(CURRENT_EVENTS))
    
    for event in EVENTS:
        event_results = {}
        url = 'https://www.formula1.com/en/results.html/' + str(year) + Links[wknd] + event + '.html'
        result = requests.get(url).text
        doc = BeautifulSoup(result, 'html.parser')
        
        goal = list(doc.tbody.children)
        j=1
        for child in goal[1::2]:
            times = [convert(time.string) for time in child.find_all(class_='dark bold')[1::]]
            if event[0]=='p':
                times = times[0]
                
            man = child.find_all('span',class_='hide-for-mobile')[0].string
            event_results[man] = {'pos':j, 'times':times}
            j+=1
            
        for driver in Drivers:
            if driver not in list(event_results.keys()):
                event_results[driver] = None
        
        results[event] = event_results
    
    return results 
    
def get_season(year,verbose=0):
    #returns the list of drivers, Grand Prix's and links and the dictionary of results    
    Drivers = get_drivers(year)
    Weekends, Links = get_weekends(year)
    
    Results = {}
    N = len(Links.keys())
    count=1

    for wknd in Weekends:
        wknd_results = {}
    
        url = 'https://www.formula1.com/en/results.html/' + str(year) + Links[wknd] + 'practice-1.html'
        result = requests.get(url).text
        doc = BeautifulSoup(result, 'html.parser')
        selects = doc.find_all('select')
    
        for select in selects:
            if select['name']=='resultType':
                CURRENT_EVENTS = [thing['value'] for thing in select.contents[1::2]]
   
        EVENTS = list(set(ALL_EVENTS) & set(CURRENT_EVENTS))
    
        for event in EVENTS:
            event_results = {}
            if event[0]=='p':
                min_times = 10000
            elif event[0]=='q':
                min_times = [10000,10000,10000]
                
            url = 'https://www.formula1.com/en/results.html/' + str(year) + Links[wknd] + event + '.html'
            result = requests.get(url).text
            doc = BeautifulSoup(result, 'html.parser')
        
            goal = list(doc.tbody.children)
            j=1
            for child in goal[1::2]:
                man = child.find_all('span',class_='hide-for-mobile')[0].string
                if event[0]!='r' and event[0]!='s':
                    #print(year,wknd,event)
                    times = [convert(time.string) for time in child.find_all(class_='dark bold')[1::]]
                    #loss = convert_loss([time.string for time in child.find_all(class_="dark bold")[-1]][0])
                    if event[0]=='p':
                        times = times[0]
                        if times<min_times:
                            min_times = times
                    else:
                        for j in range(3):
                            if times[j]!=None and times[j]<min_times[j]:
                                min_times[j] = times[j]
                                
                    event_results[man] = {'pos':j, 'times':times}
                else:
                    event_results[man] = {'pos':j}
                j+=1
            
            for driver in Drivers:
                if driver not in list(event_results.keys()):
                    event_results[driver] = None
                else:
                    if event[0]!='r' and event[0]!='s':
                        times = event_results[driver]['times']
                    if event[0]=='p':
                        if times!=None:
                            event_results[driver]['loss'] = times - min_times
                        else:
                            event_results[driver]['loss'] = None
                    elif event[0]=='q':
                        if times!=None:
                            loss = [times[j]-min_times[j] for j in range(3)]
                            event_results[driver]['loss'] = loss
                        else:
                            event_results[driver]['loss'] = None
        
            wknd_results[event] = event_results

        Results[wknd] = wknd_results
    
        if verbose>0:
            print(count,'/',N,' '+wknd+' is loaded')
        count += 1
    
    return Drivers, Weekends, Links, Results
    
    
def get_results(Years,verbose=0):
    #returns a dictionaries of drivers participating in given years
    #grand prix's and links to them
    #results 
    Drivers = {}
    Weekends = {}
    Links = {}
    Results = {}
    for year in Years:
        drivers, weekends, links, results = get_season(year,verbose-1)
        Drivers[year] = drivers
        Weekends[year] = weekends
        Links[year] = links
        Results[year] = results
        
        if verbose>0:
            print('Year',year,'is loaded')
        
    return Drivers, Weekends, Links, Results
    
    
def get_data(Years,verbose=0):
    Drivers,Weekends,Links,Results = get_results(Years,verbose)
    data = convert_dict_to_df(Drivers,Weekends,Results)
    return data
    
    
def write_results_to_file(path,Drivers,Weekends,Links,Results):
    Everything = {'Drivers':Drivers, 'Weekends':Weekends, 'Links':Links, 'Results':Results}
    data = str(Everything)
    
    with open(path,'w',encoding="utf-8") as file:
        file.write(data)
    
  
def load_results_from_file(path):
    with open(path,'r',encoding="utf-8") as file:
        data = file.read()
        
    Everything = ast.literal_eval(data)
    
    return Everything['Drivers'], Everything['Weekends'], Everything['Links'], Everything['Results']
    