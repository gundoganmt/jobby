from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from jobby import db, last_updated
from jobby.models import Users, Jobs, Skills
import re, bleach

postjob = Blueprint('postjob',__name__)

@postjob.route('/postjob', methods=['GET', 'POST'])
@login_required
def post_job():
    return render_template('Jobs/post-a-job.html')
