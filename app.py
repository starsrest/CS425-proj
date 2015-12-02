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
        _firstName = request.form['firstName']
        _lastName = request.form['lastName']
        _email = request.form['email']
        _address = request.form['address']
        _phone = request.form['phone']
        _gender = request.form['gender']

        if _username and _password and _firstName and _lastName and _email and _address and _phone and _gender: # all fieled get filled
            conn = sqlite3.connect('ticket_management.sqlite3')
            cur = conn.cursor()

            # check if username is taken
            cur.execute('SELECT * FROM Members WHERE username=?', (_username, )) 
            if cur.fetchone():
                flash('This username is taken!')
            else: # store the user info into database
                cur.execute('INSERT INTO Members (username, password, f_name, l_name, gender, email, address, phone, status, points, reward) \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (_username, _password, _firstName, _lastName, _gender, _email, _address, _phone, "SILVER", 0, "none"))
                conn.commit()

                session['username'] = _username
                flash('Welcome! You have created a new account!')
                return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    _name = request.form['inputName']
    _password = request.form['inputPassword']

    conn = sqlite3.connect('ticket_management.sqlite3')
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
        conn = sqlite3.connect('ticket_management.sqlite3')
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

        conn = sqlite3.connect('ticket_management.sqlite3')
        cur = conn.cursor()

        cur.execute('INSERT INTO Credit_Card (card_number, holder_name, type, expiration_date) VALUES (?, ?, ?, ?)', (_cardNumber, _holderName, _cardType, _expirationDate))
        conn.commit()
        flash('You"ve successfully added a credit card')
        return redirect(url_for('profile'))

    else:
        return render_template('addCreditCard.html')

@app.route('/schedule')
def schedule():
    conn = sqlite3.connect('ticket_management.sqlite3')
    cur = conn.cursor()

    cur.execute('SELECT time, movie_title, name, address, price, discount FROM Movie_Schedule NATURAL JOIN\
        Theaters')
    movies = cur.fetchall()
    return render_template('schedule.html', username=session.get('username'), movies=movies)
    

@app.route('/editProfile', methods=['GET', 'POST'])
def editProfile():
    if request.method == 'POST':
        _phone = request.form['phone']

        conn = sqlite3.connect('ticket_management.sqlite3')
        cur = conn.cursor()

        cur.execute('UPDATE Members SET phone=? WHERE username=?', (_phone, session['username']))
        conn.commit()
        flash('Your phone number has been modified.')

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
    conn = sqlite3.connect("ticket_management.sqlite3")
    cur = conn.cursor()

    if request.method == 'POST':
        _titleYear = request.form['movieTitleYear']
        _title, _year= _titleYear.split('-')
        _star = request.form['movieStar']
        _director = request.form['movieDirector']
        cur.execute('SELECT * FROM Movies NATURAL JOIN Stars WHERE title=? AND director=? AND star_name=?', (_title, _director, _star))
        if cur.fetchone(): # if the movie-star-director combination is valid
            _review = request.form['review']
            cur.execute('INSERT INTO Reviews (username, time, type, content) VALUES(?, ?, ?, ?)', (session.get('username'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Movie", _review))
            cur.execute('INSERT INTO Review_of_Movies (year, title, username, time) VALUES(?, ?, ?, ?)', (_year, _title, session.get('username'), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            flash('You have started a new thread! You''ve got 5 points')
            cur.execute('UPDATE Members SET points = (SELECT points FROM Members WHERE username=?) + 5 WHERE username=?', (session.get('username'), session.get('username'))) # get credit for writing review
            conn.commit()
        else:
            flash('Invalid movie-star-director combination!')
    
    # reviews table
    _loggedIn = (session.get('username') is not None)
    cur.execute('SELECT title, content, username, time FROM Reviews NATURAL JOIN Review_of_Movies ORDER BY datetime(time) DESC')
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
    conn = sqlite3.connect("ticket_management.sqlite3")
    cur = conn.cursor()

    if request.method == 'POST':
        _nameLocation = request.form['nameLocation']
        _name, _location= _nameLocation.split('-')
    
        _review = request.form['review']
        cur.execute('INSERT INTO Reviews (username, time, type, content) VALUES(?, ?, ?, ?)', (session.get('username'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Theater", _review))
        cur.execute('INSERT INTO Review_of_Theaters (address, username, time) VALUES(?, ?, ?)', (_location, session.get('username'), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
        # award 5 points for review
        flash('You have started a new thread! You''ve got 5 points') 
        cur.execute('UPDATE Members SET points = (SELECT points FROM Members WHERE username=?) + 5 WHERE username=?', (session.get('username'), session.get('username'))) # get credit for writing review
        conn.commit()

    # reviews table
    _loggedIn = (session.get('username') is not None)
    cur.execute('SELECT name, address, content, username, time FROM Reviews NATURAL JOIN Review_of_Theaters NATURAL JOIN Theaters ORDER BY datetime(time) DESC')
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

    conn = sqlite3.connect('ticket_management.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT username, time, content FROM Comments WHERE review_username=? AND review_time=?', (_reviewUser, _reviewTime))
    _comments = cur.fetchall()
    
    return render_template('thread.html',
                            username=session.get('username'), 
                            review=_review,
                            reviewUser=_reviewUser,
                            reviewTime=_reviewTime,
                            comments=_comments)

    
# -------------------------------------- Management View --------------------------------------

@app.route('/managementEntry', methods=['GET'])
def managementEntry():
    return render_template('managementEntry.html')

@app.route('/management_signin', methods=['POST'])
def management_signin():
    conn = sqlite3.connect('ticket_management.sqlite3')
    cur = conn.cursor()

    _ssn = request.form['ssn']
    job_type = cur.execute('SELECT job_type FROM Staff WHERE ssn=?', (_ssn, )).fetchone()[0]
    session['privilege'] = str(job_type)
    return redirect(url_for('management_view'))

@app.route('/management_view', methods=['GET', 'POST'])
def management_view():
    _privilege = session['privilege']    

    conn = sqlite3.connect('ticket_management.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT day, f_name, l_name, ssn, assignment, work_at FROM working_schedule NATURAL JOIN Staff')
    _latestAssignments = cur.fetchall()

    cur.execute('SELECT f_name, l_name, ssn, job_type FROM Staff')
    _staff = []
    for row in cur.fetchall():
        # _staff.append({'firstName':str(row[0]), 'lastName':str(row[1]), 'ssn':str(row[2]), 'jobType':str(row[3])})
        _staff.append( (str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + ' ' + str(row[3])) )

    _assignments = ['sell ticket', 'sell snack', 'clean the cinema', 'secure the cinema']

    cur.execute('SELECT address FROM theaters')
    _locations = []
    for row in cur.fetchall():
        _locations.append(row[0]) # extract theater address from tuple

    cur.execute('SELECT username, f_name, l_name, email, address, phone, status, points FROM Members')
    _memebers = cur.fetchall()

    return render_template('management_view.html',
                            privilege=_privilege,
                            staff=_staff,
                            assignments=_assignments,
                            locations=_locations,
                            latestAssignments=_latestAssignments,
                            members=_memebers)

@app.route('/assign_work', methods=['POST', ])
def assign_work():
    _date = request.form['d']
    _namewssn = request.form['employee']
    _ssn = re.findall('[0-9]+', _namewssn)[0]
    _assignment = request.form['assignment']
    _work_at = request.form['work_at']

    conn = sqlite3.connect('ticket_management.sqlite3')
    cur = conn.cursor()

    # not allowed to work at two different theaters at the same day
    cur.execute('SELECT day, work_at FROM working_schedule WHERE ssn=?', (_ssn, ))
    res = cur.fetchone()
    if _date == res[0] and _work_at != res[1] :
        flash('Not allowed to work in two different theaters in the same day!')
        return redirect(url_for('management_view'))

    # not allowed to work the same job at the same time
    cur.execute('SELECT day, assignment FROM working_schedule WHERE ssn=?', (_ssn, ))
    if (_date, _assignment) == cur.fetchone():
        flash('Not allowed to work the same job in the same day')
        return redirect(url_for('management_view'))        

    cur.execute('INSERT INTO working_schedule (day, ssn, assignment, work_at) VALUES (?, ?, ?, ?)', (_date, _ssn, _assignment, _work_at))
    conn.commit()

    return redirect(url_for('management_view'))

@app.route('/delegateManager', methods=['POST'])
def delegateManager():
        _employee = request.form['managerSSN']
        _name = str(_employee).split()[0] + ' '+ str(_employee).split()[1] 
        _ssn = str(_employee).split()[2]
        
        conn = sqlite3.connect('ticket_management.sqlite3')
        cur = conn.cursor()

        cur.execute('UPDATE Staff SET description_of_duty=? WHERE _ssn=?', ('Updating movies', _ssn))
        conn.commit()
        return redirect(url_for('management_view'))

@app.route('/addMovie', methods=['POST','GET'])
def addMovie():
    if request.method == 'POST':
        _title = request.form['title']
        _year = request.form['year']
        _genre = request.form['genre']
        _length = request.form['length']
        _director = request.form['director']
        _description = request.form['description']

        conn = sqlite3.connect('ticket_management.sqlite3')
        cur = conn.cursor()

        cur.execute('SELECT * FROM Movies WHERE title=? AND year=?',
                    (_title, _year))

        if cur.fetchone() is None: # if this mvoies is not in database
            cur.execute('INSERT INTO Movies VALUES (?, ?, ?, ? ,?, ?)',\
                       (_title, _year, _genre, _length, _director, _description))
            
            conn.commit()
            return redirect(url_for('management_view'))
        else:
            flash('This movie already in database!')
    else:
        return render_template('addMovie.html')

@app.route('/deleteMovie', methods=['POST','GET'])
def deleteMovie():
    if request.method == 'POST':
        _title = request.form['title']
        _year = request.form['year']

        conn = sqlite3.connect('ticket_management.sqlite3')
        cur = conn.cursor()

        cur.execute('SELECT * FROM Movies WHERE title=? AND year=?',
                    (_title, _year))
        if cur.fetchone() is not None:
            cur.execute('DELETE FROM Movies WHERE title=? AND year=?'
                        (_title, _year,))

            conn.commit()
            return redirect(url_for('management_view'))
        else:
            flash('This movie is not in database!')
            
    else:
        return render_template('deleteMovie.html')

@app.route('/modifySchedule')
def modifySchedule():
    return render_template('movieTable.html')

# @app.route('/setDiscount')
# def setDiscount():


# Run
if __name__ == '__main__':
    app.run(debug=True)