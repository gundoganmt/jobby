from flask import render_template, Blueprint, request, flash, redirect, url_for, abort, jsonify
from flask_login import current_user, login_required
from jobby.models import Bids, Tasks, Users, Jobs, Views, Notification, Reviews, Offers
from jobby import db, csrf, last_updated
manage = Blueprint('manage',__name__)

@manage.route('/dashboard')
@login_required
def dashboard():
    tasks = Tasks.query.filter_by(poster=current_user).all()
    if len(tasks) == 0:
        flash("Proje ilanlarınızın göruntuleme sayıları burada görunur.")
    views = Views.query.filter_by(viewed=current_user).first()
    return render_template('dashboard.html', views=views, tasks=tasks, last_updated=last_updated)

@csrf.exempt
@manage.route('/reviews', methods=['GET', 'POST'])
@login_required
def reviews():
    if request.method == 'GET':
        notifs = Notification.query.filter_by(notification_to=current_user, not_type=5).all()
        for notif in notifs:
            notif.seen = True
        db.session.commit()
        i_review = Reviews.query.filter_by(reviewed_emp=current_user).all()
        if current_user.status == 'professional':
            my_reviews = Reviews.query.filter_by(reviewed_pro=current_user).all()
        else:
            my_reviews = Reviews.query.filter_by(reviewed_emp=current_user).all()
        return render_template('reviews.html', my_reviews=my_reviews, i_review=i_review)
    else:
        review_id, recom, intime, rating = request.form['RadioValues'].split()
        comment = request.form['comment']
        review = Reviews.query.get(int(review_id))
        if recom == 'true':
            review.recommendation = True
        else:
            review.recommendation = False
        if intime == 'true':
            review.in_time = True
        else:
            review.in_time = False
        review.rating = float(rating)
        review.body = comment
        notif = Notification(notification_to=review.reviewed_pro, notification_from=review.reviewed_emp, notedTask=review.reviewed, not_type=5)
        review.reviewed_pro.addRating(float(rating))
        return redirect(request.url)

@manage.route('/get-review/<int:review_id>')
@login_required
def getReview(review_id):
    reviewData = Reviews.query.get(review_id)
    return jsonify({"winner": reviewData.reviewed_pro.name+" "+reviewData.reviewed_pro.surname, "reviewed": reviewData.reviewed.project_name})

# @csrf.exempt
# @manage.route('/reply-review/<int:review_id>', methods=['POST'])
# @login_required
# def replyReview(review_id):
#     reply = request.get_json(force=True)['reply']
#     review = Reviews.query.get(review_id)
#     print(reply)
#     review.reply = reply
#     db.session.commit()
#     return jsonify({"success": True, "pro": review.reviewed_pro.name + " " + review.reviewed_pro.surname})

@manage.route('/active-bids')
@login_required
def activeBids():
    notifs = Notification.query.filter_by(notification_to=current_user, not_type=3).all()
    for notif in notifs:
        notif.seen = True
    db.session.commit()
    bids = Bids.query.filter_by(bidder=current_user).all()
    if len(bids) == 0:
        flash('Henuz bir işe teklifiniz bulunmuyor')
    return render_template('my-active-bids.html', bids=bids, last_updated=last_updated)

@manage.route('/delete-bid/<int:bid_id>')
@login_required
def deleteBid(bid_id):
    data = Bids.query.filter_by(id=bid_id).first_or_404()
    if current_user == data.bidder:
        data.bidded.num_bids -= 1
        current_user.num_bids -= 1
        db.session.delete(data)
        db.session.commit()
        flash("Teklifiniz Silindi")
        return redirect(url_for('.activeBids'))
    #here i should return 500 forbidden
    else:
        abort(404)

