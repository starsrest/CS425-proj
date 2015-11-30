import sqlite3

def createDB():
	con = sqlite3.connect("ticket_management.sqlite3")
	cur = con.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS Movies\
				(year INT, title TEXT, genre TEXT NOT NULL,\
				length INT NOT NULL, director TEXT NOT NULL,\
				description TEXT NOT NULL, PRIMARY KEY (year, title))')

	cur.execute('CREATE TABLE IF NOT EXISTS Stars\
				(year INT, title TEXT,star_name TEXT,\
				PRIMARY KEY (year, title, star_name))')

	cur.execute('CREATE TABLE IF NOT EXISTS Reviews\
				(username TEXT REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
				time TIMESTAMP NOT NULL, type TEXT NOT NULL,\
				content TEXT NOT NULL, visits INT NOT NULL,\
				PRIMARY KEY (username, time))')
 
	cur.execute('CREATE TABLE IF NOT EXISTS Theaters\
				(address TEXT PRIMARY KEY,\
				 name TEXT NOT NULL,\
				 company TEXT NOT NULL,\
				 number_of_screens INT NOT NULL)')

	cur.execute('CREATE TABLE IF NOT EXISTS Review_of_Movies\
				(year INT REFERENCES Movies(year) ON DELETE SET NULL ON UPDATE CASCADE,\
				title TEXT REFERENCES Movies(title) ON DELETE SET NULL ON UPDATE CASCADE,\
				username TEXT REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
				time TIMESTAMP NOT NULL, PRIMARY KEY (year, title, username, time))')

	cur.execute('CREATE TABLE IF NOT EXISTS Review_of_Theaters\
				(address TEXT REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE,\
				username TEXT REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
				time TIMESTAMP NOT NULL, PRIMARY KEY (address, username, time))')

	cur.execute('CREATE TABLE IF NOT EXISTS Staff\
				(ssn INT PRIMARY KEY, f_name TEXT NOT NULL,\
				l_name TEXT NOT NULL, gender TEXT NOT NULL,\
				email TEXT NOT NULL, address TEXT NOT NULL,\
				phone TEXT NOT NULL, job_type TEXT NOT NULL,\
				description_of_duty TEXT NOT NULL)')

	cur.execute('CREATE TABLE IF NOT EXISTS Members\
				(username TEXT PRIMARY KEY, password TEXT NOT NULL,\
  				reward TEXT NOT NULL, f_name TEXT NOT NULL,\
  				l_name TEXT NOT NULL, gender TEXT NOT NULL,\
  				email TEXT NOT NULL, address TEXT NOT NULL,\
  				phone TEXT NOT NULL, status TEXT NOT NULL,\
  				points INT NOT NULL)')

	cur.execute('CREATE TABLE IF NOT EXISTS Favorite_Type\
				(username REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
				type REFERENCES Movies(genre) ON DELETE SET NULL ON UPDATE CASCADE,\
				PRIMARY KEY(username, type))')

	cur.execute('CREATE TABLE IF NOT EXISTS Favorite_Theater\
				(username REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
				theater_address REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE,\
				PRIMARY KEY(username, theater_address))')

	cur.execute('CREATE TABLE IF NOT EXISTS Credit_Card\
				(card_number INT PRIMARY KEY, holder_name TEXT NOT NULL,\
				type TEXT NOT NULL, expiration_date DATE NOT NULL)')

	cur.execute('CREATE TABLE IF NOT EXISTS Own\
				(username INT REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
				card_number INT REFERENCES Credit_Card(card_number) ON DELETE SET NULL ON UPDATE CASCADE,\
				PRIMARY KEY(username, card_number))')

	cur.execute('CREATE TABLE IF NOT EXISTS Employed_By\
				(ssn INT PRIMARY KEY REFERENCES Staff(ssn) ON DELETE SET NULL ON UPDATE CASCADE,\
				theater_address TEXT REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE)')

	cur.execute('CREATE TABLE IF NOT EXISTS Members_of\
				(username INT PRIMARY KEY REFERENCES Member(username) ON DELETE SET NULL ON UPDATE CASCADE,\
				theater_address TEXT REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE)')

	cur.execute('CREATE TABLE IF NOT EXISTS Working_Schedule\
				(day date NOT NULL,\
				ssn INT REFERENCES Staff(ssn) ON DELETE SET NULL ON UPDATE CASCADE,\
				assignment TEXT NOT NULL,\
				work_at TEXT REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE,\
				PRIMARY KEY(time, ssn, work_at))')

	cur.execute('CREATE TABLE IF NOT EXISTS Movie_Schedule\
				(time TIMESTAMP NOT NULL,\
				movie_title TEXT REFERENCES Movies(title) ON DELETE SET NULL ON UPDATE CASCADE,\
				address TEXT REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE,\
				movie_year INT REFERENCES Movies(year) ON DELETE SET NULL ON UPDATE CASCADE,\
				discount REAL NOT NULL,\
				price REAL NOT NULL,\
				total_ticket INT NOT NULL,\
				sold_ticket INT NOT NULL,\
				PRIMARY KEY(time, movie_title, address, movie_year))')

	cur.execute('CREATE TABLE IF NOT EXISTS Comments\
				(username TEXT REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
				time TIMESTAMP NOT NULL,\
				content TEXT NOT NULL,\
				review_username TEXT REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,\
				review_time TIMESTAMP REFERENCES Reviews(time)ON DELETE SET NULL ON UPDATE CASCADE,\
				PRIMARY KEY(username, time))')

	con.commit()


