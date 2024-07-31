from bracketer import db , app
from flask import render_template,redirect,url_for,session,json
from bracketer.forms import editdb
from bracketer.models import schools  , chart2024 , chart2023 , students , users , chartinfo , students



#admin panel edit students
@app.route('/processstudents', methods=["POST","GET"])
def processstudents():
    session.pop('dbinfo',None)
    edit = editdb()
    if edit.validate_on_submit() and edit.remove.data:
        removeitems = json.loads(edit.remove.data) #this array contains the teams to remove
        print('this is removedteams',removeitems)
        for student in range(len(removeitems)):
            removeitems[student]= json.loads(removeitems[student])   
        for student in removeitems:
            db.session.query(students).filter(students.ID == student['studentid']).delete()
            db.session.commit()

    if 'dbinfo' not in session: #if the students is not deleting but accessed here --> get chart2024 ( also work, later change to chart2024)
        session['dbinfo'] = []
        for student in  db.session.query(students.ID,students.SID,students.TID,students.USER).all():

            newstudent = {
                'studentid':student[0],
                'sid':student[1],
                'tid':student[2],
                'studentname':student[3]
            }
            session['dbinfo'].append(newstudent)
    session['load'] = 'students'
    print("hi about to redirect")
    return redirect(url_for('profile'))

#admin panel edit non students
@app.route('/processnonstudents', methods=["POST","GET"])
def processnonstudents():
    session.pop('dbinfo',None)
    edit = editdb()
    if edit.validate_on_submit() and edit.remove.data:
        print("Hi")
        removeitems = json.loads(edit.remove.data) #this array contains the teams to remove
        print('this is removedteams',removeitems)
        for user in range(len(removeitems)):
            removeitems[user]= json.loads(removeitems[user])   
        for user in removeitems:
            db.session.query(users).filter(users.ID == users['id']).delete()
            db.session.commit()

    if 'dbinfo' not in session: #if the user is not deleting but accessed here --> get chart2024 ( also work, later change to chart2024)
        session['dbinfo'] = []
        for user in  db.session.query(users.ID,users.EMAIL,users.USER,users.ADMIN).all():

            newuser = {
                'id':user[0],
                'email':user[1],
                'user':user[2],
                'admin':user[3]
            }

            session['dbinfo'].append(newuser)

    session['load'] = 'nonstudents'
    print("hi about to redirect")
    return redirect(url_for('profile'))
#admin panel edit schools
@app.route('/processschools', methods=["POST","GET"])
def processschools():
    session.pop('dbinfo',None)
    edit = editdb()
    if edit.validate_on_submit() and edit.remove.data:
        removeitems = json.loads(edit.remove.data) #this array contains the teams to remove
        print('this is removedteams',removeitems)
        for school in range(len(removeitems)):
            removeitems[school]= json.loads(removeitems[school])
        updatet2 = []    
        for school in removeitems:
            db.session.query(schools).filter(schools.SID == school['sid']).delete()
            db.session.commit()
            db.session.query(chart2023).filter(chart2023.SID == school['sid']).delete()
            db.session.commit()
            db.session.query(chart2024).filter(chart2024.SID == school['sid'] ).delete()
            db.session.commit()
            db.session.query(students).filter(students.SID == school['sid'] ).delete()
            db.session.commit()
            db.session.query(chart2024).update({'LOSE': False})
            db.session.query(chart2024).update({'WON':0})
            db.session.query(chartinfo).delete()
            db.session.commit()
            session.pop('charts', None)
            session.pop('losers', None)
        
    if 'dbinfo' not in session: #if the students is not deleting but accessed here --> get chart2024 ( also work, later change to chart2024)
        session['dbinfo'] = []
        for school in  db.session.query(schools.NAME, schools.SID).all():

            newschool = {
                'name' :school[0],
                'sid' :school[1],
            }

            session['dbinfo'].append(newschool)

    session['load'] = 'schools'
    print("hi about to redirect")
    return redirect(url_for('profile'))