@csrf.exempt
@manage.route('/accept-bid/<int:bid_id>', methods=['GET', 'POST'])
@login_required
def acceptBid(bid_id):
    data = Bids.query.filter_by(id=bid_id).first_or_404()
    if request.method == 'GET':
        return jsonify({"bidder": data.bidder.name, "bid_id": bid_id, "bid_amount": data.bid_amount, "bidder_id": data.bidder.id})
    else:
        review = Reviews()
        data.bidded.winner = data.bidder
        not_win = Notification(notification_to=data.bidder, notedTask=data.bidded, not_type=3)
        review.reviewed_pro = data.bidder
        review.reviewed = data.bidded
        review.reviewed_emp = data.bidded.poster
        db.session.add(not_win)
        db.session.add(review)
        db.session.commit()
        return jsonify({"success": True})

@manage.route('/manage-tasks')
@login_required
def manageTasks():
    tasks = Tasks.query.filter_by(poster=current_user).all()
    if len(tasks) == 0:
        flash('Henuz bir proje ilanınız bulunmuyor')
    return render_template('manage-tasks.html', tasks=tasks, last_updated=last_updated)

@manage.route('/manage-offers')
@login_required
def manageOffers():
    notifs = Notification.query.filter_by(notification_to=current_user, not_type=4).all()
    for notif in notifs:
        notif.seen = True
    db.session.commit()
    offers = Offers.query.filter_by(offered=current_user).all()
    return render_template('manage-offers.html', offers=offers, last_updated=last_updated)

@manage.route('/manage-bidders/<int:task_id>')
@login_required
def manageBidders(task_id):
    notifs = Notification.query.filter_by(notification_to=current_user, not_type=1).all()
    for notif in notifs:
        notif.seen = True
    db.session.commit()
    bids = Bids.query.filter_by(task_id=task_id).all()
    task = Tasks.query.filter_by(id=task_id).first_or_404()
    winner_bid = Bids.query.filter_by(bidder=task.winner, bidded=task).first()
    return render_template('manage-bidders.html', bids=bids, task=task, winner_bid=winner_bid, last_updated=last_updated)

@manage.route('/manage-jobs')
@login_required
def manageJobs():
    jobs = Jobs.query.filter_by(employer=current_user).all()
    if len(jobs) == 0:
        flash('Henuz bir iş ilanınız bulunmuyor')
    return render_template('Jobs/manage-jobs.html', jobs=jobs, last_updated=last_updated)

@csrf.exempt
@manage.route('/bookmark/<int:bookmark_id>', methods=['POST'])
def bookmark(bookmark_id):
    type = request.get_json(force=True)
    if current_user.is_anonymous:
        return jsonify({"result": False})
    #if it is user
    if type["bookmarkType"] == 1:
        user = Users.query.filter_by(id=bookmark_id).first()
        current_user.BookmarksUser.append(user)
    else:
        task = Tasks.query.filter_by(id=bookmark_id).first()
        current_user.BookmarksTasks.append(task)
    db.session.commit()
    return jsonify({"success": True})

@csrf.exempt
@manage.route('/unmark/<int:bookmark_id>', methods=['POST'])
@login_required
def unmark(bookmark_id):
    type = request.get_json(force=True)
    #if it is user
    if type["bookmarkType"] == 1:
        user = Users.query.filter_by(id=bookmark_id).first()
        current_user.BookmarksUser.remove(user)
    else:
        task = Tasks.query.filter_by(id=bookmark_id).first()
        current_user.BookmarksTasks.remove(task)
    db.session.commit()
    return jsonify({"success": True})

@manage.route('/bookmarked-tasks')
@login_required
def bookmarkedTasks():
    bookmarked_tasks = current_user.BookmarksTasks.all()
    return render_template('bookmark-tasks.html', bookmarked_tasks=bookmarked_tasks, last_updated=last_updated)

@manage.route('/bookmarked-users')
@login_required
def bookmarkedUsers():
    bookmarked_users = current_user.BookmarksUser.all()
    return render_template('bookmark-users.html', bookmarked_users=bookmarked_users, last_updated=last_updated)
