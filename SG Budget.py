# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 15:54:43 2021

@author: Eugene
"""

import numpy as np
import pandas as pd

# Import government expenditure data downloaded from Data.gov.sg

df = pd.read_csv('government-total-expenditure.csv')
df2 = pd.read_csv('government-fiscal-position.csv')
df_fp_rev =df2[df2['actual_revised_estimated'] == 'Actual'][df2['category']=='Revenue'][['year_of_balance','item','amount']]
df_fp_exp =df2[df2['actual_revised_estimated'] == 'Actual'][df2['category']=='Expenditure'][['year_of_balance','item','amount']]

df_budget =df[df['actual_revised_estimated'] == 'Actual'][['financial_year','ministry','amount']].groupby(['financial_year','ministry']).sum().reset_index()
df_temp = df2[(df2['actual_revised_estimated'] == 'Actual') & (df2['item'] == 'Special Transfers Excluding Top-ups to Endowment and Trust Funds')][['year_of_balance','item','amount']]
df_temp.columns = ['financial_year','ministry','amount']
df_budget = df_budget.append(df_temp)
df_budget = df_budget.dropna()
df_budget.columns = ['Financial Year','Ministry','Amount (in SGD Million)']
df_budget['Ministry'] = df_budget['Ministry'].replace('Special Transfers Excluding Top-ups to Endowment and Trust Funds','Special Transfers')
list_of_min = df_budget['Ministry'].unique()

df_by_min = {}

# Sum expenditure for each year for each ministry

for i in list_of_min:
    temp = df_budget[df_budget['Ministry'] == i].groupby('Financial Year').sum().reset_index()
    df_by_min[i] = temp
    
df_byyear = df_budget.groupby('Financial Year').sum().reset_index()

# Create static plots of the expenditure

import matplotlib.pyplot as plt

for key in df_by_min.keys():
    temp = df_by_min[key]
    plt.bar(temp['Financial Year'],temp['Amount (in SGD Million)'])
    plt.draw()
    
labels = list(df_by_min.keys())
plt.legend(labels, bbox_to_anchor = [1,1], loc = 'upper left')

years = df_byyear['Financial Year']

df_min_by_year = pd.DataFrame(years)

for key in df_by_min.keys():
    df_min_by_year[key] = df_by_min[key]['Amount (in SGD Million)']
   
# Use plotly to create animated plots

# Of expenditure by ministry over time

import plotly.express as px
from plotly.offline import plot

x_range = df_budget['Financial Year'].unique()

fig_bar = px.bar(df_budget, x = 'Amount (in SGD Million)', y = 'Ministry', color = 'Ministry', animation_frame = 'Financial Year', animation_group = 'Ministry', range_x = [0,15000])
fig_bar.update_layout(yaxis={'categoryorder':'max ascending'}, font_size = 20)
fig_bar.update_xaxes(ticks = "outside")
fig_bar.update_yaxes(ticks = "outside")
plot(fig_bar)

# Of expenditure vs revenue for each year

df_rev_exp = df2[(df2['actual_revised_estimated'] == 'Actual') & (df2['category'] != 'Balance')]

import plotly.express as px
from plotly.offline import plot

fig_bar2 = px.bar(df_rev_exp, x = 'category', y = 'amount', color = 'item', animation_frame = 'year_of_balance', animation_group = 'item', range_x = ['Revenue','Expenditure'], range_y = [0,100000])
fig_bar2.update_layout(yaxis={'categoryorder':'max ascending'}, font_size = 20)
fig_bar2.update_xaxes(ticks = "outside")
fig_bar2.update_yaxes(ticks = "outside")
plot(fig_bar2)
