--JIACHENG LI CS425 HW2

CREATE TABLE Movies(
  year INT,
  title VARCHAR(40),
  genre VARCHAR(20) NOT NULL,
  length INT NOT NULL,
  director VARCHAR(40) NOT NULL,
  description VARCHAR(255) NOT NULL,
  PRIMARY KEY (year, title)
);

CREATE TABLE Stars(
  year INT,
  title VARCHAR(40),
  star_name VARCHAR(40),
  PRIMARY KEY (year, title, star_name)
);

CREATE TABLE Members(
  username VARCHAR(20) PRIMARY KEY,
  password VARCHAR(20) NOT NULL,
  reward VARCHAR(40) NOT NULL,
  f_name VARCHAR(20) NOT NULL,
  l_name VARCHAR(20) NOT NULL,
  gender VARCHAR(20) NOT NULL,
  email VARCHAR(40) NOT NULL,
  address VARCHAR(255) NOT NULL,
  phone CHAR(20) NOT NULL,
  status VARCHAR(20) NOT NULL,
  points INT NOT NULL
);

CREATE TABLE Reviews(
  username VARCHAR(20) REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,
  time TIMESTAMP NOT NULL,
  type VARCHAR(20) NOT NULL,
  content VARCHAR(255) NOT NULL,
  visits INT NOT NULL,
  PRIMARY KEY (username, time)
);

CREATE TABLE Theaters(
  address VARCHAR(40) PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  company VARCHAR(40) NOT NULL,
  number_of_screens INT NOT NULL
);

CREATE TABLE Review_of_Movies(
  year INT REFERENCES Movies(year) ON DELETE SET NULL ON UPDATE CASCADE,
  title VARCHAR(40) REFERENCES Movies(title) ON DELETE SET NULL ON UPDATE CASCADE,
  username VARCHAR(20) REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,
  time TIMESTAMP REFERENCES Reviews(time) ON DELETE SET NULL ON UPDATE CASCADE,
  PRIMARY KEY (year, title, username, time)
);

CREATE TABLE Review_of_Theaters(
  address VARCHAR(40) REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE,
  username VARCHAR(20) REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,
  time TIMESTAMP REFERENCES Reviews(time) ON DELETE SET NULL ON UPDATE CASCADE,
  PRIMARY KEY (address, username, time)
);

CREATE TABLE Staff(
  ssn INT PRIMARY KEY,
  f_name VARCHAR(20) NOT NULL,
  l_name VARCHAR(20) NOT NULL,
  gender VARCHAR(20) NOT NULL,
  email VARCHAR(40) NOT NULL,
  address VARCHAR(255) NOT NULL,
  phone CHAR(20) NOT NULL,
  job_type VARCHAR(20) NOT NULL,
  description_of_duty VARCHAR(255) NOT NULL
);

CREATE TABLE Favorite_Type(
  username VARCHAR(20) REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,
  type VARCHAR(20),
  PRIMARY KEY(username, type)
);

CREATE TABLE Favorite_Theater(
  username VARCHAR(20) REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,
  theater_address VARCHAR(40) REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE,
  PRIMARY KEY(username, theater_address)
);

CREATE TABLE Credit_Card(
  card_number INT PRIMARY KEY,
  holder_name VARCHAR(40) NOT NULL,
  type VARCHAR(20) NOT NULL,
  expiration_time DATE NOT NULL
);

--relation
CREATE TABLE Own(
  username VARCHAR(20) REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,
  card_number INT REFERENCES Credit_Card(card_number) ON DELETE SET NULL ON UPDATE CASCADE,
  PRIMARY KEY(username, card_number)
);

--relation
CREATE TABLE Employed_By(
  ssn INT PRIMARY KEY REFERENCES Staff(ssn) ON DELETE SET NULL ON UPDATE CASCADE,
  theater_address VARCHAR(40) REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE
);

--relation
CREATE TABLE Members_of(
  username VARCHAR(20) PRIMARY KEY REFERENCES Members(username) ON DELETE SET NULL,
  theater_address VARCHAR(40) REFERENCES Theaters(address) ON DELETE SET NULL
);

--weak entity
CREATE TABLE Working_Schedule(
  time DATE NOT NULL,
  ssn INT REFERENCES Staff(ssn) ON DELETE SET NULL ON UPDATE CASCADE,
  assignment VARCHAR(100) NOT NULL,
  work_at VARCHAR(40) REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE,
  PRIMARY KEY(time, ssn, work_at)
);

--weak entity
CREATE TABLE Movie_Schedule(
  time TIMESTAMP NOT NULL,
  movie_title VARCHAR(40) REFERENCES Movies(title) ON DELETE SET NULL ON UPDATE CASCADE,
  theater_address VARCHAR(40) REFERENCES Theaters(address) ON DELETE SET NULL ON UPDATE CASCADE,
  movie_year INT REFERENCES Movies(year) ON DELETE SET NULL ON UPDATE CASCADE,
  discount REAL NOT NULL,
  price REAL NOT NULL,
  total_ticket INT NOT NULL,
  sold_ticket INT NOT NULL,
  PRIMARY KEY(time, movie_title, theater_address, movie_year)
);

CREATE TABLE Comments(
  username VARCHAR(20) REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,
  time TIMESTAMP NOT NULL,
  content VARCHAR(255) NOT NULL,
  reviews_username REFERENCES Members(username) ON DELETE SET NULL ON UPDATE CASCADE,
  review_time REFERENCES Reviews(time)ON DELETE SET NULL ON UPDATE CASCADE,
  PRIMARY KEY(username, time)
);


