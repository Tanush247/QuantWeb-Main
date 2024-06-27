import pandas as pd
import numpy as np
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')
import pandas_ta as ta

## DOWNLOAWDINF DATA AND GENRATING SIGNALS

        
apple = yf.download('AAPL', '2018-01-01', '2022-01-01')
tnx = yf.download('^TNX', '2018-01-01', '2022-01-01')
apple['signals'] = 0
apple['ATR'] = ta.atr(apple['High'], apple['Low'], apple['Close'], length= 14)

def macd(df):
    
    df['MACD'] = df['Close'].ewm(span = 12,adjust=False).mean() - df['Close'].ewm(span=28,adjust=False).mean()
    df['Signal_MACD'] = df['MACD'].ewm(span = 9,adjust = False).mean()
    return df
apple = macd(apple)



for i in range(len(apple)):
    if(apple.MACD[i] > apple.Signal_MACD[i] and apple.MACD[i-1]< apple.Signal_MACD[i-1]):
        apple.signals[i] = 1
    elif(apple.MACD[i] < apple.Signal_MACD[i] and apple.MACD[i-1] > apple.Signal_MACD[i-1]):
        apple.signals[i] = -1
    else:
        apple.signals[i] = 0

#------------------------------------------------------------------------------------------------------------------------

class Trading_Bot():
    def __init__(self, data, tnx,capital, stop_loss_percent = 1, trailing_stop_loss_percent = 1, normal_take_profit_percent = 100, dynamic_exit_percent = 100, atr_based_stopp_loss_multi = 1000, atr_based_take_profit_multi = 1000):
        self.capital = capital
        self.data = data
        self.ATR= ta.atr(self.data['High'], self.data['Low'], self.data['Close'], length= 14)
        ## For long trades
        
        # normal stop-loss
        self.stop_loss_percent = stop_loss_percent
        self.normal_stop_loss = (1 - stop_loss_percent)*capital
        
        # trailing stop loss
        self.trailing_stop_loss_percent = trailing_stop_loss_percent
        self.trailing_stop_loss = (1 - trailing_stop_loss_percent)*capital
        
        # ATR based stop-loss
        self.atr_based_stop_loss_multi = atr_based_stopp_loss_multi
        self.atr_based_stop_loss = self.capital - atr_based_stopp_loss_multi*self.ATR[0]
        
        ## For short trades
        
        # dynamic exit 
        self.dynamic_exit_percent = dynamic_exit_percent
        self.dynamic_exit = (1 + dynamic_exit_percent)*capital
        
        # normal take profit
        self.normal_take_profit_percent = normal_take_profit_percent
        self.normal_take_profit = (1 + normal_take_profit_percent)*capital
        
        # ATR based take profit
        self.atr_based_take_profit_multi = atr_based_take_profit_multi
        self.atr_based_take_profit = self.capital + atr_based_take_profit_multi*self.ATR[0]
        
        
        self.trailing_stop_loss = (1 - trailing_stop_loss_percent)*capital
        self.current = 0
        self.number_of_stocks = 0
        self.portfolio_value = []
        self.exit = []
        self.entry = []
        self.type_of_trade = []
        self.win = 0
        self.loss = 0
        self.check_index = -1
        self.stop_loss_hit = []
        self.current_maxima = 0
        self.current_minima = 0
        self.dynamic_profit_hit = []
        self.drawdown = []
        self.dip = []
        self.time = []
        self.p_and_l = []
        self.returns_for_sharpe = []
        self.total_transaction_cost = []
        self.signal = []
        self.benchmark = int(capital/data.Close[0])*(data.Close[len(data)-1] - data.Close[0])
        self.returns = 0
        self.transaction_cost = 0.001
        self.tnx = tnx

        
    ## Drawdown and dip
    def calculate_drawdown_dip(self):
        for i in range(len(self.entry)):
            entry = self.entry[i]
            exit = self.exit[i]
            temp =  self.portfolio_value[entry]
            max_draw = 0
            for j in range(entry, exit+1):
                temp = max(temp, self.portfolio_value[j])
                draw = (temp - self.portfolio_value[j])*100/temp
                max_draw = max(draw, max_draw)
            self.drawdown.append(max_draw)
            # temp1 = max(self.portfolio_value[entry:exit+1])
            temp2 = min(self.portfolio_value[entry:exit+1])
            dip = (temp - temp2)*100/temp
            self.dip.append(dip)
                
                
    ##Checking entry conditions   
    
    def check_entry_condition(self,i):
        
        if(self.data.signals[i] == 1):
            self.signal.append(1)
            self.check_index += 1
            self.current = 1
            self.total_transaction_cost.append(self.capital*self.transaction_cost)
            # self.capital = self.capital*(1 - self.transaction_cost)
            
            self.number_of_stocks = int(self.capital/self.data.Close[i])
            
            self.normal_stop_loss = (1 - self.stop_loss_percent)*self.capital
            
            self.trailing_stop_loss = (1 - self.stop_loss_percent)*self.capital
            
            self.atr_based_stop_loss = self.capital - self.atr_based_stop_loss_multi*self.ATR[i]
            
            self.portfolio_value.append(self.capital)
            self.current_maxima = self.capital
            self.capital = self.capital - self.number_of_stocks*self.data.Close[i]
            self.entry.append(i)
            self.type_of_trade.append('long')
            
            
        elif(self.data.signals[i] == -1):
            self.signal.append(-1)
            self.check_index += 1
            self.current = -1
            self.total_transaction_cost.append(self.capital*self.transaction_cost)
            # self.capital = self.capital*(1 - self.transaction_cost)
            
            self.normal_take_profit = (1 + self.normal_take_profit_percent)*self.capital
            
            self.dynamic_exit = (1 + self.dynamic_exit_percent)*self.capital
            
            self.atr_based_take_profit = self.capital + self.atr_based_take_profit_multi*self.ATR[i]
            
            self.number_of_stocks = int(self.capital/self.data.Close[i])
            self.portfolio_value.append(self.capital)
            self.current_minima = self.capital
            self.capital = self.capital + self.number_of_stocks*self.data.Close[i]
            self.entry.append(i)
            self.type_of_trade.append('short')
        else:
            self.signal.append(0)
            self.portfolio_value.append(self.capital)

            
    ## Winning or Lossing Trades
    
    def check_win_or_loss(self):
        x = (self.portfolio_value[self.exit[-1]] - self.portfolio_value[self.entry[-1]])
        self.p_and_l.append(x)
        self.returns_for_sharpe.append((100*self.p_and_l[-1]/(self.portfolio_value[self.entry[-1]])-(self.tnx['Close'][self.exit[-1]])/(np.sqrt(252))))
        if(x > 0):
            self.win += 1
        elif(x < 0):
            self.loss += 1

    ##Checking exit condition
            
    def check_exit_condition_long(self,i):
        self.capital = self.capital + self.number_of_stocks*self.data.Close[i]
        if(self.capital <= self.normal_stop_loss or self.capital <= self.trailing_stop_loss or self.capital <= self.atr_based_stop_loss):
            self.signal.append(-1)
            self.total_transaction_cost.append(self.capital*self.transaction_cost)
            # self.capital = self.capital*(1 - self.transaction_cost)
            self.portfolio_value.append(self.capital)
            self.exit.append(i)
            self.number_of_stocks = 0
            self.current = 0
            self.stop_loss_hit.append(i)
            self.check_win_or_loss()
            self.time.append(self.exit[-1] - self.entry[-1])
        elif(self.data.signals[i] == -1):
            self.signal.append(-1)
            self.total_transaction_cost.append(self.capital*self.transaction_cost)
            # self.capital = self.capital*(1 - self.transaction_cost)
            self.portfolio_value.append(self.capital)
            self.exit.append(i)
            self.number_of_stocks = 0
            self.current = 0
            self.check_win_or_loss()
            self.time.append(self.exit[-1] - self.entry[-1])
        elif(self.capital > self.current_maxima):
            self.signal.append(0)
            self.portfolio_value.append(self.capital)
            self.current_maxima = self.capital
            self.trailing_stop_loss = (1 - self.stop_loss_percent)*self.current_maxima
        else:
            self.signal.append(0)
            self.portfolio_value.append(self.capital)
        self.capital = self.capital - self.data.Close[i]*self.number_of_stocks
            
    def check_exit_condition_short(self,i):
        self.capital = self.capital - self.number_of_stocks*self.data.Close[i]
        if(self.capital >= self.normal_take_profit or self.capital >= self.dynamic_exit or self.capital >= self.atr_based_take_profit):
            self.signal.append(1)
            self.total_transaction_cost.append(self.capital*self.transaction_cost)
            # self.capital = self.capital*(1 - self.transaction_cost)
            self.portfolio_value.append(self.capital)
            self.exit.append(i)
            self.number_of_stocks = 0
            self.current = 0
            self.dynamic_profit_hit.append(i)
            self.check_win_or_loss()
            self.time.append(self.exit[-1] - self.entry[-1])
        elif(self.data.signals[i] == 1):
            self.signal.append(1)
            self.total_transaction_cost.append(self.capital*self.transaction_cost)
            # self.capital = self.capital*(1 - self.transaction_cost)
            self.portfolio_value.append(self.capital)
            self.exit.append(i)
            self.number_of_stocks = 0
            self.current = 0
            self.check_win_or_loss()
            self.time.append(self.exit[-1] - self.entry[-1])
        elif(self.capital<self.current_minima):
            self.signal.append(0)
            self.portfolio_value.append(self.capital)
            multiplier=(self.current_minima-self.capital)/self.current_minima
            self.current_minima = self.capital
            self.dynamic_exit=(1+ self.dynamic_exit_percent)*multiplier*self.current_minima
        else:
            self.signal.append(0)
            self.portfolio_value.append(self.capital)
        self.capital = self.capital + self.data.Close[i]*self.number_of_stocks
            
    #Returns
    def Returns(self):
        self.returns = (self.portfolio_value[-1] - self.portfolio_value[0])*100/self.portfolio_value[0]
    ## Main backtesting
    
    def backtesting(self):
        
        for i in range(len(self.data)-1):
           
            if(self.current == 1): 
                self.check_exit_condition_long(i)

            
            elif(self.current == -1):
                self.check_exit_condition_short(i)
                
            else:
                self.check_entry_condition(i)
                
        if(self.current == 1):
            self.signal.append(-1)
            self.total_transaction_cost.append(self.capital*self.transaction_cost)
            # self.capital = self.capital*(1 - self.transaction_cost)
            self.portfolio_value.append(self.capital) 
            self.exit.append(i)
            self.capital = self.capital + self.number_of_stocks*self.data.Close[i]
        elif(self.current == -1):
            self.signal.append(1)
            self.total_transaction_cost.append(self.capital*self.transaction_cost)
            # self.capital = self.capital*(1 - self.transaction_cost)
            self.portfolio_value.append(self.capital)
            self.exit.append(i)
            self.capital = self.capital - self.number_of_stocks*self.data.Close[i]
        else:
            self.signal.append(0)
            self.portfolio_value.append(self.capital)
        self.calculate_drawdown_dip()
        self.Returns() 
        return (self.returns, self.benchmark, self.win + self.loss, np.max(self.time), np.mean(self.time), self.portfolio_value[-1] - self.portfolio_value[0] , self.portfolio_value[-1] - self.portfolio_value[0] - np.sum(self.total_transaction_cost), np.max(self.drawdown), np.mean(self.drawdown), np.max(self.dip), np.mean(self.dip), np.sqrt(252)*(np.mean(self.returns_for_sharpe)/(np.std(self.returns_for_sharpe))))
    
    def alternate_signal(self, signal1, signal2, portfolio1, portfolio2):
        strt = 1
        signals = []
        count = 0
        flag = 0
        for i in range(len(self.data)):
            if(strt == 1):
                signals.append(signal1[i])
                if( signal1[i] == 1 or signal1[i] == -1 and flag != 1):
                    index = i
                    flag = 1
                count += signal1[i]
                if(flag == 1 and count == 0):
                    returns = (portfolio1[i] - portfolio1[index])*100/portfolio1[index]
                    check = (portfolio2[i] - portfolio2[index])*100/portfolio2[index]
                    if(check > returns):
                        strt = 2
                        flag = 0
            
            elif(strt == 2):
                signals.append(signal2[i])
                if( signal2[i] == 1 or signal2[i] == -1 and flag != 1):
                    index = i
                    flag = 1
                count += signal2[i]
                if(flag == 1 and count == 0):
                    returns = (portfolio2[i] - portfolio2[index])*100/portfolio2[index]
                    check = (portfolio1[i] - portfolio1[index])*100/portfolio1[index]
                    if(check > returns):
                        strt = 1
                        flag = 0
        return signals
            
                    
                
            

