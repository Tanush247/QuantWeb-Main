from django.shortcuts import render,redirect
from .models import CommonModel,UserModel
from .forms import StrategyForm,csvForm,userstrategy
import yfinance as yf
from django.urls import reverse
from django.http import HttpResponse
from .backtesting_frameworks import backtesting_class
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
import io
import plotly.express as px

@login_required
def risk_management(request, destination):
    array = [
        ['NA',0],
        ['normal stop loss', 1],
        ['normal take profit', 2],
        ['trailing stop loss', 3],
        ['dynamic exit condition', 4],
        ['atr based stop loss', 5],
        ['atr based take profit', 6],
    ]

    if request.method == 'POST':
        selected_options = request.POST.getlist('risk_management')
        bitmask = 0
        for option in selected_options:
            bitmask |= (1 << int(option))
        if(bitmask%2==1 and bitmask!=1):
            context = {
                'array': array,
                'error':"Cannot select NA with any other option",
            }
            return render(request, 'app1/risk_management1.html', context)
       
        # Determine the destination URL based on the 'destination' parameter
        if destination == 'backtesting':
            url_name = 'app1:backtesting'
        elif destination == 'csv':
            url_name = 'app1:csv'
        else:
            # Handle the case where an invalid destination is provided
            # You can raise an error, redirect to a default page, etc.
            raise ValueError('Invalid destination')

        # Generate the URL with the bitmask as a query parameter
        url = f"{reverse(url_name)}?bitmask={bitmask}"
        return redirect(url)

    else:
        context = {
            'array': array,
        }
        return render(request, 'app1/risk_management1.html', context)
def execute_python_code(code_string, *args, **kwargs):
    # Prepare a dictionary to capture the result and any global variables
    code_globals = {}
    
    try:
        # Execute the code within a controlled environment
        exec(code_string, code_globals)
        
        # Extract the function 'hello' from the executed code
        hello_function = code_globals.get('hello')
        if callable(hello_function):
            # Call the 'hello' function with arguments *args and **kwargs
            result = hello_function(*args, **kwargs)
            return result, None  # Return result and no error message
        else:
            return None, "Function 'hello' not found in the provided code"
    
    except Exception as e:
        return None, f"Error executing code: {str(e)}"
    
@login_required  
def home(request):
    return render(request,'app1/hello.html')

@login_required
def created(request):
    user=request.user
    error_message=None
    if request.method =='POST':
        form=userstrategy(request.POST)
        if form.is_valid():
            strategy=form.cleaned_data['strategy']
            source=form.cleaned_data['source']
            object1=UserModel(owner=user,source=source,name=strategy)
            object1.save()
            return render(request,'app1/hello.html')
        else:
            error_message="Invalid"
    else:
        form=userstrategy()

    context={

        'error':error_message,
        'form':form
    }
    return render(request,'app1/your_strategy.html',context)

        
    

