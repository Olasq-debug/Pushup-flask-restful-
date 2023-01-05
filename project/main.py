from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from . import db
from .models import Workout, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user)

@main.route('/new', methods = ['GET', 'POST'])
@login_required
def new_workout():
    if request.method == 'POST':
        pushups = request.form.get('pushups')
        comment = request.form.get('comment')

        workout = Workout(pushups=pushups, comment=comment, author = current_user)
        db.session.add(workout)
        db.session.commit()
        return redirect(url_for('main.all_workout'))
    return render_template('new_workout.html')

@main.route('/allworkout')
@login_required
def all_workout():
    user = User.query.filter_by(id=current_user.id).first_or_404()
    workouts = user.workout
    return render_template('allworkout.html', user=user, workouts=workouts)

@main.route('/update_workout/<int:workout_id>/update', methods=['GET', 'POST'])
@login_required
def updateWorkout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if request.method == 'POST':
        workout.pushups = request.form['pushups']
        workout.comment = request.form['comment']
        db.session.commit()
        return redirect(url_for('main.all_workout'))
    return render_template('update_workout.html', workout=workout)

@main.route('/delete_workout/<int:workout_id>/delete')
@login_required
def DeleteWorkout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for('main.all_workout'))
