import pandas as pd
import numpy as np
# def backtest_1(data,stop_loss_percent=0.1):
#     current=0 #what position you are having
#     capital=1000000
#     entry=[]
#     exit=[]
#     number_of_stock=0
#     type_of_trade=[]
#     duration=[]
#     win=0
#     stop_loss=0
#     loss=0
#     count_stop_loss=0
#     current_maxima=0
#     portfolio_value=[] #total capital-> non investment+ investment
#     pl=[] # profit and loss
#     for i in range(len(data)-1):
#         if(current==1):
#             if(data.signals[i]==1 or data.signals[i]==0):
# #                 print("Hello")
#                 capital=capital+(number_of_stock*data.Close[i])
#                 portfolio_value.append(capital)
#                 if(capital<=stop_loss):
#                     count_stop_loss=count_stop_loss+1
#                     exit.append(i)
#                     current=0
#                     duration.append(exit[-1]-entry[-1])
#                     x=portfolio_value[exit[-1]]-portfolio_value[entry[-1]]
#                     pl.append(x)
#                     number_of_stock=0
#                     if(x>0):
#                         win=win+1
#                     elif(x<0):
#                         loss=loss+1
#                 elif(capital>current_maxima):
#                     current_maxima=capital
#                     stop_loss=(1-stop_loss_percent)*current_maxima
#                 capital=capital-number_of_stock*data.Close[i]
#             elif(data.signals[i]==-1):
#                 capital=capital+(number_of_stock*data.Close[i])
#                 portfolio_value.append(capital)
#                 exit.append(i)
#                 current=0
#                 duration.append(exit[-1]-entry[-1])
#                 x=portfolio_value[exit[-1]]-portfolio_value[entry[-1]]
#                 pl.append(x)
#                 if(x>0):
#                     win=win+1
#                 elif(x<0):
#                     loss=loss+1
                
                
#         elif(current==-1):
#             if(data.signals[i]==-1 or data.signals[i]==0):
#                 capital=capital-(number_of_stock*data.Close[i])
#                 portfolio_value.append(capital)
#                 if(capital<=stop_loss):
#                     count_stop_loss=count_stop_loss+1
#                     exit.append(i)
#                     current=0
#                     duration.append(exit[-1]-entry[-1])
#                     x=portfolio_value[exit[-1]]-portfolio_value[entry[-1]]
#                     pl.append(x)
#                     number_of_stock=0
#                     if(x>0):
#                         win=win+1
#                     elif(x<0):
#                         loss=loss+1
#                 elif(capital>current_maxima):
#                     current_maxima=capital
#                     stop_loss=(1-stop_loss_percent)*current_maxima
#                 capital=capital+number_of_stock*data.Close[i]
                
#             elif(data.signals[i]==1):
#                 capital=capital-(number_of_stock*data.Close[i])
#                 portfolio_value.append(capital)
#                 exit.append(i)
#                 current=0
#                 duration.append(exit[-1]-entry[-1])
#                 x=portfolio_value[exit[-1]]-portfolio_value[entry[-1]]
#                 pl.append(x)
#                 if(x>0):
#                     win=win+1
#                 elif(x<0):
#                     loss=loss+1
            
