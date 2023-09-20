import json
from pydoc import doc
from random import random
import firebase_admin
import firestore
import time
from firebase_admin import credentials
import random


import schedule
import time


nbr_mold_last=0
nbr_madult_last=0
nbr_mkid_last=0
nbr_myoung_last=0

nbr_fold_last=0
nbr_fadult_last=0
nbr_fkid_last=0
nbr_fyoung_last=0



data_last_hour={
        "total_persons":0,

    }

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

firestore_db =firebase_admin.firestore.client()


database = firebase_admin.firestore.client()


def upDB():
    global data_last_hour
    global nbr_mold_last
    global nbr_madult_last
    global nbr_mkid_last
    global nbr_myoung_last

    global nbr_fold_last
    global nbr_fadult_last
    global nbr_fkid_last
    global nbr_fyoung_last
    with open("count.json", "r") as jsonFile:
        data=json.load(jsonFile)
        
    total_persons_hour=data['total_persons']-data_last_hour['total_persons']

    with open("/home/gouga/Documents/models/jdid.json", "r") as jsonFile:
        data_jdid=json.load(jsonFile)
    
    nbr_mold2now=data['total_persons']*data_jdid["mold"]/100
    nbr_madult2now=data['total_persons']*data_jdid["madult"]/100
    nbr_mkid2now=data['total_persons']*data_jdid["mkid"]/100
    nbr_myoung2now=data['total_persons']*data_jdid["myoung"]/100

    nbr_fold2now=data['total_persons']*data_jdid["fold"]/100
    nbr_fadult2now=data['total_persons']*data_jdid["fadult"]/100
    nbr_fkid2now=data['total_persons']*data_jdid["fkid"]/100
    nbr_fyoung2now=data['total_persons']*data_jdid["fyoung"]/100

    if total_persons_hour:
        perc_mold=100*(nbr_mold2now-nbr_mold_last)/total_persons_hour
        perc_fold=100*(nbr_fold2now-nbr_fold_last)/total_persons_hour


        perc_madult=100*(nbr_madult2now-nbr_madult_last)/total_persons_hour
        perc_fadult=100*(nbr_fadult2now-nbr_fadult_last)/total_persons_hour

        perc_myoung=100*(nbr_myoung2now-nbr_myoung_last)/total_persons_hour
        perc_fyoung=100*(nbr_fyoung2now-nbr_fyoung_last)/total_persons_hour

        perc_mkid=100*(nbr_mkid2now-nbr_mkid_last)/total_persons_hour
        perc_fkid=100*(nbr_fkid2now-nbr_fkid_last)/total_persons_hour
    else:
        perc_fadult=perc_fkid=perc_fold=perc_fyoung=perc_madult=perc_mold=perc_myoung=perc_mkid=0

    nbr_mold_last=nbr_mold2now
    nbr_madult_last=nbr_madult2now
    nbr_myoung_last= nbr_myoung2now
    nbr_mkid_last= nbr_mkid2now

    nbr_fold_last=nbr_fold2now
    nbr_fadult_last=nbr_fadult2now
    nbr_fyoung_last= nbr_fyoung2now
    nbr_fkid_last= nbr_fkid2now


    
    data_hour={
        'total_persons':total_persons_hour,
        'mold':perc_mold,
        'fold':perc_fold,

        'madult':perc_madult,
        'fadult':perc_fadult,

        'myoung':perc_myoung,
        'fyoung':perc_fyoung,


        'mkid':perc_mkid,
        'fkid':perc_fkid,
        

    }
    x=time.ctime()
    
    
    t=int(x[11:13])
    h=f"{t}h"

    from datetime import date

    today = date.today()

    d3 = today.strftime("20%y-%m-%d")

    data_last_hour=data_hour
    ready_data={}
    ready_data[h]=data_hour
    data_jdid["total_persons"]=data['total_persons']
    ready_data['all_day_stats']=data_jdid
    

    

    exist = database.collection(u'users').document('user2').collection(u'gadgets').document(f"gadget1").collection(u'days').document(d3).get()
    print(exist)


    
    col_ref = database.collection(u'users').document('user3').collection(u'gadgets').document(f"gadget1").collection(u'days').document(d3)
    col_ref.update(ready_data)

def toDB():
    
    try:
        upDB()
    except:
        print('an error has occurd') 
        
        
"""
x=time.ctime()
t=60-int(x[14:16])

time.sleep(1)
print("waiting for",t,'minutes to start counting')



    
schedule.every(60).seconds.do(toDB)


while True:
    schedule.run_pending()
    
    time.sleep(1)

"""

upDB()