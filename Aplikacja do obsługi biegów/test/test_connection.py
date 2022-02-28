import pyodbc

conn = pyodbc.connect("DSN=mysql01;UID={};PWD={}".format('userLog001', 'userpwd'))

cursor = conn.cursor()
cursor.execute('SELECT * FROM Wydarzenie;')

for i in cursor:
    print(i)