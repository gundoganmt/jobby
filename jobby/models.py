from flask_login import UserMixin
from jobby import db
from sqlalchemy import or_
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

UserSkills = db.Table('UserSkills',
    db.Column("user_id",db.Integer, db.ForeignKey('Users.id'), primary_key=True),
    db.Column("skill_id",db.Integer, db.ForeignKey('Skills.id'), primary_key=True)
)

TasksSkills = db.Table('TasksSkills',
    db.Column("task_id",db.Integer, db.ForeignKey('Tasks.id'), primary_key=True),
    db.Column("skill_id",db.Integer, db.ForeignKey('Skills.id'), primary_key=True)
)

JobSkills = db.Table('JobSkills',
    db.Column("job_id",db.Integer, db.ForeignKey('Jobs.id'), primary_key=True),
    db.Column("skill_id",db.Integer, db.ForeignKey('Skills.id'), primary_key=True)
)

BookmarksTasks = db.Table('BookmarksTasks',
    db.Column("task_id",db.Integer, db.ForeignKey('Tasks.id'), primary_key=True),
    db.Column("user_id",db.Integer, db.ForeignKey('Users.id'), primary_key=True)
)

BookmarksJobs = db.Table('BookmarksJobs',
    db.Column("task_id",db.Integer, db.ForeignKey('Jobs.id'), primary_key=True),
    db.Column("user_id",db.Integer, db.ForeignKey('Users.id'), primary_key=True)
)

BookmarksUsers = db.Table('BookmarksUsers',
    db.Column("marker_id",db.Integer, db.ForeignKey('Users.id'), primary_key=True),
    db.Column("marked_id",db.Integer, db.ForeignKey('Users.id'), primary_key=True)
)

