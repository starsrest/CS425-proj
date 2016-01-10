from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3
import re
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Set session secret key
app.secret_key = 'catch_me_if_you_can'

# Route '/' and '/index' to `index`
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', username=session.get('username'))

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST': 
        _username = request.form['username']
        _password = request.form['password']
        _email = request.form['email']

        if _username and _password and _email: # all fieled received
            conn = sqlite3.connect('ticketing_database.sqlite3')
            cur = conn.cursor()

            # check if the username is taken
            cur.execute('SELECT * FROM Members WHERE username=?', (_username, )) 
            if cur.fetchone():
                flash('This username is taken!')
            else: # store the user info into database
                cur.execute('INSERT INTO Members (username, password, email) VALUES (?, ?, ?)', (_username, _password, _email))
                conn.commit()

                session['username'] = _username
                flash('Welcome! You have created a new account!')
                return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    _name = request.form['inputName']
    _password = request.form['inputPassword']

    conn = sqlite3.connect('ticketing_database.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT username, password FROM Members WHERE username = ? AND\
                password = ?', (_name, _password))

    if cur.fetchone() is None: # check if this user exists
        flash('Incorrect password!')    
    else:
        session['username'] = _name
        flash('Welcome back!')
        
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You were successfully logged out!')
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html', username=session.get('username'))

@app.route('/profile')
def profile():
    if session.get('username'):
        conn = sqlite3.connect('ticketing_database.sqlite3')
        cur = conn.cursor()
        cur.execute('SELECT username, password, f_name, l_name, gender, email, address, phone, points, status, reward FROM Members WHERE username=?', (session['username'], ))
        [_username, _password, _firstName, _lastName, _gender, _email, _address, _phone, _points, _status, _reward] = cur.fetchone()

        cur.execute('SELECT card_number, holder_name, type, expiration_time FROM Credit_Card WHERE holder_name=?', (_username, ))
        card = cur.fetchone()
        if card:
            _cardNumber, _holderName, _cardType, _expirationDate = card
            _creditCard = {"number":_cardNumber, "holder":_holderName, "cardType":_cardType, "expirationDate":_expirationDate}
        else:
            _creditCard = card
        return render_template('profile.html',
                                username=_username, 
                                password=_password, 
                                firstName=_firstName, 
                                lastName=_lastName, 
                                gender=_gender, 
                                email=_email, 
                                address=_address, 
                                phone=_phone, 
                                points=_points, 
                                status=_status, 
                                reward=_reward,
                                creditCard=_creditCard )
    else: # if user is not logged in
        flash('Please sign in before accessing your profile!')
        return render_template('index.html')

@app.route('/addCreditCard', methods=['GET', 'POST'])
def addCreditCard():
    if request.method == 'POST':
        _cardNumber = request.form['cardNumber']
        _holderName = request.form['holderName']
        _cardType = request.form['cardType']
        _expirationDate = request.form['expirationDate']

        conn = sqlite3.connect('ticketing_database.sqlite3')
        cur = conn.cursor()

        cur.execute('INSERT INTO Credit_Card (card_number, holder_name, type, expiration_date) VALUES (?, ?, ?, ?)', (_cardNumber, _holderName, _cardType, _expirationDate))
        conn.commit()
        flash('You"ve successfully added a credit card')
        return redirect(url_for('profile'))

    else:
        return render_template('addCreditCard.html')

@app.route('/schedule')
def schedule():
    conn = sqlite3.connect('ticketing_database.sqlite3')
    cur = conn.cursor()

    cur.execute('SELECT time, movie_title, name, address, price, discount FROM Movie_Schedule NATURAL JOIN\
        Theaters')
    movies = cur.fetchall()
    return render_template('schedule.html', username=session.get('username'), movies=movies)
    

@app.route('/editProfile', methods=['GET', 'POST'])
def editProfile():
    if request.method == 'POST':
        _phone = request.form['phone']
        _email = request.form['email']
        _address = request.form['address']

        if not _phone and not _email and not _address:
            flash('You must fill in at least one filed!')
            return redirect(url_for('editProfile'))

        conn = sqlite3.connect('ticketing_database.sqlite3')
        cur = conn.cursor()

        if _phone: # if user filled in phone number
            cur.execute('UPDATE Members SET phone=? WHERE username=?', (_phone, session['username']))
        if _email:
            cur.execute('UPDATE Members SET email=? WHERE username=?', (_email, session['username']))
        if _address:
            cur.execute('UPDATE Members SET address=? WHERE username=?', (_address, session['username']))
        conn.commit()
        flash('Your profile has been updated.')

        return redirect(url_for('profile'))

    return render_template('editProfile.html')

