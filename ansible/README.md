
# On Macs, you do not need to sudo for docker commands.  On Linux that is default.  
# See below to add yourself to docker group on Linux so sudo is not required.

https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo

# You must enable host networking on Macs if --net=host when using docker desktop
Settings -> Resources -> Network -> Enable host networking

# Adjust Docker Dkestop Settings -> Resources for disk, memory, cpu

# Docker image maintenance

```
docker system df

docker system prune -a
```

# Multi node shard balancing example config options

```
cluster.routing.allocation.same_shard.host: 'true'
cluster.routing.allocation.disk.threshold_enabled: 'true'
cluster.routing.allocation.disk.watermark.low: 50%
cluster.routing.allocation.disk.watermark.high: 70%
```

# Cerebro https

https://github.com/lmenezes/cerebro/issues/473

# If in python virtual env

pip install docker-compose

## On Mac OS

brew install docker-compose
brew install ansible

## On Ubuntu or WSL Ubuntu

sudo apt install ansible docker-compose


## Verify required ansible collections

$ ansible-galaxy collection list | grep docker
community.docker                         3.7.0

## Kibana manual run

$ docker run -d --name kibana -p 5601:5601 kibana:9.0.2

## Run playbook

```
sudo ansible-playbook --connection=local --inventory 127.0.0.1, es-single-playbook.yaml
```

## Links

http://localhost:5601/app/management/data/index_management/indices

http://localhost:9000/#!/overview?host=http:%2F%2Flocalhost:9200
