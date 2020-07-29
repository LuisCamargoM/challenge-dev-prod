#!/usr/bin/python3
import sys
import json
import csv
import datetime

def getTimestamp(tm):
    return datetime.datetime.strptime(tm,'%Y-%m-%dT%H:%M:%S.%fZ').timestamp()

def getValuesFirst(v):
    v.pop()
    t1 = v.pop()
    t2 = v.pop()
   # Transform String to Timestamp
    ncTime = v.pop() 
    ncTIme = getTimestamp(ncTime)
    return [ncTIme,t2,t1]   

def getValuesSecond(v): 
   # BEFORE: '(a=0010100000001110'
    fHalf = v[0].replace('=',',').replace('(','')
    fHalfVec = fHalf.split(',')     
   # AFTER: ['a', '1100101101000100'],

   # BEFORE: 'b=66d25020-00ea13de::66d2502064ea33fe;c=66c34131)'
    sHalf = v[1].replace(')','')
    sHalfVec = sHalf.split(';')
   
    sHalfVec[0] = str(sHalfVec[0]).replace('=',',')
    sHalfVec[1] = str(sHalfVec[1]).replace('=',',')

    s = sHalfVec[0]
    s = s.split(',')
    sHalfVec[0] = s  
    b = sHalfVec[1]
    b = b.split(',')
    sHalfVec[1] = b 

    c = sHalfVec[0][1]
    c = c.replace('-',',').replace('::',',')
    c = c.split(',')
    sHalfVec[0][1] = c
   # AFTER: [['b',['66d25020','00ea13de','66d2502064ea33fe']],['c','66c34131']]
    return [fHalfVec,sHalfVec]   

def formatLine(line):
    half = line.split('"')
    firstHalf = half[0].split(',')
    secondHalf = half[1].split(',')
      
    half[0] = getValuesFirst(firstHalf)
    half[1] = getValuesSecond(secondHalf)
    
    return half


while True:
        try:
            print('Streaming new Data....')
            line = sys.stdin.readline()
            half = formatLine(line)
            a =({
                'timestamp': int(half[0][0]), 
                'index':int(half[0][1]),
                'signalWave':float(half[0][2]),
                'metadata':{
                    'a':half[1][0][1],
                    'b':half[1][1][0][1],
                    'c':half[1][1][1][1]}
                    })
            with open('results.json', mode='a+') as json_File:
                json_File.write(json.dumps(a))
                json_File.write('\n')
        except KeyboardInterrupt:
            print('\nStream Ended!')
            break
