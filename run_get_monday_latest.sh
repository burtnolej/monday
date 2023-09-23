#!/bin/bash

if [ -z "$1" ]
then
      delay=60
      echo "\$1 is empty: setting delay to 60"
else
      delay=$1
      echo "seting delay to "$1
fi

cd /home/burtnolej/sambashare/veloxmon/monday
. ~/.bashrc
TODAY=`date +%Y%m%d`
NOW=`date +%Y%m%d_%H%M`

csvoutputpath=./csv
jsonoutputpath=./json
timewindow=20
finalpath=/var/www/html/datafiles/Monday/$timewindow

boardids=("4977328922" "1140656959" "2193345626" "2259144314" "2763786972" "4973959122" "4974012540" "4909340518" "4973204278")

cat /dev/null > $csvoutputpath/$timewindow/*

for boardid in ${boardids[@]}; do
  dt=$(date)
  echo $dt" "$boardid"["$timewindow"] sleeping for "$delay
  sleep $delay # to allow monday api complexity quota cool down
  #cat /dev/null > $csvoutputpath/$boardid.txt

  python ./monday5.py "board_id:"$boardid"^timewindow:"$timewindow > $csvoutputpath/$timewindow/$boardid.txt 2>&1

  #num_rows=$(wc -l $csvoutputpath"/5555786972.txt")
  echo "num rows added $num_rows"
done

cat $csvoutputpath/$timewindow/*.txt > $csvoutputpath/$timewindow/6666786972.txt

echo $dt" updates ["$timewindow"] sleeping for "$delay
python monday_notifications.py timewindow:20 > $csvoutputpath/$timewindow/updates.txt

cp $csvoutputpath/$timewindow/* $finalpath
rm $csvoutputpath/$timewindow/* 
