from bracketer import db , app
from flask import render_template,redirect,url_for,session
from bracketer.forms import editdb , endapplication  
from bracketer.admininsertforms import insertteam , insert2023 ,insertschools , insertnonstudent
from bracketer.adminupdateforms import update2024 , updatenonstudent ,update2023 , updateschool ,updatestudent

#profile page 

@app.route('/profile',methods =["POST","GET"])
def profile(): 
    print("i got in profile")
    if 'dbinfo' not in session: #if dbinfo does not exist
        session['dbinfo'] = []
    if 'load' not in session:
        session['load'] = ''
    if 'passwords' not in session:
        print('hi123')
        session['passwords'] = None
        session['STUID'] = None
    edit = editdb()
    ##load all admin forms
    teaminsert = insertteam()
    lastyearinsert = insert2023()
    schoolsinsert = insertschools()
    nonstudentinsert = insertnonstudent()
    updatechart2024 = update2024()
    updateuser = updatenonstudent()
    updatechart2023 = update2023()
    schoolupdate = updateschool()
    applystatus = endapplication()
    updatestu= updatestudent()
    #if not logged in , return to homepage
    if session['username'] == None:
        return redirect(url_for('homepage'))
    load = session.pop('load',None)
    pws = session.pop('passwords',None)
    studentid = session.pop('STUID',None)
    if 'inserterror' in session:
        inserterror = session.pop('inserterror',None)
        inserterror = inserterror[0]
    else:
        inserterror = None
    return render_template('profile.html' , edit = edit , insertteam = teaminsert, insert2023 = lastyearinsert , insertschools = schoolsinsert , insertnonstudent = nonstudentinsert , load = load , inserterror = inserterror , updatechart = updatechart2024 , updateuser = updateuser , update2023 = updatechart2023 , updateschool = schoolupdate , endapplication = applystatus , passwords = pws , stuid = studentid , updatestudent = updatestu)
