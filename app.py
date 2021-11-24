from flask import Flask
from main import mainbp as main_blueprint
from dbworker import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
    app.config['SQLALCHEMY_BINDS'] = {'TWO': 'sqlite:///two.db',
                                      'THREE': 'sqlite:///final.db'}

    db.init_app(app)
    app.register_blueprint(main_blueprint)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)