#!/usr/bin/python
from flask import Flask, render_template, request
import json
import pymongo
import socket

server = Flask(__name__)
user_collection = pymongo.MongoClient().users.host_users

def ip(hostname):
    return socket.gethostbyname(hostname)

def is_system_user(user):
    system_users = ['root','tomcat7','news','ubuntu','ntp','ntp','irc','www-data',
            'daemon','bin','sys','sync','games','man','lp','uucp','nobody','sshd',
            'backup','irc','postgres','gnats','syslog','mongodb','landscape',
            'pollinate','list','mail','libuuid','messagebus','proxy','openldap',
            'app']
    return True if user in system_users else False

@server.route('/api/', methods=['POST'])
def db_update():
    json_list = json.loads(request.get_json(force=True))
    for posted_json in json_list:
        if not is_system_user(posted_json['username']):
            user_collection.update(posted_json, posted_json, upsert = True)
    return 'Done'

@server.route('/')
def base():
    user_list=[i for i in user_collection.find()]
    return render_template('index.html', user_list=user_list)

@server.route('/users')
def con_on_user():
    consol = {}
    for user_row in [i for i in user_collection.find()]:
        if not is_system_user(user_row['username']):
            info = [user_row['hostname'], ip(user_row['hostname']), user_row['group'], user_row['sudo']]
            try:
                consol[user_row['username']].append(info)
            except KeyError:
                consol[user_row['username']] = [info]
    all_users = sorted([{user: value} for user, value in consol.iteritems()])
    return render_template('all_users.html', all_users=all_users)

@server.route('/hosts')
def con_on_host():
    consol = {}
    for host_row in [i for i in user_collection.find()]:
        if not is_system_user(host_row['username']):
            info = [host_row['username'], ip(host_row['hostname']), host_row['group'], host_row['sudo']]
            try:
                consol[host_row['hostname']].append(info)
            except KeyError:
                consol[host_row['hostname']] = [info]
    all_hosts = sorted([{key: value} for key, value in consol.iteritems()])
    return render_template('all_hosts.html', all_hosts=all_hosts)

@server.route('/user/<username>')
def search_user(username):
    user_info = [i for i in user_collection.find({u'username': username})]
    return render_template('single_user.html', user_info = user_info)


@server.route('/host/<hostname>')
def search_host(hostname):
    host_info = [i for i in user_collection.find({u'hostname': hostname})]
    return render_template('single_host.html', host_info = host_info)

server.run(debug = True, host = '0.0.0.0')
