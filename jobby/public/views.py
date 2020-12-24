from flask import render_template, Blueprint, request, redirect, url_for, abort, flash
from flask_login import current_user
from jobby.models import (
    Tasks, Bids, Users, Jobs,
    WorkExperiences, Educations,
    Views, Notification, Reviews, Offers,
    Notification
    )
from jobby import db, last_updated
from werkzeug.utils import secure_filename
import uuid, os, json
from utils import allowed_offer_file, get_extension, UPLOAD_OFFER_FOLDER

public = Blueprint('public',__name__)

@public.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form['location']
        keyword = request.form['keyword']
        return redirect(url_for('.browseTasks', location=location, keyword=keyword))
    else:
        users = Users.query.filter_by(status='professional').all()[:5]
        featured_tasks = Tasks.query.all()[:3]
        if current_user.is_authenticated:
            return render_template('index-logged-out.html', users=users, featured_tasks=featured_tasks, last_updated=last_updated)
        #return render_template('index-logged-out.html', users=users, featured_tasks=featured_tasks, last_updated=last_updated)
        return render_template('public/index.html')

@public.route('/tasks/<int:task_id>', methods=['GET', 'POST'])
def task_page(task_id):
    task = Tasks.query.filter_by(id=task_id).first_or_404()
    taskbids = Bids.query.filter_by(task_id=task_id).all()
    if request.method == 'GET':
        sk = task.TSkills.all()
        return render_template('single-task-page.html',task=task, sk=sk, taskbids=taskbids, last_updated=last_updated)
    else:
        if current_user.is_authenticated:
            if current_user.status == 'employer':
                flash('Statunuz işveren olarak görunuyor, değiştirmek için ayarlara gidiniz!')
                return redirect(request.url)
            else:
                bid_amount = request.form['bid_amount']
                if not bid_amount:
                    flash('Teklif miktarını girmediniz!')
                    return redirect(request.url)
                num_delivery = request.form['qtyInput']
                type_delivery = request.form['time']
                msg = request.form['message']
                bid = Bids(user_id=current_user.id, task_id=task_id, bid_amount=bid_amount,
                           num_delivery=num_delivery, type_delivery=type_delivery, message=msg)
                notification = Notification(task_id=task_id, not_from=current_user.id, not_to=task.poster.id, not_type=1)
                task.num_bids += 1
                current_user.num_bids += 1
                db.session.add(bid)
                db.session.add(notification)
                db.session.commit()
                return redirect(url_for('manage.activeBids'))
        else:
            flash('Teklif verebilmek için giriş yapmalısınız!')
            return redirect(url_for('account.login'))

@public.route('/jobs/<int:job_id>', methods=['GET', 'POST'])
def job_page(job_id):
    job = Jobs.query.filter_by(id=job_id).first_or_404()
    sk = job.JSkills.all()
    return render_template('Jobs/single-job-page.html', job=job, sk=sk)

@public.route('/browse-tasks')
def browseTasks():
    with open("category.json") as category:
        categories = json.load(category)
    location = request.args.get('lc', type=str)
    keyword = request.args.get('kw', type=str)
    category = request.args.get('ct', type=str)
    page = request.args.get('page', 1, type=int)
    if location:
        tasks = Tasks.query.filter_by(location=location).paginate(page=page, per_page=3)
    elif category:
        tasks = Tasks.query.filter_by(category=category).paginate(page=page, per_page=3)
    else:
        tasks = Tasks.query.paginate(page=page, per_page=5)
    return render_template('tasks-list.html', tasks=tasks, last_updated=last_updated,
        lc=location, ct=category, categories=categories)

@public.route('/freelancer/<int:user_id>', methods=['GET', 'POST'])
def freelancer(user_id):
    user = Users.query.filter_by(id=user_id, status='professional').first_or_404()
    if request.method == 'GET':
        reviews = Reviews.query.filter_by(reviewed_pro=user).all()
        user.add_view()
        workExps = WorkExperiences.query.filter_by(user_id=user_id).all()
        edus = Educations.query.filter_by(user_id=user_id).all()
        sk = user.UserSkills.all()
        return render_template('freelancer-profile.html', user=user, sk=sk, reviews=reviews, workExps=workExps, edus=edus, last_updated=last_updated)
    else:
        if current_user.is_authenticated:
            offer = Offers(offered=user, offers=current_user)
            offer.subject = request.form['subject']
            offer.message = request.form['message']
            if 'file' in request.files:
                file = request.files['file']
                filename = file.filename
            if file and allowed_offer_file(filename):
                filename = secure_filename(filename)
                unique_filename = str(uuid.uuid4())+get_extension(filename)
                offer.filename = unique_filename
                file.save(os.path.join(UPLOAD_OFFER_FOLDER, unique_filename))

            notif = Notification(notification_from=current_user, notification_to=user, not_type=4)
            db.session.add(offer)
            db.session.add(notif)
            db.session.commit()
            flash("Teklifiniz Başarıyla iletildi.")
            return redirect(request.url)
        else:
            flash("Teklif sunabilmek için giriş yapmalısınız!")
            return redirect(url_for('account.login'))

@public.route('/freelancers')
def browseFreelancers():
    with open("category.json") as category:
        categories = json.load(category)
    page = request.args.get('page', 1, type=int)
    users = Users.query.filter_by(status='professional').paginate(page=page, per_page=3)
    return render_template('freelancers-list.html', users=users, last_updated=last_updated, categories=categories)

@public.app_errorhandler(404)
def page_not_found(e):
    return render_template('pages-404.html'), 404
