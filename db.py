import sqlite3

def insertDB(number, length):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS lengths(
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    number INTEGER,
                    length INTEGER) ''')
    conn.commit()
    sql = 'INSERT INTO lengths (number,length) VALUES (?,?)'
    cursor.execute(sql, (number, length.total_seconds()))
    conn.commit()
    conn.close()

def getRecords():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lengths')
        result = cursor.fetchall()
        conn.close()
    except sqlite3.Error:
        result = []
    return result

def flush():
    try:
        print('Flushing')
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM lengths WHERE id % 2 = 0')
        conn.commit()
        conn.close()
        print('Finished')
    except sqlite3.Error:
        print('Error')