@login_required
def csv(request):
    user = request.user
    bitmask = int(request.GET.get('bitmask', 0))
    
    print(2,bitmask)
    error_message=None
    results=None

    port = None
    dates = None

    if request.method == "POST":
        form = csvForm(request.POST,request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            strategy = form.cleaned_data['strategy']
            df = pd.read_csv(csv_file, index_col=0, parse_dates=True)
            print(df)
            normal_stop_loss=0
            normal_take_profit=0
            trailing_stop_loss=0
            dynamic_exit_condition=0
            atr_take_loss=0
            atr_take_profit=0
            if(bitmask & (1<<1) !=0):
                normal_stop_loss=form.cleaned_data['normal_stop_loss']
                if(normal_stop_loss==None):
                    bitmask=bitmask-(1<<1)
            if(bitmask & (1<<2) !=0):
                normal_take_profit=form.cleaned_data['normal_take_profit']
                if(normal_take_profit==None):
                    bitmask=bitmask-(1<<2)
            if(bitmask & (1<<3) !=0):
                trailing_stop_loss=form.cleaned_data['trailing_stop_loss']
                if(trailing_stop_loss==None):
                    bitmask=bitmask-(1<<3)
            if(bitmask & (1<<4) !=0):
                dynamic_exit_condition=form.cleaned_data['dynamic_exit_condition']
                if(dynamic_exit_condition==None):
                    bitmask=bitmask-(1<<4)
            if(bitmask & (1<<5) !=0):
                atr_take_loss=form.cleaned_data['atr_stop_loss']
                if(atr_take_loss==None):
                    bitmask=bitmask-(1<<5)
            if(bitmask & (1<<6) !=0):
                atr_take_profit=form.cleaned_data['atr_take_profit']
                if(atr_take_profit==None):
                    bitmask=bitmask-(1<<6)
            

            start_date=df.index[0]
            end_date=df.index[len(df)-1]
        
            tnx=yf.download('^TNX',start_date,end_date)

            object1 = CommonModel.objects.filter(name=strategy).first()
            object2=UserModel.objects.filter(owner=user,name=strategy).first()
            if object1:
                python_code_string = object1.source
                
                
                df, error_message = execute_python_code(python_code_string,df)

                a = backtesting_class( bitmask,df, normal_stop_loss, normal_take_profit, trailing_stop_loss, dynamic_exit_condition, atr_take_loss, atr_take_profit, tnx)
                results = a.start_backtest()

                if (results != None) :
                    port = (results[12])
                    dates = (results[13])

                    fig = px.line( x=dates, y=port, title='CSV')
                    fig.update_yaxes(tickprefix='INR ')

                    fig.update_layout(
                    title={
                        'text': f'{strategy} Strategy Performance on CSV ',
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },

                    xaxis_title="Time Period",
                    yaxis_title="Portfolio Value (INR)",
                    title_font=dict(size=24, color='black', family='Arial'),

                    xaxis=dict(

                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(204, 204, 204)',
                        linewidth=1,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(82, 82, 82)',
                        ),

                    ),

                    yaxis=dict(
                        showgrid=True,
                        zeroline=False,
                        showline=True,
                        showticklabels=True,
                    ),

                    plot_bgcolor='white' )

                    fig.update_traces(mode='lines', line_shape='linear', line=dict(width=2))
                    plot_div = fig.to_html(full_html=False)


                
            else:
                if(object2):
                    python_code_string = object2.source
                
                    df, error_message = execute_python_code(python_code_string,df)

                    a = backtesting_class(bitmask,df, normal_stop_loss, normal_take_profit, trailing_stop_loss, dynamic_exit_condition, atr_take_loss, atr_take_profit, tnx)
                    results = a.start_backtest()
                        
                    if (results != None) :
                        port = (results[12])
                        dates = (results[13])

                        fig = px.line( x=dates, y=port, title=f'CSV')
                        fig.update_yaxes(tickprefix='INR ')

                        fig.update_layout(
                        title={
                            'text': f'{strategy} Strategy Performance on CSV ',
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'
                        },

                        xaxis_title="Time Period",
                        yaxis_title="Portfolio Value (INR)",
                        title_font=dict(size=24, color='black', family='Arial'),

                        xaxis=dict(

                            showline=True,
                            showgrid=True,
                            showticklabels=True,
                            linecolor='rgb(204, 204, 204)',
                            linewidth=1,
                            ticks='outside',
                            tickfont=dict(
                                family='Arial',
                                size=12,
                                color='rgb(82, 82, 82)',
                            ),

                        ),

                        yaxis=dict(
                            showgrid=True,
                            zeroline=False,
                            showline=True,
                            showticklabels=True,
                        ),

                        plot_bgcolor='white' )

                        fig.update_traces(mode='lines', line_shape='linear', line=dict(width=2))
                        plot_div = fig.to_html(full_html=False)

                else:
                    error_message = f"Backtesting failed"
    else:
        form=csvForm()


    if(results==None):
       context = {
        'first':None,
        'second':None,
        'third':None,
        'four':None,
        'five':None,
        'six':None,
        'seven':None,
        'eight':None,
        'nine':None,
        'ten':None,
        'eleven':None,
        'twelve':None,
        'thirteen':0,
        'graph' : None,
        'form': form,
        'error_message': error_message,
        'bitmask': bitmask,
        'show_normal_stop_loss': bitmask & (1 << 1) != 0,
        'show_normal_take_profit': bitmask & (1 << 2) != 0,
        'show_trailing_stop_loss': bitmask & (1 << 3) != 0,
        'show_dynamic_exit_condition': bitmask & (1 << 4) != 0,
        'show_atr_take_loss': bitmask & (1 << 5) != 0,
        'show_atr_take_profit': bitmask & (1 << 6) != 0,
        } 
    else:
        context = {
            'first':results[0],
            'second':results[1],
            'third':results[2],
            'four':results[3],
            'five':results[4],
            'six':results[5],
            'seven':results[6],
            'eight':results[7],
            'nine':results[8],
            'ten':results[9],
            'eleven':results[10],
            'twelve':results[11],
            'twelve':results[11],
            'thirteen':1,
            'graph' : plot_div,
            'form': form,
            'error_message': error_message,
            'bitmask': bitmask,
            'show_normal_stop_loss': bitmask & (1 << 1) != 0,
            'show_normal_take_profit': bitmask & (1 << 2) != 0,
            'show_trailing_stop_loss': bitmask & (1 << 3) != 0,
            'show_dynamic_exit_condition': bitmask & (1 << 4) != 0,
            'show_atr_take_loss': bitmask & (1 << 5) != 0,
            'show_atr_take_profit': bitmask & (1 << 6) != 0,
        }
    
    return render(request, 'app1/csv.html', context)

    
