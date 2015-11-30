import sqlite3

conn = sqlite3.connect('ticket_management.sqlite3')
cursor = conn.cursor()

tables = ["Movies", "Stars", "Reviews", "Theaters",
 "Review_of_Movies", "Review_of_Theaters", "Staff",
  "Members", "Favorite_Type", "Favorite_Theater",
   "Credit_Card", "Own", "Employed_by", "Members_of",
    "Working_Schedule", "Movie_Schedule"]

for table in tables:
	cursor.execute('SELECT * FROM ' + table)
	print table
	for row in cursor:
		print row
	print '\n'
