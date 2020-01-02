# set crontab: * /1 * * * cron.sh

spark-submit --master spark://spark-master:7077 /pyfile/walkerland.py
spark-submit --master spark://spark-master:7077 /pyfile/ifood.py
spark-submit --master spark://spark-master:7077 /pyfile/trip_advisor.py
