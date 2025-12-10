from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
app = Flask(__name__)
app.secret_key = "someSuperSecretKey123"
@app.route('/')
def index():
    return redirect('/Menu')
@app.route('/Menu')
def menu():
    return render_template('menu.html', title="Menu")
@app.route('/Characters', methods=["POST", "GET"])
def all_characters():
    # Connect to DB
    mydb = mysql.connector.connect(
        host="10.200.14.14",
        port=3306,
        user="TheCatNamed",
        password="Catia",
        database="CASproject"
    )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT charname, charbio, creator FROM chars")
    characters = mycursor.fetchall()
    # mycursor.execute("SELECT creator FROM chars")
    # # mycursor.execute("SELECT creator FROM chars WHERE id = %s", (session['user_id']))
    # creatorid = mycursor.fetchall()
    # mycursor.execute("SELECT username FROM users WHERE id = %s", (creatorid))
    # creatorname =  mycursor.fetchall()

    return render_template("chars.html", characters=characters)
# @app.route('/News')
# @app.route('/Accounts')
# def accounts():

@app.route('/Profile')
def Profile():
    if "user_id" not in session:
        return redirect('/login')
    
    return render_template("profile.html", username=session.get("username"), email=session.get("email"))
@app.route('/Profile/Create', methods=["POST", "GET"])
def ProfileCreate():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == 'POST':
        # Connect to DB
        mydb = mysql.connector.connect(
            host="10.200.14.14",
            port=3306,
            user="TheCatNamed",
            password="Catia",
            database="CASproject"
        )
        mycursor = mydb.cursor(dictionary=True)

        # Get form values
        creator_id = session["user_id"]
        charname = request.form.get("charname")
        chardesc = request.form.get("description")
        charbio = request.form.get("minorbio")

        # Convert stats to integers
        try:
            strength = int(request.form.get("strength", 1))
            durability = int(request.form.get("durability", 1))
            endurance = int(request.form.get("endurance", 1))
            agility = int(request.form.get("agility", 1))
            intelligence = int(request.form.get("intelligence", 1))
            powers = int(request.form.get("powers", 1))
        except ValueError:
            return jsonify({"error": "Stats must be numbers"}), 400

        # Insert into char table
        sql = """
            INSERT INTO chars 
            (charname, chardesc, charbio, creator, strength, durability, endurance, agility, intelligence, powers)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (charname, chardesc, charbio, creator_id,
                  strength, durability, endurance, agility, intelligence, powers)
        
        mycursor.execute(sql, values)
        mydb.commit()

        mycursor.close()
        mydb.close()

        return jsonify({"success": True, "message": "Character created!"})

    # If GET request, render the character creation page
    return render_template("create.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        loginuser = request.form['loginuser']
        password = request.form['password']

        mydb = mysql.connector.connect(
            host="10.200.14.14",
            port=3306,
            user="TheCatNamed",
            password="Catia",
            database="CASproject"
        )
        mycursor = mydb.cursor(dictionary=True)

        # Search by username OR email
        query = "SELECT * FROM users WHERE username=%s OR email=%s"
        mycursor.execute(query, (loginuser, loginuser))
        user = mycursor.fetchone()

        if not user:
            return "User not found"

      
        if not user:
            return "User not found"

        # Compare passwords
        if user["password"] != password:
            return "Incorrect password"

        # -------------------
        # SET SESSION
        # -------------------
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["email"] = user["email"]

        
        return redirect('/Menu')
    return render_template("login.html")
@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        logins = 1
        mydb = mysql.connector.connect(
            host="10.200.14.14",
            port = 3306,
            user="TheCatNamed",
            password="Catia",
            database="CASproject"
        )
        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO users (username, email, password, logins) VALUES (%s, %s, %s, %s)", (username, email, password, logins))
        mydb.commit()

         # Get the new user's ID
        mycursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = mycursor.fetchone()

        # -------------------
        # SET SESSION
        # -------------------
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["email"] = user["email"]
        
        return redirect("/Menu")
    return render_template("register.html")