#         else:
#             if(data.signals[i]==1):
# #                 print("Hello")
#                 current=1
#                 stop_loss=(1-stop_loss_percent)*capital
#                 current_maxima=capital
#                 number_of_stock=int(capital/data.Close[i])
#                 portfolio_value.append(capital)
#                 capital=capital-number_of_stock*data.Close[i]
#                 entry.append(i)
#                 type_of_trade.append("long")
#             elif(data.signals[i]==-1):
#                 current=-1
#                 stop_loss=(1-stop_loss_percent)*capital
#                 number_of_stock=int(capital/data.Close[i])
#                 portfolio_value.append(capital)
#                 capital=capital+number_of_stock*data.Close[i]
#                 entry.append(i)
#                 type_of_trade.append("short")
#             else:
#                 portfolio_value.append(capital)
#     if(current==1):
#         capital=capital+(number_of_stock*data.Close[i])
#         portfolio_value.append(capital)
#         exit.append(i)
#         current=0
#         duration.append(exit[-1]-entry[-1])
#         x=portfolio_value[exit[-1]]-portfolio_value[entry[-1]]
#         pl.append(x)
#         if(x>0):
#             win=win+1
#         elif(x<0):
#             loss=loss+1
#     elif(current==-1):
#         capital=capital-(number_of_stock*data.Close[i])
#         portfolio_value.append(capital)
#         exit.append(i)
#         current=0
#         duration.append(exit[-1]-entry[-1])
#         x=portfolio_value[exit[-1]]-portfolio_value[entry[-1]]
#         pl.append(x)
#         if(x>0):
#             win=win+1
#         elif(x<0):
#             loss=loss+1
        
#     else:
#         portfolio_value.append(capital)
        
        
#     a=pd.DataFrame(columns=['entry'])
#     a['entry']=entry
#     a['exit']=exit
#     a['duration']=duration
#     a['P and L']=pl
#     a['type']=type_of_trade
#     data['portfolio value']=portfolio_value
#     # print("Stop loss hit: ",count_stop_loss)
#     return a,capital

# import numpy as np

# def parameters(data, trade, tnx,capital_initial=1000000):
#     # print("RETURNS (in %):", (trade['P and L'].sum() / capital_initial) * 100)
    
#     temp = capital_initial
#     number_of_stock = int(temp / data.Close[0])
#     final_value = capital_initial - number_of_stock * (data.Close[0] - data.Close.iloc[-1])
    
#     drawdown = []
#     dip = []
#     returns_for_sharpe=[]
    
#     for i in range(len(trade)):
#         entry_index = trade['entry'][i]
#         exit_index = trade['exit'][i]
        
#         initial_value = data['portfolio value'][entry_index]
#         min_value = min(data['portfolio value'][entry_index:exit_index + 1])
#         dip.append(100 * (initial_value - min_value) / initial_value)
        
#         returns_for_sharpe.append((100*trade['P and L']/(initial_value)-(tnx['Close'].iloc[exit_index])/(np.sqrt(252))))
        
#         max_drawdown = 0
#         temp1 = initial_value
        
#         for j in range(entry_index + 1, exit_index + 1):
#             temp1 = max(temp1, data['portfolio value'][j])
#             drawdown_value = (temp1 - data['portfolio value'][j]) / temp1
#             max_drawdown = max(max_drawdown, drawdown_value)
        
#         drawdown.append(max_drawdown)
    
#     trade['drawdown'] = drawdown 
#     trade['dip'] = dip
    
#     # print("Benchmark Return (in rupees):", final_value - capital_initial)
#     # print("Number of closed trades:", len(trade))
#     # print("Max holding time:", np.max(trade['duration']))
#     # print("Avg Holding time:", np.mean(trade['duration']))
#     # print("Gross Profit:", trade['P and L'].sum())
#     # print("Net Profit:", trade['P and L'].sum() - 20 * len(trade))
#     # print("Max drawdown (in %):", 100 * np.max(trade['drawdown']))
#     # print("Avg drawdown (in %):", 100 * np.mean(trade['drawdown']))
#     # print("Max dip (in %):", np.max(trade['dip']))
#     # print("Avg dip (in %):", np.mean(trade['dip']))
#     # print("Sharpe Ratio: ",np.sqrt(252)*(np.mean(returns_for_sharpe)/(np.std(returns_for_sharpe))))

#     return (trade['P and L'].sum() / capital_initial) * 100, final_value - capital_initial, len(trade), np.max(trade['duration']),np.mean(trade['duration']),trade['P and L'].sum(),trade['P and L'].sum() - 20 * len(trade),100 * np.max(trade['drawdown']),100 * np.mean(trade['drawdown']), np.max(trade['dip']),np.mean(trade['dip']),np.sqrt(252)*(np.mean(returns_for_sharpe)/(np.std(returns_for_sharpe)))
        
