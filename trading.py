# - Using Analysis of Highs Lows and Trading Volume

#imports
from time import *
from sklearn import tree
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import time
start_time = time.time()
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
    

#trading algorithm
def trading(points,highs,lows,volume):

    features = []
    labels = []

    for i in range(len(points) - acc):
        
        temp_p = points[acc + i - 1]
        temp_h = highs[acc + i - 1]
        temp_l = lows[acc + i - 1]
        temp_v = volume[acc + i - 1]
        
        features.append([temp_p, temp_h, temp_l, temp_v])
    
        
        if points[acc + i] > points[acc + i - 1]:
            labels.append([1])
        else:
            labels.append([0])
            
    clf = tree.DecisionTreeClassifier()
    clf.fit(features, labels)
    temp_list = []
    
    for i in range(acc):
        temp_list.append([])
        temp_list[i].append(points[-1*(acc - i)])
        temp_list[i].append(highs[-1*(acc - i)])
        temp_list[i].append(lows[-1*(acc - i)])
        temp_list[i].append(volume[-1*(acc - i)])
        
    if clf.predict(temp_list)[0] == 1:
        return 1
    else:
        return 0

#variables  
acc = 10
Points = []
Highs = []
Lows = []
Volumes = []
dates = []
CashRecords = []

Cash = int(raw_input("Enter Cash Investment "))
startingCash = Cash
Bought = False
days = 0
decision = 0
stockSymbol = raw_input("Enter stock symbol ")

style.use('ggplot')
start = dt.datetime(2016,1,1)
end = dt.datetime(2017,12,31)

df = web.DataReader(stockSymbol,'yahoo',start,end)
df.to_csv('data.csv')

df = pd.read_csv('data.csv', parse_dates = True)

for i in df[['Close']]:
    for j in df[i]:
        Points.append(round(j,2))
        
for i in df[['High']]:
    for j in df[i]:
        Highs.append(round(j,2))

for i in df[['Low']]:
    for j in df[i]:
        Lows.append(round(j,2))
        
for i in df[['Volume']]:
    for j in df[i]:
        Volumes.append(round(j,2))

for i in df[['Date']]:
    for j in df[i]:
        dates.append(dt.datetime.strptime(j, "%Y-%m-%d"))
        

#graph labels        
plt.figure(num = stockSymbol)
plt.title(stockSymbol + " Stock Trading Analysis")
plt.xlabel('Date')
plt.ylabel('Cash / Stock Price')

while days <= len(df[['Close']]) - 1:
    
    #stock info
    days += 1
    StockPrice = Points[days - 1]
    
    if days == 1:
        initP = StockPrice
        initC = Cash
        
    #your money
    if Bought == True:
        Cash = round(Cash*StockPrice/Points[days-2],2)
        c = "green"
    else:
        c = "red"
                  
    CashRecords.append(Cash)
    
    if days > acc:
        decision = trading(Points[:days],Highs[:days],Lows[:days],Volumes[:days])

    if Bought == True:
        if decision == 0:
            Bought = False
    else:
        if decision == 1:
            Bought = True

    
    plt.plot(dates[days - 2:days], Points[days - 2:days], color=c)
    
print("Ending Cash: " + str(CashRecords[-1]))
print("Expected Cash: " + str(round(CashRecords[0] * Points[-1] / Points[0],2)))


plt.plot(dates, CashRecords, color='blue')
plt.show()