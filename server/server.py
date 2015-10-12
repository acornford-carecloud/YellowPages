from flask import Flask, render_template, request
import json
import pymongo

server = Flask('app')
user_collection = pymongo.MongoClient().users.host_users

@server.route('/api/', methods=['POST'])
def db_update():
    json_list = json.loads(request.get_json(force=True))

    for posted_json in json_list:
        user_collection.update(posted_json, upsert = True)
    return ''

@server.route('/')
def base():
    user_list=[i for i in user_collection.find()]
    return render_template('index.html', user_list=user_list)

@server.route('/user')
def con_on_user():
    consol = {}
    for user_row in [i for i in user_collection.find()]:
        info = [user_row['hostname'], user_row['ip'], user_row['sudo']]
        try:
            consol[user_row['username']].append(info)
        except KeyError:
            consol[user_row['username']] = [info]
    return render_template('consol.html', consol=consol)

@server.route('/ip')
def con_on_host():
    return

@server.route('/group')
def con_on_group():
    return

@server.route('/user/<username>')
def search_user(username):
    return


@server.route('/ip/<ip>')
def search_host(hostname):
    return


@server.route('/group/<group>')
def search_group(group):
    return


server.run(debug = True, host = '0.0.0.0')
