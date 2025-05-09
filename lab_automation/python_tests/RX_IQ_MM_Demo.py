# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 09:52:30 2017

@author: jdennis

Removed anything proprietary - this is more of a skeleton of some coding to use for dicussion
"""


import visa  
import time
import numpy
def median(lst):
    return numpy.median(numpy.array(lst))
import os

import sys
part ='xyz'

chain=1 # input('chain?) --alternate way
chx='ch'=str(chain)
#SETUP Ch1 oscope on I.  Meas Phase 1-2.  2nd spot pk to pk on 2.  3rd spot pk to pk on 1.

if chain==1 or chain ==3 or chain==6 or chain==8:    
    sys.path.insert(0, 'C:/Users/jdennis/Desktop/SVNRepository/')
    import RFIC_Driver
    rfic = RFIC_Driver.Digital(True, False,'C:/Users/jdennis/Desktop/SVNRepository/PLL_freq_6G.csv' )
    path_svn = 'C:/Users/jdennis/Desktop/SVNRepository/'
    

if chain==2 or chain ==4 or chain==5 or chain==7:    
    sys.path.insert(0, 'C:/Users/jdennis/Desktop/SVNRepository/')
    import RFIC_Driver
    rfic = RFIC_Driver.Digital(True, False,'C:/Users/jdennis/Desktop/SVNRepository/PLL_freq_3G.csv' )
    path_svn = 'C:/Users/jdennis/Desktop/SVNRepository/' 
    
    
from RegMap_Tools import Read_SPI_Seq
#    import PHX_Driver
#    rfic1 = PHX_Driver.Digital(True, False,'C:\RFIC10.C0_depot/gui/RFIC10_SPI_Loader/RFIC10_code_loader_C0.csv','C:\RFIC10.C0_depot/gui/RFIC10_SPI_Loader/RFIC10_PLL_freq_settings_C0.csv'  )
   
    

        

save_data = 0
if save_data == 0:
    path = os.getcwd()
    path1 = 'C:\data'
    filetime = time.strftime("_%Y_%H_%M_%S", time.localtime()) 
    fname = 'RX_IQMM'
    fext = '.csv'
    fpath = path1 + '/' + fname + filetime + fext
    print fpath
    data=open(fpath, 'a')
    data.write('var,chx,tone2,sumQ,sqrtQ,sumI,sqrtI,sumIQ,cross_corr,phase,Amp_log,Ipower,Qpower') 
    data.close()
    temp=85 




#rfic.Set_PLL_Freq('160MHz', lo, True, False)

import socket
z=socket.gethostname()
print z
        

        
if z == 'az-lab-1':
    oscope = visa.instrument('TCPIP::10.0.76.16::INSTR') #121
    sg = visa.instrument('TCPIP::10.0.76.15::INSTR') #111


oscope.write('WAVeform:FORMat ASCii') # SETUP
oscope.write('WAVeform:POINts 2001')#setupp




if chain==1 or chain ==3 or chain==6 or chain==8:        
#    freqrange=[5150,6025,7080]
    freqrange=[]
    for loop in range(466):
        freq=4800+5*loop
        freqrange.append(freq)
if chain==2 or chain ==4 or chain==5 or chain==7:        
#    freqrange=[5150,6025,7080]
    freqrange=[]
    for loop in range(441):
        freq=3000+5*loop
        freqrange.append(freq)
#print freqrange, type(freqrange)
      
##varuabkes ###
genx=1000000

for freq_sweep in freqrange:  
    
 

    fc=freq_sweep
    
   
    if chain==1:
        rfic.Set_PLL_Freq('44.8MHz_2xfout', fc, False, False) #4x4
        
     
       
        
    if chain==2:
        fc_val='44.8MHz_3xfout'
        if fc<=3599:
            fc_val='44.8MHz_4xfout'
        if fc>=4799:
            fc_val='44.8MHz_2xfout'
        rfic.Set_tgen_Freq(fc_val, fc, False, False)
        
      
     

            
    for bwloop in range(1):
        
        bwloop=0
        
    
        if bwloop == 0:
            bw = 80
            bws='80MHz'
            bw_range = 11
            bw_loop_div=1
    
        sg.write('OUTPut:STATe ON')
        

        for sg_loop in range (bw_range):
            
            for sg_loop1 in range (2):
                tone=1*genx+4*sg_loop*genx
                
                    

                  
                    
                oscopef=2.8/tone
                oscope.write('TIMEBASE:SCALE %.10f' %oscopef)  
                time.sleep(.5)
                oscope.write('RUN')
                oscope.write('ACQuire:TYPE NORM')
#              
                    
                if sg_loop1==0:
                    gen_freq= fc*genx + tone
                if sg_loop1==1:
                    gen_freq=fc*genx - tone
                    
                  
                sg.write('FREQuency:FIXed %1f' %gen_freq)
                
                
                if sg_loop==0:
                    
                    if sg_loop1==0:
                        
                        gg=-30
                        sg.write('POWer:AMPLitude %1f' %gg)
                        time.sleep(1)
                        tttt= oscope.ask('MEASure:VPP? CHANNEL1')
                        t1=float(tttt)
                        
                        count=0
                        if t1<=.75:
                            while t1<=.75:
                               
                                if t1<=.75:
                                    count=count+1
                                gg1=gg+1*count
                                sg.write('POWer:AMPLitude %1f' %gg1)
                                tttt= oscope.ask('MEASure:VPP? CHANNEL1')
                                
                                t1=float(tttt)
                                if count>=7:
                                    break
                        
                        
                        if t1>=.75:
                            while t1>=.75:
                               
                                if t1>=.75:
                                    count=count+1
                                gg1=gg-1*count
                                sg.write('POWer:AMPLitude %1f' %gg1)
                                tttt= oscope.ask('MEASure:VPP? CHANNEL1')
                                t1=float(tttt)
                                
                                if count>=30:
                                    break
#                        print t1,gg1
    #                    time.sleep(.1)
                
                oscope.write(':ACQuire:TYPE AVERage')
                oscope.write(':ACQuire:COMPlete 100')
                oscope.write('ACQuire:COUNt 20')
                time.sleep(.60)
                 
                oscope.write('DIGitize CHANnel1,CHANnel2')
                
                oscope.write('WAVeform:SOURce CHANnel1')
                Qp=oscope.ask('WAVeform:DATA?')
                
                oscope.write('WAVeform:SOURce CHANnel2')
                Ip=oscope.ask('WAVeform:DATA?')
                
                
                result = [x.strip() for x in Qp.split(',')] # Converts string into a list of strings -  have to strip first number or ignaore
                result.pop(0) # removed first value 'result.pop(0)'
                resultQ = list(map(float, result))
                multQ=numpy.multiply(resultQ,resultQ)
                sumQ=numpy.sum(multQ)
                sqrtQ=numpy.sqrt(sumQ)
                
                result2 = [x.strip() for x in Ip.split(',')] # Converts string into a list of strings -  have to strip first number or ignaore
                result2.pop(0) # removed first value 'result.pop(0)'
                resultI = list(map(float, result2))
                multI=numpy.multiply(resultI,resultI)
                sumI=numpy.sum(multI)
                sqrtI=numpy.sqrt(sumI)
                
                multIQ=numpy.multiply(resultI,resultQ)
                sumIQ=sum(multIQ)
                
                cross_corr=sumIQ/(sqrtI*sqrtQ)
                
                
                phase=numpy.arcsin(cross_corr)*180/numpy.pi
                
                
                cc=numpy.log10(sqrtQ/sqrtI)
                gm_log = 20*cc
                
                powQ=numpy.log10(sumQ/2000)*10
                powI=numpy.log10(sumI/2000)*10
                
                
                
                
              
             
                
                
                
                
                tone1=gen_freq/1000000-fc
                
                tone2=tone/1000000
                if sg_loop1==1:
                    tone2=-1*tone/1000000
                    
                print fc,tone2,sumQ,sqrtQ,sumI,sqrtI,sumIQ,cross_corr,phase,gm_log,powI,powQ
                
                gain_setting = 30#add featre
                if save_data == 0:
                    data=open(fpath, 'a')
                    #data.write('%.2f\n' % (cl))
                    data.write('\n %s,%s,%i,%i,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f' % \
                    (part,chx,fc,tone2,sumQ,sqrtQ,sumI,sqrtI,sumIQ,cross_corr,phase,gm_log,powI,powQ))
                    data.close()
                

                
                
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    