# Apple_M = Trading_Bot(apple, tnx, 1000)

# km = Apple_M.backtesting()
# portfolio_value_macd = Apple_M.portfolio_value
# signals_macd = Apple_M.signal

# def rsi(df):
#     df['RSI'] = ta.rsi(df['Close'], length = 14)
# rsi(apple)

# # print(apple)

# for i in range(len(portfolio_value_macd)):
#     if apple['RSI'][i] > 70:
#         apple['signals'][i] = 1
#     elif apple['RSI'][i] < 30:
#         apple['signals'][i] = -1
#     else:
#         apple['signals'][i] = 0

# Apple_R = Trading_Bot(apple, tnx, 1000)    

# kr = Apple_R.backtesting()
# portfolio_value_rsi = Apple_R.portfolio_value
# signals_rsi = Apple_R.signal

# apple['signals'], macd_times, rsi_times = Apple_R.alternate_signal(signals_macd, signals_rsi, portfolio_value_macd, portfolio_value_rsi)

# Apple = Trading_Bot(apple, tnx, 1000)

# k = Apple.backtesting()


# print(Apple.capital) 

# # apple['portfolio_value_oops'] = Apple.portfolio_value
# apple.to_csv('output.csv')

# trades_won = Apple.win
# trades_loss = Apple.loss
# win_rate = (trades_won)*100/(trades_won + trades_loss)
# number_of_closed_trades = trades_won + trades_loss
# max_drawdown = np.max(Apple.drawdown)
# average_drawdown = np.mean(Apple.drawdown)
# max_dip = np.max(Apple.dip)
# avg_dip = np.mean(Apple.dip)
# max_holding_time = np.max(Apple.time)
# avg_holding_time = np.mean(Apple.time)
# benchmark_returns = Apple.benchmark
# returns = Apple.returns

# print('RETURNS: ', returns)
# print('BENCHMARK RETURNS: ', benchmark_returns)
# print('NUMBER OF CLOSED TRADES: ', number_of_closed_trades)
# print('MAX HOLDING TIME: ', max_holding_time, 'DAYS')
# print('AVG HOLDING TIME: ', avg_holding_time, 'DAYS')
# print('MAX DRAWDOWN: ', max_drawdown)
# print('AVG DRAWDOWN: ', average_drawdown)
# print('MAX DIP: ', max_dip)
# print('AVG DIP: ', avg_dip)
# print("SHARPE RATIO: ",np.sqrt(252)*(np.mean(Apple.returns_for_sharpe)/(np.std(Apple.returns_for_sharpe))))
# print(portfolio_value_rsi[-1], portfolio_value_macd[-1], macd_times, rsi_times)
