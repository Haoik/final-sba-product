from bracketer import app,db 
from bracketer.subprograms import addteam
from flask import render_template,redirect,url_for,session
from bracketer.admininsertforms import insertteam , insertschools, insert2023, insertnonstudent
from bracketer.models import chart2023,schools,users , chart2024,chartinfo


#insert new team in admin panel
@app.route('/insertteam', methods=['GET', 'POST'])
def teaminsert():
    form = insertteam()
    if form.validate_on_submit():
        session.pop('STUID',None)
        session.pop('passwords',None)
        addteam(form)
        db.session.query(chart2024).update({'LOSE': False})
        db.session.query(chart2024).update({'WON':0})
        db.session.query(chartinfo).delete()
        db.session.commit()
        session.pop('charts', None)
        session.pop('losers', None)
    else:
        session['inserterror']=[]
        
        for fieldName, errorMessages in form.errors.items():
            for error in errorMessages:   
                session['inserterror'].append(error)
    session['load'] = 'insertchoosedb'

    return redirect(url_for('profile'))

#insert new school in admin panel
@app.route('/insert2023', methods=['GET', 'POST'])
def lastyearinsert():
    form = insert2023()
    if form.validate_on_submit():
        newschool = chart2023(TID = form.tid.data , SID = form.sid.data , WON = 0 , SEED = 0)
        db.session.add(newschool)
        db.session.commit()
        db.session.query(chart2024).update({'LOSE': False})
        db.session.query(chart2024).update({'WON':0})
        db.session.query(chartinfo).delete()
        db.session.commit()
        session.pop('charts', None)
        session.pop('losers', None)
        session.pop('charts2023', None)
        session.pop('losers2023', None)
    else:
        session['inserterror']=[]
        
        for fieldName, errorMessages in form.errors.items():
            for error in errorMessages:   
                session['inserterror'].append(error)
    
    session['load'] = 'insertchoosedb'
    return redirect(url_for('profile'))

@app.route('/insertschool', methods=['GET', 'POST'])
def schoolinsert():
    form = insertschools()
    if form.validate_on_submit():
        newschool = schools(NAME = form.name.data , SID = form.sid.data)
        db.session.add(newschool)
        db.session.commit()
       
    else:
        session['inserterror']=[]
        
        for fieldName, errorMessages in form.errors.items():
            for error in errorMessages:   
                session['inserterror'].append(error)
    
    session['load'] = 'insertchoosedb'
    return redirect(url_for('profile'))

@app.route('/insertnonstudent', methods=['GET', 'POST'])
def userlinsert():
    form = insertnonstudent()
    if form.validate_on_submit():
        newuser = users(USER = form.username.data, EMAIL = form.email.data , PW = form.password.data , ADMIN = form.admin.data)
        db.session.add(newuser)
        db.session.commit()
    else:
        session['inserterror']=[]
        for fieldName, errorMessages in form.errors.items():
            for error in errorMessages:   
                session['inserterror'].append(error)
    
    session['load'] = 'insertchoosedb'
    return redirect(url_for('profile'))