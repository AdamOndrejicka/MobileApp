from flask import Flask, request
from datetime import datetime
from database import Database

server = Flask(__name__)

@server.get('/data')
def get_records():
    try:
        data = Database().get_data()
    except Exception:
        return 'Failed', 500
    return data

@server.delete('/data/<int:id>')
def delete_record(id):
    try: 
        Database().delete_data(id)
    except Exception:
        return 'Failed', 500
    return 'Success', 200

@server.post('/data/add')
def add_record():
    data = request.get_json(force=True)
    if '/' in data['pressure']:
        validated_pressure = data['pressure'].strip().split('/')
        systolic = validated_pressure[0]
        diastolic = validated_pressure[1]
    else:
        return 'PRESSURE', 500
    try:
        validated_datetime = datetime.strptime(data['time'].strip() + " " + data['date'].strip(), '%H:%M %d.%m.%Y')
    except Exception:
        return 'DATETIME', 500
    try:
        Database().add_data(systolic, diastolic, validated_datetime)
    except:
        return 'Failed', 500
    return 'Success', 200

if __name__ == '__main__':
    server.run(debug=True)