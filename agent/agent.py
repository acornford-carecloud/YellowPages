import json
import requests
import socket

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

sudo_file = open('/etc/sudoers','r').read()
def is_sudo(user_name):
    return user_name in sudo_file


group_assoc = {}
with open('/etc/group','r') as group_file:
    for group in group_file:
        group_data =  group.split(":")
        group_assoc[group_data[2]] = group_data[0]


user_dict = {}
with open('/etc/passwd','r') as user_file:
    for user in user_file:
        user_data = user.split(":")
        user_dict[user_data[0]] = { "group": group_assoc[user_data[3]], "sudo": is_sudo(user_data[0])}

json_dump = json.dumps({'ip': ip, 'hostname': hostname, 'users': user_dict})
requests.post('http://127.0.0.1:5000/api/', json=json_dump)

