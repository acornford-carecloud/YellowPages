from flask import Flask, render_template, request
import json

server = Flask('app')

@server.route('/api/', methods=['POST'])
def db_update():
    posted_json = request.get_json(force=True)
    print json.loads(posted_json)
    return 'hell yes'

@server.route('/<int:number>')
def test(number):
    return render_template('index.html', number=number)

server.run(debug=True)
