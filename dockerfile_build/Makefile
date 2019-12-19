network:
		docker network create -d overlay --attachable cluster
hadoop:
		docker stack deploy -c docker-compose-hadoop.yml hadoop

spark:
		docker stack deploy -c docker-compose-spark.yml spark

kafka:
		docker stack deploy -c docker-compose-kafka.yml kafka
		sleep 5
		docker exec -it `docker ps | grep cck0812/kafka | awk '{print $$1}'` /etc/init.d/ssh start
service:
		docker stack deploy -c docker-compose-service.yml service
		sleep 5
		docker exec -it `docker ps | grep cck0812/nifi | awk '{print $$1}'` /etc/init.d/ssh start