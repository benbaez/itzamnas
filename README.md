# Itzamnas
AI that collaborates with other AI

Forked from TwoAI created by Fus3n on GitHUb.  Going to take original code in a completely different direction.

##  Google Presentation
https://docs.google.com/presentation/d/1LSTmVEutbStEQnW6_chnADENHm7b2OuCHLMiTVWhyTg/edit?usp=sharing

## Instal WSL (Ubuntu Linux)

https://techcommunity.microsoft.com/discussions/windows11/how-to-install-the-linux-windows-subsystem-in-windows-11/2701207

## Install ollama

https://ollama.com/download/linux

## Install Ubuntu packages

```
sudo apt update && sudo apt upgrade
apt install git python3.12-venv python-is-python3 python3-full
```

## Create Python Virtual Environment

```
cd ~/
python3 -m venv python-ai
export PYTHONPATH="$PYTHONPATH:/home/bbaez/itzamnas/src"
export PATH=/home/bbaez/python-ai/bin:/home/bbaez/.local/bin:$PATH
```

## Create ssh key to use with GitHub

```
cd ~/.ssh
ssh-keygen -t ed25519 -C "<email address or some other identifier>"
ssh-add /home/bbaez/.ssh/id_ed25519
systemctl | grep ssh
sudo apt install ssh-agent
sudo apt search ssh-agent
systemctl enable ssh-agent
sudo systemctl enable ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat id_ed25519.pub
```

## Ollama setup

```
ollama pull mistral
ollama pull llama3
ollama pull llama3.3
ollama pull qwq
ollama pull deepseek-r1
```

## Prepare itzamnas

```
git clone git@github.com:benbaez/itzamnas.git
cd itzamnas
git checkout tags/0.1
pip install -r requirements.txt
```

## Elasticsearch

```
$ sudo apt install python3-elasticsearch
```

## Test run

```
python src/examples/main.py llama3 qwq
```

Just enter at all questions for default prompts.
