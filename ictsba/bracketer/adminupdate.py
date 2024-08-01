from bracketer import app,db ,bcrypt
from flask import redirect,url_for,session , json
from bracketer.adminupdateforms import update2024 , updatenonstudent , update2023 , updateschool , updatestudent
from bracketer.models import chart2023,schools,users,students,chart2024 , chartinfo


#update 2024 db in admin panel
@app.route('/updatechart2024', methods=['GET', 'POST'])
def updatechart2024():
    form = update2024()
          
    if form.validate_on_submit():
        og = json.loads(form.original.data)

        originalsid = og['chartsid']
        originaltid = og['charttid']
       
            
        #change related records
        negativeinfo = False
        if db.session.query(chart2024).filter(chart2024.SID == originalsid).count() == 2:
            # to prevent violating the primary key constraint , first turn the update record 's tid to an impossilbe value (negative)
            db.session.query(chart2024).filter(chart2024.SID == originalsid,chart2024.TID == originaltid).update({chart2024.TID:-1,chart2023.SID:-1})
            db.session.query(students).filter(students.SID == originalsid,students.TID == originaltid).update({students.TID:-1,students.SID:-1})
            negativeinfo = True
            ## if sid is not changed + sid unchange
            if form.sid.data == originalsid and form.tid.data != originaltid: 

                #change tid of the other team to 3-its original tid so that (if tid = 2 --> 1 , if tid= 1 -->2)
                db.session.query(chart2024).filter(chart2024.SID == originalsid , chart2024.TID == 3-originaltid).update({chart2024.TID:3-chart2024.TID})
                db.session.query(students).filter(students.SID == originalsid , students.TID == 3-originaltid).update({students.TID:3-students.TID})
                
            ##if originally have two team and sid is changed (only hv to change when team one left)
            elif originaltid == 1: 
                    
                db.session.query(chart2024).filter(chart2024.SID == originalsid , chart2024.TID == 2).update({chart2024.TID:1})

                db.session.query(students).filter(students.SID == og['chartsid'], students.TID == 2).update({students.TID:1})

            # if add to another school, and that school hv one teams already + when you add you are team 1 
        if negativeinfo == False:
                db.session.query(chart2024).filter(chart2024.SID == originalsid,chart2024.TID == originaltid).update({chart2024.TID:-1,chart2023.SID:-1})
                db.session.query(students).filter(students.SID == originalsid,students.TID == originaltid).update({students.TID:-1,students.SID:-1})    
        if originalsid != form.sid.data and form.tid.data == 1:
            # to prevent violating the primary key constraint , first turn the update record 's tid to an impossilbe value (negative)       
            db.session.query(chart2024).filter(chart2024.SID == form.sid.data , chart2024.TID == 1).update({chart2024.TID:2})
            db.session.query(students).filter(students.SID == form.sid.data , students.TID == 1).update({students.TID:2})
        #after all update is done, update the record
        db.session.query(chart2024).filter(chart2024.SID == -1 , chart2024.TID == -1).update({chart2024.TID: form.tid.data, chart2024.SID: form.sid.data, chart2024.LOSE: form.losed.data})
        print(type(form.sid.data))
        print('asjd;fasd;lkfjsdal;kfjsda',form.losed.data)
        db.session.query(students).filter(students.SID == -1 , students.TID == -1 ).update({students.TID:form.tid.data, students.SID: form.sid.data})
            #commit 
        db.session.commit()
        db.session.query(chart2024).filter(chart2024.SID != form.sid.data , chart2024.TID != form.tid.data).update({'LOSE': False})
        db.session.query(chart2024).update({'WON':0})
        db.session.query(chartinfo).delete()
        db.session.commit()
        session.pop('charts', None)
        session.pop('losers', None)
    else:
        print('oopsie')
        session['inserterror']=[]
        
        for fieldName, errorMessages in form.errors.items():
            for error in errorMessages:   
                session['inserterror'].append(error)
        session['load'] = 'chart2024'
        return redirect(url_for('profile'))
    return redirect(url_for('processchart2024'))
#update nonstudent in admin panel
@app.route('/updateuser', methods=['GET', 'POST'])
def updateuser():
    
    form = updatenonstudent()
    og = json.loads(form.original.data)
    if form.validate_on_submit():
        
        db.session.query(users).filter(users.ID == og['userid']).update({users.ID:form.id.data,users.EMAIL:form.email.data,users.ADMIN:form.admin.data,users.USER:form.user.data})
        db.session.commit()
        if form.pw.data:
            print(form.pw.data)
            db.session.query(users).filter(users.ID == form.id.data).update({users.PW: bcrypt.generate_password_hash(form.pw.data)})
            db.session.commit()
    else:
        print('oopsie')
        session['inserterror']=[]
        
        for fieldName, errorMessages in form.errors.items():
            for error in errorMessages:   
                session['inserterror'].append(error)
        session['load']='nonstudents'
        return redirect(url_for('profile'))
    return redirect(url_for('processnonstudents'))

