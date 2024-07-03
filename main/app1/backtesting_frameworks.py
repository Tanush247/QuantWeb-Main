import pandas as pd
import numpy as np



class backtesting_class ():
    
    def __init__(self,  bitmask,data, normal_sl, normal_tp, trailing_sl_percent, trailing_tp_percent, atr_sl_multiplier, atr_tp_multiplier, tnx):

        self.capital_initial = 1000000
        self.capital = 1000000
        self.data = data
        self.quantity = 0
        self.quantity_for_trade = []

        self.current = 0
        self.number_of_trades = 0
        
        self.entry = []
        self.exit = []

        self.current_maxima = 0
        self.portfolio_value = []
        self.pl = []
        self.duration = []
        self.type_of_trade = []
        self.close = data['Close']

        self.drawdown = 0
        self.maximum_drawdown_for_trade = 0
        self.drawdown_for_all_trades = []

        self.dip = []


        self.bitmask = bitmask
        self.maxima_for_risk = 0
        self.minima_for_risk = 0

        self.normal_sl = float(self.capital_initial*(1-normal_sl))
        self.trailing_sl_percent =float(trailing_sl_percent) 
        self.trailing_sl = 0
        self.atr_sl_multiplier = float (atr_sl_multiplier)
        self.atr_sl = 0

        self.normal_tp =  float(self.capital_initial*(1+normal_tp))
        self.trailing_tp_percent = float(trailing_tp_percent)
        self.trailing_tp = 0
        self.atr_tp_multiplier = float(atr_tp_multiplier)
        self.atr_tp = 0
        

        self.tnx_close = tnx['Close']
        if isinstance(data.index, pd.DatetimeIndex):
            self.dates = data.index.tolist()
        else :
            self.dates = data['datetime']     


        if ((self.atr_sl_multiplier or self.atr_tp_multiplier)!= 0 ) :
            df = pd.DataFrame()
            df['High-Low'] = data['High'] - data['Low']
            df['High-PrevClose'] = np.abs(data['High'] - data['Close'].shift(1))
            df['Low-PrevClose'] = np.abs(data['Low'] - data['Close'].shift(1))
            
            df['TR'] = df[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1) 
            df['ATR'] = df['TR'].rolling(window=14).mean()
            data['ATR'] = df['ATR']



    
    def update_drawdown (self, i) :
        if (self.close[i] > self.current_maxima) :
            self.current_maxima = self.close[i]

        self.drawdown = (self.current_maxima - self.close[i])/self.current_maxima*100

        if ( self.drawdown > self.maximum_drawdown_for_trade) :
            self.maximum_drawdown_for_trade = self.drawdown


    def update_dip (self, i):
        self.initial_value = self.portfolio_value[self.entry[-1]]
        self.min_value = min(self.portfolio_value[self.entry[-1]:self.exit[-1] +1 ])
        self.dip.append(100 * (self.initial_value - self.min_value) / self.initial_value)


    def start_long_position(self,i) :
        self.quantity = int(self.capital / self.close[i])
        self.quantity_for_trade.append(self.quantity)
        self.portfolio_value.append(self.capital)
        self.entry.append(i)
        self.capital = self.capital - self.quantity*self.close[i]
        self.type_of_trade.append('long')
        self.number_of_trades += 1
        self.current=1

        self.update_drawdown( i)   



    def start_short_position(self, i) :
        self.quantity = int(self.capital / self.close[i])
        self.quantity_for_trade.append(self.quantity)
        self.portfolio_value.append(self.capital)
        self.entry.append(i)
        self.capital = self.capital + self.quantity*self.close[i]
        self.type_of_trade.append('short')
        self.number_of_trades += 1
        self.current=-1

        self.update_drawdown( i)
        



    def end_long_position(self, i) :    
    
        self.exit.append(i)
        self.capital = self.capital + self.quantity*self.close[i]
        self.portfolio_value.append(self.capital)
        self.current=0

        self.update_drawdown(i)
        self.drawdown_for_all_trades.append(self.maximum_drawdown_for_trade)
        self.maximum_drawdown_for_trade= 0
        self.current_maxima = 0
        
        self.update_dip(i)

        self.duration.append(self.exit[-1] - self.entry[-1])
        self.pl.append(self.portfolio_value[self.exit[-1]] - self.portfolio_value[self.entry[-1]])

    

    def end_short_position(self , i) :

        self.exit.append(i)
        self.capital = self.capital - self.quantity*self.close[i]
        self.portfolio_value.append(self.capital)
        self.current=0

        self.update_drawdown( i)
        self.drawdown_for_all_trades.append(self.maximum_drawdown_for_trade)
        self.maximum_drawdown_for_trade= 0
        self.current_maxima = 0

        self.update_dip(i)

        self.duration.append(self.exit[-1] - self.entry[-1])
        self.pl.append(self.portfolio_value[self.exit[-1]] - self.portfolio_value[self.entry[-1]])



    def update_long_trade(self, i) :
        self.portfolio_value.append(self.capital + self.quantity*self.close[i])   
        self.update_drawdown( i)


    def update_short_trade(self, i) :
        self.portfolio_value.append(self.capital - self.quantity*self.close[i])
        self.update_drawdown(  i )


    def set_sl (self, i ):
        
        if (self.bitmask & (1<<3)) !=0 :
            self.trailing_sl = (1 - self.trailing_sl_percent)*self.portfolio_value[i]
            self.maxima_for_risk = self.portfolio_value[i]

        if (self.bitmask & (1<<5)) !=0:
            if self.current == 1 :
                self.atr_sl =  self.close[i] - self.atr_sl_multiplier*self.data['ATR'].iloc[i]
            elif self.current == -1 :
                self.atr_sl =  self.close[i] + self.atr_sl_multiplier*self.data['ATR'].iloc[i]
            

    def set_tp (self, i ):
        
        if (self.bitmask & (1<<4)) !=0 :
            self.trailing_tp = (1 + self.trailing_tp_percent)*self.portfolio_value[i]  
            self.minima_for_risk = self.portfolio_value[i]

        if (self.bitmask & (1<<6)) !=0 :    
            if self.current == 1 :
                self.atr_tp =  self.close[i] + self.atr_tp_multiplier*self.data['ATR'].iloc[i]
            elif self.current == -1 :
                self.atr_tp =  self.close[i] - self.atr_tp_multiplier*self.data['ATR'].iloc[i]


    def update_sl (self, i ):  
        if (self.bitmask & (1<<3)) !=0 :  
            if (self.portfolio_value[i]>self.maxima_for_risk) :
                self.trailing_sl = (1 - self.trailing_sl_percent)*self.portfolio_value[i]
                self.maxima_for_risk = self.portfolio_value[i]

        if (self.bitmask & (1<<5)) != 0 :
            if self.current == 1 :
                self.atr_sl =  self.close[i] - self.atr_sl_multiplier*self.data['ATR'].iloc[i]
            elif self.current == -1 :
                self.atr_sl =  self.close[i] + self.atr_sl_multiplier*self.data['ATR'].iloc[i] 

                
                     

    def  update_tp (self, i ):   
        if (self.bitmask & (1<<4)) !=0 :  
            if (self.portfolio_value[i]<self.minima_for_risk) :
                self.trailing_tp = (1 + self.trailing_tp_percent)*self.portfolio_value[i]
                self.minima_for_risk = self.portfolio_value[i]

                
        if (self.bitmask & (1<<6)) != 0 :
            if self.current == 1 :
                self.atr_tp =  self.close[i] + self.atr_tp_multiplier*self.data['ATR'].iloc[i]
            elif self.current == -1 :
                self.atr_tp =  self.close[i] - self.atr_tp_multiplier*self.data['ATR'].iloc[i]  


    def check_sl_tp (self):    
        if  (self.bitmask & (1<<1)) !=0 :
            if (self.portfolio_value[-1] <= self.normal_sl) :
                return 1
        if  (self.bitmask & (1<<2)) !=0 :
            if (self.portfolio_value[-1] >= self.normal_tp) :
                return 1    
        if  (self.bitmask & (1<<3)) !=0 :
            if (self.portfolio_value[-1] <= self.trailing_sl) :
                return 1
        if  (self.bitmask & (1<<4)) !=0 :
            if (self.portfolio_value[-1] >= self.trailing_tp) :
                return 1
        if  (self.bitmask & (1<<5)) !=0 :
            if (self.portfolio_value[-1] <= self.atr_sl) :
                return 1
        if  (self.bitmask & (1<<6)) !=0 :
            if (self.portfolio_value[-1] >= self.atr_tp) :
                return 1        

        return 0    


    def start_backtest(self) :

        for i in range (len(self.data)-1) :

            if ( self.current  == 0):

                if(self.data['signals'].iloc[i]==1 ) :
                    self.start_long_position( i)
                    self.set_sl( i)
                    self.set_tp( i)
                    

                elif(self.data['signals'].iloc[i]==-1) :
                    self.start_short_position( i)
                    self.set_sl( i)
                    self.set_tp( i)                    

                else:
                    if( len(self.portfolio_value) == 0 ):
                        self.portfolio_value.append(self.capital_initial)
                    else :    
                        self.portfolio_value.append(self.portfolio_value[-1]) 
                       



            elif( self.current == 1) :

                if (self.data['signals'].iloc[i]==0 or self.data['signals'].iloc[i]==1  ) :
                    if( self.check_sl_tp() == 1) :
                        self.end_long_position( i)
                    else :
                        self.update_long_trade( i)
                        self.update_sl( i )
                        self.update_tp( i )


                elif(self.data['signals'].iloc[i]== -1 ) :
                    self.end_long_position( i)
                    


            elif( self.current == -1) :

                if (self.data['signals'].iloc[i]==0 or self.data['signals'].iloc[i]==-1  ) :
                    if( self.check_sl_tp() == 1) :
                        self.end_short_position( i)
                    else :
                        self.update_short_trade( i)
                        self.update_sl( i )
                        self.update_tp( i )

                elif(self.data['signals'].iloc[i]== 1 ) :
                    self.end_short_position(i)



        if self.current == 1:
            self.end_long_position(len(self.data) -1)
        elif self.current == -1:
            self.end_short_position(len(self.data) -1)
        else:
           self.portfolio_value.append(self.portfolio_value[-1])   

        
        self.returns_percent = (np.sum(self.pl) / self.capital_initial) * 100
        self.benchmark =  ( self.close.iloc[-1] - self.close[0]) *  (int(self.capital_initial / self.close[0]))

        self.returns_for_sharpe = []
        
        for i in range  (len(self.entry)) :
            entry_index = self.entry[i]
            exit_index = self.exit[i]
            self.returns_for_sharpe.append((100*self.pl[i]/(self.portfolio_value[entry_index])-(self.tnx_close[exit_index])/(np.sqrt(252))))

        return (self.returns_percent , self.benchmark,self.number_of_trades, np.max(self.duration),np.mean(self.duration),np.sum(self.pl) ,np.sum(self.pl)- 20 * self.number_of_trades , np.max(self.drawdown_for_all_trades),np.mean(self.drawdown_for_all_trades), np.max(self.dip),np.mean(self.dip),np.sqrt(252)*(np.mean(self.returns_for_sharpe)/(np.std(self.returns_for_sharpe))) , self.portfolio_value, self.dates)




