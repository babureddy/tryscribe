from flask import Flask, render_template, flash, request, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug import secure_filename
import os
import smtplib
import sqlite3
import db
from flask_mail import Mail, Message
 
# App  config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
file_name = "c:\\Users\\LOKESH\\tryscribe\\campaign.csv";
UPLOAD_FOLDER = 'c:\\Users\\LOKESH\\tryscribe\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

conn = sqlite3.connect('database.db')
#print ("Opened database successfully");
#conn.execute('DROP TABLE campaign')
conn.execute('CREATE TABLE if not exists campaign (id integer primary key AUTOINCREMENT, name TEXT NOT NULL, stages integer NOT NULL, schedule integer NOT NULL, subject TEXT NOT NULL, body TEXT NOT NULL, email TEXT, status integer default 0 )')

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
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        fp = open(app.config['UPLOAD_FOLDER'] + '\\' + filename)
        emails = fp.read()
        db.saveRecipients(emails)		
    return redirect("/campaigns", code=302)

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
 
@app.route("/campaigns", methods=['GET', 'POST'])
def campaigns():
	return render_template("list.html",rows = db.campaigns())

@app.route("/active/<id>", methods=['GET', 'POST'])
@app.route("/Active/<id>", methods=['GET', 'POST'])
def active(id):
	db.updateStatus(id,1)
	sendmail(id)
	return redirect("/campaigns", code=302)

@app.route("/inactive/<id>", methods=['GET', 'POST'])
@app.route("/Inactive/<id>", methods=['GET', 'POST'])
def inactive(id):
	db.updateStatus(id,0)
	return redirect("/campaigns", code=302)

@app.route("/delete/<id>", methods=['GET', 'POST'])
def delete(id):
	db.deleteCampaign(id)
	return redirect("/campaigns", code=302)

@app.route("/sendmail/<id>", methods=['GET', 'POST'])
def sendmail(id):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login(os.environ['GMAIL_ID'], os.environ['GMAIL_PWD'])
	campaign = db.list(id)
	subject = campaign[0]['subject']
	body = campaign[0]['body']
	emails = campaign[0]['email']

	msg = "\r\n".join([
	  "From: " + os.environ['GMAIL_ID'],
	  "To: " + emails,
	  "Subject: " + subject,
	  "",
	  body
	  ])
	server.sendmail(os.environ['GMAIL_ID'],os.environ['GMAIL_ID'], msg)
	return redirect("/campaigns", code=302)

def saveCampaign(request):
    r = {"name":request.form["name"],"stages":request.form["stages"],"schedule":request.form["schedule"],"subject":request.form["subject"],"body":request.form["body"]}
    db.saveCampaign(r)
    return "Campaign created successfully"

if __name__ == "__main__":
    app.run()
