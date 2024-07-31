
from flask_wtf import FlaskForm 
from flask import json
from wtforms import StringField , BooleanField , validators , HiddenField , SubmitField , PasswordField , IntegerField
from wtforms.validators import  Email ,Optional
from bracketer import db
from bracketer.models import users , schools , chart2023 , chart2024 , students
from re import search
from hanzidentifier import identify, BOTH


def check12(form,field):
    if field.data != 1 and field.data!= 2:
        raise validators.ValidationError("Only team one or team two is accepted!")

def checkschool(form,field):
    if not db.session.query(schools).filter(schools.SID == field.data).first():
        raise validators.ValidationError("This School ID does not exist in the database! Please insert new school data first!")
    
def check2team2024(form,field):
    og = json.loads(form.original.data)
    #hen u didnt change the sid but you changed the tid , and theres only one team , you can not change teamno to 2
    #or when there are no teams with the same sid , you can not change teamno to 2
    if (db.session.query(chart2024).filter(chart2024.SID == form.sid.data).count() == 1 and og['chartsid'] == form.sid.data and field.data == '2') or (db.session.query(chart2024).filter(chart2024.SID == form.sid.data).count() == 0 and field.data == '2'):
        raise validators.ValidationError("You can not set TID to 2 if theres only one team of that school!")

def check2sid2024(form,field):
    og = json.loads(form.original.data)
    #if after updating the team's sid , there will be three teams
    if db.session.query(chart2024).filter(chart2024.SID == field.data).count() == 2 and og['chartsid'] != int(field.data):
        raise validators.ValidationError("That school already have two teams!")

def check2team2023(form,field):
    og = json.loads(form.original.data)
    #hen u didnt change the sid but you changed the tid , and theres only one team , you can not change teamno to 2
    #or when there are no teams with the same sid , you can not change teamno to 2
    if (db.session.query(chart2023).filter(chart2023.SID == form.sid.data).count() == 1 and og['sid2023'] == form.sid.data and field.data == '2') or (db.session.query(chart2024).filter(chart2024.SID == form.sid.data).count() == 0 and field.data == '2'):
        raise validators.ValidationError("You can not set TID to 2 if theres only one team of that school!")

def check2sid2023(form,field):
    og = json.loads(form.original.data)
    #if after updating the team's sid , there will be three teams
    if db.session.query(chart2023).filter(chart2023.SID == field.data).count() == 2 and og['sid2023'] != int(field.data):
        raise validators.ValidationError("That school already have two teams!")

def checkrepeatid(form,field):
    og = json.loads(form.original.data)

    if field.data: #if id is changed
        id = int(field.data)
        #if the user changed the id and there are already someone using that id --> arise error
        if db.session.query(users).filter(users.ID == id).count() == 1 and og['userid'] != id: 
            raise validators.ValidationError("Do not use duplicated ID!")

def checkrepeatsid(form,field):
    og = json.loads(form.original.data)
    if field.data: #if id is changed
        id = int(field.data)
        #if the user changed the sid and there are already some school using that sid --> arise error
        if db.session.query(schools).filter(schools.SID == id).count() == 1 and og['schoolsid'] != id: 
            raise validators.ValidationError("Do not use duplicated SID!")
        

def checkstuid(form,field):
    og = json.loads(form.original.data)
    if db.session.query(students).filter(students.ID == field.data).count() == 1 and og['studentid'] != int(field.data): 
        raise validators.ValidationError("Duplicated student id!")
    
def pwstrength(form,field):
    if len(field.data) < 8 or any(i.isdigit() for i in field.data) == False or (any(i.isupper() for i in field.data) == False and any(i.islower() for i in field.data) == False):
        raise validators.ValidationError("Password length must be at least 8 and contains both letters and digit!") 


## update forms 

class update2024(FlaskForm):
    name = StringField(validators=[Optional()])
    sid = IntegerField(validators=[Optional(),checkschool,check2sid2024,check2team2024])
    tid = IntegerField(validators=[Optional(),check12])
    seed = IntegerField(validators=[Optional()])
    losed = BooleanField(validators=[Optional()])
    original = HiddenField()
    submit = SubmitField()

class updatenonstudent(FlaskForm):
    id = StringField(validators=[checkrepeatid])
    user = StringField(validators=[Optional()])
    email = StringField(validators=[Optional(),Email("Invalid Email Address!")])
    admin = BooleanField(validators=[Optional()])
    pw = StringField(validators=[Optional(), pwstrength])
    original = HiddenField()
    submit = SubmitField()

class updatestudent(FlaskForm):
    id = StringField(validators=[Optional(),checkstuid])
    user = StringField(validators=[Optional()])
    pw = StringField(validators=[Optional(), pwstrength])
    original = HiddenField()
    submit = SubmitField()

class update2023(FlaskForm):
    name = StringField(validators=[Optional()])
    sid = IntegerField(validators=[Optional(),checkschool,check2team2023,check2sid2023])
    tid = IntegerField(validators=[Optional(),check12])
    seed = IntegerField(validators=[Optional()])
    losed = BooleanField(validators=[Optional()])
    won = IntegerField(validators=[Optional()])
    original = HiddenField()
    submit = SubmitField()


class updateschool(FlaskForm):
    sid = StringField(validators=[Optional(),checkrepeatsid])
    name = StringField(validators=[Optional()])
    original = HiddenField()
    submit = SubmitField()
