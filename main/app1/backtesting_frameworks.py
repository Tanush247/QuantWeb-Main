import pandas as pd
import numpy as np

def normal_stop_loss_check(capital, stop_loss):
    return capital <= stop_loss

def normal_take_profit_check(capital, take_profit):
    return capital >= take_profit

def trailing_stop_loss_check(capital, current_maxima, stop_loss_percent):
    stop_loss = (1 - stop_loss_percent) * current_maxima
    return capital <= stop_loss

def trailing_take_profit_check(capital, entry_price, take_profit_percent):
    take_profit = (1 + take_profit_percent) * entry_price
    return capital >= take_profit

def dynamic_exit_condition_check(capital, condition_value):
    return capital <= condition_value

def atr_stop_loss_check(capital, atr_value, multiplier):
    stop_loss = capital - ((float)(atr_value) *(float)(multiplier))
    return capital <= stop_loss

def atr_take_profit_check(capital, atr_value, multiplier):
    take_profit = capital + ((float)(atr_value) * (float)(multiplier))
    return capital >= take_profit

def handle_exit(index,current, capital, number_of_stock, data, entry, exit, duration, pl, portfolio_value, type_of_trade, win, loss):
    if current == 1:
        capital += number_of_stock * data.Close[index]
        portfolio_value.append(capital)
        exit.append(index)
        current = 0
        duration.append(exit[-1] - entry[-1])
        x = portfolio_value[exit[-1]] - portfolio_value[entry[-1]]
        pl.append(x)
        if x > 0:
            win += 1
        elif x < 0:
            loss += 1
        number_of_stock = 0

    elif current == -1:
        capital -= number_of_stock * data.Close[index]
        portfolio_value.append(capital)
        exit.append(index)
        current = 0
        duration.append(exit[-1] - entry[-1])
        x = portfolio_value[exit[-1]] - portfolio_value[entry[-1]]
        pl.append(x)
        if x > 0:
            win += 1
        elif x < 0:
            loss += 1
        number_of_stock = 0

    return current, capital, number_of_stock, exit, duration, pl, portfolio_value, win, loss

