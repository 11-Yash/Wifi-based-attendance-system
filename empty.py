import sqlite3

conn = sqlite3.connect('attendance.db')
c = conn.cursor()

# delete all rows from table
c.execute('DELETE FROM attend;',)

print('We have deleted', c.rowcount, 'records from the table.')

#commit the changes to db			
conn.commit()
#close the connection
conn.close()