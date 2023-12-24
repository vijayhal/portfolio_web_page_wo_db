from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
# from flask_sqlalchemy import SQLAlchemy
import smtplib
import os

# On Windows type:
# python -m pip install -r requirements.txt

# db = SQLAlchemy()
#
app = Flask(__name__)

global user_mail
global password

user_mail = os.environ.get('USER_ID')
login_password = os.environ.get('USER_PASSWORD')

# to create a form we have to provide secret key


app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)


# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new_book_msg.db"
#
# db.init_app(app)



# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_inpt = db.Column(db.String(50), nullable=False)
#     second_inpt = db.Column(db.String(50), nullable=False)
#     subject_inpt = db.Column(db.String(500), nullable=False)


# Optional: this will allow each book object to be identified by its title when printed.
# def __repr__(self):
#     return f'<Book {self.title}>'
# Create table schema in the database. Requires application context.
# with app.app_context():
#     db.create_all()



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/submit_form', methods=["GET", "POST"])
def submit():
    if request.method == 'POST':

        # data = request.form
        # with app.app_context():
        #     new_book = Book(first_inpt = data["full_name"], second_inpt = data["email_id"], subject_inpt = data["subject"])
        #     db.session.add(new_book)
        #     db.session.commit()



        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            data = request.form
            connection.starttls()
            connection.login(user=user_mail, password=login_password)
            connection.sendmail(
            from_addr=user_mail,
            to_addrs = {data["email_id"]},
            msg=f'subject:{data["subject"]}\n\nDear {data["full_name"]},\n\nThanks for your email.\n\n'
                            f'Your Message: {data["message_input"]}\n\n\n I will revert to you, soon.\n\n'
                f'Regards\n\nVijay M Halagani')


            return render_template("submitted.html")

    else:

        return f"Enter data correctly"




if __name__ == "__main__":
    app.run(debug=False)