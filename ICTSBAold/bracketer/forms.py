
from flask_wtf import FlaskForm 
from flask import json
from wtforms import StringField , BooleanField , validators , HiddenField , SubmitField , PasswordField , IntegerField
from wtforms.validators import DataRequired , Email ,Optional
from bracketer import db
from bracketer.models import users , schools , chart2023 , chart2024 , students
import re




## custom validators
def schoolcode(form,field):
    if len(field.data)!= 6 or field.data.isdigit() == False :
        raise validators.ValidationError("invalid School Code (must be 6 digits)")
def notfilled(form,field):
    if not field.data:
       raise validators.ValidationError("Please fill all fields") 

def optionalteam2(form, field):
   if form.team2.data == True and field.data.strip() =='' :
            raise validators.ValidationError("Required team two data")
        
def confirmpw(form,field):
     if field.data != form.password.data :
        raise validators.ValidationError("Wrong password!")
     
def pwstrength(form,field):
    if len(field.data) < 8 or any(i.isdigit() for i in field.data) == False or (any(i.isupper() for i in field.data) == False and any(i.islower() for i in field.data) == False):

        raise validators.ValidationError("Password length must be at least 8 and contains both letters and digit!") 
    
def applyrepeat2024(form,field):
    if db.session.query(chart2024).filter(chart2024.SID == form.sid.data).first():
        raise validators.ValidationError("This school already applied!")

def checkchineseexist(form,field):
    def checkchinese(text):
        # Regular expression for matching Chinese characters
        pattern = re.compile(r'[\u4e00-\u9fff]+')
        return bool(pattern.match(text))
    if (checkchinese(field.data)) == False:
        raise validators.ValidationError("Enter Your *Chinese* School Name")
def checkchinese(form,field):
    def checkchinese(text):
        # Regular expression for matching Chinese characters
        pattern = re.compile(r'[\u4e00-\u9fff]+')
        return bool(pattern.match(text))
    chinese = True
    if field.data:
        for string in field.data:
            if (checkchinese(string.strip())) == False:
                chinese = False
        if chinese == False:
            raise validators.ValidationError("Enter Your *Chinese* Name")
def checkrepeatmail(form,field):
    if db.session.query(users).filter(users.EMAIL == field.data).first():
       raise validators.ValidationError("This email belongs to another account!")
    
def checkrepeatuser(form,field):
    if db.session.query(users).filter(users.USER == field.data).first():
        raise validators.ValidationError("This username already existed!")
## forms
class apply(FlaskForm):

    ## school name
    name = StringField('School Name', validators=[notfilled,checkchineseexist])

    sid = StringField('School Code', validators=[notfilled,applyrepeat2024,schoolcode])

    ## team 1 members
    t1participant1 = StringField('Participant 1', validators=[notfilled,checkchinese])
    t1participant2 = StringField('Participant 2', validators=[notfilled,checkchinese])
    t1participant3 = StringField('Participant 3', validators=[notfilled,checkchinese])
    t1participant4 = StringField('Participant 4', validators=[notfilled,checkchinese])

    team2 = BooleanField('no second team')
    ## team 2 members
    t2participant1 = StringField('Participant 1', validators=[optionalteam2,checkchinese])
    t2participant2 = StringField('Participant 2', validators=[optionalteam2,checkchinese])
    t2participant3 = StringField('Participant 3', validators=[optionalteam2,checkchinese])
    t2participant4 = StringField('Participant 4', validators=[optionalteam2,checkchinese]) 


class progress(FlaskForm):
    team1 = BooleanField()
    team2 = BooleanField()
    wontid =  HiddenField()
    wonsid =  HiddenField()
    losetid = HiddenField()
    losesid = HiddenField()
    confirm = SubmitField()

            
class reset(FlaskForm):
    reset = SubmitField()  

class studentlogin(FlaskForm):
    sid = StringField('SID',validators=[notfilled])
    password = PasswordField('password',validators=[ notfilled])
    submit = SubmitField()      

            
class loginform(FlaskForm):
    username = StringField(validators=[notfilled])
    password = PasswordField(validators=[notfilled])
    submit = SubmitField() 

class guestregister(FlaskForm):
    username = StringField(validators=[notfilled,checkrepeatuser])
    email = StringField(validators=[notfilled, Email("Invalid Email Address!"),checkrepeatmail])
    password = PasswordField(validators=[notfilled , pwstrength])
    repassword = PasswordField(validators=[notfilled,confirmpw,pwstrength]) 
    submit = SubmitField()
class logout(FlaskForm):
    logout = SubmitField()

class editdb(FlaskForm):
    remove = HiddenField()
    confirm = SubmitField()


class endapplication(FlaskForm):
    submit = SubmitField()

class setcolor(FlaskForm):
    color = HiddenField()
    
class chooseyear(FlaskForm):
    year = HiddenField()  