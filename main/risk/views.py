from django.shortcuts import render

def home(request):
    
    indicators = [
        {
            'name': 'Trailing Stop-Loss',
            'description': 'A stop-loss is a pre-set order to sell a security when it reaches a specified price, minimizing potential losses for an investor or trader. A trailing stop loss is a dynamic risk management strategy where the stop loss level adjusts automatically based on the asset’s price movement, helping to lock in profits or limit losses. The trade is closed when the market price decreases by more than a defined percent from the current high.',
            'image_url': 'risk/images/tsl1.png',
        },
        {
           'name': 'Trailing Take-Profit',
           'description':'Trailing stop loss prevented us from booking sufficient profits in short trades. The stop loss gets triggered too soon everytime there is a fall , In this the boundary is set at above the portfolio price rather than below it.This helps us minimise the loss in short trades. As the portfolio value rises, the exit condition remains constant. It falls as soon as there is a dip in price.',
           'image_url': 'risk/images/ttp1.png',
       },
       {
           'name': 'ATR Stop-Loss',
           'description': 'ATR stop loss is a market volatility based stop loss indicator. When volatility increases, the ATR value rises, and the stop-loss widens to accommodate larger price swings. Conversely, during periods of lower volatility, the stop-loss tightens. Using ATR allows us to set levels that are proportional to the current volatility, helping to account for the varying ranges of price movement.',
           'image_url':'risk/images/atr1.jpg',
       },
       {
           'name': 'Max Drawdown Limit',
           'description':'An increased drawdown indicates a risky trade. Drawdowns will anyway be high in a volatile market. Our work should be to minimise the risk. This we can do by using a max drawdown limit. As soon as this limit is reached, the trade is squared off. This will ensure we don’t lose too much on the trade.',
           'image_url': 'risk/images/md1.webp',
       },
    ]
    
    codes = [
        {
            'name': 'Trailing Stop-Loss Code',
            'description': 'To calculate the trailing stop loss we calculate the current maximum portfolio value during the trade and as this value changes we update the trailing stop loss price and square off the trade when the portfolio value crosses this price. This helps to keep the exit price dynamic which ensures a better exit position than the fixed stop loss risk management method.',
            'image_url': 'risk/images/tsl2.png',
        },
        {
           'name': 'Trailing Take-Profit Code',
           'description':'To calculate the trailing take profit we calculate the current minimum portfolio value during the trade and as this value changes we update the trailing take profit price and square off the trade when the portfolio value crosses this price. This helps to keep the exit price dynamic which ensures a better exit position than the fixed take profit risk management method.',
           'image_url': 'risk/images/ttp2.png',
       },
       {
           'name': 'ATR Stop-Loss Code',
           'description': 'TrueRange -> The true range of a stock for the day is the greatest of the following: current high less the current low; the absolute value of the current high less the previous close; and the absolute value of the current low less the previous close. AverageTrueRange -> The Average True Range is a moving average of the true ranges. For Long Trades Stop Loss price = closing price - multiplier * ATR value, For Short Trades Stop Loss price = closing price + multiplier * ATR value.',
           'image_url':'risk/images/atr2.png',
       },
       {
           'name': 'Max Drawdown Limit Code',
           'description':'Drawdown denotes the maximum difference between a peak and the corresponding trough. Calculate the drawdown always using the portfolio value. For each trade we calculate the drawdown in percent, the maximum of them would be the maximum drawdown. We square off a trade as soon as the max drawdown reaches the limit set.',
           'image_url': 'risk/images/md2.png',
       },
    ]
    
    context = {
        'indicators': indicators,
        'codes': codes
    }
    
    return render(request,'risk/home.html', context)