class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80))
    status = db.Column(db.String(15), default="employer")
    rating = db.Column(db.Integer, default=0.0)
    num_of_rating = db.Column(db.Integer, default=0)
    email_approved = db.Column(db.Boolean, default=False)
    setting_completed = db.Column(db.Boolean, default=False)
    introduction = db.Column(db.Text,default="")
    message_sid = db.Column(db.String(80), default="")
    num_bids = db.Column(db.Integer, default=0)
    member_since = db.Column(db.DateTime)
    profile_picture = db.Column(db.String(80), nullable=True, default="guest.jfif")
    field_of_work = db.Column(db.String(25), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True, default="")
    province = db.Column(db.String(25), nullable=True)
    tagline = db.Column(db.String(80), nullable=False, default="")
    UserSkills = db.relationship('Skills', secondary=UserSkills, backref=db.backref('Users', lazy='dynamic'), lazy='dynamic')
    BookmarksTasks = db.relationship('Tasks', secondary=BookmarksTasks, backref=db.backref('taskMarker', lazy='dynamic'), lazy='dynamic')
    BookmarksJobs = db.relationship('Jobs', secondary=BookmarksJobs, backref=db.backref('jobMarker', lazy='dynamic'), lazy='dynamic')
    BookmarksUser = db.relationship('Users', secondary=BookmarksUsers, backref=db.backref('marker', lazy='dynamic'),
        lazy='dynamic', primaryjoin=(BookmarksUsers.c.marker_id==id), secondaryjoin=(BookmarksUsers.c.marked_id==id))
    tasks = db.relationship('Tasks', foreign_keys='Tasks.user_id', backref='poster', cascade='all, delete-orphan')
    offered = db.relationship('Offers', foreign_keys='Offers.offered_user', backref='offered', cascade='all, delete-orphan')
    offers = db.relationship('Offers', foreign_keys='Offers.offers_user', backref='offers', cascade='all, delete-orphan')
    won = db.relationship('Tasks', foreign_keys='Tasks.winner_id', backref='winner', cascade='all, delete-orphan')
    work_experience = db.relationship('WorkExperiences', backref='Worker', cascade='all, delete-orphan')
    educations = db.relationship('Educations', backref='student', cascade='all, delete-orphan')
    jobs = db.relationship('Jobs', backref='employer', cascade='all, delete-orphan')
    views = db.relationship('Views', backref='viewed', cascade='all, delete-orphan')
    reviews_pro = db.relationship('Reviews', foreign_keys='Reviews.professional', backref='reviewed_pro', cascade='all, delete-orphan')
    reviews_emp = db.relationship('Reviews', foreign_keys='Reviews.employer', backref='reviewed_emp', cascade='all, delete-orphan')
    bids = db.relationship('Bids', backref='bidder', lazy='dynamic', cascade='all, delete-orphan')
    JobApplies = db.relationship('JobApply', backref='employee', lazy='dynamic', cascade='all, delete-orphan')
    messages_sent = db.relationship('Messages', foreign_keys='Messages.sender_id', backref='sender', cascade='all, delete-orphan')
    messages_received = db.relationship('Messages', foreign_keys='Messages.recipient_id', backref='recipient', cascade='all, delete-orphan')
    not_to = db.relationship('Notification', foreign_keys='Notification.not_to', backref='notification_to', cascade='all, delete-orphan')
    not_from = db.relationship('Notification', foreign_keys='Notification.not_from', backref='notification_from', cascade='all, delete-orphan')
    last_message_read_time = db.Column(db.DateTime)

    def num_new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Messages.query.filter_by(recipient=self).filter(
            Messages.timestamp > last_read_time).count()

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Messages.query.filter_by(recipient=self).filter(
            Messages.timestamp > last_read_time)

    def new_notifications(self):
        return Notification.query.filter_by(notification_to=self, seen=False).all()

    def get_confirmation_token(self, expires_sec=1800):
        s = Serializer("qazxswedcvfrtgb", expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_confirmation_token(token):
        s = Serializer("qazxswedcvfrtgb")
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)

    def is_marked_task(self, task):
        return self.BookmarksTasks.filter(BookmarksTasks.c.task_id == task.id).count() > 0

    def is_marked_user(self, user):
        return self.BookmarksUser.filter(BookmarksUsers.c.marked_id == user.id).count() > 0

    def is_bidder(self, task):
        if self.is_anonymous:
            return False
        return self.bids.filter(Bids.task_id == task.id).count() > 0

    def canPost(self):
        if self.email_approved:
            return True
        return False

    def canBid(self):
        if self.setting_completed:
            return True
        return False

    def num_not(self):
        return Notification.query.filter_by(notification_to=self).count()

    def add_view(self):
        weekday = datetime.today().weekday()
        view = Views.query.filter_by(viewed=self).first()
        if not view:
            view = Views(viewed=self,monday=0,tuesday=0,wednesday=0,thursday=0,friday=0,saturday=0,sunday=0)
            db.session.add(view)
        else:
            if weekday == 0:
                view.monday +=1
            elif weekday == 1:
                view.tuesday +=1
            elif weekday == 2:
                view.wednesday +=1
            elif weekday == 3:
                view.thursday +=1
            elif weekday == 4:
                view.friday +=1
            elif weekday == 5:
                view.saturday +=1
            elif weekday == 6:
                view.sunday +=1
        db.session.commit()

    def addRating(self, rating):
        total = self.num_of_rating * self.rating
        self.num_of_rating += 1
        self.rating = (total+rating)/self.num_of_rating
        db.session.commit()

    def total_win(self):
        return Tasks.query.filter_by(winner=self).count()

    def total_reviews(self):
        return Reviews.query.filter_by(reviewed_pro=self).count()

    def recom(self):
        total_success = Reviews.query.filter_by(reviewed_pro=self, recommendation=True).count()
        if self.total_reviews() == 0:
            return 0
        return (total_success/self.total_reviews())*100

    def intime(self):
        total_success = Reviews.query.filter_by(reviewed_pro=self, in_time=True).count()
        if self.total_reviews() == 0:
            return 0
        return (total_success/self.total_reviews())*100

    def is_offered(self):
        return Offers.query.filter_by(offered=self).count() > 0

    def __repr__(self):
        return self.name + " " + self.surname

