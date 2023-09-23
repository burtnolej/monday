#!/bin/bash

cd /home/burtnolej/sambashare/veloxmon/monday
. ~/.bashrc
TODAY=`date +%Y%m%d`
NOW=`date +%Y%m%d_%H%M`

csvoutputpath=./csv
jsonoutputpath=./json
finalpath=/var/www/html/datafiles/Monday

boardids=("4909340518" "4977328922" "1140656959" "2193345626" "2259144314" "2763786972" "4973959122" "4974012540" "4909340518" "4973204278")

for boardid in ${boardids[@]}; do
  cat /dev/null > $csvoutputpath/*.txt

  cat /dev/null > $jsonoutputpath/$boardid.json
  cat /dev/null > $jsonoutputpath/$boardid.all.json

  python monday4.py "board_id:"$boardid"^output:json^columntype:select" >> $jsonoutputpath/$boardid.json 2>&1
  python monday4.py "board_id:"$boardid"^output:json^columntype:all" >> $jsonoutputpath/$boardid.all.json 2>&1
  python monday4.py "board_id:"$boardid"^output:csv^columntype:select" > $csvoutputpath/$boardid.txt 2>&1
done

cat $csvoutputpath/*.txt > $csvoutputpath/5555786972.txt

python monday_notifications.py > $csvoutputpath/updates.txt

cp $csvoutputpath/*.txt $finalpath
rm $csvoutputpath/*.txt
