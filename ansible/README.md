
# If in python virtual env

pip install docker-compose

## On Mac OS

brew install docker-compose
brew install ansible

## On Ubuntu or WSL Ubuntu

sudo apt install ansible docker-compose


## Verify required ansible collections

bbaez@frankenstein3090-01:/persist/bbaez/es$ ansible-galaxy collection list | grep docker
community.docker                         3.7.0

## Run playbook

```
sudo ansible-playbook --connection=local --inventory 127.0.0.1, es-single-playbook.yaml
```
