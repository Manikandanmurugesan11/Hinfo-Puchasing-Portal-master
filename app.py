from flask import Flask, redirect, url_for, request,render_template,session, flash
app = Flask(__name__)
import smtplib
import sqlite3 
import binascii
# from Crypto.Cipher import AES

sqlite_file='DATABASE.sqlite'
global globalFID
app.secret_key = 'thisisdatabase'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

import snowflake.connector
PASSWORD = 'Hinfotech@123'
WAREHOUSE = 'COMPUTE_WH'
USER ='HINFOTECH'
ACCOUNT ='xo63848.ap-south-1'
DATABASE ='IOT'
SCHEMA ='IOT'

conns = snowflake.connector.connect(
                user=USER,
                password=PASSWORD,
                account=ACCOUNT,
                warehouse=WAREHOUSE,
                database=DATABASE,
                schema=SCHEMA
                )
curs=conns.cursor()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def encrypt(s):
    s =s 
    # obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    # s1=s.rjust(16,',')
    # u=obj.encrypt(s1)
    # bar=binascii.b2a_hex(u)
    return s


def decryption(s):
    s = s
    # obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    # u=binascii.a2b_hex(s)
    # u1=obj.decrypt(u)
    # ux=u1.strip(',')
    return s

@app.route('/')           
@app.route('/<name>',methods=['GET','POST'])
def index(name=None):
    return render_template('HomePage.html',session=session,text=name)

@app.route('/purchaser',methods=['GET','POST'])
def purchaser(name=None):
    return render_template('purchaser_login.html',session=session,text=name)


@app.route('/success/<name>',methods=['GET','POST'])
def success(name):
    return name

@app.route('/signuppage',methods=['GET','POST'])
def signuppage():
   return render_template('SignUp.html')

@app.route('/forgotpassword',methods=['GET','POST'])
@app.route('/forgotpassword/<name>')
def forgotpassword(name=None):
   return render_template('Forgot.html',text=name)

@app.route('/rfid_login',methods=['GET','POST'])
    
def flask():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM user').fetchall()
    conn.close()
    return render_template('index.html')

def rfid_login():
    if request.method == 'GET':
        rfid = int(request.json['num1'])
        query =("select * from token where ID = %s"% (rfid))
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchall()
        if results:
            available = 1
            return f'{available}'
        else:
            available = 0
            return f'{available}'

@app.route('/product_details',methods = ['POST', 'GET'])
def product_details():
        query = ("select * from product1")
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchall()
        mytuple = sorted(results)
        print(results)
        return render_template('product_details.html',rows=mytuple,)

@app.route('/customer_details',methods = ['POST', 'GET'])
def customer_details():
        query = ("select * from customer")
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchall()
        return render_template('customer_details.html',rows=results,)

@app.route("/create_purchaser",methods=['GET','POST'])
def create_purchaser():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        address=request.form['address']
        phone=request.form['phone']
        conn = sqlite3.connect(sqlite_file)
        curs=conns.cursor()
        sql="INSERT INTO customer(User_Name,Email_id,User_Address,Telephone) values (%s,%s,%s,%s)"
        value = (name,email,address,phone)
        curs = conns.cursor().execute(sql,value)
        conns.commit()
        flash('customer added successfully','success')
        return redirect(url_for("customer_details"))
    return render_template("create_purchaser.html")


@app.route("/reset_password", methods=["GET","POST"])
def reset_password(name=None):
    return render_template("reset_password.html",session=session,text=name)

@app.route('/resetpass',methods = ['POST', 'GET'])
def resetpass():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['new_password']
        passcon = request.form['new_pass_confirm']
        action = request.form.get('action', '')
        print("----------test1start----------")
        print(request.form.get)
        print("----------test1end----------")
        if email is None:
            message = "Invalid/Unknown user_id."
            return render_template("reset_password.html",name=message)
            
        elif password != passcon:
            message = "Password mismatch"
            return render_template("reset_password.html",name=message)
            
        else:
            sql = ("update users1 set password = '%s' WHERE EMAIL_ID = '%s'" %(password,email))
            curs=conns.cursor()
            curs = conns.cursor().execute(sql)
            message = "Password Reset successfully!" 
            return redirect(url_for("reset_password"))
    return render_template("reset_password.html",name=message)


  
