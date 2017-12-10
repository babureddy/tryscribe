from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug import secure_filename
import os
import smtplib
import sqlite3
import db
 
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
file_name = "c:\\Users\\LOKESH\\tryscribe\\campaign.csv";
UPLOAD_FOLDER = 'c:\\Users\\LOKESH\\tryscribe\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

conn = sqlite3.connect('database.db')
#print ("Opened database successfully");
conn.execute('DROP TABLE campaign')
conn.execute('CREATE TABLE campaign (id integer primary key AUTOINCREMENT, name TEXT NOT NULL, stages integer NOT NULL, schedule integer NOT NULL, subject TEXT NOT NULL, body TEXT NOT NULL)')

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    stages = TextField('Stages:', validators=[validators.required()])
    schedule = TextField('Schedule:', validators=[validators.required()])
    subject = TextField('Subject:', validators=[validators.required()])
    body = TextField('Body:', validators=[validators.required()])

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        flash('filename ' + file.filename)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "file uploaded successfully"

@app.route("/hello", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form) 
    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
        stages=request.form['stages']
        schedule=request.form['schedule']
        subject=request.form['subject']
        body=request.form['body']
        #print (name + ' ' + stages + ' ' + schedule + ' ' + subject + ' ' + body)
 
        if form.validate():
            # Save the comment here.
            msg = name + "\\t" + stages + "\\t" + schedule + "\\t" + subject + "\\t" + body
            #save(msg)
            saveCampaign(request)
            with open(file_name) as f:
                content = ""
                for line in f.readlines():
                    flash(line)
            return render_template('recipients.html', form=form)
        else:
            flash('All the form fields are required. ')
 
    return render_template('hello.html', form=form)
 
@app.route("/list", methods=['GET', 'POST'])
def list():
	return render_template("list.html",rows = db.list())


@app.route("/sendmail", methods=['GET', 'POST'])
def sendmail():
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	#Next, log in to the server
	server.login("babureddy1969@gmail.com", "babs331969")

	#Send the mail
	msg = "\r\n".join([
	  "From: babureddy1969@gmail.com",
	  "To: babureddy@rocketmail.com",
	  "Subject: Just a message",
	  "",
	  "This is cool"
	  ])
	server.sendmail("babureddy1969@gmail.com", "babureddy@rocketmail.com", msg)
	return "mail sent ok"

def saveCampaign(request):
    r = {"name":request.form["name"],"stages":request.form["stages"],"schedule":request.form["schedule"],"subject":request.form["subject"],"body":request.form["body"]}
    db.saveCampaign(r)
    return "Campaign created successfully"

if __name__ == "__main__":
    app.run()