@app.route('/checkout', methods=['POST'])
def checkout():
    _movie = request.form['movieSelected']

    _movie = str(_movie) # convert from unicode to string
    
    split = re.findall("u\'(.*?)\'", _movie)
    movie = {}
    movie['time']= split[0]
    movie['title']= split[1]
    movie['theater']= split[2]
    movie['location']=split[3]

    split = re.findall('[0-9.]+', _movie)
    movie['listprice'] = split[-2]
    movie['discount'] = str(int(float(split[-1]) * 100)) + '%' # convert from string to int
    movie['price'] = float(split[-2]) * float(split[-1])

    if session.get('username'): # if user has logged in
        return render_template('ticket.html', username=session['username'], movie=movie)
    else:
        session['movie'] = movie
        return render_template('checkoutGuest.html')

@app.route('/checkoutGuest', methods=['POST'])
def checkoutGuest():
    return render_template('ticket.html', movie=session.get('movie'))

@app.route('/discussion')
def discussion():
    return render_template('discussionEntry.html', username=session.get('username'))


@app.route('/movieDiscussion', methods=['GET', 'POST']) # movie forum
def movieDiscussion():
    conn = sqlite3.connect("ticketing_database.sqlite3")
    cur = conn.cursor()

    if request.method == 'POST':
        _titleYear = request.form['movieTitleYear']
        _title, _year= _titleYear.split('-')
        _star = request.form['movieStar']
        _director = request.form['movieDirector']
        cur.execute('SELECT * FROM Movies NATURAL JOIN Stars WHERE title=? AND director=? AND star_name=?', (_title, _director, _star))
        if cur.fetchone(): # if the movie-star-director combination is valid
            _review = request.form['review']
            cur.execute('INSERT INTO Review_of_Movies (year, title, username, time, content) VALUES(?, ?, ?, ?, ?)', (_year, _title, session.get('username'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), _review))
            
            flash('You have started a new thread!')
            
            conn.commit()
        else:
            flash('Invalid movie-star-director combination!')
    
    # reviews table
    _loggedIn = (session.get('username') is not None)
    cur.execute('SELECT title, content, username, time FROM Review_of_Movies ORDER BY datetime(time) DESC')
    _threads = cur.fetchall()

    # start a new thread
    cur.execute('SELECT title, year, director FROM Movies')
    _titlesYears = {}
    _directors = []
    for row in cur:
        _titlesYears[str(row[0])] = str(row[1])
        _directors.append(str(row[2]))

    cur.execute('SELECT star_name FROM Stars')
    _stars = []
    for row in cur:
        _stars.append(str(row[0]))

    return render_template('movieDiscussion.html',
                            username=session.get('username'),
                            threads=_threads,
                            loggedIn=_loggedIn,
                            titlesYears=_titlesYears,
                            stars=_stars,
                            directors = _directors)

@app.route('/theaterDiscussion', methods=['GET', 'POST']) # movie forum
def theaterDiscussion():
    conn = sqlite3.connect("ticketing_database.sqlite3")
    cur = conn.cursor()

    if request.method == 'POST':
        _nameLocation = request.form['nameLocation']
        _name, _location= _nameLocation.split('-')
    
        _review = request.form['review']
        cur.execute('INSERT INTO Review_of_Theaters (address, username, time, content) VALUES(?, ?, ?, ?)', (_location, session.get('username'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), _review))
    
        # award 5 points for review
        flash('You have started a new thread!') 

        conn.commit()

    # reviews table
    _loggedIn = (session.get('username') is not None)
    cur.execute('SELECT name, address, content, username, time FROM Review_of_Theaters NATURAL JOIN Theaters ORDER BY datetime(time) DESC')
    _threads = cur.fetchall()

    # start a new thread
    cur.execute('SELECT name, address FROM Theaters')
    _theaters = {}
    for row in cur:
        _theaters[str(row[0])] = str(row[1])

    return render_template('theaterDiscussion.html',
                            username=session.get('username'),
                            threads=_threads,
                            loggedIn=_loggedIn,
                            theaters=_theaters,)


@app.route('/thread')
def thread():
    _reviewUser = request.args.get('reviewUser')
    _reviewTime = request.args.get('reviewTime')
    _review = request.args.get('reviewContent')

    conn = sqlite3.connect('ticketing_database.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT username, time, content FROM Comments WHERE review_username=? AND review_time=?', (_reviewUser, _reviewTime))
    _comments = cur.fetchall()
    
    return render_template('thread.html',
                            username=session.get('username'), 
                            review=_review,
                            reviewUser=_reviewUser,
                            reviewTime=_reviewTime,
                            comments=_comments)


# Run
if __name__ == '__main__':
    app.run(debug=True)