@app.route('/edit_purchaser/<string:id>',methods = ['POST','GET'])  
def edit_purchaser(id):
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        address=request.form['address']
        phone=request.form['phone']
        conn = sqlite3.connect(sqlite_file)
        curs=conns.cursor()
        task = "update customer set User_Name = %s, Email_id = %s,User_Address = %s,Telephone = %s WHERE Rfid_Id = %s"
        value = (name,email,address,phone,id)
        curs = conns.cursor().execute(task,value)
        conn.commit()
        flash('customer updated successfully','success')
        return redirect (url_for('customer_details'))
    
    if request.method=='GET':
        conn = sqlite3.connect(sqlite_file)
        curs=conns.cursor()
        sql="select * from customer where Rfid_Id= %s"
        curs = conns.cursor().execute(sql,[id])
        results = curs.fetchone()
        return render_template("edit_purchaser.html", results = results)


@app.route('/delete_purchaser/<string:id>',methods = ['POST', 'GET'])  
def delete_purchaser(id):
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    curs=conns.cursor()
    sql="delete from customer where Rfid_Id=%s"
    curs = conns.cursor().execute(sql,[id])
    conn.close()
    flash('customer deleted successfully','success')
    return redirect(url_for("customer_details"))


@app.route('/purchaser_details',methods = ['POST', 'GET'])
def purchaser_login():
    user_id = request.form['UserName']
    user_id=encrypt(user_id)
    print(user_id)
    pwd1 = request.form['Password']
    pwd=encrypt(pwd1)
    print (pwd)
    #validate if all fields are entered
    if not user_id or not pwd:
        error = "Any of the fields cannot be left blank"
        return redirect(url_for('purchaser', name=error))

    query = ("select * from purchaser1 where id = '%s' and password = '%s' " %(user_id,pwd))
    query = ("select * from purchaser1 where id = '%s' and password = '%s' " %(user_id,pwd))

    curs = conns.cursor().execute(query)
    query_id = curs.sfqid
    curs.get_results_from_sfqid(query_id)
    results = curs.fetchall()

    if results:
        query = ("select * from purchaser_details1 where PURCHASER_ID = '%s' "%(user_id))
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchall()
        mytuple = sorted(results)
        print(results)
        return render_template('purchaser_details.html',rows=mytuple)
    else:
        error = "Username/Password is incorrect!"
        return redirect(url_for('purchaser', name=error))


@app.route('/vendor_dashboard',methods = ['POST', 'GET'])
def login():
    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    curs=conns.cursor()
    SIDtopass = 0
    user1 = request.form['UserName']
    user=encrypt(user1)
    print(user)
    pwd1 = request.form['Password']
    pwd=encrypt(pwd1)
    print (pwd)
    #validate if all fields are entered
    if not user or not pwd:
        error = "Any of the fields cannot be left blank"
        return redirect(url_for('index', name=error))

    query = ("select * from vendor1 where shopname = '%s' and password = '%s' " %(user,pwd))
    curs = conns.cursor().execute(query)
    query_id = curs.sfqid
    curs.get_results_from_sfqid(query_id)
    results = curs.fetchall()

    if results:
        query = ("select * from product1")
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchall()
        mytuple = sorted(results)
        print(results)
        # return render_template('product_details.html',rows=mytuple)
        return render_template('index.html',rows=mytuple)
    
    else:
        error = "Username/Password is incorrect!"
        return redirect(url_for('index', name=error))
    
    if results:
        query = ("select * from customer")
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchall()
        mytuple = sorted(results)
        print(results)
        # return render_template('product_details.html',rows=mytuple)
        return render_template('index.html',rows=mytuple)
    else:
        error = "Username/Password is incorrect!"
        return redirect(url_for('index', name=error))
    
# @app.route('/forgothandling',methods = ['POST', 'GET'])
# def forgothandling():
#     email = request.form['Email']
#     action = request.form.get('action', '')

#     if not email or not action:``
#         error = "Any of the fields cannot be left blank"
#         return redirect(url_for('forgotpassword', name=error))

