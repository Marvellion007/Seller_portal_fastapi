#!/bin/bash
port=$1
n=0 && \
until [ "$n" -ge 5 ]
do
   if(curl 172.17.0.1:${port}/docs)
   then
   break
   fi
   n=$((n+1)) 
   sleep 10
done 