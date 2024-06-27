import pandas as pd
import numpy as np
import math

class TradingStrategy_compounding:

    '''This function initializes the class according to the data provided, it creates several variables for inside the class, as described'''
    def __init__(self, data, nsl, ntp, tsl, dec, atrsl, atrtp):

        self.initial_balance= 100000 # Initial Capital
        self.capital = 100000 # this represents the current capital
        self.data = data # this variable is created to use the data inside each function of the class
        self.nsl=float(nsl/100) # Normal stop loss in %
        self.ntp=float(ntp/100) # Normal take profit in %
        self.tsl=float(tsl/100) # Trailing stop loss in %
        self.dec=float(dec/100) # Trailing take profit in %
        self.atrsl_m=float(atrsl) # ATR multiplier for stop loss
        self.atrtp_m=float(atrtp) # ATR multiplier for take profit
       
        if 'Close' in data.columns:
            data['close']=data['Close']
        if 'Open' in data.columns:
            data['open']=data['Open']
        if 'High' in data.columns:
            data['high']=data['High']
        if 'Low' in data.columns:
            data['low']=data['Low']
        if 'Volume' in data.columns:
            data['volume']=data['Volume']
        if 'Date' in data.columns:
            data['datetime']=data['Date']
        if 'Datetime' in data.columns:
            data['datetime']=data['Datetime']
        if 'Close' in data.columns:
            data['TR'] = np.maximum(data['High'] - data['Low'],
                                        np.maximum(abs(data['High'] - data['Close'].shift(1)),
                                                abs(data['Low'] - data['Close'].shift(1))))
            data['ATR'] = data['TR'].rolling(window=14).mean()
            
        data['TR'] = np.maximum(data['high'] - data['low'],
                                        np.maximum(abs(data['high'] - data['close'].shift(1)),
                                                abs(data['low'] - data['close'].shift(1))))
        data['ATR'] = data['TR'].rolling(window=14).mean()
        
        self.atr_value=data['ATR']
        self.entry_price = 0 
        # self.datetime = [] # datetime colmun, it is for daily trade log, will remain same as in data originally
        # self.low = data.low
        self.portfolio_value = [] # this is the portfolio value we have at each index (each day)
        self.quantity = [] # this represents the holding at each index (each day)
        self.current_position = 0 # this represents the current position (-1 = short, 1 = long, 0 = no position)
        self.holding = 0 # this represents the current holding (will be updated at each index)
        self.remain = 0 # un-invested capital

        self.current_portfolio_value = 0 # this represents the current portfolio value (will be updated at each index)

        self.current_stop_loss_value = 0 # this is the temporary variable for the trade in action
        self.current_trade_peak = 0 # this is the maximum portfolio value for trade in action (as we implemented trailing stop-loss)
        self.stop_loss_percent = self.tsl 
        
        self.normal_stop_loss_value = 0
        self.take_profit_value = 0 # this is the temporary variable for the trade in action
        self.normal_take_profit_value = 0
        self.take_profit_percent = self.dec 
        self.atr_stop_loss_value = 0
        self.atr_take_profit_value = 0

        self.stop_loss_count = [] 
        self.normal_stop_loss_count = [] 
        self.trailing_stop_loss_count = [] 
        self.atr_stop_loss_count = [] 
        self.take_profit_count = [] 
        self.normal_take_profit_count = [] 
        self.trailing_take_profit_count = [] 
        self.atr_take_profit_count = [] 

        self.entry = [] # list to store entry index of each trade
        self.exit = [] # list to store exit index of each trade
        self.new_signals = [] # list to new signals, after implementation of stop loss and take profit, and if required, other exit conditions
        self.close = data['close'] # close value of stock

        self.trade_type = [] # this is for trade type, according to entry type
        self.drawdown = [] # this is drawdown for each day
        self.tradewise_drawdown = []
        self.dip = [] 
        self.tradewise_dip = []
        self.benchmark_return = (((int(100000/self.close[0]) * self.close[len(self.data) - 1] - 100000)/100000)*100) # this is benchmark returns, according to buy & hold
        self.signals = data['signals'] # signals column according to strategy
        self.transaction_percentage = 0.0015

        self.risk_free_rate = 0.05 # you can change it

        self.amount_in_trade = []
        self.trade_wise_returns = []
        self.PL_in_dollars = []
        self.amount_invested_in_trade = []

    '''This is the function to calculate drawdown, it returns an array of drawdown according to portolio value,
     for maximum drawdown, we will take maximum of this drawdown array'''
    def calculate_drawdown(self):
        data = self.portfolio_value
        drawdown = []
        tradewise_drawdown = []
        temp_peak = data[0]
        for i in range(len(data)):
            if data[i] > temp_peak:
                temp_peak = data[i]
            drawdown.append(((temp_peak - data[i])/temp_peak) * 100)
        for j in range(len(self.entry)):
            k=self.entry[j]
            l=self.exit[j]
            temp_peak = data[k]
            drawdown2 = []
            for i in range(k,l+1):
                if data[i] > temp_peak:
                    temp_peak = data[i]
                drawdown2.append(((temp_peak - data[i])/data[i]) * 100)
            tradewise_drawdown.append(max(drawdown2))
        return drawdown,tradewise_drawdown

    '''This is the function to calculate dip, it returns an array of dip according to portolio value,
     for maximum dip, we will take maximum of this dip array'''
    def calculate_dip(self):
        data = self.portfolio_value
        tradewise_dip = []
        for j in range(len(self.entry)):
            k=self.entry[j]
            l=self.exit[j]
            temp_min = data[k]
            for i in range(k,l+1):
                if data[i] < temp_min:
                    temp_min = data[i]
            tradewise_dip.append(((data[k]-temp_min)/data[k])*100)
        return tradewise_dip

    '''This function is used to start a long position on the equity'''
    def take_long_position(self,i):
        self.current_position = 1
        self.holding = int(self.capital / self.close[i]) # as we buy the equity from all the capital we posses
        self.remain = self.capital - self.holding * self.close[i]
        self.capital = 0
        self.entry_price=self.close[i]
        self.new_signals.append(1)
        self.quantity.append(self.holding)
        self.current_portfolio_value = (self.holding * self.close[i]) + self.remain
        self.portfolio_value.append(self.current_portfolio_value)
        self.entry.append(i)
        self.trade_type.append('long')
        self.amount_in_trade.append(self.current_portfolio_value)
        self.amount_invested_in_trade.append(self.current_portfolio_value)

    '''This function is used to start a short position on the equity'''
    def take_short_position(self,i):
        self.current_position = -1
        self.holding = int(self.capital / self.close[i])
        self.capital = 2 * self.capital
        self.entry_price = self.close[i]
        self.new_signals.append(-1)
        self.quantity.append(self.holding)
        self.current_portfolio_value = self.capital - self.holding * self.close[i]
        self.portfolio_value.append(self.current_portfolio_value)
        self.entry.append(i)
        self.trade_type.append('short')
        self.amount_in_trade.append(self.current_portfolio_value)
        self.amount_invested_in_trade.append(self.current_portfolio_value)

    '''This function is called when we currently have no position, and do not intend to start either. So portfolio value will be same as capital'''
    def update_no_trade(self,i):
        self.current_position = 0
        self.new_signals.append(0)
        self.holding = 0
        self.portfolio_value.append(self.capital)
        self.quantity.append(0)

    '''This function is called when we are currently on long, and we don't want to exit the trade,so current holding and capital remain same'''
    def update_long_trade(self, i):
        self.current_position = 1
        self.quantity.append(self.holding)
        self.current_portfolio_value = (self.holding * self.close[i]) + self.remain
        self.portfolio_value.append(self.current_portfolio_value)
        self.new_signals.append(0)

    '''This function is called when we are currently on short, and we don't want to exit the trade,so current holding and capital remain same'''
    def update_short_trade(self, i):
        self.current_position = -1
        self.quantity.append(self.holding)
        self.current_portfolio_value = self.capital - self.holding * self.close[i]
        self.portfolio_value.append(self.current_portfolio_value)
        self.new_signals.append(0)

    '''This function is called when we want to exit a long trade, so we will increase in hand capital in this case'''
    def close_long_trade(self, i):
        self.current_position = 0
        self.quantity.append(0)
        self.capital = (self.close[i] * self.holding) + self.remain
        self.current_portfolio_value = self.capital
        self.portfolio_value.append(self.current_portfolio_value)
        self.new_signals.append(-1)
        self.exit.append(i)
        self.amount_in_trade.append(self.current_portfolio_value)

    '''This function is called when we want to exit a short trade, so we will increase in hand capital in this case'''
    def close_short_trade(self, i):
        self.current_position = 0
        self.capital = self.capital - self.close[i] * self.holding
        self.quantity.append(0)
        self.current_portfolio_value = self.capital
        self.portfolio_value.append(self.current_portfolio_value)
        self.new_signals.append(1)
        self.exit.append(i)
        self.amount_in_trade.append(self.current_portfolio_value)

    '''This function is called when we are currently on long/short position. It checks if we should exit the trade based on stop-loss and take-profit'''
    def check_exit_condition(self, i):
        if self.current_position == 1:
            temp_value = (self.holding * self.close[i]) + self.remain
            if temp_value < self.current_stop_loss_value:
                self.stop_loss_count.append(i)
                self.trailing_stop_loss_count.append(i)
                return 1
            elif temp_value >= self.take_profit_value:
                self.take_profit_count.append(i)
                self.trailing_take_profit_count.append(i)
                return 1
            elif self.close[i] <= self.normal_stop_loss_value:
                self.stop_loss_count.append(i)
                self.normal_stop_loss_count.append(i)
                return 1
            elif self.close[i] >= self.normal_take_profit_value:
                self.take_profit_count.append(i)
                self.normal_take_profit_count.append(i)
                return 1
            elif self.close[i] <= self.atr_stop_loss_value:
                self.stop_loss_count.append(i)
                self.atr_stop_loss_count.append(i)
                return 1
            elif self.close[i] >= self.atr_take_profit_value:
                self.take_profit_count.append(i)
                self.atr_take_profit_count.append(i)
                return 1
            
        elif self.current_position == -1:
            temp_value = self.capital - self.holding * self.close[i]
            if temp_value > self.current_stop_loss_value:
                self.stop_loss_count.append(i)
                self.trailing_stop_loss_count.append(i)
                return 1
            elif temp_value <= self.take_profit_value:
                self.trailing_take_profit_count.append(i)
                return 1
            elif self.close[i] >= self.normal_stop_loss_value:
                self.stop_loss_count.append(i)
                self.normal_stop_loss_count.append(i)
                return 1
            elif self.close[i] <= self.normal_take_profit_value:
                self.take_profit_count.append(i)
                self.normal_take_profit_count.append(i)
                return 1
            elif self.close[i] >= self.atr_stop_loss_value:
                self.stop_loss_count.append(i)
                self.atr_stop_loss_count.append(i)
                return 1
            elif self.close[i] <= self.atr_take_profit_value:
                self.take_profit_count.append(i)
                self.atr_take_profit_count.append(i)
                return 1
            
        return 0

    '''This function is to set the stop-loss depending on entry price'''
    def set_stop_loss(self, i):
        if self.current_position == 1:
            self.current_stop_loss_value = (1 - self.stop_loss_percent) * (self.current_trade_peak)
        elif self.current_position == -1:
            self.current_stop_loss_value = (1 + self.stop_loss_percent) * (self.current_trade_peak)

    '''This function is used to update the trailing_stop-loss value, if the portfolio value increases (TRAILING STOP-LOSS)'''
    def update_stop_loss(self, i):
        if self.current_position == 1:
            if (self.holding * self.close[i]) + self.remain > self.current_trade_peak:
                self.current_trade_peak = (self.holding * self.close[i]) + self.remain
                self.set_stop_loss(i)
        elif self.current_position == -1:
            if self.capital - self.holding * self.close[i] < self.current_trade_peak:
                self.current_trade_peak = self.capital - self.holding * self.close[i]
                self.set_stop_loss(i)

    '''This function is to set the trailing_take-profit depending on entry price'''
    def set_take_profit(self, i):
        if self.current_position == 1:
            self.take_profit_value = (1 + self.take_profit_percent) * (self.current_portfolio_value)
        elif self.current_position == -1:
            self.take_profit_value = (1 - self.take_profit_percent) * (self.current_portfolio_value)
            
    '''This function is to set the normal_take-profit depending on entry price'''
    def set_normal_take_profit(self, i):
        if self.current_position == 1:
            self.normal_take_profit_value = self.entry_price * (1 + self.ntp)
        elif self.current_position == -1:
            self.normal_take_profit_value = self.entry_price * (1 - self.ntp)
            
    '''This function is to set the normal_stop-loss depending on entry price'''
    def set_normal_stop_loss(self, i):
        if self.current_position == 1:
            self.normal_stop_loss_value = self.entry_price * (1 - self.ntp)
        elif self.current_position == -1:
            self.normal_stop_loss_value = self.entry_price * (1 + self.ntp)

    '''This function is to set the atr_take-profit depending on entry price'''
    def set_atr_take_profit(self, i):
        if self.current_position == 1:
            self.atr_take_profit_value = self.entry_price + (self.atrtp_m * self.atr_value[i])
        elif self.current_position == -1:
            self.atr_take_profit_value = self.entry_price - (self.atrtp_m * self.atr_value[i])
            
            
    '''This function is to set the atr_stop-loss depending on entry price'''
    def set_atr_stop_loss(self, i):
        if self.current_position == 1:
            self.atr_stop_loss_value = self.entry_price - (self.atrtp_m * self.atr_value[i])
        elif self.current_position == -1:
            self.atr_stop_loss_value = self.entry_price + (self.atrtp_m * self.atr_value[i])
            
            

    '''This is the function, which when called will analyse all the trades'''
    def compounding(self):

        x = len(self.data) - 1 # we don't care about the signal on last date, because we cannot open anew position, and if a position is already open, we must close it
        for i in range(x):
            # self.datetime.append(self.data.datetime[i])
            if self.capital < 0: # this possibility may arise in compounding approach
                # print('capital wiped')
                break

            if self.current_position == 0:

                if self.signals[i] == 0:
                    self.update_no_trade(i)
                elif self.signals[i] == 1:
                    self.take_long_position(i) # to start a new long position
                    self.current_trade_peak = self.current_portfolio_value
                    self.set_take_profit(i)
                    self.set_stop_loss(i)
                    self.set_normal_take_profit(i)
                    self.set_atr_take_profit(i)
                    self.set_normal_stop_loss(i)
                    self.set_atr_stop_loss(i)
                elif self.signals[i] == -1:
                    self.take_short_position(i) # to start a new short position
                    self.current_trade_peak = self.current_portfolio_value
                    self.set_take_profit(i)
                    self.set_stop_loss(i)
                    self.set_normal_take_profit(i)
                    self.set_atr_take_profit(i)
                    self.set_normal_stop_loss(i)
                    self.set_atr_stop_loss(i)

            elif self.current_position == 1:
                if self.signals[i] == 0 or self.signals[i] == 1:
                    if self.check_exit_condition(i) == 1:
                        self.close_long_trade(i) # to close a long position
                    else:
                        self.update_stop_loss(i)
                        self.update_long_trade(i)
                        self.set_normal_take_profit(i)
                        self.set_atr_take_profit(i)
                        self.set_normal_stop_loss(i)
                        self.set_atr_stop_loss(i)
                else:
                    self.close_long_trade(i) # to close a long position

            elif self.current_position == -1:
                if self.signals[i] == 0 or self.signals[i] == -1:
                    if self.check_exit_condition(i) == 1:
                        self.close_short_trade(i) # to close a short position
                    else:
                        self.update_stop_loss(i)
                        self.update_short_trade(i)
                        self.set_normal_take_profit(i)
                        self.set_atr_take_profit(i)
                        self.set_normal_stop_loss(i)
                        self.set_atr_stop_loss(i)
                else:
                    self.close_short_trade(i) # to close a short position

        # for the last trade
        # self.datetime.append(self.data.datetime[x])

        if self.current_position == 1:
            self.close_long_trade(x)
        elif self.current_position == -1:
            self.close_short_trade(x)
        else:
            self.update_no_trade(i)

        '''''''''''''''''''''''''''''''''''''''''''''''Trade log completed'''''''''''''''''''''''''''''''''''''''''''''''
        # we now calculate the remaining parameters like trade-wise profit/loss, max drawdown, net pnl. This is purely maths as we already have our portfolio vlaue for each day stored

        self.trade_wise_duration = np.array(self.exit) - np.array(self.entry)
        self.trade_wise_profit = []
        self.trade_wise_loss = []

        for i in range(len(self.entry)):
            current_trade_return = 100*((self.portfolio_value[self.exit[i]]/self.portfolio_value[self.entry[i]])-1)
            self.PL_in_dollars.append(self.portfolio_value[self.exit[i]]-self.portfolio_value[self.entry[i]])
            self.trade_wise_returns.append(current_trade_return)
            if current_trade_return >= 0:
                self.trade_wise_profit.append(current_trade_return)
            else:
                self.trade_wise_loss.append(current_trade_return)

        self.gross_profit = np.sum(self.PL_in_dollars)
        self.calculate_transaction_cost()
        self.net_profit = self.gross_profit - self.transaction_cost
        self.returns = ((self.net_profit / self.initial_balance)*100)
        self.drawdown,self.tradewise_drawdown = self.calculate_drawdown()
        self.dip = self.calculate_dip()
        self.calculate_ratios()
        '''''''''''''''''''''''''''''''''''''''''''''''All parameters calculated'''''''''''''''''''''''''''''''''''''''''''''''
        
        return self.create_strategy_dataframes() , self.create_trade_wise_dataframe() , self.create_every_day_dataframe() , self.return_parameters()

    def calculate_ratios(self):
        df = pd.DataFrame()
        df['portfolio_value'] = self.portfolio_value
        df['daily_return'] = df['portfolio_value'].pct_change()
        daily_volatility = df['daily_return'].std()
        annual_volatility = daily_volatility * math.sqrt(365)
        annual_volatility_negative = df[df['daily_return'] < 0]['daily_return'].std() * math.sqrt(365)
        risk_free_rate = self.risk_free_rate
        df['excess_return'] = (df['daily_return'] - risk_free_rate)
        annual_excess_return = (df['daily_return'].mean()*365 - risk_free_rate)
        cumulative_excess_return = df['excess_return'].sum()
        negative_returns = [r for r in df['excess_return'] if r < 0]
        cumulative_volatility = df['daily_return'].std()*math.sqrt(365)
        x = np.std(negative_returns)*math.sqrt(365)
        self.sharpe_ratio = annual_excess_return / annual_volatility
        self.sortino_ratio = annual_excess_return / annual_volatility_negative

    def calculate_transaction_cost(self):
        self.transaction_cost = 0
        for i in range(len(self.entry)):
            self.transaction_cost += self.transaction_percentage * (self.amount_invested_in_trade[i])

    '''After backtesting is complete, this function generated a dataframe which is the final one, after take-profit and stop-loss is implemented'''
    def create_strategy_dataframes(self):
        to_submit = pd.DataFrame(columns=['open'])
        # to_submit['datetime'] = self.datetime
        to_submit['open'] = self.data.open
        to_submit['high'] = self.data.high
        to_submit['low'] = self.data.low
        to_submit['close'] = self.data.close
        to_submit['volume'] = self.data.volume
        to_submit['signals'] = self.new_signals
        return to_submit

    '''This function generated a trade-log for our strategy, giving returns in each trade'''
    def create_trade_wise_dataframe(self):
        trade_wise = pd.DataFrame(columns=['entry', 'exit'])
        trade_wise['entry'] = self.entry
        trade_wise['exit'] = self.exit
        trade_wise['duration'] = self.trade_wise_duration
        trade_wise['trade type'] = self.trade_type
        trade_wise['returns'] = self.trade_wise_returns
        return trade_wise

    '''This function creates and everyday log of our strategy, to analyze the portfolio value and drawdown for each day'''
    def create_every_day_dataframe(self):
        every_day = pd.DataFrame(columns=['portfolio value', 'quantity'])
        # every_day['datetime'] = self.datetime
        every_day['quantity'] = self.quantity
        every_day['portfolio value'] = self.portfolio_value
        every_day['daily_return'] = every_day['portfolio value'].pct_change()
        every_day['drawdown'] = self.drawdown
        return every_day

    '''This function is used to return the necassary parameters, useful for analyzing our strategy'''
    def return_parameters(self):
        return self.returns,self.benchmark_return,len(self.entry),np.max(self.trade_wise_duration),np.mean(self.trade_wise_duration),self.gross_profit,self.net_profit,np.max(self.tradewise_drawdown),np.mean(self.tradewise_drawdown),np.max(self.dip),np.mean(self.dip),self.sharpe_ratio,len(self.normal_stop_loss_count),len(self.normal_take_profit_count),len(self.trailing_stop_loss_count),len(self.trailing_take_profit_count),len(self.atr_stop_loss_count),len(self.atr_take_profit_count)











# print('hello')
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
        