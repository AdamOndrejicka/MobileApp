import sqlite3

class Database():
    def __init__(self):
        self.connection = sqlite3.connect('app.db')
        self.cursor = self.connection.cursor()
    def add_data(self, systolic, diastolic, datetime):
        query = 'INSERT INTO data (systolic, diastolic, datetime) VALUES (?, ?, ?)'
        parameters = (systolic, diastolic, datetime)
        self.cursor.execute(query, parameters)
        self.connection.commit()
    def delete_data(self, id):
        query = 'DELETE FROM data WHERE id = ?'
        parameters = (id, )
        self.cursor.execute(query, parameters)
        self.connection.commit()
    def get_data(self):
        return self.cursor.execute('SELECT * FROM data ORDER BY datetime').fetchall()
    def __del__(self):
        self.cursor.close()
        self.connection.close()

if __name__ == '__main__':
    pass
    #db.cursor.execute('CREATE TABLE data (id INTEGER PRIMARY KEY AUTOINCREMENT, systolic INTEGER NOT NULL, diastolic INTEGER NOT NULL, datetime TEXT NOT NULL)')