# class Bactesting_Framework():
    # def __init__(self,data,tnx,normal_stop_loss=100,normal_take_profit=100,trailing_stop_loss_percent=100,dynamic_exit_condition=100,atr_take_profit_percent=100,atr_stop_loss_percent=100):
        # self.data = data
        # self.normal_stop_loss =float(0 if normal_stop_loss==100 else normal_stop_loss)
        # self.stop_loss =float(0) 
        # self.normal_take_profit =float( 0 if normal_take_profit==100 else normal_take_profit)
        # self.take_profit=0
        # self.trailing_stop_loss_percent = float(0 if trailing_stop_loss_percent==100 else trailing_stop_loss_percent)
        # self.trailing_stop_loss=0
        # self.dynamic_exit_condition =float( 0 if  dynamic_exit_condition ==100 else dynamic_exit_condition)
        # self.dynamic_exit=0
        # self.atr_take_profit_percent = float(0 if  atr_take_profit_percent==100 else atr_take_profit_percent)
        # self.atr_take_profit=0
        # self.atr_stop_loss_percent = float(0 if  atr_stop_loss_percent ==100 else atr_stop_loss_percent)
        # self.atr_stop_loss=0
        # self.current_position = 0
        # self.intial_balance = 1000000
        # self.capital = self.intial_balance
        # self.entry=[]
        # self.exit=[]
        # self.number_of_stock=0
        # self.type_of_trade=[]
        # self.duration=[]
        # self.win=0
        # self.stop_loss=0
        # self.loss=0
        # self.count_stop_loss=0
        # self.current_maxima=0
        # self.current_minima=0
        # self.a=pd.DataFrame(columns=['entry'])
        # self.portfolio_value=[] 
        # self.pl=[]
        # self.i=0
        # self.result=[]
        # self.tnx=tnx
        # self.atr()
        # self.bactest()
        # self.parameters()
    # -------------------------------------------------------------------------------------------------------------
    # def atr(self):
        # self.data['High-Low'] = self.data['High'] - self.data['Low']
        # self.data['High-PrevClose'] = np.abs(self.data['High'] - self.data['Close'].shift(1))
        # self.data['Low-PrevClose'] = np.abs(self.data['Low'] - self.data['Close'].shift(1))

        # self.data['TR'] = self.data[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)

        # Calculate Average True Range (ATR)
        # period = 14
        # self.data['ATR'] = self.data['TR'].rolling(window=period).mean()

        # Clean up
        # self.data.drop(['High-Low', 'High-PrevClose', 'Low-PrevClose', 'TR'], axis=1, inplace=True)
    # -------------------------------------------------------------------------------------------------------------
    # def hello(self):
        # print("hello")
    # def portfolio(self):
        # capital=self.capital+self.number_of_stock*self.data["Close"][self.i]
        # self.portfolio_value.append(capital)
    # def stop_loss_checker(self):
        # if self.normal_stop_loss==0:return 0
        # if self.portfolio_value[-1]<self.stop_loss:
            # return 1
        # else: return 0
    # def square_off(self):
        # self.exit.append(self.i)
        # self.current_position=0
        # self.capital=self.portfolio_value[-1]
        # self.number_of_stock=0
        # self.duration.append(self.exit[-1]-self.entry[-1])
        # self.profit_loss()
    # def profit_loss(self):
        # if self.portfolio_value[self.exit[-1]]>self.portfolio_value[self.entry[-1]]:
            # self.win+=1
        # else:
            # self.loss+=1
        # self.pl.append(self.portfolio_value[self.exit[-1]]-self.portfolio_value[self.entry[-1]])
    # def trailing_stop_loss_checker(self):
        # if self.trailing_stop_loss_percent==0:return 0
        # if self.portfolio_value[-1]<self.trailing_stop_loss:
            # return 1
        # else:
            # if  self.portfolio_value[-1]>self.current_maxima:
                # self.current_maxima=self.portfolio_value[-1]
                # self.stop_loss=self.current_maxima*(1-self.trailing_stop_loss_percent/100)
            # return 0
    # def atr_stop_loss_checker(self):
        # if self.atr_stop_loss_percent==0:return 0
        # self.atr_stop_loss=self.portfolio_value[self.entry[-1]]-self.atr_stop_loss_percent*self.data["ATR"][self.i]
 
        # if self.portfolio_value[-1]<self.atr_stop_loss:
            # return 1
        # else: 
            # return 0    
    # def take_profit_checker(self):
        # if self.normal_take_profit==0:return 0
        # if self.portfolio_value[-1]>self.take_profit:
            # return 1
        # else:
            # return 0
    # def dynamic_exit_condition_checker(self):
        # if self.dynamic_exit_condition==0:return 0
        # if self.portfolio_value[-1]>self.dynamic_exit:
            # return 1
        # else: 
            # if self.portfolio_value[-1]<self.current_minima:
                # self.current_minima=self.portfolio_value[-1]
                # 
                # self.dynamic_exit=self.current_minima*(1+self.dynamic_exit_condition/100)
            # return 0
    # def atr_take_profit_checker(self):
        # if self.atr_take_profit_percent==0:return 0
        # self.atr_take_profit=self.portfolio_value[self.entry[-1]]+self.atr_take_profit_percent*self.data["ATR"][self.i]
        # if self.portfolio_value[-1]>self.atr_take_profit:
            # return 1
        # else:
            # return 0
    # def bactest(self):
        # for self.i in range(len(self.data)-1):
            # self.portfolio()
            # if self.current_position==1:
                # 
                # if self.data["signals"][self.i]==1 or self.data["signals"][self.i]==0:
                    # if  self.stop_loss_checker():
                    #    self.square_off()
                    # elif  self.trailing_stop_loss_checker():
                        # self.square_off()
                    # elif self.atr_stop_loss_checker():
                        # 
                        # self.square_off()
                # elif self.data["signals"][self.i]==-1:
                    # self.square_off()
            # if self.current_position==-1:
                # if self.data["signals"][self.i]==-1 or self.data["signals"][self.i]==0:
                    # if self.take_profit_checker():
                        # self.square_off()
                    # elif self.dynamic_exit_condition_checker():
                        # self.square_off()
                    # elif self.atr_take_profit_checker():
                        # self.square_off()
                # elif self.data["signals"][self.i]==1:
                    # self.square_off()
            # if self.current_position==0:
                # if self.data["signals"][self.i]==1:
                    # self.entry.append(self.i)
                    # self.current_position=1
                    # self.stop_loss=self.portfolio_value[-1]*(1-self.normal_stop_loss/100)
                    # self.current_maxima=self.portfolio_value[-1]
                    # self.type_of_trade.append("Long")
                    # self.number_of_stock=int(self.capital/self.data["Close"][self.i]*self.current_position)
                    # self.capital=self.capital-self.number_of_stock*self.data["Close"][self.i]
                # elif self.data["signals"][self.i]==-1:
                    # self.entry.append(self.i)
                    # self.current_position=-1
                    # self.take_profit=self.portfolio_value[-1]*(1+self.normal_take_profit/100)
                    # self.current_minima=self.portfolio_value[-1]
                    # self.type_of_trade.append("Short")
                    # self.number_of_stock=int(self.capital/self.data["Close"][self.i]*self.current_position)
                    # self.capital=self.capital+self.number_of_stock*self.data["Close"][self.i]
        # self.square_off() if self.number_of_stock!=0 else None
        # self.portfolio()
        # self.a["entry"]=self.entry
        # self.a["exit"]=self.exit
        # self.a["type_of_trade"]=self.type_of_trade
        # self.a["duration"]=self.duration
        # self.a["P and L"]=self.pl
        # self.data["portfolio value"]=self.portfolio_value
    # def parameters(self):
        # self.result.append(100*(self.capital-self.intial_balance)/self.intial_balance) 
        # self.result.append(self.intial_balance*(self.data["Close"].iloc[-1]-self.data["Close"].iloc[0])/self.data["Close"].iloc[0])
        # self.result.append(len(self.a))
        # self.result.append(np.max(self.a['duration']))
        # self.result.append(np.mean(self.a['duration']))
        # self.result.append(self.a['P and L'].sum())
        # self.result.append(self.a['P and L'].sum() - 20 * len(self.a))
        # drawdown = []
        # dip = []
        # returns_for_sharpe=[]

        # for i in range(len(self.a)):
            # entry_index = self.a['entry'][i]
            # exit_index = self.a['exit'][i]

            # initial_value = self.data['portfolio value'][entry_index]
            # min_value = min(self.data['portfolio value'][entry_index:exit_index + 1])
            # dip.append(100 * (initial_value - min_value) / initial_value)

            # returns_for_sharpe.append((100*self.a['P and L']/(initial_value)-(self.tnx['Close'].iloc[exit_index])/(np.sqrt(252))))

            # max_drawdown = 0
            # temp1 = initial_value

            # for j in range(entry_index + 1, exit_index + 1):
                # temp1 = max(temp1, self.data['portfolio value'][j])
                # drawdown_value = (temp1 - self.data['portfolio value'][j]) / temp1
                # max_drawdown = max(max_drawdown, drawdown_value)

            # drawdown.append(max_drawdown)

        # self.a['drawdown'] = drawdown 
        # self.a['dip'] = dip
        # self.result.append(100 * np.max(self.a['drawdown']))
        # self.result.append(100 * np.mean(self.a['drawdown']))
        # self.result.append(np.max(self.a['dip']))
        # self.result.append(np.mean(self.a['dip']))
        # self.result.append(np.sqrt(252)*(np.mean(returns_for_sharpe)/(np.std(returns_for_sharpe))))
        # return self.result
    
