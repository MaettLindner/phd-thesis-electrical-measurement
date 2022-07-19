# -*- coding: utf-8 -*-
"""
Bibliothek Funktionen zum vermessen mit Kondensatoren:
    - PolyArea zur Flächenbestimmung
    - read_A_Vmax_df Dataframe der Messwerte eines Ordners
    
    
Spyder Befehle:
    - %matplotlib qt/inline (unterscheidet ob Plot in ein extra fenster soll)
"""

from glob import glob
import numpy as np
import math as m
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

#für Text.Box
import ctypes
#für System.exit
import sys


# =============================================================================
# Variablen der Messung
# =============================================================================
frequenz = 1000             # Mess Frequenz
perioden = 4                # Aufgezeichneten Perioden am Oszi
periodeN = frequenz/perioden



# =============================================================================
# Funktion für die Flächenberechnung
# =============================================================================
'''
Achtung Nomrmiert (geteilt duchrch 5cm)!!!
'''
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1))) / 4 # Perioden da auch 4 Umläufe #/0.05       #längen 0.05 pro m Normierung
# =============================================================================
# Funktion ENDE


Path = 'data/Elektroden/glatte_elektrode/*.dat'
# =============================================================================
# Funktion um Messdaten Daten zu ermitteln Vmax Amax Leistung etc.
# =============================================================================
def read_A_Vmax_df(Path):
    path = Path
    dirList = sorted(glob(path))
    dateien = len(dirList)
    
    #sind Dateien im dir
    if dateien == 0:
        ctypes.windll.user32.MessageBoxW(0, "Keine Dateien (.dat) im angegebenen Pfad! \n\nPfad: ---> (" + str(path)+ ") <---", "Achtung", 1)
        sys.exit()
    
    #df initialisieren
    df = pd.DataFrame()
    
    ###############################
    # Werte Einlesen in DataFrame
    for i in range(0,dateien):
        df["V"+str(i)] = np.loadtxt(dirList[i], delimiter=",")[:,1]
        df['C'+str(i)] = np.loadtxt(dirList[i], delimiter=",")[:,2]

    ###############################
    # Werte der Fläche in Array speichern
    A_array=[]
    for i in range(0,dateien):
        A_array.append((PolyArea(df['V'+str(i)], df['C'+str(i)])) *1000) #/4 ist oben bei Polyarea implementiert - Perioden *1000Hz TODO: Maett hat die 1000 Hz weggelassen da bereits vorher über die Frequenz gemittelt wird. 
    
    ###############################
    # Maxima_Werte der Spannung in Array speichern
    Vmax_array=[]
    for i in range(0,dateien):
        Vmax_array.append(np.amax((df['V'+str(i)])/m.sqrt(2)))           #rms = Effektivwert gleich Wurzel2 der positiven Halbwelle!!!
        
    return(A_array,  Vmax_array, df)
# =============================================================================
# Funktion ENDE


# =============================================================================
# Funktion zum smoothen
# =============================================================================
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
# =============================================================================
# Funktion ENDE


# =============================================================================
# Funktion Mittelwert berechnen
# =============================================================================
def df_mean(df, spalte):
    counter = 0 # set counter
    df_mean = pd.DataFrame()
    
    for i in range(0,perioden):
        per = str(counter)
        a = []
        a = df.loc[(counter*250):((counter+1)*250-1), spalte]       # bereich der Spalten ansprechen eine loop
        a.index = range(len(a))
        counter = counter + 1
        a[len(a)-1] = a[0]
        df_mean[per] = a
    
    df_mean['mean'] = df_mean.mean(axis=1)
    df_mean = df_mean.drop(['0', '1', '2', '3'], axis=1)        # überflüssiges läschen
    return(df_mean)
# =============================================================================
# Funktion ENDE



