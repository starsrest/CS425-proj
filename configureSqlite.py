import sqlite3

def createDB():
	con = sqlite3.connect("ticketing_database.sqlite3")
	cur = con.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS Movies\
				(year INT,\
				 title TEXT,\
				 genre TEXT NOT NULL,\
				 length INT NOT NULL,\
				 director TEXT NOT NULL,\
				 description TEXT NOT NULL,\
				 PRIMARY KEY (year, title))')

	cur.execute('CREATE TABLE IF NOT EXISTS Stars\
				(year INT, title TEXT,star_name TEXT,\
				PRIMARY KEY (year, title, star_name))')

	cur.execute('CREATE TABLE IF NOT EXISTS Members\
				(username TEXT PRIMARY KEY,\
				 password TEXT NOT NULL,\
  				 email TEXT NOT NULL)')

	# cur.execute('CREATE TABLE IF NOT EXISTS Reviews\
	# 			(username TEXT REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
	# 			 time TIMESTAMP NOT NULL, type TEXT NOT NULL,\
	# 			content TEXT NOT NULL, visits INT NOT NULL,\
	# 			PRIMARY KEY (username, time))')

	cur.execute('CREATE TABLE IF NOT EXISTS Theaters\
				(address TEXT PRIMARY KEY,\
				 name TEXT NOT NULL,\
				 company TEXT NOT NULL,\
				 number_of_screens INT NOT NULL)')

	cur.execute('CREATE TABLE IF NOT EXISTS Review_of_Movies\
				(year INT REFERENCES Movies(year) ON DELETE SET NULL ON UPDATE CASCADE,\
				title TEXT REFERENCES Movies(title) ON DELETE SET NULL ON UPDATE CASCADE,\
				username TEXT REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
				time TIMESTAMP NOT NULL,\
				content TEXT NOT NULL,\
				PRIMARY KEY (year, title, username, time))')

	cur.execute('CREATE TABLE IF NOT EXISTS Review_of_Theaters\
				(address TEXT REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE,\
				username TEXT REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
				time TIMESTAMP NOT NULL,\
				content TEXT NOT NULL,\
				PRIMARY KEY (address, username, time))')

	# cur.execute('CREATE TABLE IF NOT EXISTS Credit_Card\
	# 			(card_number INT PRIMARY KEY, holder_name TEXT NOT NULL,\
	# 			type TEXT NOT NULL, expiration_time DATE NOT NULL)')

	# cur.execute('CREATE TABLE IF NOT EXISTS Own\
	# 			(username TEXT REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
	# 			card_number INT REFERENCES Credit_Card(card_number) ON DELETE SET NULL ON UPDATE CASCADE,\
	# 			PRIMARY KEY(username, card_number))')

	# cur.execute('CREATE TABLE IF NOT EXISTS Members_of\
	# 			(username TEXT PRIMARY KEY REFERENCES Member(username) ON DELETE SET NULL ON UPDATE CASCADE,\
	# 			theater_address REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE)')

	cur.execute('CREATE TABLE IF NOT EXISTS Movie_Schedule\
				(time TIMESTAMP NOT NULL,\
				movie_title TEXT REFERENCES Movies(title) ON DELETE SET NULL ON UPDATE CASCADE,\
				theater_address TEXT REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE,\
				movie_year INT REFERENCES Movies(year) ON DELETE SET NULL ON UPDATE CASCADE,\
				discount REAL NOT NULL,\
				price REAL NOT NULL,\
				total_ticket INT NOT NULL,\
				sold_ticket INT NOT NULL,\
				PRIMARY KEY(time, movie_title, theater_address))')

	# cur.execute('CREATE TABLE IF NOT EXISTS Comments\
	# 			(username TEXT REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
	# 			time TIMESTAMP NOT NULL,\
	# 			content TEXT NOT NULL,\
	# 			reviews_username REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
	# 			review_time REFERENCES Reviews(time)ON DELETE SET NULL ON UPDATE CASCADE,\
	# 			PRIMARY KEY(username, time))')

	# cur.execute('CREATE TABLE IF NOT EXISTS Logger\
	# 			(message TEXT PRIMARY KEY)')

	con.commit()