class Offers(UserMixin, db.Model):
    __tablename__ = 'Offers'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=True)
    message = db.Column(db.String(300), nullable=True)
    filename = db.Column(db.String(50), nullable=True)
    offered_user = db.Column(db.Integer, db.ForeignKey('Users.id'))
    offers_user = db.Column(db.Integer, db.ForeignKey('Users.id'))

class Views(db.Model):
    __tablename__ = 'Views'
    id = db.Column(db.Integer, primary_key=True)
    monday = db.Column(db.Integer, default=0)
    tuesday = db.Column(db.Integer, default=0)
    wednesday = db.Column(db.Integer, default=0)
    thursday = db.Column(db.Integer, default=0)
    friday = db.Column(db.Integer, default=0)
    saturday = db.Column(db.Integer, default=0)
    sunday = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

class Notification(db.Model):
    __tablename__ = 'Notification'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.id'))
    not_from = db.Column(db.Integer, db.ForeignKey('Users.id'))
    not_to = db.Column(db.Integer, db.ForeignKey('Users.id'))
    not_type = db.Column(db.Integer)
    seen = db.Column(db.Boolean, default=False)

class Tasks(UserMixin, db.Model):
    __tablename__ = 'Tasks'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))
    budget_min = db.Column(db.Integer, nullable=True, default=10)
    budget_max = db.Column(db.Integer, nullable=True, default=100000)
    description = db.Column(db.Text, nullable=False)
    num_bids = db.Column(db.Integer, default=0)
    location = db.Column(db.String(100), nullable=True)
    notification = db.relationship('Notification', backref='notedTask', cascade='all, delete-orphan')
    time_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    review = db.relationship('Reviews', backref='reviewed', cascade='all, delete-orphan')
    bids = db.relationship('Bids', backref='bidded', lazy='dynamic', cascade='all, delete-orphan')
    TSkills = db.relationship('Skills', secondary=TasksSkills, backref=db.backref('Tasks', lazy='dynamic'), lazy='dynamic')

    def getAvarageBid(self):
        if self.num_bids == 0:
            return 0
        bids = Bids.query.filter_by(bidded=self).all()
        total = 0
        for bid in bids:
            total += bid.bid_amount
        return int(total/self.num_bids)

    def __repr__(self):
        return self.project_name

class Reviews(UserMixin, db.Model):
    __tablename__ = 'Reviews'
    id = db.Column(db.Integer, primary_key=True)
    recommendation = db.Column(db.Boolean, nullable=True)
    in_time = db.Column(db.Boolean, nullable=True)
    body = db.Column(db.String(300), nullable=True)
    reply = db.Column(db.String(300), nullable=True)
    rating = db.Column(db.Integer)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.id'))
    professional = db.Column(db.Integer, db.ForeignKey('Users.id'))
    employer = db.Column(db.Integer, db.ForeignKey('Users.id'))

class Jobs(UserMixin, db.Model):
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
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
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

class Bids(db.Model):
    __tablename__ = 'Bids'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.id'), nullable=False)
    bid_amount = db.Column(db.Integer, nullable=False)
    num_delivery = db.Column(db.Integer, nullable=True)
    type_delivery = db.Column(db.String(10))
    message = db.Column(db.String(140))

class Messages(db.Model):
    __tablename__ = "Messages"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return self.body

class WorkExperiences(db.Model):
    __tablename__ = "WorkExperiences"
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    start_month = db.Column(db.String(20), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_month = db.Column(db.String(20), nullable=False)
    end_year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return self.position

class Educations(db.Model):
    __tablename__ = "Educations"
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(50), nullable=False)
    school = db.Column(db.String(50), nullable=False)
    start_month = db.Column(db.String(20), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_month = db.Column(db.String(20), nullable=False)
    end_year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return self.field

class Skills(db.Model):
    __tablename__ = 'Skills'
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return self.skill
