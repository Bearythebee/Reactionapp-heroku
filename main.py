from flask import Blueprint, render_template, request, redirect, url_for
from dbworker import db
from datetime import datetime
from VideoTrimmer import trim_video
import shutil
from Converttoinput import converttoimages
import os
from databases import mail, access, final
from Model import predict_result

mainbp = Blueprint('main', __name__)

@mainbp.route("/login", methods=['GET', 'POST'])
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


@mainbp.route("/", methods=['GET', 'Post'])
def game():
    if request.method == 'POST':
        db.session.query(mail).delete()

        post_name = request.form['name']
        post_mail = request.form['mail']
        post_clear = request.form['clear']

        new_post = mail(name=post_name, mail=post_mail, clear=post_clear)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/prediction#session')

    return render_template("Game.html")


@mainbp.route('/delete/<int:id>')
def delete(id):
    post2 = final.query.get_or_404(id)
    db.session.delete(post2)
    db.session.commit()
    return redirect(url_for('show_user'))


@mainbp.route("/UVEXi403T")
def show_user():
    allfinal = final.query.all()
    return render_template("show-users.html", finals=allfinal)


@mainbp.route('/prediction')
def prediction():

    return render_template("Prediction.html")

@mainbp.route('/whatvideo')
def whatvideo():

    return render_template("whatvideo.html")

@mainbp.route('/instruction')
def instruction():

    return render_template("instruction.html")



# Route for prediction functionailty
@mainbp.route('/prediction-upload video', methods=['Post'])
def prediction_uploadvideo():

    start = datetime.now()
    uploaded_file = request.files.get('videofile').read()
    uploaded_timings= request.form['timings']

    if os.path.isdir('tmp/'):
        shutil.rmtree('tmp/')

    if os.path.isdir('tmpframes/'):
        shutil.rmtree('tmpframes/')

    print('##### -  Extracting Relevant Parts - #####')
    trim_video.delay(uploaded_file, uploaded_timings)
    print('##### -  End Of Extraction - #####')
    os.remove('tmp/tmpfile.mp4')
    print('##### -  Extraction of frames and coordinates - #####')
    data = converttoimages().delay()
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
    name = mail.query.all()[0].name
    email = mail.query.all()[0].mail
    clear = mail.query.all()[0].clear
    potential = ('{}'.format(sum(result) / len(result)))

    new_post = final(name=name, mail=email, clear=clear, video=potential)
    db.session.add(new_post)

    remove = mail.query.get_or_404(1)
    db.session.delete(remove)
    db.session.commit()

###################################################################################3

    end = datetime.now()
    print(end - start)

    return render_template("Game.html")
