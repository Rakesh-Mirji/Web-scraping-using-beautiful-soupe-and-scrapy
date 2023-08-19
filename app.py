from flask import Flask, render_template, request, redirect, url_for, jsonify, json, Response, session, g, flash, request, make_response
from sqlalchemy import create_engine, and_, text
from sqlalchemy.orm import sessionmaker, exc
from dbsetup import *
import hashlib
import subprocess
app = Flask(__name__)
# initialise the database
engine = create_engine('sqlite:///scrape.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
dbsession = DBSession() 

# open the index page
@app.route('/', methods=['GET', 'POST'])
def main():
    if g.user: # check for user session
        query = dbsession.query(Catches).all()
        # print(query)
        if request.method == 'POST': # webform submission
            subprocess.run(['python', 'reddit.py', '-l', request.form['url_1'] ])
            subprocess.run(['python', 'reddit.py', '-l', request.form['url_2'] ])
            return redirect(url_for('report'))
        return render_template('index.html',data=True, query=query)
    return redirect(url_for('signin'))  


# display report
@app.route('/report/')
def report():
    if g.user: # check for user session
        report = dbsession.query(Report).all()
        return render_template('report.html', report=report )
    return redirect(url_for('signin')) # generate dynamic query


@app.route('/about/')
def about():
    if g.user: # check for user session
        return render_template('about.html')
    return redirect(url_for('signin'))

@app.route('/know/')
def know():
    if g.user: # check for user session
        return render_template('know.html')
    return redirect(url_for('signin'))


@app.route('/report/search/', methods=['GET', 'POST'])
def advancedSearch():
    if g.user: # check for user session
        if request.method == 'POST':
            if request.form['field']:
                field = request.form['field']
            if request.form['param']:
                param = request.form['param']
                param = param.replace("/", "%2f")
            elif not request.form['param']:
                param = "%"
            param = param.replace("%2f", "/")
            q = text("select * from catches where catches.word like '%?%' ")
            query = dbsession.query(Catches).filter(Catches.word == param.lower())
            # query = dbsession.execute(f"select * from catches where catches.{field} like '%{param}%' ")
            rows = query.all()
            # result = []
            # for row in rows:
            #     result.append(dict(row))
            return render_template('searchReport.html', query=rows)
        return render_template('advanced.html')
    return redirect(url_for('signin'))


# compare password with database
def check_password(hashed_password, user_password, salt):
    return hashed_password == hashlib.sha256((user_password.encode()) + salt).hexdigest()


# compare credentials with database
def validate(username, password):
    completion = False
    users = dbsession.query(User)
    for user in users:
        if user.username == username:
            completion = check_password(user.password, password, user.salt)
    return completion


# sign in user
@app.route('/signin/', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        session.pop('user', None)
        uname = request.form['username']
        pword = request.form['password']
        completion = validate(uname, pword)
        if completion == True:
            session['user'] = uname # create user session
            return redirect(url_for('main'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('signin.html', error=error)

# delete session
@app.route('/signout/')
def signout():
    session.pop('user', None)
    return redirect(url_for('main'))


# create user session
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


if __name__ == '__main__':
    app.secret_key = "\xc2\x0f\xdc\x9d0\x10A\xfa:DO\xcf\xa8%\xf0\x8e\xc1\xcb=\xf8$\xaa\xc8\xfb"
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000,threaded=False)
