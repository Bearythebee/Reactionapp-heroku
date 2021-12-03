from flask import Flask
from main import mainbp as main_blueprint
from dbworker import db
from Send_mail import Sendmail


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
    app.config['SQLALCHEMY_BINDS'] = {'TWO': 'sqlite:///two.db',
                                      'THREE': 'sqlite:///final.db'}


    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    #app.config['MAIL_DEBUG'] = True
    app.config['MAIL_USERNAME'] = 'fortesting2222@hotmail.com'
    app.config['MAIL_PASSWORD'] = 'Fortestingacc123'
    app.config['MAIL_DEFAULT_SENDER'] = 'fortesting2222@hotmail.com'
    app.config['MAIL_MAX_EMAILS'] = None
    #app.config['MAIL_SUPPRESS_SEND'] = False
    app.config['MAIL_ASCII_ATTACHMENTS'] = False


    Sendmail.init_app(app)
    db.init_app(app)
    app.register_blueprint(main_blueprint)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)