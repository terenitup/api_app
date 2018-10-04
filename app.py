from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy 

from flask.ext.heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
heroku = Heroku(app)
db = SQLAlchemy(app)


# Create database model

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rereg', methods=['POST'])
def rereg():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        reg = User(email)
        db.session.add(reg)
        db.session.commit()
        return render_template('success.html')
    return render_template('index.html')

@app.route('/return_emails', methods=['GET'])
def return_emails():
    all_emails = db.session.query(User.email).all()
    return jsonify(all_emails)


if __name__ == '__main__': 
    app.debug = True 
    app.run()