#admin panel edit chart2023
@app.route('/processchart2023', methods=["POST","GET"])
def processchart2023():
    session.pop('dbinfo',None)
    edit = editdb()
    if edit.validate_on_submit() and edit.remove.data:
        removeitems = json.loads(edit.remove.data) #this array contains the teams to remove
        print('this is removedteams',removeitems)
        for team in range(len(removeitems)):
            removeitems[team]= json.loads(removeitems[team])
        updatet2 = []    
        for team in removeitems:

            count = db.session.query(chart2023).filter(chart2023.SID == team['sid']).count()
            db.session.query(chart2023).filter(chart2023.SID == team['sid'] , chart2023.TID == team['tid']).delete()
            db.session.commit()
            if count == 2 and team['tid'] == 1: ## as a record was delete
                updatet2.append(team['sid'])

        for sid in updatet2:
            db.session.query(chart2023).filter(chart2023.SID ==  sid , chart2023.TID == 2 ).update({'TID':1})
            db.session.commit()
        db.session.query(chart2024).update({'LOSE': False})
        db.session.query(chart2024).update({'WON':0})
        db.session.query(chartinfo).delete()
        db.session.commit()
        session.pop('charts', None)
        session.pop('losers', None)
    if 'dbinfo' not in session: #if the students is not deleting but accessed here --> get chart2024 ( also work, later change to chart2024)
        session['dbinfo'] = []
        for school in  db.session.query(chart2023.SID, chart2023.TID ,chart2023.SEED,chart2023.WON,chart2023.LOSE ).all():

            newschool = {
                'name' :db.session.query(schools.NAME).filter(schools.SID == school[0]).all()[0][0],
                'sid' :school[0],
                'tid' :school[1],
                'seed':school[2],
                'won':school[3],
                'losed' :school[4]
            }
            session['dbinfo'].append(newschool)
    session['load'] = 'chart2023'
    print("hi about to redirect")
    return redirect(url_for('profile'))

#admin panel edit chart2024
@app.route('/processchart2024', methods=["POST","GET"])
def processchart2024():
    session.pop('dbinfo',None)
    edit = editdb()
    if edit.validate_on_submit() and edit.remove.data:
        removeitems = json.loads(edit.remove.data) #this array contains the teams to remove
        print('this is removedteams',removeitems)
        for team in range(len(removeitems)):
            removeitems[team]= json.loads(removeitems[team])
        updatet2 = [] 
        for team in removeitems:
            count = db.session.query(chart2024).filter(chart2024.SID == team['sid'] ).count()
            team['sid'] = str(team['sid'])
            db.session.query(chart2024).filter(chart2024.SID == team['sid'] , chart2024.TID == team['tid']).delete()
            db.session.query(students).filter(students.SID == team['sid'] , students.TID == team['tid']).delete()
            db.session.commit()
  
        if count == 2 and team['tid'] == 1: ## as a record was delete
            updatet2.append(team['sid'])

        for sid in updatet2:
            db.session.query(chart2024).filter(chart2024.SID ==  sid , chart2024.TID == 2 ).update({'TID':1})
            db.session.commit()
        db.session.query(chart2024).update({'LOSE': False})
        db.session.query(chart2024).update({'WON':0})
        db.session.query(chartinfo).delete()
        db.session.commit()
        session.pop('charts', None)
        session.pop('losers', None)
    if 'dbinfo' not in session: #if the students is not deleting but accessed here --> get chart2024 ( also work, later change to chart2024)
        session['dbinfo'] = []
        for school in  db.session.query(chart2024.SID, chart2024.TID ,chart2024.SEED,chart2024.WON,chart2024.LOSE ).all():

            newschool = {
                'name' :db.session.query(schools.NAME).filter(schools.SID == school[0]).all()[0][0],
                'sid' :school[0],
                'tid' :school[1],
                'seed':school[2],
                'won':school[3],
                'losed' :school[4]
            }
            session['dbinfo'].append(newschool)
    session['load'] = 'chart2024'
    print("hi about to redirect")
    return redirect(url_for('profile'))