# =============================================================================
# Funktion zum ablesen der Steigungen
# =============================================================================
#Einheit umrechnen
pF = 10 ** 12
nF = 10 ** 9
def tangentensteigung(df, i):#, label, farbe):
    df = df
    i = i
    #id ist die Position der Max Min Werte im Dataframe um die Lissajou ecken zu finden
    idAmax = df['V'+str(i)].idxmax()
    idAmin = df['V'+str(i)].idxmin()
    # print('Amax = ', np.amax((df['V'+str(i)])/m.sqrt(2)))
    # print('idAmax =', df['V'+str(i)].idxmax())
    # print('Amin = ', np.amin((df['V'+str(i)])/m.sqrt(2)))
    # print('idAmin =', df['V'+str(i)].idxmin())

    x_C0_plus = []
    y_C0_plus = []
    x_C0_minus = []
    y_C0_minus = []
    x_Ceff_plus = []
    y_Ceff_plus = []
    x_Ceff_minus = []
    y_Ceff_minus = []
    # =============================================================================
    # Plotten der einzelnen TANGENTEN
    # =============================================================================
    # Einstellbare Variablen:
    for x in range(0,4):
        next = 250*x
        # Tangente C0 plus
        es2 = idAmin%250+next #modulo setzt ein maxima bei 835 in den 1. Bereich 85 bis 100
        es3 = idAmin%250+next+15
        x_C0_plus = np.concatenate((x_C0_plus, (df.loc[es2:es3,'V'+str(i)]).to_numpy()))
        y_C0_plus = np.concatenate((y_C0_plus, (df.loc[es2:es3,'C'+str(i)]).to_numpy()))
        # Tangente C0 minus
        es4 = idAmax%250+next
        es5 = idAmax%250+next+15
        x_C0_minus = np.concatenate((x_C0_minus, (df.loc[es4:es5,'V'+str(i)]).to_numpy()))
        y_C0_minus = np.concatenate((y_C0_minus, (df.loc[es4:es5,'C'+str(i)]).to_numpy()))
        # Tangente Ceff minus
        es6 = idAmin%250+next-20
        es7 = idAmin%250+next
        x_Ceff_minus = np.concatenate((x_Ceff_minus, (df.loc[es6:es7,'V'+str(i)]).to_numpy()))
        y_Ceff_minus = np.concatenate((y_Ceff_minus, (df.loc[es6:es7,'C'+str(i)]).to_numpy()))
        # Tangente Ceff plus
        es8 = idAmax%250+next-20
        es9 = idAmax%250+next
        x_Ceff_plus = np.concatenate((x_Ceff_plus, (df.loc[es8:es9,'V'+str(i)]).to_numpy()))
        y_Ceff_plus = np.concatenate((y_Ceff_plus, (df.loc[es8:es9,'C'+str(i)]).to_numpy()))
        # Show Lissajou
        es11 = 250
        es22= 499
        # plt.plot(df.loc[es11:es22,'V'+str(i)], nF*df.loc[es11:es22,'C'+str(i)], '.',color='black', markersize=0.5)

    #Umrechnen der WERTE hier in nano
    y_C0_plus    =  pF * y_C0_plus    
    y_C0_minus   =  pF * y_C0_minus
    y_Ceff_plus  =  pF * y_Ceff_plus
    y_Ceff_minus =  pF * y_Ceff_minus
    # PUNKTE
    # plt.plot(x_C0_plus,     y_C0_plus, '.',markersize=0.5,color='k', label='C0 plus -'+label+'-')
    # plt.plot(x_C0_minus,    y_C0_minus, '.',markersize=0.5,color='k', label='C0 minus -'+label+'-')
    # plt.plot(x_Ceff_plus,   y_Ceff_plus, '.',markersize=0.5,color='k', label='Ceff plus -'+label+'-')
    # plt.plot(x_Ceff_minus,  y_Ceff_minus, '.',markersize=0.5,color='k', label='Ceff minus-'+label+'-')
    # TANGENTEN
    marker = 1
    slope1, intercept1, r_value, p_value, std_err = stats.linregress(x_C0_plus,y_C0_plus)
    slope2, intercept2, r_value, p_value, std_err = stats.linregress(x_C0_minus,y_C0_minus)
    slope3, intercept3, r_value, p_value, std_err = stats.linregress(x_Ceff_plus,y_Ceff_plus)
    slope4, intercept4, r_value, p_value, std_err = stats.linregress(x_Ceff_minus,y_Ceff_minus)
    # plt.plot(x_C0_plus,       intercept1 + slope1*x_C0_plus,    markersize=marker, color=farbe, label='fitted C0 plus')
    # plt.plot(x_C0_minus,      intercept2 + slope2*x_C0_minus,   markersize=marker, color=farbe, label='fitted C0 minus')
    # plt.plot(x_Ceff_plus,     intercept3 + slope3*x_Ceff_plus,  markersize=marker, color=farbe, label='fitted Ceff plus')
    # plt.plot(x_Ceff_minus,    intercept4 + slope4*x_Ceff_minus, markersize=marker, color=farbe, label='fitted Ceff minus')
    # print('\n -'+label+'-')
    # print(' C0p = ', slope1, '\n C0m = ' , slope2, '\n Ceffp = ', slope3, '\n Ceffm = ', slope4)
    return (slope1, slope2, slope3, slope4)
# =============================================================================
# Funktion ENDE



# =============================================================================
# einzellne Werte anpassen Verwendungen etc.
# =============================================================================
''' zu Series '''
#s= pd.Series(my_list)
#s=s*5
#oder
#(s*5).tolist())
    
#df_perioden3 = pd.DataFrame()
    

''' zu Dataframes '''
#df_perioden1['Vp1'] = df.loc[0:249, 'V20']                  # DF_Perioden 1. Colum
#df_perioden['Vp1'] = df.loc[0:249, 'V20']                  # DF_Perioden 1. Colum
#
#df_perioden2['Vp2'] = df.loc[250:499, 'V20']                # 2. Colum
#df_perioden2 = df_perioden2.reset_index(drop=True)          # Colum Index reset
#df_perioden['Vp2'] = df_perioden2                           # zu DF_Perioden Hinzufügen
##df_perioden.join(df_perioden2, ignore_index = True)
  