@login_required
def backtesting(request):
    bitmask = int(request.GET.get('bitmask', 0))
    print(1,bitmask)
    user = request.user
    
    result = None
    error_message = None
    results=None

    port = None
    dates = None

    if request.method == "POST":
        form = StrategyForm(request.POST)
        if form.is_valid():
            
            ticker = form.cleaned_data['ticker']
            strategy = form.cleaned_data['strategy']
            end_date = form.cleaned_data['end_date']
            start_date = form.cleaned_data['start_date']
            normal_stop_loss=0
            normal_take_profit=0
            trailing_stop_loss=0
            dynamic_exit_condition=0
            atr_take_loss=0
            atr_take_profit=0
            if(bitmask & (1<<1) !=0):
                normal_stop_loss=form.cleaned_data['normal_stop_loss']
                if(normal_stop_loss==None):
                    bitmask=bitmask-(1<<1)
                    normal_stop_loss = 0
            if(bitmask & (1<<2) !=0):
                normal_take_profit=form.cleaned_data['normal_take_profit']
                if(normal_take_profit==None):
                    bitmask=bitmask-(1<<2)
                    normal_take_profit = 0
            if(bitmask & (1<<3) !=0):
                trailing_stop_loss=form.cleaned_data['trailing_stop_loss']
                if(trailing_stop_loss==None):
                    bitmask=bitmask-(1<<3)
                    trailing_stop_loss = 0
            if(bitmask & (1<<4) !=0):
                dynamic_exit_condition=form.cleaned_data['dynamic_exit_condition']
                if(dynamic_exit_condition==None):
                    bitmask=bitmask-(1<<4)
                    dynamic_exit_condition = 0
            if(bitmask & (1<<5) !=0):
                atr_take_loss=form.cleaned_data['atr_stop_loss']
                if(atr_take_loss==None):
                    bitmask=bitmask-(1<<5)
                    atr_take_loss = 0
            if(bitmask & (1<<6) !=0):
                atr_take_profit=form.cleaned_data['atr_take_profit']
                if(atr_take_profit==None):
                    bitmask=bitmask-(1<<6)
                    atr_take_profit = 0
           

            data = yf.download(ticker, start_date, end_date)
            tnx=yf.download('^TNX',start_date,end_date)
           
           
            object1 = CommonModel.objects.filter(name=strategy).first()
            object2=UserModel.objects.filter(owner=user,name=strategy).first()
            if object1:
                python_code_string = object1.source
                
                
                data, error_message = execute_python_code(python_code_string,data)

                a = backtesting_class( bitmask,data, normal_stop_loss, normal_take_profit, trailing_stop_loss, dynamic_exit_condition, atr_take_loss, atr_take_profit, tnx)
                results = a.start_backtest()

                if (results != None) :
                    port = (results[12])
                    dates = (results[13])

                    fig = px.line( x=dates, y=port, title=f'{ticker}')
                    fig.update_yaxes(tickprefix='INR ')

                    fig.update_layout(
                    title={
                        'text': f'{strategy} Strategy Performance on {ticker} ',
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },

                    xaxis_title="Time Period",
                    yaxis_title="Portfolio Value (INR)",
                    title_font=dict(size=24, color='black', family='Arial'),

                    xaxis=dict(

                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(204, 204, 204)',
                        linewidth=1,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(82, 82, 82)',
                        ),

                    ),

                    yaxis=dict(
                        showgrid=True,
                        zeroline=False,
                        showline=True,
                        showticklabels=True,
                    ),

                    plot_bgcolor='white' )

                    fig.update_traces(mode='lines', line_shape='linear', line=dict(width=2))
                    plot_div = fig.to_html(full_html=False)


                
            else:
                if(object2):
                    python_code_string = object2.source
                
                    data, error_message = execute_python_code(python_code_string,data)

                    a = backtesting_class(data, bitmask, normal_stop_loss, normal_take_profit, trailing_stop_loss, dynamic_exit_condition, atr_take_loss, atr_take_profit, tnx)
                    results = a.start_backtest()
                        
                    if (results != None) :
                        port = (results[12])
                        dates = (results[13])

                        fig = px.line( x=dates, y=port, title=f'{ticker}')
                        fig.update_yaxes(tickprefix='INR ')

                        fig.update_layout(
                        title={
                            'text': f'{strategy} Strategy Performance on {ticker} ',
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'
                        },

                        xaxis_title="Time Period",
                        yaxis_title="Portfolio Value (INR)",
                        title_font=dict(size=24, color='black', family='Arial'),

                        xaxis=dict(

                            showline=True,
                            showgrid=True,
                            showticklabels=True,
                            linecolor='rgb(204, 204, 204)',
                            linewidth=1,
                            ticks='outside',
                            tickfont=dict(
                                family='Arial',
                                size=12,
                                color='rgb(82, 82, 82)',
                            ),

                        ),

                        yaxis=dict(
                            showgrid=True,
                            zeroline=False,
                            showline=True,
                            showticklabels=True,
                        ),

                        plot_bgcolor='white' )

                        fig.update_traces(mode='lines', line_shape='linear', line=dict(width=2))
                        plot_div = fig.to_html(full_html=False)    
                                

                else:
                    error_message = f"No strategy found with name '{strategy}'"               
                
    else:
        
        form = StrategyForm()



        
    if(results==None):
       context = {
        'first':None,
        'second':None,
        'third':None,
        'four':None,
        'five':None,
        'six':None,
        'seven':None,
        'eight':None,
        'nine':None,
        'ten':None,
        'eleven':None,
        'twelve':None,
        'thirteen':0,
        'graph' : None,

        'form': form,
        'result': result,
        'error_message': error_message,
        'bitmask': bitmask,
        'show_normal_stop_loss': bitmask & (1 << 1) != 0,
        'show_normal_take_profit': bitmask & (1 << 2) != 0,
        'show_trailing_stop_loss': bitmask & (1 << 3) != 0,
        'show_dynamic_exit_condition': bitmask & (1 << 4) != 0,
        'show_atr_take_loss': bitmask & (1 << 5) != 0,
        'show_atr_take_profit': bitmask & (1 << 6) != 0,
        
        } 
    else:
        
        context = {
            'first':results[0],
            'second':results[1],
            'third':results[2],
            'four':results[3],
            'five':results[4],
            'six':results[5],
            'seven':results[6],
            'eight':results[7],
            'nine':results[8],
            'ten':results[9],
            'eleven':results[10],
            'twelve':results[11],
            'thirteen':1,
            'graph' : plot_div,
            'form': form,
            'result': result,
            'error_message': error_message,
            'bitmask': bitmask,
            'show_normal_stop_loss': bitmask & (1 << 1) != 0,
            'show_normal_take_profit': bitmask & (1 << 2) != 0,
            'show_trailing_stop_loss': bitmask & (1 << 3) != 0,
            'show_dynamic_exit_condition': bitmask & (1 << 4) != 0,
            'show_atr_take_loss': bitmask & (1 << 5) != 0,
            'show_atr_take_profit': bitmask & (1 << 6) != 0,
            
        }
    return render(request, 'app1/result.html', context)

@login_required
def contact(request):
    return render(request, 'app1/contact.html')
    
