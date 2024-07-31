from bracketer import app,db
from bracketer.models import chart2023, schools  , chart2024  , students
from random import choice , randint
from string import ascii_letters
from flask import session
from numpy import concatenate





def addteam(form):
        def createpw():
    #create password for applicants and hash it for security
            for i in range(0,4):
                password = '' 
                while len(password) != 10:
                    
                    password += (choice(ascii_letters)) #add a random ascii letter 
                    password += str(randint(0,9)) #add a random digit
                session['passwords'].append(password)
    ## find top4's sid of last year (2023)
        rank4 = []
        session['passwords']=[]
        top4 = db.session.query(chart2023.SID).order_by(chart2023.WON.desc()).limit(4).all()  
        for i in range(len(top4)):
            if top4[i][0] not in rank4:
                rank4.append(top4[i][0])     
       
        ## add new school to schools
        if db.session.query(schools).filter(schools.SID == form.sid.data).count() == 0 :
            newschool = schools(NAME= form.name.data , SID = form.sid.data)
            db.session.add(newschool)
            db.session.flush()
            db.session.refresh(newschool) 
        
        ## get the seed of team one (only team one will be seeded)
        if form.sid.data in rank4:                              
            seed = rank4.index(form.sid.data) + 1
        else: 
            seed = 0

        ## add team one                    

        ## add team one to chart2024 
        newteam = chart2024(SID = form.sid.data, TID = 1 , SEED = seed, WON = 0, LOSE = False)
        db.session.add(newteam)
        db.session.commit()

        ## add team 1 memebers to students

        print("hi")
        createpw()
        print(session['passwords'])
        users = [students(SID = form.sid.data, TID = 1 , USER = form.t1participant1.data , PW = session['passwords'][0] ),
                 students(SID = form.sid.data, TID = 1 , USER = form.t1participant2.data, PW = session['passwords'][1] ),
                 students(SID = form.sid.data, TID = 1 , USER = form.t1participant3.data, PW = session['passwords'][2]),
                 students(SID = form.sid.data, TID = 1 , USER = form.t1participant4.data, PW = session['passwords'][3]) ]

        for student in users:
            db.session.add(student)
            db.session.commit()
        session.pop('STUID', None)
        session['STUID'] = []
        studentinfo = db.session.query(students.ID).filter(students.SID == form.sid.data, students.TID == 1)
        for student in studentinfo:
            session['STUID'].append(student[0])
        
        ## add team two if theres two teams
        if form.team2.data == True:

        ## add team two to chart2024 if theres two teams
            newteam = chart2024(SID = form.sid.data, TID = 2 , SEED = 0 , WON = 0, LOSE = False)
            db.session.add(newteam)
            db.session.commit()

        ## add team 2 memebers 
            createpw()
            print(session['passwords'])

            users = [students(SID = form.sid.data, TID = 2 , USER = form.t2participant1.data , PW = session['passwords'][4]),
                    students(SID = form.sid.data, TID = 2 , USER = form.t2participant2.data, PW = session['passwords'][5]),
                    students(SID = form.sid.data, TID = 2 , USER = form.t2participant3.data, PW = session['passwords'][6]),
                    students(SID = form.sid.data, TID = 2 , USER = form.t2participant4.data, PW = session['passwords'][7])]
            
      
            for student in users:
                db.session.add(student)
                db.session.commit()
            studentinfo = db.session.query(students.ID).filter(students.SID == form.sid.data, students.TID == 2)
            for student in studentinfo:
                session['STUID'].append(student[0])
        db.session.commit()
        session.pop('charts', None)
        session.pop('losers',None)
