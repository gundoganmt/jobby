from flask_login import UserMixin
from jobby import db
from datetime import datetime

JobSkills = db.Table('JobSkills',
    db.Column("job_id",db.Integer, db.ForeignKey('Jobs.id'), primary_key=True),
    db.Column("skill_id",db.Integer, db.ForeignKey('Skills.id'), primary_key=True)
)

class Company(UserMixin, db.Model):
    __tablename__ = 'Company'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80))
    company_name = db.Column(db.String(100), nullable=True, default="")
    profile_picture = db.Column(db.String(80), nullable=True, default="guest.jfif")
    sector = db.Column(db.String(50))
    worker_num = db.Column(db.Integer)
    founded = db.Column(db.Integer)
    website = db.Column(db.String(100))
    location = db.Column(db.String(200))
    about = db.Column(db.Text)
    member_since = db.Column(db.DateTime)
    jobs = db.relationship('Jobs', backref='JobPoster', cascade='all, delete-orphan')

class Jobs(db.Model):
    __tablename__ = 'Jobs'
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))
    job_type = db.Column(db.String(50))
    salary_min = db.Column(db.Integer, nullable=True)
    salary_max = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=False)
    num_apply = db.Column(db.Integer, default=0)
    location = db.Column(db.String(25))
    time_posted = db.Column(db.DateTime, default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('Company.id'))
    appliance = db.relationship('JobApply', backref='applied', lazy='dynamic', cascade='all, delete-orphan')
    JSkills = db.relationship('Skills', secondary=JobSkills, backref=db.backref('Jobs', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return self.job_name

class JobApply(db.Model):
    __tablename__ = 'JobApply'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('Jobs.id'), nullable=False)
    message = db.Column(db.String(140))
