from bracketer import db , bcrypt
from sqlalchemy.schema import PrimaryKeyConstraint , CheckConstraint , ForeignKeyConstraint
from sqlalchemy import event
class schools(db.Model):      
    __tablename__ = 'schools'                                               
    NAME = db.Column(db.String(length=50), nullable=False)                                                                
    SID = db.Column(db.Integer, autoincrement = True)
    __table_args__ = (
    PrimaryKeyConstraint('SID'),
    )

class chart2024(db.Model):
    SID = db.Column(db.String(length=6))
    TID = db.Column(db.Integer)
    SEED = db.Column(db.Integer, default = 0)
    WON = db.Column(db.Integer, default = 0)
    LOSE = db.Column(db.Boolean , default= False)
    __table_args__ = (
    PrimaryKeyConstraint(SID,TID ),
    CheckConstraint(SEED.in_((0, 1, 2, 3, 4)), name='checkseed'),
    CheckConstraint(TID.in_((1, 2)), name='checkteam'),
    ForeignKeyConstraint(['SID'], ['schools.SID']),
    )

class chart2023(db.Model):
    SID = db.Column(db.String(length=6))
    TID = db.Column(db.Integer)
    SEED = db.Column(db.Integer, default = 0)
    WON = db.Column(db.Integer, default = 0)
    LOSE = db.Column(db.Boolean , default= False)
    __table_args__ = (
    PrimaryKeyConstraint(SID,TID),
    CheckConstraint(SEED.in_((0, 1, 2, 3, 4)), name='checkseed'),
    CheckConstraint(TID.in_((1, 2)), name='checkteam'),
    ForeignKeyConstraint(['SID'], ['schools.SID']),
    )

class chartinfo(db.Model):
    ID = db.Column(db.Integer , primary_key= True) 
    TURN = db.Column(db.Integer, default = 0 )
    AMOUNT = db.Column(db.Integer)

class students(db.Model):
    ID = db.Column(db.Integer , primary_key= True ,autoincrement = True)
    SID = db.Column(db.String(length=6))
    TID = db.Column(db.Integer)
    USER = db.Column(db.String(length=255))
    PW = db.Column(db.String(length=255))
    __table_args__ = (
    ForeignKeyConstraint(['SID', 'TID'], ['chart2024.SID', 'chart2024.TID']),
    )

@event.listens_for(students.PW, 'set', retval=True)
def hash_user_password(target, value, oldvalue , initiator):
    if value != oldvalue:
        return bcrypt.generate_password_hash(value)
    return value

class users(db.Model):
    ID = db.Column(db.Integer , primary_key= True ,autoincrement = True)
    EMAIL = db.Column(db.String(length=255))
    USER = db.Column(db.String(length=255))
    PW = db.Column(db.String(length=255))
    ADMIN = db.Column(db.Boolean , default= False)

@event.listens_for(users.PW, 'set', retval=True)
def hash_user_password(target, value, oldvalue , initiator):
    if value != oldvalue:
        return bcrypt.generate_password_hash(value)
    return value



