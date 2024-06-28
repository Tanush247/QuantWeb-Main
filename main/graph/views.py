from datetime import timedelta
from django.shortcuts import render
import plotly.express as px
import pandas as pd
from .forms import GraphForm
from yfinance import download

def home(request):
    graph_html = None

    if request.method == 'POST':
        form = GraphForm(request.POST)
        if form.is_valid():
            # Process the input data
            ticker = form.cleaned_data['input_string']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Subtract one day from the end date
            end_date -= timedelta(days=1)
            
            # Fetch stock data
            stock_data = download(ticker, start=start_date, end=end_date)
            
            if not stock_data.empty:
                # Create a line plot of the closing prices
                fig = px.line(stock_data, x=stock_data.index, y='Close', title=f'{ticker} Closing Prices')
                fig.update_layout(title_x=0.5)
                fig.update_yaxes(tickprefix='INR ')
                
                # Convert the plotly figure to HTML
                graph_html = fig.to_html(full_html=False)
            else:
                graph_html = '<p>No data found for the given ticker and date range.</p>'
    else:
        form = GraphForm()

    return render(request, 'graph/home.html', {'form': form, 'graph_html': graph_html})
