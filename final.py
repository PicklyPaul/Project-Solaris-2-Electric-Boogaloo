#imports and login
import earthaccess as ea
import datetime as dt
import pandas as pd
import os
import h5py
import sys
#put into earthaccess info here if you wish to stop repeating login
#os.environ['EARTHDATA_USERNAME'] = ''
#os.environ['EARTHDATA_PASSWORD'] = ''

ea.login()
#"GLDAS_NOAH10_M"
print("begin")
#downloads the files from 2001 to 2025
#will be changed, just to speed up development
#sn = short name, v = version, m = month of analysis
def downloader(sn, v, m):
    i = 2001
    for i in range(2001,2025):
        #print("looping through"+str(i))
        results = ea.search_data(
            short_name = sn ,
            version = v,
            temporal = (
                    dt.datetime(i,int(m),2),
                    dt.datetime(i,int(m),3)
                    ),
        )
        #print("starting download for"+str(i))
        ea.download(results, local_path="data")
        i+=1

#'Tair_f_inst'
#mote these are for x.5 and y.5
def lister(var, y, x,m):
    i = 2001
    lists = []
    for i in range(2001,2025):
        #this file name is scuffed, work to make it so it's just shortname
        file = h5py.File("data/GLDAS_NOAH10_M.A"+str(i)+str(m)+".021.nc4")
        data = file[var][0, :, :]
        #so the data is flipped south up north down, starts at 59.5 degrees south(rest is antartica)
        #also missing values, need to clean up
        df = pd.DataFrame(data)
        lists.append(float(df.iloc[(x+60),(y+179)]))
        #idk what youre going to do here good luck
        file.close()
        del df
        i+=1
    return lists

#average of the list
def trender(list, years):
    #chl = the list of the change between years, rl = rate of change betwween the change(chl)
    chl = []
    rl = []
    for i in range(len(list)-1):
        ch = list[i+1]-list[i]
        chl.append(ch)
    for j in range(len(chl)-1):
        r = chl[j+1]-chl[j]
        rl.append(r)

    avgr = sum(rl)/len(rl)
    avgc = sum(chl)/len(chl)
    boo = (len(list))
    boop = int(boo + years)
    z = list[int(boo-1)]       
    for k in range(boop):
        inc = avgc*(avgr*k)
        z+= inc
    return z
      
def compute(m,y,x,p):
    print(m)
    yz = round(y+0.5)
    xz = round(x+0.5)
    az = []
    downloader("GLDAS_NOAH10_M", "2.1", m)
    #vars = ['Swnet_tavg', 'Lwnet_tavg', 'Qle_tavg', 'Qh_tavg', 'Qg_tavg', 'Snowf_tavg', 'Rainf_tavg', 'Evap_tavg', 'Qs_acc', 'Qsb_acc', 'Qsm_acc', 'AvgSurfT_inst', 'Albedo_inst', 'SWE_inst', 'SnowDepth_inst', 'SoilMoi0_10cm_inst', 'SoilMoi10_40cm_inst', 'SoilMoi40_100cm_inst', 'SoilMoi100_200cm_inst', 'SoilTMP0_10cm_inst', 'SoilTMP10_40cm_inst', 'SoilTMP40_100cm_inst', 'SoilTMP100_200cm_inst', 'PotEvap_tavg', 'ECanop_tavg', 'Tveg_tavg', 'ESoil_tavg', 'RootMoist_inst', 'CanopInt_inst', 'Wind_f_inst', 'Rainf_f_tavg', 'Tair_f_inst', 'Qair_f_inst', 'Psurf_f_inst', 'SWdown_f_tavg', 'LWdown_f_tavg',]
    vars = ['AvgSurfT_inst','Qair_f_inst','Rainf_tavg','Snowf_tavg','Wind_f_inst']
    for i in vars:
        zz = trender(lister(i,yz,xz,m),p)# - 273.15
        az.append(zz)
    return az
print("sent")
