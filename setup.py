"""
Created on Tue Nov 27 14:28:07 2018

@author: assaf
"""
#Libreriapara I²C con arduino 
import time
#import smbus

#Libraria para la FFT
import numpy as np
import scipy.fftpack as fourier
import matplotlib.pyplot as plt

# Import the ADS1x15 module.
from ADS1x15 import ADS1115,ADS1015

# Create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

adc = ADS1015(address=0x48, busnum=1)
GAIN = 1

#Configuracion bus I2C
#bus = smbus.SMBUS(1)
#address=0x04


def VelocidadMotor(val):
    bus.write_byte(address, val)
    #bus.write_byte_data(address, 0, val)
    return -1

# Definicion de la funcion de Entrada 
def senal(t,fs):
    #x=np.cos(2*np.pi*fs*t)
    x=np.sin(2*np.pi*fs*t)
    return(x)
  
 
print('Leamos ADS1x15 valores, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| xyz = {0:>6} |'.format(*range(1)))
print('---------------------------Las datos del acelerometro------------------------')

# Main loop.
while True:
    
    #data = raw_input("Entrega un numero entre 0-9")
   # data_list = list(data)
    #for i in data_list:
        #if i is [0:9]:
    
    
    # Read all the ADC channel values in a list.
    values = [0]*1
    j=0
    while j<1024:
        for i in range(1):
        # Lee el canal del ADC con el especifico gain.
            values[i] = adc.read_adc(i, gain=GAIN)
    # Print the ADC values.
            print('| xyz= {0:>6} mg |'.format(*values))
            j=j+1
    print('----------------------------------')        
    #Creacion del archivo datos.txt
    mi_archivo = open('datos.txt','a');
    mi_archivo.close();
    
    #Escritura en el archivo
    mi_archivo = open('datos.txt','a');
    mi_archivo.write('--| xyz= {0:>6} mg |--'.format(*values));
    mi_archivo.write('\n');
    mi_archivo.close();
   
    # Pausa                 
    time.sleep(0.5)

# Administracion del tiempo 
    t0=0
    tn=15 # [0,tn]
    n= 1024 # Para calcular el paso  
    dt=(tn-t0)/n    # el paso de quantificacion 
    t=np.arange(-tn,tn,dt)  # discretizacion del tiempo


# Inicializacion del senal 
    m=len(t) # Para construir la senal 
    xanalog=np.zeros(m, dtype=float) # Tabla de tamano 'm'

#Procesiamiento del senal 
    for i in range(0,m):
        for item in values:
            xanalog[i]=senal(t[i],item)
        #print(item)
        
# FFT: Transformada Rapida de Fourier

    xf=fourier.fft(xanalog) # FFT de la funcion xanalog
    xf=fourier.fftshift(xf) # centramos los valores 
# Rango de frecuencia para eje
    frq=fourier.fftfreq(n, dt)
    frq=fourier.fftshift(frq) # Centramos los valores

# x[w] real
    xfreal=(1/n)*np.real(xf)

        

    plt.figure(1)       # define el grafico
    plt.suptitle('Transformada Fourier Discreta FFT')

#Primero sub-grafico 
    plt.subplot(431)    # grafica de 4x1, subgrafica 1
    plt.ylabel('xanalog[t]')
    plt.xlabel('tiempo')
    plt.plot(t,xanalog)
    plt.axis([-0.5,0.5,-2,2])
    plt.grid()        

    ventana=0.5 # ventana de frecuencia a observar alrededor f=0
    ra=int(len(frq)*(0.5-ventana))
    rb=int(len(frq)*(0.5+ventana))

#Segundo sub-grafico 
    plt.subplot(433)    # grafica de 4x3, subgrafica 6
    plt.ylabel('x[f] real')
    plt.xlabel(' frecuencia (Hz)')
    plt.plot(frq[ra:rb],xfreal[ra:rb])
    plt.grid()
    plt.show()
    #print(xfreal)
    #print(frq)
    #fmax1=max(xfreal,frq)
   # fmax2=max(xfreal[int(rb/2):rb])
    #f=fmax2-fmax1
    #print(fmax1)#+','+fmax2+'-->freq:'+f)