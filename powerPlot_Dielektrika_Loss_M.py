# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 16:09:52 2019

@author: sit34954
"""
"""
Messdaten lesen
Daten Plotten
Fläche berechnen

Ein/Aus - Kommentieren: STRG + 
"""
#import os
import matplotlib.pyplot as plt
import Lissajou_module
import pandas as pd
import math as m
import numpy as np
from operator import truediv 
from math import pi

# =============================================================================
# Plot einstellungen größe 20 bzw 11
# =============================================================================
plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
params = {'text.usetex' : True,
          'font.size' : 11,
          'font.family' : 'lmodern',
          'text.latex.unicode': True,
          }
plt.rcParams.update(params)
textwidth = 5.927657638888889  # achtung pt to inch 426.79135 latex textwidth
fig = plt.figure()
# fig.set_size_inches(textwidth, 0.6*textwidth)
# plt.xlim(0,9000)
# plt.ylim(1.9,11)
# =============================================================================

# Plotten der einzelnen Wafer mit ErrorBar
# =============================================================================
# ErrorBar bestimmen
# =============================================================================
def calcError(array):
    array2 = [i * 0.07 for i in array]
    return array2

#berechnete Kondensator Flächen der Wafer -
# Maett hat auf die neue Größe angepasst.
glasqm = 0.0016625
fr4qm = 0.0016625
zirkqm = 0.0016625
# =============================================================================
# Leistung auf Fläche Normieren
# =============================================================================
def Anorm(array):
    #material = 0.973384  # scaled with spikes - form factor
    normfac = 0.05 # scaled to electrode length 
    arraynorm = [x/normfac for x in array]
    return arraynorm
# =============================================================================
#Funktion um Daten in csv
# =============================================================================
def csv_schreiben(werte, speicherort):
    df = pd.DataFrame(data={"Vmax":Vmax})
    df.to_csv(speicherort, sep=',', index=False)


# Single - Export with V_rms and scaled Electrode
# export_Pathname ='FR4_1' 

# Ax, Vmaxx, df_x = Lissajou_module.read_A_Vmax_df('Plasma/'+ export_Pathname + '/*.dat')
# #Ax = Anorm(Ax, 0.973384) # old a Anorm
# Ax = Anorm(Ax)
# yerr = calcError(Ax)
# df = pd.DataFrame(data={"Vmax":Vmaxx, "A":Ax, "yerr":yerr})
# df.to_csv('CSV/Power_VPP_export/'+ export_Pathname +'_Vrms_compare.csv', sep=',', index=False)

# Export of Vpp with scaled electrode - to apply Andrei's formula 
def Vpp_export(): 
    export_Pathname = 'AL2O3_4_Layer_3_Cycle'  
    Ax, Vmaxx, df_x = Lissajou_module.read_A_Vmax_df('3 Cycle/down/*.dat') 
    V_pp = [x * m.sqrt(2) * 2 for x in Vmaxx] 
    #V_pp = Vmaxx * m.sqrt(2) * 2 
    Ax = Anorm(Ax) # scale to length 
    yerr = calcError(Ax) 
    df = pd.DataFrame(data={"V_pp":V_pp, "A":Ax, "yerr":yerr})
    df.to_csv('export/'+ export_Pathname +'_VPP_down.csv', sep=',', index=False) 
Vpp_export() 

def Vrms_export(): 
    export_Pathname = 'AL2O3_4_Layer_3_Cycle' 
    Ax, Vrms, df_x = Lissajou_module.read_A_Vmax_df('3 Cycle/down/*.dat') 
    #V_rms = [x for x in Vmaxx] 
    #V_pp = Vmaxx * m.sqrt(2) * 2  
    Ax = Anorm(Ax) # scale to length  
    yerr = calcError(Ax) 
    df = pd.DataFrame(data={"V_rms":Vrms, "A":Ax, "yerr":yerr}) 
    df.to_csv('export/'+ export_Pathname +'_vrms_down.csv', sep=',', index=False) 
Vrms_export() 


# =============================================================================
# Plasma
# =============================================================================


#Rationplot nicht möglich da verschiedene Spannungen 
# def pl_ratio(plasma_data, loss_data):
#     res = list(map(truediv, plasma_data, loss_data)) 
#     print(res)



###############################
# Plot Eigenschaften
# plt.figure()                  # um extra fenster zu erzeugen
# plt.xlabel('Glasdurchmesser D [mu]')
# plt.xlabel('operating voltage rms V [V]')
#plt.ylabel('capacitor charge Q [C]')
# plt.ylabel('Tangenten in [pF]')
#plt.legend(loc='lower left')
plt.xlabel('voltage $V_{pp}$ [V]')
plt.ylabel('red. Power P [W/m]')


# Plotten der einzelnen Wafer mit ErrorBar
###############################




'''
# =============================================================================
#Funktion um Daten in csv
# =============================================================================
def csv_schreiben(Vmax, A, speicherort):
        df = pd.DataFrame(data={"x1":Vmax, "y1":A, "yerr1":calcError(A)})
        df.to_csv(speicherort, sep=',', index=False)

#for i in range(1,9):
#print (vars()['A'+str(i)])
  
################################
# Daten in csv speichern DATEN
speicherort='csv/Keramik_dicken.csv'
for i in range(1,10):
    csv_schreiben(vars()['Vmax'+str(i)], vars()['A'+str(i)], 'csv/Keramik_dicke'+str(500*i)+'mu.csv')

'''