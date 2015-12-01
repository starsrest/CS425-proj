import sqlalchemy

engine = sqlalchemy.create_engine('oracle://ypu1:YCsBUo3...uK3Y15@fourier.cs.iit.edu:1521/orcl')
conn = engine.connect()

conn.execute('CREATE TABLE Movies(\
year INT NOT NULL,\
title VARCHAR(40) NOT NULL,\
genre VARCHAR(20) NOT NULL,\
length INT NOT NULL,\
director VARCHAR(40) NOT NULL,\
description VARCHAR(255) NOT NULL)')

conn.execute('CREATE TABLE StarsIn(\
year INT NOT NULL,\
title VARCHAR(40) NOT NULL,\
star_name VARCHAR(40) NOT NULL)')

conn.execute('CREATE TABLE Members(\
username VARCHAR(20) PRIMARY KEY,\
password VARCHAR(20) NOT NULL,\
reward VARCHAR(40) NOT NULL,\
f_name VARCHAR(20) NOT NULL,\
l_name VARCHAR(20) NOT NULL,\
gender VARCHAR(20) NOT NULL,\
email VARCHAR(40) NOT NULL,\
address VARCHAR(255) NOT NULL,\
phone CHAR(20) NOT NULL,\
status VARCHAR(20) NOT NULL,\
points INT NOT NULL)')

conn.execute('CREATE TABLE Reviews(\
username VARCHAR(20) UNIQUE,\
time TIMESTAMP NOT NULL,\
type VARCHAR(20) NOT NULL,\
content VARCHAR(255) NOT NULL,\
visits INT NOT NULL)')

conn.execute('CREATE TABLE Theaters(\
address VARCHAR(40) PRIMARY KEY,\
name VARCHAR(40) NOT NULL,\
company VARCHAR(40) NOT NULL,\
number_of_screens INT NOT NULL)')

conn.execute('CREATE TABLE Review_of_Movies(\
year INT NOT NULL,\
title VARCHAR(40) NOT NULL,\
username VARCHAR(20) NOT NULL,\
time TIMESTAMP NOT NULL)')

conn.execute('CREATE TABLE Review_of_Theaters(\
address VARCHAR(40) NOT NULL,\
username VARCHAR(20) NOT NULL,\
time TIMESTAMP NOT NULL)')

conn.execute('CREATE TABLE Staff(\
ssn INT PRIMARY KEY,\
f_name VARCHAR(20) NOT NULL,\
l_name VARCHAR(20) NOT NULL,\
gender VARCHAR(20) NOT NULL,\
email VARCHAR(40) NOT NULL,\
address VARCHAR(255) NOT NULL,\
phone CHAR(20) NOT NULL,\
job_type VARCHAR(20) NOT NULL,\
description_of_duty VARCHAR(255) NOT NULL)')

conn.execute('CREATE TABLE Favorite_Type(\
username VARCHAR(20) NOT NULL,\
type VARCHAR(20) NOT NULL)')

conn.execute('CREATE TABLE Favorite_Theater(\
username VARCHAR(20) NOT NULL,\
theater_address VARCHAR(40) NOT NULL)')

conn.execute('CREATE TABLE Credit_Card(\
card_number INT PRIMARY KEY,\
holder_name VARCHAR(40) NOT NULL,\
type VARCHAR(20) NOT NULL,\
expiration_time DATE NOT NULL)')

conn.execute('CREATE TABLE Own(\
username VARCHAR(20) NOT NULL,\
card_number INT NOT NULL)')

conn.execute('CREATE TABLE Employed_By(\
ssn INT NOT NULL,\
theater_address VARCHAR(40) NOT NULL)')

conn.execute('CREATE TABLE Members_of(\
username VARCHAR(20) NOT NULL,\
theater_address VARCHAR(40) NOT NULL)')

conn.execute('CREATE TABLE Working_Schedule(\
time DATE NOT NULL,\
ssn INT NOT NULL,\
assignment VARCHAR(100) NOT NULL,\
work_at VARCHAR(40) NOT NULL)')

conn.execute('CREATE TABLE Movie_Schedule(\
time TIMESTAMP NOT NULL,\
movie_title VARCHAR(40) NOT NULL,\
theater_address VARCHAR(40) NOT NULL,\
movie_year INT NOT NULL,\
discount REAL NOT NULL,\
price REAL NOT NULL,\
total_ticket INT NOT NULL,\
sold_ticket INT NOT NULL)')

conn.execute('CREATE TABLE Comments(\
username VARCHAR(20) NOT NULL,\
time TIMESTAMP NOT NULL,\
content VARCHAR(255) NOT NULL,\
review_username VARCHAR(20) NOT NULL,\
review_time TIMESTAMP NOT NULL)')