#update nonstudent in admin panel
@app.route('/updatestudent', methods=['GET', 'POST'])
def updatestudents():
    
    form = updatestudent()
    og = json.loads(form.original.data)
    print(og)
    if form.validate_on_submit():
        print(form.id.data)
        db.session.query(students).filter(students.ID == og['studentid']).update({students.ID:form.id.data,students.USER:form.user.data})
        db.session.commit()

        if form.pw.data:
            print(form.pw.data)
            db.session.query(students).filter(students.ID == form.id.data).update({students.PW: bcrypt.generate_password_hash(form.pw.data)})
            db.session.commit()
    else:
        print('oopsie')
        session['inserterror']=[]
        
        for fieldName, errorMessages in form.errors.items():
            for error in errorMessages:   
                session['inserterror'].append(error)
        session['load']='students'
        return redirect(url_for('profile'))
    return redirect(url_for('processstudents'))

#update 2024 db in admin panel
@app.route('/updatechart2023', methods=['GET', 'POST'])
def updatechart2023():
    form = update2023()
    

    if form.validate_on_submit():
        og = json.loads(form.original.data)
        originalsid = og['sid2023']
        originaltid = og['tid2023']
            #change related records
        negativeinfo = False
        if db.session.query(chart2023).filter(chart2023.SID == originalsid).count() == 2:
                # to prevent violating the primary key constraint , first turn the update record 's tid to an impossilbe value (negative)
            db.session.query(chart2023).filter(chart2023.SID == originalsid,chart2023.TID == originaltid).update({chart2023.TID:-1,chart2023.SID:-1})
               
            negativeinfo = True
                ## if sid is not changed + sid unchange
            if form.sid.data == originalsid and form.tid.data != originaltid: 

                    #change tid of the other team to 3-its original tid so that (if tid = 2 --> 1 , if tid= 1 -->2)
                db.session.query(chart2023).filter(chart2023.SID == originalsid , chart2023.TID == 3-originaltid).update({chart2023.TID:3-chart2023.TID})
                   
                
                ##if originally have two team and sid is changed (only hv to change when team one left)
            elif originaltid == 1: 
                    
                db.session.query(chart2023).filter(chart2023.SID == originalsid , chart2023.TID == 2).update({chart2023.TID:1})

        # to prevent violating the primary key constraint , first turn the update record 's tid to an impossilbe value (negative)      
        if negativeinfo == False:
                db.session.query(chart2023).filter(chart2023.SID == originalsid,chart2023.TID == originaltid).update({chart2023.TID:-1,chart2023.SID:-1})
            # if add to another school, and that school hv one teams already + when you add you are team 1     
        if originalsid != form.sid.data and form.tid.data == 1:
               
                  
            db.session.query(chart2023).filter(chart2023.SID == form.sid.data , chart2023.TID == 1).update({chart2023.TID:2})
              
            
            #after all update is done, update the record    
        db.session.query(chart2023).filter(chart2023.SID == -1 , chart2023.TID == -1).update({chart2023.TID: form.tid.data, chart2023.SID: form.sid.data, chart2023.LOSE: form.losed.data , chart2023.SEED : form.seed.data ,chart2023.WON:form.won.data})
       
           
            #commit 
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
        print('oopsie')
        session['inserterror']=[]
        
        for fieldName, errorMessages in form.errors.items():
            for error in errorMessages:   
                session['inserterror'].append(error)
        session['load'] = 'chart2023'
        return redirect(url_for('profile'))
    return redirect(url_for('processchart2023'))


@app.route('/updateschool', methods=['GET', 'POST'])
def updateschools():
    form = updateschool()
    if form.validate_on_submit():
        og = json.loads(form.original.data)
        db.session.query(schools).filter(schools.SID == og['schoolsid']).update({schools.SID: form.sid.data, schools.NAME : form.name.data})
        db.session.query(chart2024).filter(chart2024.SID == og['schoolsid']).update({chart2024.SID: form.sid.data})
        db.session.query(chart2023).filter(chart2023.SID == og['schoolsid']).update({chart2023.SID: form.sid.data})
        db.session.query(students).filter(students.SID == og['schoolsid']).update({students.SID: form.sid.data})
        db.session.commit()
        db.session.query(chart2024).update({'LOSE': False})
        db.session.query(chart2024).update({'WON':0})
        db.session.query(chartinfo).delete()
        db.session.commit()
        session.pop('charts', None)
        session.pop('losers', None)
    else:
        print('oopsie')
        session['inserterror']=[]
        
        for fieldName, errorMessages in form.errors.items():
            for error in errorMessages:   
                session['inserterror'].append(error)
        session['load'] = 'schools'
        return redirect(url_for('profile'))
    return redirect(url_for('processschools'))

@app.route('/applystatus', methods=['GET', 'POST']) ##change status of the application 
def applystatuschange():
    if session['usertype'] == 'admin':
        if 'applyopen' not in session:
            session['applyopen'] = True
        session['applyopen'] = not session['applyopen']
        print(session['applyopen'])
        session['load'] = 'functions'
    return redirect(url_for('profile'))