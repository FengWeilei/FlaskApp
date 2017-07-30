from flask import Flask,render_template,request,flash,redirect,url_for
from wtforms import StringField, SubmitField,validators, PasswordField
from flask_wtf import FlaskForm
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

app = Flask(__name__)



#Config to mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abc230002'
app.config['MYSQL_DB'] = 'FLASKAPP'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#Initialize the extension
mysql = MySQL(app)

@app.route('/')
def index():
	return render_template("index.html")


class RegisterForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        ##Creat cursor
        cur = mysql.connection.cursor()

        #Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",(name, email,username,password))
        
        #Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash("You are now registered.Please log in.",'success')

        return redirect(url_for('index'))

    return render_template('register.html',form=form)

#CSRF
#app.config.from_object('config')

if __name__ == "__main__":
    app.secret_key="It doesn't matter"
    app.run(debug=True)
