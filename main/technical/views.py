from django.shortcuts import render

def home(request):
    
    indicators = [
        {
            'name': 'Bollinger Bands',
            'description': 'This indicator consists of three bands. The middle band is a simple moving average typically. The two outer bands are standard deviations(usually with a multiplier of 2) from the middle band. The distance between the bands is a measure of volatility. This is used to guage oversold and overbought conditions in the market.',
           
            'image_url': 'technical/images/bb2.webp',


        },
       {
           'name': 'MACD',
           'description': 'Moving average convergence/divergence (MACD) is a technical indicator to help investors identify price trends, measure trend momentum, and identify market entry points for buying or selling. Moving average convergence/divergence (MACD) is a trend-following momentum indicator that shows the relationship between two exponential moving averages (EMAs) of a security’s price.',
           'image_url':'technical/images/macd3.jpg',
       },
       {
           'name': 'Ichimoku Cloud',
           'description':'The Ichimoku Cloud is a collection of technical indicators that show support and resistance levels, as well as momentum and trend direction. It does this by taking multiple averages and plotting them on a chart. It also uses these figures to compute a “cloud” that attempts to forecast where the price may find support or resistance in the future.',
           'image_url': 'technical/images/ic2.png',
       },
       {
           'name': 'OBV',
           'description':'On-balance volume (OBV) is a technical trading momentum indicator that uses volume flow to predict changes in stock price. When volume increases sharply without a significant change in the stocks price, the price will eventually jump upward or fall downward.',

           'image_url': 'technical/images/obv2.gif',
       },
       {
           'name': 'RSI',
           'description':'The relative strength index (RSI) is a momentum indicator used in technical analysis. RSI measures the speed and magnitude of a securitys recent price changes to evaluate overvalued or undervalued conditions in the price of that security. It gives us the value of strength in change of price movements. ',
           'image_url':'technical/images/rsi2.webp',
       },
    ]
    
    codes = [
        {
            'name': 'Bollinger Bands',
            'description': 'Bollinger Bands Indicator implementation in python. The center line is the stock prices 20-day simple moving average (SMA). The upper and lower bands are set at a certain number of standard deviations, usually two, above and below the middle line. The bands widen when a stocks price becomes more volatile and contract when it is more stable. Many traders see stocks as overbought as their price nears the upper band and oversold as they approach the lower band, signaling an opportune time to trade.',
           
            'image_url': 'technical/images/bb.png',


        },
       {
           'name': 'MACD',
           'description': 'MACD Indicator implementation in python. #) The MACD line is calculated by subtracting the 26-period exponential moving average (EMA) from the 12-period EMA. The signal line is a nine-period EMA of the MACD line. #) Traders may buy the security when the MACD line crosses above the signal line and sell or short the security when the MACD line crosses below the signal line.',
           'image_url':'technical/images/macd.png',
       },
       {
           'name': 'Ichimoku Cloud',
           'description':'Ichimoku Cloud Indicator implementation in python. The Ichimoku Cloud is composed of five lines or calculations, two of which comprise a cloud where the difference between the two lines is shaded in. The lines include a nine-period average, a 26-period average, an average of those two averages, a 52-period average, and a lagging closing price line. The cloud is a key part of the indicator. When the price is below the cloud, the trend is down. When the price is above the cloud, the trend is up.',
           'image_url': 'technical/images/ic.png',
       },
       {
           'name': 'OBV',
           'description':'OBV Indicator implementation in python. #) Calculating On-Balance Volume -> , 1) If todays closing price is higher than yesterdays closing price, then: Current OBV = Previous OBV + todays volume, 2) If todays closing price is lower than yesterdays closing price, then: Current OBV = Previous OBV - todays volume, 3) If todays closing price equals yesterdays closing price, then: Current OBV = Previous OBV',
           'image_url': 'technical/images/obv.png',
       },
       {
           'name': 'RSI',
           'description':'RSI Indicator implementation in python. #) The average gain or loss used in this calculation is the average percentage gain or loss during a look-back period. The formula uses a positive value for the average loss. Periods with price losses are counted as zero in the calculations of average gain. Periods with price increases are counted as zero in the calculations of average loss.' ,
           'image_url':'technical/images/rsi.png',
       },
    ]
    
    context = {
        'indicators': indicators,
        'codes': codes
    }
    
    return render(request,'technical/home.html', context)
def about(request):
    return render(request,'technical/about.html')