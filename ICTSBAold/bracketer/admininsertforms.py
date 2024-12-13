from flask_wtf import FlaskForm 
from wtforms import StringField , BooleanField , validators  , SubmitField , PasswordField 
from wtforms.validators import  Email ,Optional
from bracketer import db
from bracketer.models import users , schools , chart2023 , chart2024 

def checkschool(form,field):
    if not db.session.query(schools).filter(schools.SID == field.data).first():
        raise validators.ValidationError("This School ID does not exist in the database! Please insert new school data first!")
    
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
    if len(field.data) < 8 and any(i.isdigit() for i in field.data) == False and (any(i.isupper() for i in field.data) == False or any(i.islower() for i in field.data) == False):
        raise validators.ValidationError("Password length must be at least 8 and contains both letters and digit!") 
    
def optionalforadmin(form,field):
    if db.session.query(users.EMAIL).filter(users.USER == field.data).first():
        if not field.data or field.data.strip() == '':
            raise validators.ValidationError("Please fill all fields!")
    else:
        pass

def repeatedsid(form,field):
    if db.session.query(schools).filter(schools.SID == field.data).first():
        raise validators.ValidationError("The SID you used is duplicated!")

def repeatedsid2024(form,field):
    if db.session.query(chart2024).filter(chart2024.SID == field.data).first():
        raise validators.ValidationError("The SID you used is duplicated!")
    
def repeated2023(form,field):
    if db.session.query(chart2023).filter(chart2023.SID == form.sid.data , chart2023.TID == form.tid.data).first():
        raise validators.ValidationError("This team already existed in the table!")
def repeateduser(form,field):
    if db.session.query(users).filter(users.USER == field.data).first():
        raise validators.ValidationError("This username already existed!")
def check12(form,field):
    if int(field.data) != 1 and int(field.data) != 2:
        raise validators.ValidationError("Only team one or team two is accepted!")
    
def check2team(form,field):
    #when there are zero team , cant set to 2
    if db.session.query(chart2023).filter(chart2023.SID == form.sid.data).count() == 0 and int(field.data) == 2:
        raise validators.ValidationError("You can not set TID to 2 if theres no team of that school!")
def applyrepeat2024(form,field):
    if db.session.query(chart2024).filter(chart2024.SID == form.sid.data).first():
        raise validators.ValidationError("This school already applied!")
    
class insertteam(FlaskForm):
    ## school name
    name = StringField('School Name', validators=[notfilled])
    ##school code
    sid = StringField('School Code', validators=[notfilled,applyrepeat2024,schoolcode])
    ## team 1 members
    t1participant1 = StringField('Participant 1', validators=[notfilled])
    t1participant2 = StringField('Participant 2', validators=[notfilled])
    t1participant3 = StringField('Participant 3', validators=[notfilled])
    t1participant4 = StringField('Participant 4', validators=[notfilled])

    team2 = BooleanField()
    ## team 2 members
    t2participant1 = StringField('Participant 1', validators=[optionalteam2])
    t2participant2 = StringField('Participant 2', validators=[optionalteam2])
    t2participant3 = StringField('Participant 3', validators=[optionalteam2])
    t2participant4 = StringField('Participant 4', validators=[optionalteam2]) 

    submit = SubmitField()


class insertschools(FlaskForm):
    name = StringField('School Name', validators=[notfilled])
    sid = StringField('sid', validators=[notfilled ,repeatedsid ,schoolcode])
    submit = SubmitField()


class insert2023(FlaskForm):
    sid = StringField( validators=[notfilled,repeated2023,checkschool])
    tid = StringField(validators=[notfilled,repeated2023,check12,check2team])
    submit = SubmitField()


class insertnonstudent(FlaskForm):
    username = StringField(validators=[notfilled,repeateduser])
    email = StringField(validators=[Optional(),Email("Invalid Email Address!")])
    password = PasswordField(validators=[notfilled , pwstrength])
    admin = BooleanField()
    submit = SubmitField()

