from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from jobby import db, last_updated
from jobby.models import Users, Jobs, Skills
import re, bleach

postjob = Blueprint('postjob',__name__)

@postjob.route('/postjob', methods=['GET', 'POST'])
@login_required
def post_job():
    if request.method == 'GET':
        return render_template('Jobs/post-a-job.html')
    else:
        job_name = request.form["job_name"]
        job_type = request.form["job_type"]
        category = request.form["category"]
        location = request.form["location"]
        salary_min = request.form["salary_min"]
        salary_max = request.form["salary_max"]
        edu_level = request.form["edu_level"]
        exp_min = request.form["exp_min"]
        exp_max = request.form["exp_max"]
        military = request.form["military"]
        position_level = request.form["position_level"]
        description = bleach.clean(request.form["description"], tags=bleach.sanitizer.ALLOWED_TAGS+['u', 'br', 'p'])
        return "{}, {}, {}, {}".format(job_name, salary_min, edu_level, description)
