import sqlite3

conn = sqlite3.connect('ticketing_database.sqlite3')
cursor = conn.cursor()

tables = ["Movies", "Stars", "Theaters", "Review_of_Movies", "Review_of_Theaters", "Members", "Movie_Schedule"]

for table in tables:
	cursor.execute('SELECT * FROM ' + table)
	print table
	for row in cursor:
		print row
	print '\n'