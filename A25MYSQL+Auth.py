#-----MySQL---heroes_db----

#1)mysql
#2)flask
#3)web interface
#4)API
#5)Authentication(Reg/Log)


from flask import Flask,request,redirect,render_template,jsonify
import mysql.connector
import bcrypt #R/L

app=Flask(__name__)
# this will store usernames who logged in
logged_users=set()


@app.route('/')
def show():
    c=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database ="heroes_db")

    cursor=c.cursor()
    cursor.execute('''SELECT * FROM heroes ORDER BY rank ASC''')
    row=cursor.fetchall()

    c.close()
    return render_template("index.html",heroes=row)

@app.route('/add',methods=['POST'])
def add_hero():

    nameweb=request.form.get("newname")
    skillweb=request.form.get("newskill")
    rankweb=request.form.get("newrank")

    c=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="heroes_db")

    cursor=c.cursor()

    cursor.execute(
        "INSERT INTO heroes(name,skill,rank) VALUES(%s,%s,%s)",
        (nameweb,skillweb,rankweb))

    c.commit()
    c.close()

    return redirect('/')

@app.route('/del/', methods=['POST'])
def del_hero():
    dname=request.form.get("delname")

    c=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="heroes_db")

    cursor=c.cursor()
    cursor.execute('''DELETE FROM heroes WHERE name=%s'''
    ,(dname,))
    c.commit()
    c.close()

    return redirect('/')

@app.route('/edit/<name>')
def edit_hero(name): #Only for edit option
    c=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="heroes_db")

    cursor=c.cursor()
    cursor.execute('''SELECT * FROM heroes WHERE name=%s''',(name,))
    row=cursor.fetchone()
    c.close()

    return render_template("edit.html",heroes=row)

@app.route('/update/', methods=['POST'])
def update_hero():
    name=request.form.get("name")
    skill=request.form.get("skill")
    rank=request.form.get("rank")

    c=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="heroes_db")
    cursor=c.cursor()
    cursor.execute('''UPDATE heroes SET skill=%s,rank=%s WHERE name=%s''',(skill,rank,name))
    c.commit()
    c.close()
    return redirect('/')

#-----API-------
@app.route('/api/heroes/')
def api_heroes():

    c=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="heroes_db")

    cursor=c.cursor()

    cursor.execute("SELECT * FROM heroes ORDER BY rank ASC")
    row=cursor.fetchall()

    c.close()

    heroes=[]
    for i in row:
        h={"name":i[0],"skill":i[1],"rank":i[2]}
        heroes.append(h)

    return jsonify(heroes)

@app.route('/api/heroes/<name>')
def api_search(name):

    c=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="heroes_db")

    cursor=c.cursor()

    cursor.execute('''SELECT * FROM heroes WHERE name=%s''', (name,))
    row=cursor.fetchone()

    if row:
        h={"name":row[0],"skill":row[1],"rank":row[2]}
    else:
        h={"Error":"Hero not found"}
    c.close()
    return jsonify(h)

@app.route('/api/heroes/', methods=['POST'])
def api_add():
    username=request.json.get("username") #R/L
    
    if username not in logged_users:
        return jsonify({"Error":"login required"})



    c=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="heroes_db")
    try:
        cursor=c.cursor()
        name=request.json.get("name")
        skill=request.json.get("skill")
        rank=request.json.get("rank")

        cursor.execute('''INSERT INTO heroes(name,skill,rank) VALUES(%s,%s,%s)''',(name,skill,rank))
        c.commit()
        return jsonify({"message":"Hero added successfully"})

    except mysql.connector.IntegrityError:
        return jsonify({"Error":"The rank already exist"})
    finally:
        c.close()

@app.route('/api/delete/<name>')
def api_del(name):
    username=request.args.get("username") #R/L

    if username not in logged_users:
        return jsonify({"Error":"login required"})

    c=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="heroes_db")

    cursor=c.cursor()

    cursor.execute("DELETE FROM heroes WHERE name=%s", (name,))
    c.commit()

    if cursor.rowcount == 0:
        result={"message":"Hero not found"}
    else:
        result={"message":"Hero deleted successfully"}

    c.close()

    return jsonify(result)

@app.route('/api/update/<name>', methods=['POST'])
def api_upgrade(name):
    c=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="heroes_db")
    try:
        cursor=c.cursor()
        skill= request.json.get("skill")
        rank=request.json.get("rank")
        cursor.execute('''UPDATE heroes SET skill=%s,rank=%s WHERE name=%s''',(skill,rank,name))
        c.commit()

        if cursor.rowcount == 0:
            j = {"message": "Hero not found"}
        else:
            j = {"message": "Hero updated successfully"}

    except mysql.connector.IntegrityError:
        j={"Error":"The rank already exists"}
    finally:
        c.close()
    return jsonify(j)
#------Reg/Login--------
@app.route('/api/register', methods=['POST'])
def register():
    username=request.json.get("username")
    email=request.json.get("email")
    password=request.json.get("password")

    hashed=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
    
    c=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="heroes_db")

    try:
        cursor=c.cursor()
        cursor.execute('''INSERT INTO users(username,email,password) 
VALUES(%s,%s,%s)''',(username,email,hashed))
        c.commit()

        return jsonify({"message":"username registered successfully"})
                
    except mysql.connector.IntegrityError:
       return  jsonify({"Error":"username or email already exists"})

    finally:
         c.close()

@app.route('/api/login', methods=['POST'])
def login():

    login=request.json.get("login")
    password=request.json.get("password")

    c=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="heroes_db")

    cursor=c.cursor()

    # search user by username OR email
    cursor.execute(
        "SELECT username,password FROM users WHERE username=%s OR email=%s",
        (login,login))

    row=cursor.fetchone()

    c.close()

    if row is None:
        return jsonify({"error":"User not found"})

    username=row[0]
    spw=row[1]

    # verify password using bcrypt
    if bcrypt.checkpw(password.encode(),spw.encode()):

        # store logged in user
        logged_users.add(username)
        

        return jsonify({"message":"Login successful","user":username})

    else:
        return jsonify({"error":"Wrong password"})



if __name__=='__main__':
     app.run(debug=True)


#API test↓
''''
curl -X POST http://127.0.0.1:5000/api/register \
-H "Content-Type: application/json" \
-d '{"username":"neo","email":"neo@mail.com","password":"1234"}'

curl -X POST http://127.0.0.1/api/login \
-H "Content-Type:application/json" \
-d '{"login":"---","password":"1234"}

curl -X POST http://127.0.0.1:5000/api/heroes/ \
-H "Content-Type: application/json" \
-d '{"username":"kdraj","name":"Invi","skill":"Invisible","rank":14}'


'''
