from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy 

from flask.ext.heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://znuruigvzerygf:eb6b81ead56323a0284c9d77b8729aea89daee4822fc03ab61a2c24cebc52284@ec2-54-235-90-0.compute-1.amazonaws.com:5432/d57qln1fkivs85'
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