def insertDB():
	con = sqlite3.connect("ticketing_database.sqlite3")
	cur = con.cursor()

	#insert 3 movies
	cur.execute("""
				INSERT INTO Movies VALUES(2001, 'Crouching Tiger, Hidden Dragon', 'Action',
				120, 'Ang Lee', 'Two warriors in pursuit of a stolen sword and a notorious fugitive are led to an impetuous, physically skilled, adolescent nobleman''s daughter, who is at a crossroads in her life.')
			   	""")

	cur.execute("""
				INSERT INTO Movies VALUES(2014, 'Gone Girl', 'Thriller',
				149, 'David Fincher', 'With his wife''s disappearance having become the focus of an intense media circus, a man sees the spotlight turned on him when it''s suspected that he may not be innocent.')
			   	""")

	cur.execute("""
				INSERT INTO Movies VALUES(2014, 'Interstellar', 'Sci-Fi',
				169, 'Christopher Nolan', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity''s survival')
			   	""")

	#insert stars, 3 stars per movie
	cur.execute("""
				INSERT INTO Stars VALUES(2001, 'Crouching Tiger, Hidden Dragon', 'Yun-Fat Chow')
				""")

	cur.execute("""
				INSERT INTO Stars VALUES(2001, 'Crouching Tiger, Hidden Dragon', 'Michelle Yeoh')
				""")

	cur.execute("""
				INSERT INTO Stars VALUES(2001, 'Crouching Tiger, Hidden Dragon', 'Ziyi Zhang')
				""")

	cur.execute("""
				INSERT INTO Stars VALUES(2014, 'Gone Girl', 'Ben Affleck')
				""")

	cur.execute("""
				INSERT INTO Stars VALUES(2014, 'Gone Girl', 'Neil Patrick Harris')
				""")

	cur.execute("""
				INSERT INTO Stars VALUES(2014, 'Gone Girl', 'Rosamund Pike')
				""")

	cur.execute("""
				INSERT INTO Stars VALUES(2014, 'Interstellar', 'Matthew McConaughey')
				""")

	cur.execute("""
				INSERT INTO Stars VALUES(2014, 'Interstellar', 'Anne Hathaway')
				""")

	cur.execute("""
				INSERT INTO Stars VALUES(2014, 'Interstellar', 'Jessica Chastain')
				""")

	#insert Members, there are 6 members.
	cur.execute("INSERT INTO Members VALUES('jim', '1111', '007@bond.uk')")

	cur.execute("""
				INSERT INTO Members VALUES('rose', '2222', 'rose@mond.com')
				""")

	cur.execute("""
				INSERT INTO Members VALUES('beth', '3333', 'beth@gmail.com')
				""")

	cur.execute("""
				INSERT INTO Members VALUES('todd', '4444', 'todd@yahoo.com')
				""")

	cur.execute("""
				INSERT INTO Members VALUES('barb', '5555', 'barb@space.com')
				""")

	cur.execute("""
				INSERT INTO Members VALUES('christ', '6666', 'ops@gmail.com')
				""")


	#insert 3 theaters
	cur.execute("""
				INSERT INTO Theaters VALUES('322 E Illinois St, Chicago, IL 60611', 'AMC River East 21',
				'AMC', 10)
				""")

	cur.execute("""
				INSERT INTO Theaters VALUES('600 E Grand Ave, Chicago, IL 60611', 'Navy Pier IMAX Theatre',
				'IMAX', 6)
				""")

	cur.execute("""
				INSERT INTO Theaters VALUES('600 N Michigan Ave, Chicago, IL 60611', 'AMC 600 North Michigan 9',
				'AMC', 8)
				""")

	#insert reviews of movies, each movie has 3 reviews
	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2001, 'Crouching Tiger, Hidden Dragon', 
					'jim', '2015-11-1 15:30:26', 'Great movie!')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2001, 'Crouching Tiger, Hidden Dragon', 
					'rose', '2015-11-2 08:46:11', 'Not bad.')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2001, 'Crouching Tiger, Hidden Dragon', 
					'beth', '2015-11-3 20:01:30', '5/10. Waste of my money.')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2014, 'Gone Girl', 'todd', 
					'2015-11-4 20:01:30', '6/10. I wound not recommend everyone to watch this.')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2014, 'Gone Girl', 'barb', 
					'2015-11-5 20:01:30', '4/10. Not worth watching.')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2014, 'Gone Girl', 'christ', 
					'2015-11-6 20:01:30', '9/10. Movie of the year.')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2014, 'Interstellar', 'jim', 
					'2015-11-7 20:01:30', 'Great theater!')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2014, 'Interstellar', 'rose', 
					'2015-11-8 20:01:30', 'Not bad')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2014, 'Interstellar', 'beth', 
					'2015-11-9 20:01:30', 'Movie of the year!')
				""")

	#insert review of theaters, each theater has 3 reviews
	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('322 E Illinois St, Chicago, IL 60611', 
					'todd', '2015-11-10 20:01:30', 'I will recommend everyone I know to watch movie in here.')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('322 E Illinois St, Chicago, IL 60611', 
					'barb', '2015-11-11 20:01:30', 'I love this place!')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('322 E Illinois St, Chicago, IL 60611', 
					'christ', '2015-11-12 20:01:30', '7/10')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('600 E Grand Ave, Chicago, IL 60611', 
					'jim', '2015-11-13 20:01:30', '8/10')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('600 E Grand Ave, Chicago, IL 60611', 
					'rose', '2015-11-14 20:01:30', '8/10')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('600 E Grand Ave, Chicago, IL 60611', 
					'beth', '2015-11-15 20:01:30', '2/10')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('600 N Michigan Ave, Chicago, IL 60611', 
					'todd', '2015-11-16 20:01:30', 'Fantastic!')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('600 N Michigan Ave, Chicago, IL 60611', 
					'barb', '2015-11-17 20:01:30', 'Not bad.')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('600 N Michigan Ave, Chicago, IL 60611', 
					'christ', '2015-11-18 20:01:30', 'Great theater.')
				""")



	#insert Movie_Schedule
	cur.execute("""
				INSERT INTO Movie_Schedule VALUES('2015-11-13 10:00:00', 'Crouching Tiger, Hidden Dragon', 
					'322 E Illinois St, Chicago, IL 60611', 2001, 0.8, 15, 300, 50)
				""")

	cur.execute("""
				INSERT INTO Movie_Schedule VALUES('2015-11-14 10:00:00', 'Gone Girl', 
					'600 E Grand Ave, Chicago, IL 60611', 2014, 0.5, 14, 500, 200)
				""")

	cur.execute("""
				INSERT INTO Movie_Schedule VALUES('2015-11-15 10:00:00', 'Interstellar', 
					'600 N Michigan Ave, Chicago, IL 60611', 2014, 0.9, 12, 400, 100)
				""")

	
	con.commit()

if __name__ == "__main__":
	createDB()
	insertDB()