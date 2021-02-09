from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from jobby import db, last_updated
from jobby.models import Users, Jobs
import bleach

postjob = Blueprint('postjob',__name__)

@postjob.route('/postjob', methods=['GET', 'POST'])
@login_required
def post_job():
    job = Jobs()
    if request.method == 'GET':
        return render_template('Jobs/post-a-job.html')
    else:
        job.job_name = request.form["job_name"]
        job.job_type = request.form["job_type"]
        job.category = request.form["category"]
        job.location = request.form["location"]
        job.salary_min = request.form["salary_min"]
        job.salary_max = request.form["salary_max"]
        job.edu_level = request.form["edu_level"]
        job.exp_min = request.form["exp_min"]
        job.exp_max = request.form["exp_max"]
        job.military = request.form["military"]
        job.position_level = request.form["position_level"]
        job.description = bleach.clean(request.form["description"], tags=bleach.sanitizer.ALLOWED_TAGS+['u', 'br', 'p'])
        job.JobPoster = current_user

        db.session.add(job)
        db.session.commit()
        return redirect(url_for("manage.manageOffers"))
