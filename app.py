from jobby import create_app, socketio
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from jobby.models import (
    Users, Tasks, Bids, Skills,
    Messages, Jobs, WorkExperiences,
    Educations, Views, Notification,
    Reviews, Offers
    )
from jobby import db

app = create_app()
admin = Admin(app)
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Tasks, db.session))
admin.add_view(ModelView(Bids, db.session))
admin.add_view(ModelView(Skills, db.session))
admin.add_view(ModelView(Messages, db.session))
admin.add_view(ModelView(Jobs, db.session))
admin.add_view(ModelView(WorkExperiences, db.session))
admin.add_view(ModelView(Educations, db.session))
admin.add_view(ModelView(Views, db.session))
admin.add_view(ModelView(Notification, db.session))
admin.add_view(ModelView(Reviews, db.session))
admin.add_view(ModelView(Offers, db.session))

if __name__ == '__main__':
    socketio.run(app, debug=True)
