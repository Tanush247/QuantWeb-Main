from django.shortcuts import render
from .models import CommonModel
from .forms import StrategyForm
import yfinance as yf
from .backtesting_frameworks import backtest_1,parameters
from django.contrib.auth.decorators import login_required



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
def csv(request):
    
    return render(request,'app1/hello.html')
@login_required
def backtesting(request):
    user = request.user
    result = None
    error_message = None
    results=None
    if request.method == "POST":
        form = StrategyForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            strategy = form.cleaned_data['strategy']
            end_date = form.cleaned_data['end_date']
            start_date = form.cleaned_data['start_date']
            stop_loss=form.cleaned_data['stop_loss']
            stop_loss=float(stop_loss)
            data = yf.download(ticker, start_date, end_date)
            tnx=yf.download('^TNX',start_date,end_date)
            # Query CommonModel based on the strategy name
            object1 = CommonModel.objects.filter(name=strategy).first()
            if object1:
                python_code_string = object1.source
                
                # Example arguments for the function call
                
                # Execute the Python code (assuming 'hello' function exists)
                data, error_message = execute_python_code(python_code_string,data)
                a,capital=backtest_1(data,stop_loss)
                results=parameters(data,a,tnx)
                
                

            else:
                error_message = f"No strategy found with name '{strategy}'"
    else:
        form = StrategyForm()
    if(results==None):
       context = {
        'first':None,
        'second':None,
        'third':None,
        'fourth':None,
        'five':None,
        'six':None,
        'seven':None,
        'eight':None,
        'nine':None,
        'ten':None,
        'eleven':None,
        'twelve':None,
        'form': form,
        'result': result,
        'error_message': error_message,
        } 
    else:

        context = {
            'first':results[0],
            'second':results[1],
            'third':results[2],
            'fourth':results[3],
            'five':results[4],
            'six':results[5],
            'seven':results[6],
            'eight':results[7],
            'nine':results[8],
            'ten':results[9],
            'eleven':results[10],
            'twelve':results[11],
            'form': form,
            'result': result,
            'error_message': error_message,
        }
    return render(request, 'app1/result.html', context)