def backtest_1(data, stop_loss_percent=0.1, take_profit_percent=0.1, use_normal_stop_loss=False, use_normal_take_profit=False,
               use_trailing_stop_loss=False, use_trailing_take_profit=False, use_dynamic_exit_condition=False, use_atr_stop_loss=False,
               use_atr_take_profit=False, normal_stop_loss=100, normal_take_profit=100, trailing_stop_loss=100, trailing_take_profit=100,
               dynamic_exit_condition=100, atr_stop_loss=100, atr_take_profit=100):
    current = 0  # current position
    capital = 1000000
    entry = []
    exit = []
    number_of_stock = 0
    type_of_trade = []
    duration = []
    win = 0
    loss = 0
    current_maxima = 0
    portfolio_value = []  # total capital: non-investment + investment
    pl = []  # profit and loss

    atr = data['Close'].rolling(window=14).apply(lambda x: np.std(x))  # example ATR calculation

    for i in range(len(data) - 1):
        if current == 1:  # if in long position
            if data.signals[i] == 1 or data.signals[i] == 0:
                capital += number_of_stock * data.Close[i]
                portfolio_value.append(capital)

                if (use_normal_stop_loss and normal_stop_loss_check(capital, normal_stop_loss)) or \
                   (use_trailing_stop_loss and trailing_stop_loss_check(capital, current_maxima, stop_loss_percent)) or \
                   (use_dynamic_exit_condition and dynamic_exit_condition_check(capital, dynamic_exit_condition)) or \
                   (use_atr_stop_loss and atr_stop_loss_check(capital, atr[i], atr_stop_loss)) or \
                   (use_normal_take_profit and normal_take_profit_check(capital, normal_take_profit)) or \
                   (use_trailing_take_profit and trailing_take_profit_check(capital, data.Close[entry[-1]], take_profit_percent)) or \
                   (use_atr_take_profit and atr_take_profit_check(capital, atr[i], atr_take_profit)):
                    
                    current, capital, number_of_stock, exit, duration, pl, portfolio_value, win, loss = handle_exit(i,current, capital, number_of_stock, data, entry, exit, duration, pl, portfolio_value, type_of_trade, win, loss)

            elif data.signals[i] == -1:
                current, capital, number_of_stock, exit, duration, pl, portfolio_value, win, loss = handle_exit(i,current, capital, number_of_stock, data, entry, exit, duration, pl, portfolio_value, type_of_trade, win, loss)

        elif current == -1:  # if in short position
            if data.signals[i] == -1 or data.signals[i] == 0:
                capital -= number_of_stock * data.Close[i]
                portfolio_value.append(capital)

                if (use_normal_stop_loss and normal_stop_loss_check(capital, normal_stop_loss)) or \
                   (use_trailing_stop_loss and trailing_stop_loss_check(capital, current_maxima, stop_loss_percent)) or \
                   (use_dynamic_exit_condition and dynamic_exit_condition_check(capital, dynamic_exit_condition)) or \
                   (use_atr_stop_loss and atr_stop_loss_check(capital, atr[i], atr_stop_loss)) or \
                   (use_normal_take_profit and normal_take_profit_check(capital, normal_take_profit)) or \
                   (use_trailing_take_profit and trailing_take_profit_check(capital, data.Close[entry[-1]], take_profit_percent)) or \
                   (use_atr_take_profit and atr_take_profit_check(capital, atr[i], atr_take_profit)):
                    
                    current, capital, number_of_stock, exit, duration, pl, portfolio_value, win, loss = handle_exit(i,current, capital, number_of_stock, data, entry, exit, duration, pl, portfolio_value, type_of_trade, win, loss)

            elif data.signals[i] == 1:
                current, capital, number_of_stock, exit, duration, pl, portfolio_value, win, loss = handle_exit(i,current, capital, number_of_stock, data, entry, exit, duration, pl, portfolio_value, type_of_trade, win, loss)

        else:  # if no position
            if data.signals[i] == 1:
                current = 1
                current_maxima = capital
                stop_loss = (1 - stop_loss_percent) * current_maxima
                number_of_stock = int(capital / data.Close[i])
                portfolio_value.append(capital)
                capital -= number_of_stock * data.Close[i]
                entry.append(i)
                type_of_trade.append("long")

            elif data.signals[i] == -1:
                current = -1
                current_maxima = capital
                stop_loss = (1 + stop_loss_percent) * current_maxima
                number_of_stock = int(capital / data.Close[i])
                portfolio_value.append(capital)
                capital += number_of_stock * data.Close[i]
                entry.append(i)
                type_of_trade.append("short")

            else:
                portfolio_value.append(capital)

    if current == 1:
        current, capital, number_of_stock, exit, duration, pl, portfolio_value, win, loss = handle_exit(i,current, capital, number_of_stock, data, entry, exit, duration, pl, portfolio_value, type_of_trade, win, loss)
    elif current == -1:
        current, capital, number_of_stock, exit, duration, pl, portfolio_value, win, loss = handle_exit(i,current, capital, number_of_stock, data, entry, exit, duration, pl, portfolio_value, type_of_trade, win, loss)
    print(f"Length of portfolio_value: {len(portfolio_value)}")
    print(f"Length of data.index: {len(data.index)}")
    trade = pd.DataFrame(columns=['entry'])
    trade['entry'] = entry
    trade['exit'] = exit
    trade['duration'] = duration
    trade['P and L'] = pl
    trade['type'] = type_of_trade
    if len(portfolio_value) != len(data.index):
        # Adjust portfolio_value to match the length of data.index
        # Example: trim or pad portfolio_value
        if len(portfolio_value) > len(data.index):
            portfolio_value = portfolio_value[:len(data.index)]
        else:
            portfolio_value.extend([None] * (len(data.index) - len(portfolio_value)))

    data['portfolio value'] = portfolio_value

    return trade, capital

def parameters(data, trade, tnx, capital_initial=1000000):
    temp = capital_initial
    number_of_stock = int(temp / data.Close[0])
    final_value = capital_initial - number_of_stock * (data.Close[0] - data.Close.iloc[-1])
    
    drawdown = []
    dip = []
    returns_for_sharpe = []
    
    for i in range(len(trade)):
        entry_index = trade['entry'][i]
        exit_index = trade['exit'][i]
        
        initial_value = data['portfolio value'][entry_index]
        min_value = min(data['portfolio value'][entry_index:exit_index])/initial_value
        dip.append(100 * (initial_value - min_value) / initial_value)
        
        returns_for_sharpe.append((100 * trade['P and L'] / (initial_value) - (tnx['Close'].iloc[exit_index]) / (np.sqrt(252))))
        
        max_drawdown = 0
        temp1 = initial_value
        
        for j in range(entry_index + 1, exit_index + 1):
            temp1 = max(temp1, data['portfolio value'][j])
            drawdown_value = (temp1 - data['portfolio value'][j]) / temp1
            max_drawdown = max(max_drawdown, drawdown_value)
        
        drawdown.append(max_drawdown)
    
    trade['drawdown'] = drawdown
    trade['dip'] = dip
    
    

    


    return (trade['P and L'].sum() / capital_initial) * 100, final_value - capital_initial, len(trade), np.max(trade['duration']),np.mean(trade['duration']),trade['P and L'].sum(),trade['P and L'].sum() - 20 * len(trade),100 * np.max(trade['drawdown']),100 * np.mean(trade['drawdown']), np.max(trade['dip']),np.mean(trade['dip']),np.sqrt(252)*(np.mean(returns_for_sharpe)/(np.std(returns_for_sharpe)))
        