def insertDB():
	con = sqlite3.connect("ticket_management.sqlite3")
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
	cur.execute("""
				INSERT INTO Members VALUES('jim', '1111', 'Mug', 'James', 'Bond', 'Male', '007@bond.uk', 
					'50 Water Street Mystic CT 06355', '7731112222', 'Gold', 500)
				""")

	cur.execute("""
				INSERT INTO Members VALUES('rose', '2222', 'Hat', 'Rose', 'Mond', 'Female', 'rose@mond.com',
					'15 Cliff Street Griswold CT 06351', '2223331234', 'Silver', 300)
				""")

	cur.execute("""
				INSERT INTO Members VALUES('beth', '3333', 'Star Wars Toy', 'Beth', 'Watson', 
					'Female', 'beth@gmail.com', '104 Thomaston Road Preston CT 06365', '6663214444', 
					'Bronze', 95)
				""")

	cur.execute("""
				INSERT INTO Members VALUES('todd', '4444', 'Saber', 'Todd', 'Adams', 'Male', 'todd@yahoo.com', 
					'490 E Main Street Norwich CT 06360', '9193337474', 'Diamond', 1024)
				""")

	cur.execute("""
				INSERT INTO Members VALUES('barb', '5555', 'Secret Box', 'Barbara', 'Blais', 'Female', 'barb@space.com', 
					'574 New London Turnpike Norwich CT 06360', '1024783232', 'Gold', 630)
				""")

	cur.execute("""
				INSERT INTO Members VALUES('christ', '6666', 'Xbox One', 'Christine', 'Smith', 'Male', 'ops@gmail.com', 
					'33 Paula Lane Uncasville CT 06385', '6362990054', 'Silver', 415)
				""")

	#insert reviews, each movie or theater has 3 reviews
	cur.execute("""
				INSERT INTO Reviews VALUES('jim', '2015-11-1 15:30:26', 
					'Movie', '10/10. Awesome!', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('rose', '2015-11-2 08:46:11', 
					'Movie', '5/10. Waste of my money.', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('beth', '2015-11-3 20:01:30', 
					'Movie', '8/10. Great Movie!', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('todd', '2015-11-4 20:01:30', 
					'Movie', '6/10. I wound not recommend everyone to watch this.', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('barb', '2015-11-5 20:01:30', 
					'Movie', '3/10. It"s a piece of trash.', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('christ', '2015-11-6 20:01:30', 
					'Movie', '4/10. Not worth watching.', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('jim', '2015-11-7 20:01:30', 
					'Movie', '7/10. Not bad.', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('rose', '2015-11-8 20:01:30', 
					'Movie', '2/10. Junk movie.', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('beth', '2015-11-9 20:01:30', 
					'Movie', '9/10. Movie of the year.', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('todd', '2015-11-10 20:01:30', 
					'Theater', 'Not bad.', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('barb', '2015-11-11 20:01:30', 
					'Theater', 'Great theater!', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('christ', '2015-11-12 20:01:30', 
					'Theater', 'I will come back next time.', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('jim', '2015-11-13 20:01:30', 
					'Theater', 'It''s not what I expected.', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('rose', '2015-11-14 20:01:30', 
					'Theater', 'This theater is huge, I like it.', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('beth', '2015-11-15 20:01:30', 
					'Theater', 'The popcorn is sweat!', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('todd', '2015-11-16 20:01:30', 
					'Theater', 'I have a wonderful experience.', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('barb', '2015-11-17 20:01:30', 
					'Theater', 'I will recommend everyone I know to watch movie in here.', 0)
				""")

	cur.execute("""
				INSERT INTO Reviews VALUES('christ', '2015-11-18 20:01:30', 
					'Theater', 'I love this place!', 0)
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
					'jim', '2015-11-1 15:30:26')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2001, 'Crouching Tiger, Hidden Dragon', 
					'rose', '2015-11-2 08:46:11')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2001, 'Crouching Tiger, Hidden Dragon', 
					'beth', '2015-11-3 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2014, 'Gone Girl', 'todd', 
					'2015-11-4 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2014, 'Gone Girl', 'barb', 
					'2015-11-5 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2014, 'Gone Girl', 'christ', 
					'2015-11-6 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2014, 'Interstellar', 'jim', 
					'2015-11-7 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2014, 'Interstellar', 'rose', 
					'2015-11-8 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Movies VALUES(2014, 'Interstellar', 'beth', 
					'2015-11-9 20:01:30')
				""")

	#insert review of theaters, each theater has 3 reviews
	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('322 E Illinois St, Chicago, IL 60611', 
					'todd', '2015-11-10 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('322 E Illinois St, Chicago, IL 60611', 
					'barb', '2015-11-11 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('322 E Illinois St, Chicago, IL 60611', 
					'christ', '2015-11-12 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('600 E Grand Ave, Chicago, IL 60611', 
					'jim', '2015-11-13 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('600 E Grand Ave, Chicago, IL 60611', 
					'rose', '2015-11-14 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('600 E Grand Ave, Chicago, IL 60611', 
					'beth', '2015-11-15 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('600 N Michigan Ave, Chicago, IL 60611', 
					'todd', '2015-11-16 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('600 N Michigan Ave, Chicago, IL 60611', 
					'barb', '2015-11-17 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Review_of_Theaters VALUES('600 N Michigan Ave, Chicago, IL 60611', 
					'christ', '2015-11-18 20:01:30')
				""")

	# insert staff, 9 staff
	cur.execute("""
				INSERT INTO Staff VALUES(100000000, 'Lena', 'Zahradnik', 'Female', 'lena@gmail.com', 
					'8967 Marshall Street North Augusta, SC 29841', '8997123377', 'Owner', 'Owner of the cinema')
				""")

	cur.execute("""
				INSERT INTO Staff VALUES(200000000, 'Randolph', 'Law', 'Male', 'rand@gmail.com', 
					'6848 12th Street East Richmond, VA 23223', '8332226807', 'Administrator of the website', 
					'Manage website of the cinema')
				""")

	cur.execute("""
				INSERT INTO Staff VALUES(300000000, 'Ed', 'Glick', 'Male', 'ed@go.com', 
					'6586 High Street Wyandotte, MI 48192', '8115488984', 'Manager', 'Manage the cinema')
				""")

	cur.execute("""
				INSERT INTO Staff VALUES(400000000, 'Jeanelle', 'Scoles', 'Female', 'Jeanelle@gta.com', 
					'2392 Creek Road East Haven, CT 06512', '8228843304', 'Ticketing Staff', 'Sell tickets')
				""")

	cur.execute("""
				INSERT INTO Staff VALUES(500000000, 'Jama', 'Bui', 'Female', 'jama@tell.org', 
					'6579 Jefferson Avenue Bethlehem, PA 18015', '8992646412', 'Cleaning Staff', 
					'Maintain the cinema clean')
				""")

	cur.execute("""
				INSERT INTO Staff VALUES(600000000, 'Larita', 'Pelkey', 'Female', 'lari@z.net', 
					'8932 Williams Street Nampa, ID 83651', '8333421500', 'Snack Service Provider', 'Sell snack')
				""")

	cur.execute("""
				INSERT INTO Staff VALUES(700000000, 'Eden', 'Bolds', 'Female', 'eden@v.com', 
					'661 Cemetery Road Camden, NJ 08105', '8994894732', 'Security', 'Secure the cinema')
				""")

	cur.execute("""
				INSERT INTO Staff VALUES(800000000, 'Cletus', 'Sandlin', 'Male', 'cle@gmail.com', 
					'674 Surrey Lane Cumberland, RI 02864', '8331685735', 'Manager', 'Manage the cinema')
				""")

	cur.execute("""
				INSERT INTO Staff VALUES(900000000, 'Jacqueline', 'Barrier', 'Female', 'jac@coke.com', 
					'404 Grand Avenue Emporia, KS 66801', '8990964080', 'Cleaning Staff', 
					'Maintain the cinema clean')
				""")


	# insert Favorite_Type
	cur.execute("""
				INSERT INTO Favorite_Type VALUES('jim', 'Action')
				""")

	cur.execute("""
				INSERT INTO Favorite_Type VALUES('rose', 'Action')
				""")

	cur.execute("""
				INSERT INTO Favorite_Type VALUES('beth', 'Thriller')
				""")

	cur.execute("""
				INSERT INTO Favorite_Type VALUES('todd', 'Thriller')
				""")

	cur.execute("""
				INSERT INTO Favorite_Type VALUES('barb', 'Sci-Fi')
				""")

	cur.execute("""
				INSERT INTO Favorite_Type VALUES('christ', 'Sci-Fi')
				""")

	#insert Favorite_Theater
	cur.execute("""
				INSERT INTO Favorite_Theater VALUES('jim', '322 E Illinois St, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Favorite_Theater VALUES('rose', '322 E Illinois St, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Favorite_Theater VALUES('beth', '600 E Grand Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Favorite_Theater VALUES('todd', '600 E Grand Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Favorite_Theater VALUES('barb', '600 N Michigan Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Favorite_Theater VALUES('christ', '600 N Michigan Ave, Chicago, IL 60611')
				""")


	#insert Credit_Card
	cur.execute("""
				INSERT INTO Credit_Card VALUES(4929637849664726, 'James Bond', 'Visa', 2019-11-10)
				""")

	cur.execute("""
				INSERT INTO Credit_Card VALUES(4929775567183634, 'Rose Mond', 'Visa', 2020-11-10)
				""")

	cur.execute("""
				INSERT INTO Credit_Card VALUES(4556230768885439, 'Beth Watson', 'Visa', 2021-11-10)
				""")

	cur.execute("""
				INSERT INTO Credit_Card VALUES(5285895035979127, 'Todd Adams', 'Mastercard', 2022-11-10)
				""")

	cur.execute("""
				INSERT INTO Credit_Card VALUES(5511882275137000, 'Barbara Blais', 'Mastercard', 2023-11-10)
				""")

	cur.execute("""
				INSERT INTO Credit_Card VALUES(5356074708175520, 'Christine Smith', 'Mastercard', 2024-11-10)
				""")

	#insert Own
	cur.execute("""
				INSERT INTO Own VALUES('jim', 4929637849664726)
				""")

	cur.execute("""
				INSERT INTO Own VALUES('rose', 4929775567183634)
				""")

	cur.execute("""
				INSERT INTO Own VALUES('beth', 4556230768885439)
				""")

	cur.execute("""
				INSERT INTO Own VALUES('todd', 5285895035979127)
				""")

	cur.execute("""
				INSERT INTO Own VALUES('barb', 5511882275137000)
				""")

	cur.execute("""
				INSERT INTO Own VALUES('christ', 5356074708175520)
				""")


	#insert Employed_By

	cur.execute("""
				INSERT INTO Employed_By VALUES(100000000, '322 E Illinois St, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Employed_By VALUES(200000000, '322 E Illinois St, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Employed_By VALUES(300000000, '322 E Illinois St, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Employed_By VALUES(400000000, '600 E Grand Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Employed_By VALUES(500000000, '600 E Grand Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Employed_By VALUES(600000000, '600 E Grand Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Employed_By VALUES(700000000, '600 N Michigan Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Employed_By VALUES(800000000, '600 N Michigan Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Employed_By VALUES(900000000, '600 N Michigan Ave, Chicago, IL 60611')
				""")

	#insert Members_of
	cur.execute("""
				INSERT INTO Members_of VALUES('jim', '322 E Illinois St, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Members_of VALUES('rose', '322 E Illinois St, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Members_of VALUES('beth', '600 E Grand Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Members_of VALUES('todd', '600 E Grand Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Members_of VALUES('barb', '600 N Michigan Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Members_of VALUES('christ', '600 N Michigan Ave, Chicago, IL 60611')
				""")

	#insert Working_Schedule, each theater has 3 values
	cur.execute("""
				INSERT INTO Working_Schedule VALUES('2015-11-9', 100000000, 
					'Security', '322 E Illinois St, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Working_Schedule VALUES('2015-11-9', 200000000, 
					'Management', '322 E Illinois St, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Working_Schedule VALUES('2015-11-9', 300000000, 
					'Box Office', '322 E Illinois St, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Working_Schedule VALUES('2015-11-10', 400000000, 
					'Security', '600 E Grand Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Working_Schedule VALUES('2015-11-11', 500000000, 
					'Management', '600 E Grand Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Working_Schedule VALUES('2015-11-11', 600000000, 
					'Box Office', '600 E Grand Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Working_Schedule VALUES('2015-11-12', 700000000, 
					'Security', '600 N Michigan Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Working_Schedule VALUES('2015-11-13', 800000000, 
					'Management', '600 N Michigan Ave, Chicago, IL 60611')
				""")

	cur.execute("""
				INSERT INTO Working_Schedule VALUES('2015-11-13', 900000000, 
					'Box Office', '600 N Michigan Ave, Chicago, IL 60611')
				""")

	#insert Movie_Schedule
	cur.execute("""
				INSERT INTO Movie_Schedule VALUES('2015-11-13', 'Crouching Tiger, Hidden Dragon', 
					'322 E Illinois St, Chicago, IL 60611', 2001, 0.8, 15, 300, 50)
				""")

	cur.execute("""
				INSERT INTO Movie_Schedule VALUES('2015-11-14', 'Gone Girl', 
					'600 E Grand Ave, Chicago, IL 60611', 2014, 0.5, 14, 500, 200)
				""")

	cur.execute("""
				INSERT INTO Movie_Schedule VALUES('2015-11-15', 'Interstellar', 
					'600 N Michigan Ave, Chicago, IL 60611', 2014, 0.9, 12, 400, 100)
				""")

	#insert Comments. 72 comments. 4 comments for each review.
	#1st thread
	cur.execute("""
				INSERT INTO Comments VALUES('rose', '2015-12-1 15:30:26', 
					'I agree.', 'jim', '2015-11-1 15:30:26')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('beth', '2015-12-1 16:30:26', 
					'Totally agree with you.', 'jim', '2015-11-1 15:30:26')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('todd', '2015-12-1 17:30:26', 
					'You rate it too high.', 'jim', '2015-11-1 15:30:26')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('barb', '2015-12-1 18:30:26', 
					'If I were you I will give it 8/10.', 'jim', '2015-11-1 15:30:26')
				""")

	#2nd 
	cur.execute("""
				INSERT INTO Comments VALUES('beth', '2015-12-2 08:46:11', 
					'It''s not that bad.', 'rose', '2015-11-2 08:46:11')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('todd', '2015-12-2 09:46:11', 
					'Really a piece of junk.', 'rose', '2015-11-2 08:46:11')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('barb', '2015-12-2 10:46:11', 
					'Not that bad, but in some degree I agree with you.', 'rose', '2015-11-2 08:46:11')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('christ', '2015-12-2 11:46:11', 
					'I wish I cound give it lower.', 'rose', '2015-11-2 08:46:11')
				""")

	#3rd
	cur.execute("""
				INSERT INTO Comments VALUES('todd', '2015-12-3 21:01:30', 
					'Indeed.', 'beth', '2015-11-3 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('barb', '2015-12-3 22:01:30', 
					'I wound give it high score.', 'beth', '2015-11-3 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('christ', '2015-12-3 23:01:30', 
					'It''s a decent score for this movie.', 'beth', '2015-11-3 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('jim', '2015-12-3 23:02:30', 
					'IMO, it''s not that awesome.', 'beth', '2015-11-3 20:01:30')
				""")

	#4th
	cur.execute("""
				INSERT INTO Comments VALUES('barb', '2015-12-4 20:01:30', 
					'It''s not a good one.', 'todd', '2015-11-4 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('christ', '2015-12-4 20:02:30', 
					'Just so so.', 'todd', '2015-11-4 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('jim', '2015-12-4 20:03:30', 
					'I won''t recommend it too.', 'todd', '2015-11-4 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('rose', '2015-12-4 20:04:30', 
					'I will do the same thing.', 'todd', '2015-11-4 20:01:30')
				""")

	#5th
	cur.execute("""
				INSERT INTO Comments VALUES('christ', '2015-12-5 20:01:30', 
					'I will give it 0/10', 'barb', '2015-11-5 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('jim', '2015-12-5 20:02:30', 
					'I agree with christ.', 'barb', '2015-11-5 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('rose', '2015-12-5 20:03:30', 
					'Agreed.', 'barb', '2015-11-5 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('beth', '2015-12-5 20:04:30', 
					'It''s even worse. Not worth to the score you give.', 
					'barb', '2015-11-5 20:01:30')
				""")

	#6th
	cur.execute("""
				INSERT INTO Comments VALUES('jim', '2015-12-6 20:01:30', 
					'Totally agree.', 'christ', '2015-11-6 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('rose', '2015-12-6 20:02:30', 
					'I would choose another movie to watch.', 
					'christ', '2015-11-6 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('beth', '2015-12-6 20:03:30', 
					'I was planning to watch, now I change my mind.', 
					'christ', '2015-11-6 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('todd', '2015-12-6 20:04:30', 
					'3/10. That is the highest score I can give, lol.', 
					'christ', '2015-11-6 20:01:30')
				""")

	#7th
	cur.execute("""
				INSERT INTO Comments VALUES('rose', '2015-12-7 20:01:30', 
					'Good score for this one.', 'jim', '2015-11-7 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('beth', '2015-12-7 20:02:30', 
					'I agree with rose.', 'jim', '2015-11-7 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('todd', '2015-12-7 20:03:30', 
					'Up you go.', 'jim', '2015-11-7 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('barb', '2015-12-7 20:04:30', 
					'Same score here.', 'jim', '2015-11-7 20:01:30')
				""")

	#8th
	cur.execute("""
				INSERT INTO Comments VALUES('beth', '2015-12-8 20:01:30', 
					'Why do you say that?', 'rose', '2015-11-8 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('todd', '2015-12-8 20:02:30', 
					'Why?', 'rose', '2015-11-8 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('barb', '2015-12-8 20:03:30', 
					'Please add some reasons.', 'rose', '2015-11-8 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('christ', '2015-12-8 20:04:30', 
					'I didn''t watch this, come back later.', 
					'rose', '2015-11-8 20:01:30')
				""")

	#9
	cur.execute("""
				INSERT INTO Comments VALUES('todd', '2015-12-9 20:01:30', 
					'I love this movie.', 'beth', '2015-11-9 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('barb', '2015-12-9 20:02:30', 
					'Awesome movie, should watch it again.', 
					'beth', '2015-11-9 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('christ', '2015-12-9 20:03:30', 
					'I do agree.', 'beth', '2015-11-9 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('jim', '2015-12-9 20:04:30', 
					'Up you go!!', 'beth', '2015-11-9 20:01:30')
				""")

	#10
	cur.execute("""
				INSERT INTO Comments VALUES('barb', '2015-12-10 20:01:30', 
					'No scores?', 'todd', '2015-11-10 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('christ', '2015-12-10 20:02:30', 
					'Aha, you forgot to add scores.', 'todd', '2015-11-10 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('jim', '2015-12-10 20:03:30', 
					'I think no score is OK.', 'todd', '2015-11-10 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('rose', '2015-12-10 20:04:30', 
					'jim, I agree with you.', 'todd', '2015-11-10 20:01:30')
				""")

	#11
	cur.execute("""
				INSERT INTO Comments VALUES('christ', '2015-12-11 20:01:30', 
					'Yes, it is.', 'barb', '2015-11-11 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('jim', '2015-12-11 20:02:30', 
					'It has a great service too.', 'barb', '2015-11-11 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('rose', '2015-12-11 20:03:30', 
					'jim, up you go.', 'barb', '2015-11-11 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('beth', '2015-12-11 20:04:30', 
					'Upvote!', 'barb', '2015-11-11 20:01:30')
				""")

	#12
	cur.execute("""
				INSERT INTO Comments VALUES('jim', '2015-12-12 20:01:30', 
					'I would love too.', 'christ', '2015-11-12 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('rose', '2015-12-12 20:02:30', 
					'Indeed.', 'christ', '2015-11-12 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('beth', '2015-12-12 20:03:30', 
					'A wonderful place to watch movie.', 
					'christ', '2015-11-12 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('todd', '2015-12-12 20:04:30', 
					'10/10 for recommendation.', 'christ', '2015-11-12 20:01:30')
				""")

	#13
	cur.execute("""
				INSERT INTO Comments VALUES('rose', '2015-12-13 20:01:30', 
					'What did you expecte?', 'jim', '2015-11-13 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('beth', '2015-12-13 20:02:30', 
					'Same question as above.', 'jim', '2015-11-13 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('todd', '2015-12-13 20:03:30', 
					'Me too.', 'jim', '2015-11-13 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('barb', '2015-12-13 20:04:30', 
					'I guess no one will notice this thread.', 
					'jim', '2015-11-13 20:01:30')
				""")

	#14
	cur.execute("""
				INSERT INTO Comments VALUES('beth', '2015-12-14 20:01:30', 
					'I agree.', 'rose', '2015-11-14 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('todd', '2015-12-14 20:02:30', 
					'Up you go.', 'rose', '2015-11-14 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('barb', '2015-12-14 20:03:30', 
					'Up.', 'rose', '2015-11-14 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('christ', '2015-12-14 20:04:30', 
					'Upvote.', 'rose', '2015-11-14 20:01:30')
				""")

	#15
	cur.execute("""
				INSERT INTO Comments VALUES('todd', '2015-12-15 20:01:30', 
					'I love it too!', 'beth', '2015-11-15 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('barb', '2015-12-15 20:02:30', 
					'The popcorn is awesome!', 'beth', '2015-11-15 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('christ', '2015-12-15 20:03:30', 
					'I guess there are punch of people came here just for popcorn.', 
					'beth', '2015-11-15 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('jim', '2015-12-15 20:04:30', 
					'christ, up you go!', 'beth', '2015-11-15 20:01:30')
				""")

	#16
	cur.execute("""
				INSERT INTO Comments VALUES('barb', '2015-12-16 20:01:30', 
					'Upvote', 'todd', '2015-11-16 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('christ', '2015-12-16 20:02:30', 
					'I agree.', 'todd', '2015-11-16 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('jim', '2015-12-16 20:03:30', 
					'Really? I will try it later.', 'todd', '2015-11-16 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('rose', '2015-12-16 20:04:30', 
					'It''s the best theater I have visited!', 
					'todd', '2015-11-16 20:01:30')
				""")

	#17
	cur.execute("""
				INSERT INTO Comments VALUES('christ', '2015-12-17 20:01:30', 
					'Same here.', 'barb', '2015-11-17 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('jim', '2015-12-17 20:02:30', 
					'I don''t think so.', 'barb', '2015-11-17 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('rose', '2015-12-17 20:03:30', 
					'I won''t do that.', 'barb', '2015-11-17 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('beth', '2015-12-17 20:04:30', 
					'I will recommend.', 'barb', '2015-11-17 20:01:30')
				""")

	#18
	cur.execute("""
				INSERT INTO Comments VALUES('jim', '2015-12-18 20:01:30', 
					'I dislike this place.', 'christ', '2015-11-18 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('rose', '2015-12-18 20:02:30', 
					'I agree with jim.', 'christ', '2015-11-18 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('beth', '2015-12-18 20:03:30', 
					'Why do you say that?', 'christ', '2015-11-18 20:01:30')
				""")

	cur.execute("""
				INSERT INTO Comments VALUES('todd', '2015-12-18 20:04:30', 
					'I hope poster would give some reasons.', 
					'christ', '2015-11-18 20:01:30')
				""")


	con.commit()

if __name__ == "__main__":
	createDB()
	insertDB()