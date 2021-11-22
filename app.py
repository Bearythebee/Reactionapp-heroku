from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from VideoTrimmer import trim_video
import shutil
from Converttoinput import converttoimages
import os
import numpy as np
import torch
from Model import predict_result


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_BINDS'] = {'TWO': 'sqlite:///two.db',
                                  'THREE': 'sqlite:///final.db'}
db = SQLAlchemy(app)


class mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    clear = db.Column(db.String(100))
    video = db.Column(db.String(10), default="N/A")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'mail ' + str(self.id)

class access(db.Model):
    __bind_key__ = 'TWO'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    pw = db.Column(db.String(100), nullable=False)

class final(db.Model):
    __bind_key__ = 'THREE'
    id = db.Column(db.Integer, primary_key=True)
    video = db.Column(db.String(100), nullable=False)


@app.route("/login", methods=['GET', 'POST'])
def admin_log():
    x = access.query.all()[0].user
    y = access.query.all()[0].pw
    error = None
    if request.method == 'POST':
        if request.form['username'] != x or request.form['password'] != y:
            error = 'Please try again. '
        else:
            return redirect(url_for('show_user'))

    return render_template("admin-log.html", error=error)


@app.route("/", methods=['GET', 'Post'])
def game():
    if request.method == 'POST':
        post_name = request.form['name']
        post_mail = request.form['mail']
        post_clear = request.form['clear']

        new_post = mail(name=post_name, mail=post_mail, clear=post_clear)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/prediction')

    return render_template("Game.html")


@app.route('/delete/<int:id>')
def delete(id):
    post = mail.query.get_or_404(id)
    post2 = final.query.get_or_404(id)

    db.session.delete(post2)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('show_user'))


@app.route("/UVEXi403T")
def show_user():
    allmail = mail.query.all()
    allfinal = final.query.all()
    return render_template("show-users.html", mails=allmail, finals=allfinal)


@app.route('/prediction')
def prediction():

    return render_template("prediction.html")



# Route for prediction functionailty
@app.route('/prediction-upload video', methods=['Post'])
def prediction_uploadvideo():

    start = datetime.now()
    uploaded_file = request.files.get('videofile').read()
    uploaded_timings= request.form['timings']

    if os.path.isdir('tmp/'):
        shutil.rmtree('tmp/')

    if os.path.isdir('tmpframes/'):
        shutil.rmtree('tmpframes/')

    print('##### -  Extracting Relevant Parts - #####')
    trim_video(uploaded_file, uploaded_timings)
    print('##### -  End Of Extraction - #####')
    os.remove('tmp/tmpfile.mp4')
    print('##### -  Extraction of frames and coordinates - #####')
    data = converttoimages()
    print('##### -  End Of Extraction - #####')
    print('##### -  Start Prediction - #####')

    shutil.rmtree('tmp/')
    shutil.rmtree('tmpframes/')

    result = []

    for video in data:
        result.append(predict_result(video))

    print('Number of Videos : {}'.format(len(result)))
    print('Final result: {}'.format(sum(result)/len(result)))

######### Identify potential from video and send result to show-users ##############

    potential = ('Final result: {}'.format(sum(result) / len(result)))

    new_post = final(video=potential)
    db.session.add(new_post)
    db.session.commit()

###################################################################################3

    end = datetime.now()
    print(end - start)

    return render_template("Game.html")


if __name__ == '__main__':
    app.run(debug=True)