class Bactesting_Framework():
    def __init__(self,data,tnx,normal_stop_loss=100,normal_take_profit=100,trailing_stop_loss_percent=100,dynamic_exit_condition=100,atr_take_profit_percent=100,atr_stop_loss_percent=100):
        self.data = data
        self.normal_stop_loss =float(0 if normal_stop_loss==100 else normal_stop_loss)
        self.stop_loss = 0
        self.normal_take_profit =float( 0 if normal_take_profit==100 else normal_take_profit)
        self.take_profit=0
        self.trailing_stop_loss_percent =float( 0 if trailing_stop_loss_percent==100 else trailing_stop_loss_percent)
        self.trailing_stop_loss=0
        self.dynamic_exit_condition = float(0 if  dynamic_exit_condition ==100 else dynamic_exit_condition)
        self.dynamic_exit=0
        self.atr_take_profit_percent = float(0 if  atr_take_profit_percent==100 else atr_take_profit_percent)
        self.atr_take_profit=0
        self.atr_stop_loss_percent =float( 0 if  atr_stop_loss_percent ==100 else atr_stop_loss_percent)
        self.atr_stop_loss=0
        self.current_position = 0
        self.intial_balance = 1000000
        self.capital = self.intial_balance
        self.entry=[]
        self.exit=[]
        self.number_of_stock=0
        self.type_of_trade=[]
        self.duration=[]
        self.win=0
        self.stop_loss=0
        self.loss=0
        self.count_stop_loss=0
        self.current_maxima=0
        self.current_minima=0
        self.a=pd.DataFrame(columns=['entry'])
        self.portfolio_value=[] 
        self.pl=[]
        self.i=0
        self.result=[]
        self.tnx=tnx
        self.atr()
        self.bactest()
        # self.parameters()
    #-------------------------------------------------------------------------------------------------------------
    def atr(self):
        self.data['High-Low'] = self.data['High'] - self.data['Low']
        self.data['High-PrevClose'] = np.abs(self.data['High'] - self.data['Close'].shift(1))
        self.data['Low-PrevClose'] = np.abs(self.data['Low'] - self.data['Close'].shift(1))

        self.data['TR'] = self.data[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)

        # Calculate Average True Range (ATR)
        period = 14
        self.data['ATR'] = self.data['TR'].rolling(window=period).mean()

        # Clean up
        self.data.drop(['High-Low', 'High-PrevClose', 'Low-PrevClose', 'TR'], axis=1, inplace=True)
    #-------------------------------------------------------------------------------------------------------------
    def hello(self):
        print("hello")
    def portfolio(self):
        capital=self.capital+self.number_of_stock*self.data["Close"][self.i]
        self.portfolio_value.append(capital)
    def stop_loss_checker(self):
        if self.normal_stop_loss==0:return 0
        if self.portfolio_value[-1]<self.stop_loss:
            return 1
        else: return 0
    def square_off(self):
        self.exit.append(self.i)
        self.current_position=0
        self.capital=self.portfolio_value[-1]
        self.number_of_stock=0
        # print(len(self.exit),len(self.entry))
        self.duration.append(self.exit[-1]-self.entry[-1])
        self.profit_loss()
    def profit_loss(self):
        if self.portfolio_value[self.exit[-1]]>self.portfolio_value[self.entry[-1]]:
            self.win+=1
        else:
            self.loss+=1
        self.pl.append(self.portfolio_value[self.exit[-1]]-self.portfolio_value[self.entry[-1]])
    def trailing_stop_loss_checker(self):
        if self.trailing_stop_loss_percent==0:return 0
        if self.portfolio_value[-1]<self.trailing_stop_loss:
            return 1
        else:
            if  self.portfolio_value[-1]>self.current_maxima:
                self.current_maxima=self.portfolio_value[-1]
                self.stop_loss=self.current_maxima*(1-self.trailing_stop_loss_percent/100)
            return 0
    def atr_stop_loss_checker(self):
        if self.atr_stop_loss_percent==0:return 0
        self.atr_stop_loss=self.portfolio_value[self.entry[-1]]-self.atr_stop_loss_percent*self.data["ATR"][self.i]
 
        if self.portfolio_value[-1]<self.atr_stop_loss:
            return 1
        else: 
            return 0    
    def take_profit_checker(self):
        if self.normal_take_profit==0:return 0
        if self.portfolio_value[-1]>self.take_profit:
            return 1
        else:
            return 0
    def dynamic_exit_condition_checker(self):
        if self.dynamic_exit_condition==0:return 0
        if self.portfolio_value[-1]>self.dynamic_exit:
            return 1
        else: 
            if self.portfolio_value[-1]<self.current_minima:
                self.current_minima=self.portfolio_value[-1]
                
                self.dynamic_exit=self.current_minima*(1+self.dynamic_exit_condition/100)
            return 0
    def atr_take_profit_checker(self):
        if self.atr_take_profit_percent==0:return 0
        self.atr_take_profit=self.portfolio_value[self.entry[-1]]+self.atr_take_profit_percent*self.data["ATR"][self.i]
        if self.portfolio_value[-1]>self.atr_take_profit:
            return 1
        else:
            return 0
    def bactest(self):
        count=0
        for self.i in range(len(self.data)-1):
            self.portfolio()
            print(0) if self.capital<0 else None
            if self.current_position==1:
                
                if self.data["signals"][self.i]==1 or self.data["signals"][self.i]==0:
                    if  self.stop_loss_checker():
                       self.square_off()
                    elif  self.trailing_stop_loss_checker():
                        self.square_off()
                    elif self.atr_stop_loss_checker():
                        
                        self.square_off()
                elif self.data["signals"][self.i]==-1:
                    self.square_off()
            elif self.current_position==-1:
                if self.data["signals"][self.i]==-1 or self.data["signals"][self.i]==0:
                    if self.take_profit_checker():
                        self.square_off()
                    elif self.dynamic_exit_condition_checker():
                        self.square_off()
                    elif self.atr_take_profit_checker():
                        self.square_off()
                elif self.data["signals"][self.i]==1:
                    self.square_off()
            elif self.current_position==0:
                if self.data["signals"][self.i]==1:
                    count+=1
                    self.entry.append(self.i)
                    self.current_position=1
                    self.stop_loss=self.portfolio_value[-1]*(1-self.normal_stop_loss/100)
                    self.current_maxima=self.portfolio_value[-1]
                    self.type_of_trade.append("Long")
                    self.number_of_stock=int(self.capital/self.data["Close"][self.i])*self.current_position
                    self.capital=self.capital-self.number_of_stock*self.data["Close"][self.i]
                elif self.data["signals"][self.i]==-1:
                    count+=1
                    self.entry.append(self.i)
                    self.current_position=-1
                    self.take_profit=self.portfolio_value[-1]*(1+self.normal_take_profit/100)
                    self.current_minima=self.portfolio_value[-1]
                    self.type_of_trade.append("Short")
                    self.number_of_stock=int(self.capital/self.data["Close"][self.i])*self.current_position
                    self.capital=self.capital-self.number_of_stock*self.data["Close"][self.i]
        self.square_off() if self.number_of_stock!=0 else None
        self.portfolio()

        self.a["entry"]=self.entry
        self.a["exit"]=self.exit
        self.a["type_of_trade"]=self.type_of_trade
        self.a["duration"]=self.duration
        self.a["P and L"]=self.pl
        self.data["portfolio value"]=self.portfolio_value
    def parameters(self):
        self.result.append(100*(self.capital-self.intial_balance)/self.intial_balance) 
        temp=int(self.capital/self.data["Close"].iloc[0])
        self.result.append(temp*(self.data["Close"].iloc[-1]-self.data["Close"][0]))
        # self.result.append(self.intial_balance*(self.data["Close"].iloc[-1]-self.data["Close"].iloc[0])/self.data["Close"].iloc[0])
        self.result.append(len(self.a))
        self.result.append(np.max(self.a['duration']))
        self.result.append(np.mean(self.a['duration']))
        self.result.append(self.a['P and L'].sum())
        self.result.append(self.a['P and L'].sum() - 20 * len(self.a))
        drawdown = []
        dip = []
        returns_for_sharpe=[]

        for i in range(len(self.a)):
            entry_index = self.a['entry'][i]
            exit_index = self.a['exit'][i]

            initial_value = self.data['portfolio value'][entry_index]
            min_value = min(self.data['portfolio value'][entry_index:exit_index + 1])
            dip.append(100 * (initial_value - min_value) / initial_value)

            returns_for_sharpe.append((100*self.a['P and L']/(initial_value)-(self.tnx['Close'].iloc[exit_index])/(np.sqrt(252))))

            max_drawdown = 0
            temp1 = initial_value

            for j in range(entry_index + 1, exit_index + 1):
                temp1 = max(temp1, self.data['portfolio value'][j])
                drawdown_value = (temp1 - self.data['portfolio value'][j]) / temp1
                max_drawdown = max(max_drawdown, drawdown_value)

            drawdown.append(max_drawdown)

        self.a['drawdown'] = drawdown 
        self.a['dip'] = dip
        self.result.append(100 * np.max(self.a['drawdown']))
        self.result.append(100 * np.mean(self.a['drawdown']))
        self.result.append(np.max(self.a['dip']))
        self.result.append(np.mean(self.a['dip']))
        self.result.append(np.sqrt(252)*(np.mean(returns_for_sharpe)/(np.std(returns_for_sharpe))))
        return self.result
    

                    
         
                    
         