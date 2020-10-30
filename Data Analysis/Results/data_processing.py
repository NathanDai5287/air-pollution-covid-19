# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 13:53:00 2020

@author: ldai
"""

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr

df = pd.read_csv('final_data.csv')
df['Confirmed (Log)'] = np.log10(df['Confirmed'])
df['New Cases (Log)'] = np.where(df['New Cases']==0, np.NaN, np.log10(df['New Cases']))
df['New Cases (%)'] = np.where(df['New Cases']==0, np.NaN, np.log(df['New Cases'] / df['Confirmed']))

Y = df['New Cases']
df.rename(columns={'PM2.5': 'PM2.5 (ug/m3)', 'O3': 'O3 (ppb)', 'SO2': 'SO2 (ppm)', 'NO2': 'NO2 (ppb)', 'PM10': 'PM10 (ug/m3)',
                   'CO': 'CO (ppm)', 'tempC': 'temperature (C)', 'humidity': 'RH (%)', 'windspeedKmph': 'windspeed (km/h)', 
                   'pressure': 'pressure (mBar)', 'Confirmed': 'Confirmed Cases'}, inplace=True)
independent = [['PM2.5 (ug/m3)', 'O3 (ppb)', 'SO2 (ppm)', 'NO2 (ppb)', 'PM10 (ug/m3)', 'CO (ppm)', 'temperature (C)', 'RH (%)', 
                'windspeed (km/h)', 'pressure (mBar)', 'uvIndex', 'Confirmed Cases'],
               ['PM2.5 (ug/m3)', 'SO2 (ppm)', 'temperature (C)', 'RH (%)', 'pressure (mBar)', 'Confirmed Cases']]
for index, col in enumerate(independent):
    X = df[col]
    X = sm.add_constant(X)
    model = sm.OLS(Y, X, missing='drop')
    results = model.fit()
    print(results.summary())
    if index == 0:
        correlation_matrix = df[col].corr()
        correlation_matrix = correlation_matrix.where(np.tril(np.ones(correlation_matrix.shape)).astype(np.bool))
        correlation_matrix.fillna('', inplace=True)
        with pd.option_context('display.float_format', lambda x: f'{x:.4f}', 'max_columns', 12):
            print(correlation_matrix)
        for (col1, col2) in [('CO (ppm)', 'NO2 (ppb)'), ('PM10 (ug/m3)', 'O3 (ppb)'), ('temperature (C)', 'uvIndex')]:
            _, p = spearmanr(df[col1], df[col2], nan_policy='omit')
            print(f'p-value of correlation between {col1} and {col2}: {p:.4e}')
    else:
        figure, axes = plt.subplots(2, 3)
        figure.suptitle('Partial Residual Plots')
        for index, variable in enumerate(col):
            ax = axes[int(index/3)][index % 3]
            fig = sm.graphics.plot_ccpr(results, variable, ax)
            ax.set_title('')
            ax.set_ylabel(f'Partial Residual of {variable}')

plt.show()