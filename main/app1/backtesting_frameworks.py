import pandas as pd
import numpy as np
class trader:

  def __init__(self,df):

    self.size=len(df)

    self.ynnormal_stoploss=0
    self.ynnormal_takeprofit=0
    self.yndynamic_exitcondition=0
    self.yntraling_stoploss=0
    self.ynatr_stoploss=0
    self.ynatr_takeprofit=0

    self.normal_stoploss=0
    self.normal_takeprofit=0
    self.dynamic_exitcondition=0
    self.traling_stoploss=0
    self.atr_stoploss=0
    self.atr_takeprofit=0


    self.price=df['Close']
    self.close=df['Close']
    self.high=df['High']
    self.low=df['Low']
    self.open=df['Open']
    self.pfvalue=df['Open']
    self.maxvalue=0
    self.minvalue=0


    self.signals=df['signals']
    self.trade_wise_returns=[]
    self.entry=[]
    self.exit=[]
    self.dip=[]
    self.drawdown=[]
    self.trade_type=[]
    self.dailyreturn=[]
    self.amount=100000
    self.no_ofshare=0
    self.position=0 #Taking not in any position in the start of the trade


    self.calculate_atr(14)


  def calculate_atr(self, period=14):
      # Calculate True Range (TR)
      tr = [max(self.high[i] - self.low[i], abs(self.high[i] - self.close[i - 1]), abs(self.low[i] - self.close[i - 1])) for i in range(1, len(self.close))]

      # Calculate ATR
      atr = [sum(tr[:period]) / period]  # Initial ATR value
      for i in range(period, len(tr)):
          atr.append((atr[-1] * (period - 1) + tr[i]) / period)
      self.atr = atr



  def enter_longtrade(self,i):
    self.entry.append(i)
    self.trade_type.append('1')
    self.position=1
    self.no_ofshare=self.amount//self.price[i]
    self.amount=self.amount%self.price[i]
    self.maxvalue=self.pfvalue[i]
    self.minvalue=self.pfvalue[i]

  def enter_shorttrade(self,i):
    self.entry.append(i)
    self.position=-1
    self.no_ofshare=self.amount//self.price[i]
    self.amount+=self.price[i]*self.no_ofshare
    self.maxvalue=self.pfvalue[i]
    self.minvalue=self.pfvalue[i]


  def exit_longtrade(self,i):
    self.exit.append(i)
    self.position=0
    self.amount+=self.no_ofshare*self.price[i]

  def exit_shorttrade(self,i):
    self.exit.append(i)
    self.position=0
    self.amount-=self.no_ofshare*self.price[i]

  def exittrade(self,i):
    if(self.position==1):
      self.exit_longtrade(i)
    else:
      self.exit_shorttrade(i)

  def checkexitcondition(self,i):

    self.enterindex=self.entry[-1]

    if(self.position==-1 and self.signals[i]==1):
      self.exit_shorttrade(i)
    elif(self.position==1 and self.signals[i]==-1):
      self.exit_longtrade(i)

    if(self.ynnormal_stoploss==1 and self.pfvalue[i]<self.pfvalue[self.enterindex]*(1-self.normal_stoploss)):
      self.exittrade(i)

    elif(self.ynnormal_takeprofit==1 and self.pfvalue[i]>self.pfvalue[self.enterindex]*(1+self.normal_takeprofit)):
      self.exittrade(i)

    elif(((self.ynatr_stoploss==1 and self.position==1 ) or (self.ynatr_takeprofit==1 and self.position==-1)) and self.close[i]<self.close[self.enterindex]-self.atr_stoploss*self.atr[i]):
      self.exittrade(i)

    elif(((self.ynatr_stoploss==1 and self.position==-1 ) or (self.ynatr_takeprofit==1 and self.position==1)) and self.close[i]>self.close[self.enterindex]+self.atr_stoploss*self.atr[i]):
      self.exittrade(i)

    elif(self.yntraling_stoploss==1 and self.pfvalue[i]<self.maxvalue*(1-self.traling_stoploss)):
      self.exittrade(i)

    elif(self.yndynamic_exitcondition==1 and self.pfvalue[i]>self.minvalue*(1+self.dynamic_exitcondition)):
      self.exittrade(i)


  def entercheck(self,i):
    if(self.position==0):
      if(self.signals[i]==1):
        self.enter_longtrade(i)
        return 1
      if(self.signals[i]==-1):
        self.enter_shorttrade(i)
        return 1
    return 0

  def update(self,i):
    if(self.position==1):
      self.pfvalue[i]=self.amount+self.no_ofshare*self.price[i]
    elif(self.position==-1):
      self.pfvalue[i]=self.amount-self.no_ofshare*self.price[i]
    else :
      self.pfvalue[i]=self.amount

    if(self.pfvalue[i]>self.maxvalue):
      self.maxvalue=self.pfvalue[i]

    if(self.pfvalue[i]<self.minvalue):
      self.minvalue=self.pfvalue[i]

    self.dailyreturn.append((self.pfvalue[i]-self.pfvalue[i-1])/self.pfvalue[i-1])





  def compounding(self):
    for i in range(self.size):

      self.update(i)

      if(self.entercheck(i)):
        continue
      self.checkexitcondition(i)

    if self.position!=0:
      self.exittrade(i)

  def calculate_drawdown(self):
    for j in range(len(self.entry)):
      self.dmaxp=0
      self.drawdown.append(0)
      self.dip.append(0)

      for i in range(self.entry[j],self.exit[j]):

        if(self.pfvalue[i]>self.dmaxp):
          self.dmaxp=self.pfvalue[i]

        if(self.drawdown[-1]>(self.dmaxp-self.pfvalue[i])/self.pfvalue[i]):
          self.drawdown[-1]=(self.dmaxp-self.pfvalue[i])/self.pfvalue[i]

        if(self.dip[-1]>(self.pfvalue[self.entry[j]]-self.pfvalue[i])/self.pfvalue[i]):
          self.drawdown[-1]=(self.pfvalue[self.entry[j]]-self.pfvalue[i])/self.pfvalue[i]

  def calculatesharpe(self):
    self.riskfree=np.array(self.dailyreturn)-0.003
    self.sharpe=self.riskfree.mean()*(252**0.5)/self.riskfree.std()


  def backtest(self):
    self.compounding()
    self.holdingtime=(np.array(self.entry)-np.array(self.exit))
    self.maxtime=np.max(self.holdingtime)
    self.meantime=np.mean(self.holdingtime)
    self.gross=(self.amount-100000)
    self.net=self.gross-20*len(self.entry)
    self.calculate_drawdown()
    self.maxdraw=np.max(np.array(self.drawdown))
    self.avgdraw=np.mean(np.array(self.drawdown))
    self.maxdip=np.max(np.array(self.dip))
    self.avgdip=np.mean(np.array(self.dip))
    self.calculatesharpe()
    self.benchmark=(self.price[len(self.price)-1]-self.price[0])*100/self.price[0]
    self.returns=(self.amount-100000)/1000
    self.nooftrades=len(self.entry)

    return self.returns,self.benchmark,self.nooftrades,self.maxtime,self.meantime,self.gross,self.net,self.maxdraw,self.avgdraw,self.maxdip,self.avgdip,self.sharpe