#     if action == '':
#         c.execute("select decryption(Password) from where email = ?", (email,))
#         f = c.fetchone()
#         if not f:
#             error = "Email entered is incorrect!"
#             return redirect(url_for('forgotpassword', name=error))
#         else:
#         message = "An Email containing password has been sent to your registered email ID"
#         return redirect(url_for('forgotpassword', name=message))
#     elif action == 'Faculty':
#         c.execute("select decryption(Password) from FacultyLoginTable where Email = ?", (email,))
#         f = c.fetchall()
#         if not f:
#             error = "Email entered is incorrect!"
#             return redirect(url_for('forgotpassword', name=error))
#         else:
#             to = email
#             gmail_user = 'studentacademyportal@gmail.com'
#             gmail_pwd = 'hellostudent'
#             smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
#             smtpserver.ehlo()
#             smtpserver.starttls()
#             smtpserver.ehlo()  # extra characters to permit edit
#             smtpserver.login(gmail_user, gmail_pwd)
#             header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Confidential Message \n'
#             print(header)
#             msg = header + '\n This message contains your password to Student Academic Portal \n\n' + str(f)
#             smtpserver.sendmail(gmail_user, to, msg)
#             print("done!")
#             smtpserver.quit()
#             message = "An Email containing password has been sent to your registered email ID"
#             return redirect(url_for('forgotpassword', name=message))


@app.route('/updateproducts', methods=['GET', 'POST'])
def updateproducts():
    curs=conns.cursor()
    id=request.form.get('ID')
    product_name=request.form.get('NAME')
    product_price=request.form.get('PRICE')
    prd_qty=request.form.get('QUANTITY')
    task = (id, product_name, product_price, prd_qty)
    sql = "update GradeTable set MidTerm1 = ?, MidTerm2 = ?, MidTerm3 = ?, FinalGrade = ? where SID = ? and FID = ? and CourseId = ?"
    curs = conns.cursor().execute(sql)
    a = curs.rowcount
    if a == 0:
        return 'no update happen'
    else:
    # commit and close connection

        curs=conns.cursor()

        sql =("")
        curs = conns.cursor().execute(sql)

        # sname2 = cur.fetchone()
        # print(sname2)
        # con1 = sqlite3.connect('DATABASE.sqlite')
        # con1.create_function('decryption', 1, decryption)
        # con1.row_factory = sqlite3.Row
        # cur1 = con1.cursor()
        # cur1.execute(
        # "SELECT s.StudentName as sn,g.SID as sid,g.CourseId as crid,decryption(g.MidTerm1) as mt1,decryption(g.MidTerm2) as mt2,decryption(g.MidTerm3) as mt3,decryption(g.FinalGrade) as fg FROM GradeTable g Inner Join StudentLoginTable s on g.SID=S.SID WHERE g.FID=?",
        # z)
        # rows2 = cur1.fetchall()
        # for i in rows2:
        #     print(i)
        return render_template('product_update.html')


@app.route('/callhtml/<a>/<b>/<c>/<d>/<e>' , methods=['GET', 'POST'])
def callhtml(a,b,c,d,e):
    return render_template('update.html',a=a,b=b,c=c,d=d,e=e)


@app.route('/clear')
def clearsession():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])

def signup():

    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    curs=conns.cursor()
    name = request.form['Name']
    action = request.form.get('action', '')
    user1 = request.form['UserName']
    user=encrypt(user1)
    email = request.form['email']

    # validate if all fields are entered
    # if not action or not user or not pwd or not email or not name:
    #     error = "Any of the fields cannot be left blank"
    #     return redirect(url_for('success', name=error))

    # validate if all fields are entered
    if not action:
        error = "Any of the fields cannot be left blank"
        return redirect(url_for('success', name=error))

    if action == 'Add':
        if not action or not user or not email or not name:
            error = "Any of the fields cannot be left blank"
            return redirect(url_for('success', name=error))

        query =("select * from purchaser1 where ID = %s"% (user1))
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchall()
 
        if results:
            msg = "User already exists"
        else:
            curs.execute("INSERT INTO purchaser1(ID, USERNAME,EMAIL_ID) ""VALUES(%s, %s, %s)", (user,name,email))
            msg = "User has been registered successfully"

        return redirect(url_for('success', name=msg))
    elif action == 'Remove':
        if not user:
            error = "Enter user and name fields cannot be left blank"
            return redirect(url_for('success', name=error))
        query =("select * from purchaser1 where ID = %s"% (user1))
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchall()

        if results:
            curs.execute("DELETE FROM purchaser1 where ID = %s"%(user))
            msg = "User has been removed successfully"
        else:
            msg = "User doesn't exists"
        return redirect(url_for('success', name=msg))


if __name__ == '__main__':
    app.secret._key='hinfo@123'
    app.run(use_reloader=True)