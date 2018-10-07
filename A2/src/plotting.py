# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 11:13:31 2018

@author: Ozan Gokdemir
"""
import plotly as py
import pandas as pd


df = df = pd.read_csv("C:\\Users\\Ozan Gokdemir\\Desktop\\ozan_rain_tom\\A2\\data\\dataset.csv")

print(df.iloc[4])

rawData ={
    'data': [
  		{
  			'x': df.Distance, 
        	'y': df.Speeding, 
        	'text': df.Distance, 
        	'mode': 'markers', 
        	'name': 'Ozan'} 
    ],
    'layout': {
        'xaxis': {'title': 'Distance'},
        'yaxis': {'title': "Speeding"}
    }
}


def plotFig(fig):
    py.offline.plot(fig)


plotFig(rawData)



