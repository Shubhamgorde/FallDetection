import numpy as np
import json
import paho.mqtt.client as mqtt
import Graph_3plot_mod

import datetime
import math
from sklearn.linear_model import LogisticRegression
min_no=4

min_no_avg_x=0
min_no_avg_y=0
min_no_avg_z=0
min_no_array_x=min_no*[0]
min_no_array_y=min_no*[0]
min_no_array_z=min_no*[0]

max_no=20

max_no_avg_x=0
max_no_avg_y=0
max_no_avg_z=0
max_no_array_x=max_no*[0]
max_no_array_y=max_no*[0]
max_no_array_z=max_no*[0]



def column(matrix, i):
    return [row[i] for row in matrix]

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("FreeFallDetection")

def on_message(client, userdata, msg):

    p=str(msg.payload)


    p=json.loads(p)
    jsonL=len(p)

    index=0

    for index in range(0,jsonL-1):
        x=p[index]

        z=float(x["acc_z"])
        y=float(x["acc_y"])
        x=float(x["acc_x"])
        on_message.data.append([])

        on_message.data[on_message.counter].append(x)
        on_message.data[on_message.counter].append(y)
        on_message.data[on_message.counter].append(z)
        on_message.counter+=1
        on_message.count.append(on_message.counter)
        data_x=column(on_message.data,0)
        data_y=column(on_message.data,1)
        data_z=column(on_message.data,2)

        xchange=abs(data_x[on_message.counter-2]-data_x[on_message.counter-1])
        ychange=abs(data_y[on_message.counter-2]-data_y[on_message.counter-1])
        zchange=abs(data_z[on_message.counter-2]-data_z[on_message.counter-1])
        if on_message.flag==0:
            if xchange>9 or ychange>9 or zchange>9:
                on_message.flag=1
                timestamp=datetime.datetime.now()
                max_no_array_x[0]=data_x[on_message.counter-2]
                max_no_array_y[0]=data_y[on_message.counter-2]
                max_no_array_z[0]=data_z[on_message.counter-2]

                min_no_array_x[0]=data_x[on_message.counter-2]
                min_no_array_y[0]=data_y[on_message.counter-2]
                min_no_array_z[0]=data_z[on_message.counter-2]


            #print "hii, jerking high"
        '''
            on_message.flag=1
            timestamp=datetime.datetime.time()

        elif ychange>9:
            timestamp=datetime.datetime.time()
            on_message.flag=1

        elif zchange>9:
            timestamp=datetime.datetime.time()
            on_message.flag=1
        '''
        if on_message.flag==1:
            #print "hey flag set to 1"
            if on_message.counter_max<max_no:
            #print "counter:: ",on_message.counter_max
                max_no_array_x[on_message.counter_max]=x
                max_no_array_y[on_message.counter_max]=y
                max_no_array_z[on_message.counter_max]=z
                on_message.counter_max+=1
            ## ERRRORRR: u need to increment the counter

            if on_message.counter_max<=min_no:
                min_no_array_x[on_message.counter_max-1]=x
                min_no_array_y[on_message.counter_max-1]=y
                min_no_array_z[on_message.counter_max-1]=z
        if on_message.counter_max==4:
            #calculate avg change in x,y,z
            #loop for x points
            sumx=0
            sumy=0
            sumz=0
            for j in range(0,min_no-1):
                #print "min_x _array:: ", min_no_array_x
                #print "min_y array: ",min_no_array_y
                #print "min_z array: ",min_no_array_z
                #print "j:: ",j
                sumx+=abs(min_no_array_x[min_no-1-j]-min_no_array_x[min_no-1-j-1])
            min_no_avg_x=sumx/min_no-1

            #loop for y points
            for j in range(0,min_no-1):
                sumy+=abs(min_no_array_y[min_no-1-j]-min_no_array_y[min_no-1-j-1])
            min_no_avg_y=sumy/min_no-1

            #loop for z points
            for j in range(0,min_no-1):
                sumz+=abs(min_no_array_z[min_no-1-j]-min_no_array_z[min_no-1-j-1])
            min_no_avg_z=sumz/min_no-1
            min_no_avg=min_no_avg_x*min_no_avg_x+min_no_avg_y*min_no_avg_y+min_no_avg_z*min_no_avg_z

            on_message.min_no_avg=math.sqrt(min_no_avg)




        if on_message.counter_max==max_no:
            #calculate avg change in x,y,z for all 10 vals
            on_message.flag=0
            on_message.counter_max=1
            #calculate avg change in x,y,z
            #loop for x points
            sumx=0
            sumy=0
            sumz=0
            for j in range(0,max_no-1):
                sumx+=abs(max_no_array_x[max_no-1-j]-max_no_array_x[max_no-1-j-1])
                max_no_avg_x=sumx/max_no-1

            #loop for y points
            for j in range(0,max_no-1):
                sumy+=abs(max_no_array_y[min_no-1-j]-max_no_array_y[max_no-1-j-1])
                max_no_avg_y=sumy/max_no-1

            #loop for z points
            for j in range(0,max_no-1):
                sumz+=abs(max_no_array_z[max_no-1-j]-max_no_array_z[max_no-1-j-1])
                max_no_avg_z=sumz/max_no-1
            max_no_avg=max_no_avg_x*max_no_avg_x+max_no_avg_y*max_no_avg_y+max_no_avg_z*max_no_avg_z
            on_message.max_no_avg=math.sqrt(max_no_avg)

            #print on_message.min_no_avg,",",on_message.max_no_avg

            #print "sudden change detected or Fall detected"
            #print "@", datetime.datetime.now()
            '''
            #print "xchange:: ",xchange
            #print "ychange:: ",ychange
            #print "zchange:: ",zchange
            #exit(0)


            if on_message.min_no_avg>6 and on_message.max_no_avg<2:
                print "fall detected"
            '''
            #print "hey duf"
            val=on_message.logit.predict([on_message.min_no_avg,on_message.max_no_avg])


            ## use predict module here for min_no_avg and max_no_avg
            val=str(val)
            val=int((val).lstrip("['").strip('\\n]\''))
            print val
            if val==1:
                print "fall detected"
                on_message.value=val



        if on_message.counter>100:
            i.max_x=on_message.counter
            i.min_x=on_message.counter-100

        #x=json.loads(p)
        '''
        x=p[0]
        print x
        z=float(x["acc_z"])
        y=float(x["acc_y"])
        x=float(x["acc_x"])
        on_message.data.append([])

        on_message.data[on_message.counter].append(x)
        on_message.data[on_message.counter].append(y)
        on_message.data[on_message.counter].append(z)

        on_message.counter+=1

        on_message.count.append(on_message.counter)
        '''

        i.on_running_x(on_message.count, data_x , data_y , data_z,on_message.value )


def mqttTry():
    on_message.count=[]


    on_message.counter=0
    on_message.counter_max=1
    on_message.flag=0
    on_message.data=[]
    client.on_message = on_message
    client.loop_forever()

client = mqtt.Client()
client.on_connect = on_connect
client.connect("52.91.107.160", 1883, 20)

#Implementing logistic regression##ML algo starts
X=[]
y=[]

temp_count=0
TrainingData= open("ttraindata.txt","r")

for line in TrainingData:
     t1,t2,t3=line.split(",")
     X.append([])
     X[temp_count].append(t1)
     X[temp_count].append(t2)
     y.append(t3)
     temp_count=temp_count+1
     #print t1,t2,t3

on_message.value=0
on_message.logit=LogisticRegression()
on_message.logit.fit(X,y)      #fitting the model

#Ml algo finishes
i=Graph_3plot_mod.DynamicUpdate()

i.on_launch()
mqttTry()