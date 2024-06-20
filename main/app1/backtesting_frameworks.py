import pandas as pd
import numpy as np
def backtest_1(data,stop_loss_percent=0.1):
    current=0 #what position you are having
    capital=1000000
    entry=[]
    exit=[]
    number_of_stock=0
    type_of_trade=[]
    duration=[]
    win=0
    stop_loss=0
    loss=0
    count_stop_loss=0
    current_maxima=0
    portfolio_value=[] #total capital-> non investment+ investment
    pl=[] # profit and loss
    for i in range(len(data)-1):
        if(current==1):
            if(data.signals[i]==1 or data.signals[i]==0):
#                 print("Hello")
                capital=capital+(number_of_stock*data.Close[i])
                portfolio_value.append(capital)
                if(capital<=stop_loss):
                    count_stop_loss=count_stop_loss+1
                    exit.append(i)
                    current=0
                    duration.append(exit[-1]-entry[-1])
                    x=portfolio_value[exit[-1]]-portfolio_value[entry[-1]]
                    pl.append(x)
                    number_of_stock=0
                    if(x>0):
                        win=win+1
                    elif(x<0):
                        loss=loss+1
                elif(capital>current_maxima):
                    current_maxima=capital
                    stop_loss=(1-stop_loss_percent)*current_maxima
                capital=capital-number_of_stock*data.Close[i]
            elif(data.signals[i]==-1):
                capital=capital+(number_of_stock*data.Close[i])
                portfolio_value.append(capital)
                exit.append(i)
                current=0
                duration.append(exit[-1]-entry[-1])
                x=portfolio_value[exit[-1]]-portfolio_value[entry[-1]]
                pl.append(x)
                if(x>0):
                    win=win+1
                elif(x<0):
                    loss=loss+1
                
                
        elif(current==-1):
            if(data.signals[i]==-1 or data.signals[i]==0):
                capital=capital-(number_of_stock*data.Close[i])
                portfolio_value.append(capital)
                if(capital<=stop_loss):
                    count_stop_loss=count_stop_loss+1
                    exit.append(i)
                    current=0
                    duration.append(exit[-1]-entry[-1])
                    x=portfolio_value[exit[-1]]-portfolio_value[entry[-1]]
                    pl.append(x)
                    number_of_stock=0
                    if(x>0):
                        win=win+1
                    elif(x<0):
                        loss=loss+1
                elif(capital>current_maxima):
                    current_maxima=capital
                    stop_loss=(1-stop_loss_percent)*current_maxima
                capital=capital+number_of_stock*data.Close[i]
                
            elif(data.signals[i]==1):
                capital=capital-(number_of_stock*data.Close[i])
                portfolio_value.append(capital)
                exit.append(i)
                current=0
                duration.append(exit[-1]-entry[-1])
                x=portfolio_value[exit[-1]]-portfolio_value[entry[-1]]
                pl.append(x)
                if(x>0):
                    win=win+1
                elif(x<0):
                    loss=loss+1
            
        else:
            if(data.signals[i]==1):
#                 print("Hello")
                current=1
                stop_loss=(1-stop_loss_percent)*capital
                current_maxima=capital
                number_of_stock=int(capital/data.Close[i])
                portfolio_value.append(capital)
                capital=capital-number_of_stock*data.Close[i]
                entry.append(i)
                type_of_trade.append("long")
            elif(data.signals[i]==-1):
                current=-1
                stop_loss=(1-stop_loss_percent)*capital
                number_of_stock=int(capital/data.Close[i])
                portfolio_value.append(capital)
                capital=capital+number_of_stock*data.Close[i]
                entry.append(i)
                type_of_trade.append("short")
            else:
                portfolio_value.append(capital)
    if(current==1):
        capital=capital+(number_of_stock*data.Close[i])
        portfolio_value.append(capital)
        exit.append(i)
        current=0
        duration.append(exit[-1]-entry[-1])
        x=portfolio_value[exit[-1]]-portfolio_value[entry[-1]]
        pl.append(x)
        if(x>0):
            win=win+1
        elif(x<0):
            loss=loss+1
    elif(current==-1):
        capital=capital-(number_of_stock*data.Close[i])
        portfolio_value.append(capital)
        exit.append(i)
        current=0
        duration.append(exit[-1]-entry[-1])
        x=portfolio_value[exit[-1]]-portfolio_value[entry[-1]]
        pl.append(x)
        if(x>0):
            win=win+1
        elif(x<0):
            loss=loss+1
        
    else:
        portfolio_value.append(capital)
        
        
    a=pd.DataFrame(columns=['entry'])
    a['entry']=entry
    a['exit']=exit
    a['duration']=duration
    a['P and L']=pl
    a['type']=type_of_trade
    data['portfolio value']=portfolio_value
    # print("Stop loss hit: ",count_stop_loss)
    return a,capital

import numpy as np

def parameters(data, trade, tnx,capital_initial=1000000):
    # print("RETURNS (in %):", (trade['P and L'].sum() / capital_initial) * 100)
    
    temp = capital_initial
    number_of_stock = int(temp / data.Close[0])
    final_value = capital_initial - number_of_stock * (data.Close[0] - data.Close.iloc[-1])
    
    drawdown = []
    dip = []
    returns_for_sharpe=[]
    
    for i in range(len(trade)):
        entry_index = trade['entry'][i]
        exit_index = trade['exit'][i]
        
        initial_value = data['portfolio value'][entry_index]
        min_value = min(data['portfolio value'][entry_index:exit_index + 1])
        dip.append(100 * (initial_value - min_value) / initial_value)
        
        returns_for_sharpe.append((100*trade['P and L']/(initial_value)-(tnx['Close'].iloc[exit_index])/(np.sqrt(252))))
        
        max_drawdown = 0
        temp1 = initial_value
        
        for j in range(entry_index + 1, exit_index + 1):
            temp1 = max(temp1, data['portfolio value'][j])
            drawdown_value = (temp1 - data['portfolio value'][j]) / temp1
            max_drawdown = max(max_drawdown, drawdown_value)
        
        drawdown.append(max_drawdown)
    
    trade['drawdown'] = drawdown 
    trade['dip'] = dip
    
    print("Benchmark Return (in rupees):", final_value - capital_initial)
    print("Number of closed trades:", len(trade))
    print("Max holding time:", np.max(trade['duration']))
    print("Avg Holding time:", np.mean(trade['duration']))
    print("Gross Profit:", trade['P and L'].sum())
    print("Net Profit:", trade['P and L'].sum() - 20 * len(trade))
    print("Max drawdown (in %):", 100 * np.max(trade['drawdown']))
    print("Avg drawdown (in %):", 100 * np.mean(trade['drawdown']))
    print("Max dip (in %):", np.max(trade['dip']))
    print("Avg dip (in %):", np.mean(trade['dip']))
    print("Sharpe Ratio: ",np.sqrt(252)*(np.mean(returns_for_sharpe)/(np.std(returns_for_sharpe))))

    return (trade['P and L'].sum() / capital_initial) * 100, final_value - capital_initial, len(trade), np.max(trade['duration']),np.mean(trade['duration']),trade['P and L'].sum(),trade['P and L'].sum() - 20 * len(trade),100 * np.max(trade['drawdown']),100 * np.mean(trade['drawdown']), np.max(trade['dip']),np.mean(trade['dip']),np.sqrt(252)*(np.mean(returns_for_sharpe)/(np.std(returns_for_sharpe)))
        