#!/usr/bin/env python3

import json
import os
import logging
import paramiko

#variables
filename = 'info.json'

#logging
logging.basicConfig(filename='info.log', level=logging.INFO, format='%(asctime)s %(message)s')

#file check
if not os.path.exists(filename):
    logging.info(f'Файл {filename} не найден')
    exit()

with open(filename, 'r') as f:
    data = json.load(f)

#host and user check
has_user = False
has_host = False
for cluster_info in data['hosts'].values():
    if 'user' in cluster_info and cluster_info['user']:
        has_user = True
    if 'host' in cluster_info and cluster_info['host']:
        has_host = True
    if has_user and has_host:
        break

if not has_user:
    logging.info(f'В файле {filename} нет пользователей или у ключей "user" нет значений')
    exit()

if not has_host:
    logging.info(f'В файле {filename} нет хостов или у ключей "host" нет значений')
    exit()


#ssh connect, run command
for cluster_name, cluster_info in data['hosts'].items():
    host_name = cluster_info['host']
    user_name = cluster_info['user']
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host_name, username=user_name, password=user_name)
            stdin, stdout, stderr = ssh.exec_command('ls -lah ~/bw/')
            output = stdout.read().decode('utf-8')
            if '.git' not in output:
                logging.info(f'В каталоге ~/bw/ пользователя {user_name} на сервере {host_name} нет git репозитория')
            else:
                stdin, stdout, stderr = ssh.exec_command('cd ~/bw/ && git rev-parse --abbrev-ref HEAD && git rev-parse HEAD')
                output = stdout.read().decode('utf-8').split('\n')
                branch = output[0]
                revision = output[1]
                data['hosts'][cluster_name]['branch'] = branch
                data['hosts'][cluster_name]['revision'] = revision
        except Exception as e:
            logging.info(f'Ошибка при подключении к серверу {host_name} с пользователем {user_name}: {e}')

with open(f'{filename}', 'w') as f:
    json.dump(data, f, indent=4)