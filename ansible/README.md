
# On Macs, you do not need to sudo for docker commands.  On Linux that is default.  
# See below to add yourself to docker group on Linux so sudo is not required.

https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo

# You must enable host networking on Macs if --net=host when using docker desktop
Settings -> Resources -> Network -> Enable host networking

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

## Run playbook

```
sudo ansible-playbook --connection=local --inventory 127.0.0.1, es-single-playbook.yaml
```
