"""
Anzeige Programm:
    - Einzellne Lissajou Figuren Plotten
    
Ein/Aus - Kommentieren: STRG + 1
"""
#import os

import matplotlib.pyplot as plt
import Lissajou_module
import pandas as pd
import numpy as np
#import os

#ordner=os.getcwd()
#os.chdir('..')                                  #in dir eins höher wechseln

# =============================================================================
# Werte der Messungen einlesen: Fläche, Vmax, df (alle werte)
# =============================================================================

#Single measurement
Title = "ZIR - mulitiple plots"
# i = 14
#Multi-measurement
#Title = "FR4"
sample = "FR4_1"

Wafer_1 = Title
A1, Vmax1, df_1 = Lissajou_module.read_A_Vmax_df('Plasma/'+sample+'/*.dat')

# Wafer_2 = Title+'45V'
# A2, Vmax2, df_2 = Lissajou_module.read_A_Vmax_df('Plasma/FR4_1/*.dat')

# Wafer_3 = Title+'120V'
# A3, Vmax3, df_3 = Lissajou_module.read_A_Vmax_df('Plasma/FR4_1/*.dat')


def Anorm(array):
    #material = 0.973384 # scaling with spikes / form factor 
    material = 0.696 # scaled to flat electrode 
    arraynorm = [x/material for x in array
    return arraynorm


###############################
# Plot Eigenschaften
# plt.figure()                  # um extra fenster zu erzeugen
#plt.fill(b,c, alpha=0.2)
#plt.plot(df[], df[], '-',markersize=1, label='lower voltage')
#plt.fill(d, e, alpha=0.2)

plt.legend()
plt.xlabel('operation voltage [V]')
plt.ylabel(' red. charge Q [C/m]')
#plt.legend(loc='lower left')


# =============================================================================
# Plotten der einzelnen Lissajou
# =============================================================================

# Einstellen der Spannung über Parameter i - Count from Zero 
df=df_1
# i = 14
# plt.plot(df['V'+str(i)], df['C'+str(i)], 'o',markersize=1,color='red', label=Wafer_1)

# df=df_2
# i = 9
# plt.plot(df['V'+str(i)], df['C'+str(i)], 'o',markersize=1,color='orange', label=Wafer_1)

# df=df_3
# i = 24
# plt.plot(df['V'+str(i)], df['C'+str(i)], 'o',markersize=1,color='blue', label=Wafer_1)

# df=df_4
# i = 4
# plt.plot(df['V'+str(i)], df['C'+str(i)], '-',markersize=1, label=Wafer_4)

# for j in range(0,12):
#     voltage = j*5
#     plt.plot(df['V'+str(j)], Anorm(df['C'+str(j)]), '-',markersize=1, label=voltage)


# ###############################
# # Plot Eigenschaften
# plt.legend(loc='best')
# plt.title(Title)#, fontsize=12, fontweight='bold')
# # erste Liste: Tick-Positionen, zweite Liste: Tick-Beschriftung
# # plt.show()
# plt.grid()   




################################
# Speichern

#tests='C:/Users/sit34954/Desktop/AKTUELLE_PROGRAMME/Python_Lissajou_Condensator/Python_Lissajou_Condensator/saves/Mattdergroße.pdf'
# savestring='Plots/'+Title+'.pdf'
# plt.savefig(savestring)

# Data export

#plt.plot(df['V'+str(i)], df['C'+str(i)], 'o',markersize=1,color='red', label=Wafer_1)

def export():           
    exportname                   = "QV_Zir_380_1_"
    max_data = 25                # set max data - for ZIR mit 70V max i = 14 = 5 * 14    
    for i in range(0,max_data):             
        naming =    i*5                     
        #naming =    -i*5-5              #for down - calculate graph naming
        df2 = pd.DataFrame(data={"Voltage" : df['V'+str(i)], "Capacity" : Anorm(df['C'+str(i)]) })
        df2.to_csv('QV_scaled_to_flat/'+ exportname + str(naming) +'V_up.csv', sep=',', index=False)
# export() 

def export_voltage_shift(): 
    exportname                   = "QV_" + sample + "_" 
    max_data = 23                # set max data - for ZIR mit 70V max i = 14 = 5 * 14    
    for i in range(0,max_data):      
        #naming =    i*5         
        naming =    -i*5-5              #for down - calculate graph naming 
        df3 = pd.DataFrame(data={"Voltage" : df['V'+str(i)] + np.absolute(np.amin(df['V'+str(i)])) , "Capacity" : Anorm(df['C'+str(i)]) + np.absolute(np.amin(Anorm(df['C'+str(i)])))  })
        df3.to_csv('QV_scaled_to_flat_shifted/'+ exportname + str(naming) +'V_shifted_down.csv', sep=',', index=False)
#export_voltage_shift()    


def export_QV_max():
    max_data = 25  # 25 for FR4 and Glass 
    df4 = pd.DataFrame()
    max_v = []
    max_c = []
    chroma = []
    
    for i in range(0,max_data):
        naming =    i*5         
        #naming =    -i*5-5              #for down - calculate graph naming 
        
        max_v.append(np.amax(df['V'+str(i)] + np.absolute(np.amin(df['V'+str(i)])))) 
        max_c.append( np.amax(Anorm(df['C'+str(i)]) + np.absolute(np.amin(Anorm(df['C'+str(i)])))) )
        chroma.append(naming)
        
    df4 = pd.DataFrame(data={ "Max Voltage" : max_v , "Capacity" : max_c, "Chroma Voltage" : chroma     })
        #df4.append("Max Voltage" : max_v , "Capacity" : max_c  })
    df4.to_csv('QV_max_shifted/'+ sample + "_" + str(naming) +'V_up.csv', sep=',', index=False)
#export_QV_max()
        
# i=0
# df = pd.DataFrame(data={"Voltage":df['V'+str(i)], "Capacity":df['C'+str(i)]})
# df.to_csv('QV_data_export/'+'0V_up.csv', sep=',', index=False)
