from bracketer import app,db,bcrypt
from flask import render_template,redirect,url_for,session,request
from bracketer.forms import studentlogin, loginform, guestregister
from bracketer.models import schools, students , users 

@app.route('/login' , methods =["POST","GET"])
def loginpage():
    return render_template('login.html')


@app.route('/guest',methods =["POST","GET"])
def guestpage():
    session.pop('flash',None)
    form = loginform() 
    if form.validate_on_submit():
        valid = False
        hashedpw = db.session.query(users.PW).filter(users.USER == form.username.data)
        if hashedpw.all():
            hashedpw = hashedpw.all()[0][0]
            valid = bcrypt.check_password_hash(hashedpw, form.password.data) 
        if valid == True :
            session['flash'] = "log in sucessfully!" 
            session['username'] = form.username.data
            if db.session.query(users.ADMIN).filter(users.USER == form.username.data).all()[0][0] == False:
                session['usertype'] = 'guest'
            else: 
                session['usertype'] = 'admin'  
            session['redirect'] = url_for('guestpage') 
            return redirect(url_for('load'))
        else:
            session['flash'] = "incorrect username or password!"
    elif request.method=='POST': 
        for field , error in form.errors.items():
            session['flash'] = f'{error[0]}'  
    flash = session.pop('flash', None)
    return render_template('gstlogin.html', flash = flash, form = form)

@app.route('/student',methods =["POST","GET"])
def studentpage():
    session.pop('flash',None)
    form = studentlogin() 
    if form.validate_on_submit():
        valid = False
        hashedpw = db.session.query(students.PW).filter(students.ID == form.sid.data)
        if hashedpw.all():
            hashedpw = hashedpw.all()[0][0]
            valid = bcrypt.check_password_hash(hashedpw, form.password.data) 
        if valid == True:
            session['flash'] = "log in sucessfully!"
            session['usertype'] = 'student'
            session['username'] = db.session.query(students.USER).filter(students.ID == form.sid.data).all()[0][0]
            session['studentid'] = form.sid.data
            session['redirect'] = url_for('studentpage')
            return redirect(url_for('load'))
        else:
            session['flash'] = "incorrect student ID or password!"
    elif request.method=='POST': 
         for field , error in form.errors.items():
            session['flash'] = f'{error[0]}'   
    flash = session.pop('flash', None)
    return render_template('stulogin.html', form=form , flash = flash)

@app.route('/register',methods =["POST","GET"])
def register():
    session.pop('flash',None)
    form = guestregister()
    
    if form.validate_on_submit(): 
        session['flash'] = 'Register Successfully'
        guests = users(EMAIL = form.email.data, USER = form.username.data, PW = form.password.data)
        db.session.add(guests)
        db.session.commit()
    elif request.method == 'POST':
        for field , error in form.errors.items():
            session['flash'] = f'{error[0]}'
    flash = session.pop('flash',None)
    return render_template('register.html' , form = form , flash = flash)

@app.route('/logout', methods=["POST","GET"])
def logoutuser():
    session['usertype'] = None
    session['username'] = None
    session['studentid'] = None
    session['teamid'] = None
    session['schoolname'] = None
    session.pop('team',None)
    return redirect(url_for('homepage'))


#load student's team
@app.route('/loadinfo')
def load():
    if session['usertype'] == 'student':
        session['team']=[]
        session['schoolname'] = None
        session['teamid'] = None
        schoolid = db.session.query(students.SID).filter(students.ID == session['studentid']).all()[0][0]
        teamid = db.session.query(students.TID).filter(students.ID == session['studentid']).all()[0][0]
        team = db.session.query(students.USER).filter(students.SID == schoolid , students.TID == teamid).all()
        for member in team:
            session['team'].append(member[0])
            session['schoolname'] = db.session.query(schools.NAME).filter(schools.SID == schoolid).all()[0][0]
            session['teamid'] = teamid
    return redirect((session['redirect']))