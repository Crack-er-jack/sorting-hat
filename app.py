from flask import Flask,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import plotly.graph_objects as go
import math
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'sql12.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql12618490'
app.config['MYSQL_PASSWORD'] = 'RpNKZbFlRZ'
app.config['MYSQL_DB'] = 'sql12618490'
app.config['SECRET_KEY'] = 'thisisasecret'
 
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        email = request.form['email']
        pwd = request.form['password']
        pfp = request.form['pfp']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO users VALUES(NULL, %s, %s, NULL, NULL, %s)''',(email,pwd,pfp))
        mysql.connection.commit()
        cursor.close()
        return render_template('login.html', message='Your account was created successfully! Please login.')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", message='Login and take the Sorting Hat Quiz')
    else:
        email = request.form['email']
        pwd = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT * FROM users WHERE email = %s''',[email])
        data = cursor.fetchall()
        cursor.execute(''' SELECT * FROM questions WHERE bid = 1''')
        print(data)
        if len(data) == 0:
            return render_template('login.html', message='Your email is incorrect! Please enter correct email or signup.')
        if data[0][2] != pwd:
            return render_template('login.html', message='Your password is incorrect! Please enter correct password.')
        if email == 'dumbledore@gmail.com':
            return redirect(url_for('admin', email=data[0][1]))
        if data[0][-2] != None:
            return redirect(url_for('post_game', email=data[0][1]))
        #return render_template('board.html', email=data[0][1], image=data[0][-1], house_assigned=data[0][-2], questions=questions)
        return redirect(url_for('game', email=data[0][1]))
    
@app.route('/game/<email>')
def game(email):
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM users WHERE email = %s''',[email])
    data = cursor.fetchall()
    cursor.execute(''' SELECT * FROM questions WHERE bid = 1''')
    questions = cursor.fetchall()
    cursor.close()
    print(len(questions))
    answered = [0, 0, 0, 0, 0, 0, 0]
    place_names = ['Platform 9 3/4', "Hagrid's Hut", '', 'Quidditch Ground', 'The Great Hall', '', "Headmaster's office"]
    place_images = ['https://i.ytimg.com/vi/arUNK8GsZhY/maxresdefault.jpg',
                    'https://i.pinimg.com/originals/63/4f/d9/634fd9a61cc4bbb547e0a1f8890062b2.jpg', '',
                    'https://i.ytimg.com/vi/clqPPWDUe_U/maxresdefault.jpg',
                    'https://d.newsweek.com/en/full/1033479/mcdhapo-ec030.jpg', '',
                    'https://s.hdnux.com/photos/47/53/14/10400528/6/1200x0.jpg']
    if session.get('questions') == None: 
        questions = list(questions)
        for i in range(len(questions)):
            questions[i] = list(questions[i])
            questions[i].append(answered[i])
            questions[i].append(place_names[i])
            questions[i].append(place_images[i])
        session['questions'] = questions
    return render_template('board.html', email=email, image=data[0][-1], house_assigned=data[0][-2], questions=session['questions'], len=len(questions))

@app.route('/q/<qno>/<email>/<qid>', methods=['POST'])
def eval(qno, email, qid):
    answer = request.form['answer'+qno]
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM users WHERE email = %s''',[email])
    data = cursor.fetchall()
    cursor.execute(''' SELECT * FROM users WHERE email = %s''',[email])
    user = cursor.fetchall()[0]
    cursor.execute(''' SELECT * FROM questions WHERE id = %s''',[qid])
    question = cursor.fetchall()
    cursor.execute(''' SELECT * FROM questions WHERE bid = 1''')
    questions = cursor.fetchall()
    print(question[0][3], answer)
    if qno == '1' or qno == '2' or qno == '5':
        if question[0][3].lower() == answer.lower():
            cursor.execute('''INSERT INTO userscores VALUES(%s, 1, %s)''', [user[0], qid])
        else:
            if qno == '2':
                for i in range(len(session['questions'])):
                    if int(session['questions'][i][0]) == int(qid)+1 and session['questions'][i][-3] == 0:
                        qid = str(int(qid) + 1)
                        session['questions'][i-1][-3] = 0
                        session.modified = True
                        return redirect(url_for('alt2eval', email=email, qid=qid))    
            if qno == '5':
                for i in range(len(session['questions'])):
                    if int(session['questions'][i][0]) == int(qid)+1 and session['questions'][i][-3] == 0:
                        qid = str(int(qid) + 1)
                        return redirect(url_for('alt4eval', email=email, qid=qid))
            cursor.execute('''INSERT INTO userscores VALUES(%s, 0, %s)''', [user[0], qid])
    if qno == '4':
        score = '{:.2f}'.format(int(answer) / int(question[0][3]))
        cursor.execute('''INSERT INTO userscores VALUES(%s, %s, %s)''', [user[0], score, qid])
    for i in range(len(session['questions'])):
        if int(session['questions'][i][0]) == int(qid):
            session['questions'][i][-3] = 1
            session.modified = True
    print([q for q in session['questions'] if q[-3] == 1])
    print('illlllll')
    if qno == '7':
        print('cdasnscnnds')
        print(answer)
        cursor.execute('''INSERT INTO userscores VALUES(%s, %s, %s)''', [user[0], str(int(answer)/4), qid])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('post_game', email=email))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('game', email=email))

@app.route('/alt2/<email>/<qid>', methods=['GET', 'POST'])
def alt2eval(email, qid):
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM users WHERE email = %s''',[email])
    user = cursor.fetchall()[0]
    cursor.execute(''' SELECT * FROM questions WHERE id = %s''',[qid])
    question = cursor.fetchall()
    if request.method == 'GET':
        return render_template('alt2.html', email=email, question=question[0][2], qid=qid)
    else:
        answer = request.form['answer']
        if question[0][3].lower() == answer.lower():
            for i in range(len(session['questions'])):
                if int(session['questions'][i][0]) == int(qid)-1:
                    session['questions'][i][-3] = 0
                    session.modified = True
                if int(session['questions'][i][0]) == int(qid):
                    session['questions'][i][-3] = 1
                    session.modified = True
            return redirect(url_for('game', email=email))
        else:
            return render_template('deadend1.html')


@app.route('/alt4/<email>/<qid>', methods=['GET', 'POST'])
def alt4eval(email, qid):
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM users WHERE email = %s''',[email])
    user = cursor.fetchall()[0]
    cursor.execute(''' SELECT * FROM questions WHERE id = %s''',[qid])
    question = cursor.fetchall()
    cursor.close()
    if request.method == 'GET':
        return render_template('alt4.html', email=email, question=question[0][2], qid=qid)
    else:
        answer = request.form['answer']
        if question[0][3].lower() == answer.lower():
            for i in range(len(session['questions'])):
                if int(session['questions'][i][0]) == int(qid)-1:
                    session['questions'][i][-3] = 0
                    session.modified = True
                if int(session['questions'][i][0]) == int(qid):
                    session['questions'][i][-3] = 1
                    session.modified = True
            return redirect(url_for('game', email=email))
        else:
            return render_template('deadend2.html')


@app.route('/post_game/<email>')
def post_game(email):
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM users WHERE email = %s''',[email])
    user = cursor.fetchall()[0]
    cursor.execute('''SELECT score FROM userscores WHERE uid = %s''',[user[0]])
    scores = cursor.fetchall()
    print(scores)
    if len(scores) == 7:
        r = [float(scores[i][0]) for i in range(len(scores)) if i in [0,1,3,4,6]]
    elif len(scores) == 6:
        if session['questions'][2][-3] == 1:
            r = [float(scores[i][0]) for i in range(len(scores)) if i != 2]
        else:
            r = [float(scores[i][0]) for i in range(len(scores)) if i != 4]
    else:
        r = [float(scores[i][0]) for i in range(len(scores))]
    ha = 'Ravenclaw'
    print(r[-2], math.isclose(r[-2], 1.0))
    if math.isclose(r[-1], 0.25):
        ha = 'Hufflepuff'
    elif math.isclose(r[-1], 1.0):
        ha = 'Slytherin'
    elif math.isclose(r[-2], 1.0):
        ha = 'Gryffindor'
    elif math.isclose(r[2], 1.0):
        ha = 'Ravenclaw'
    elif math.isclose(r[2], 0.92):
        ha = 'Slytherin'
    elif len(scores) > 5 and math.isclose(r[0], 1.0):
        ha = 'Hufflepuff'
    cursor.execute('''UPDATE users SET house_assigned = %s WHERE email = %s''', [ha, email])
    fig = go.Figure(data=go.Scatterpolar(
    r=r,
    theta=['creativity','problem solving','eye for detail',
           'adaptability', 'flexibility'],
    fill='toself'
    ))

    fig.update_layout(
        polar=dict(
        radialaxis=dict(
        visible=True
            ),
        ),
        showlegend=False
    )
    fig.write_image("static/result"+ str(user[0]) +".png")
    mysql.connection.commit()
    cursor.close()
    return render_template('post_game.html', user=user, questions=session['questions'], scores=scores, len=len(scores), house_assigned=ha)

@app.route('/admin/<email>')
def admin(email):
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM users WHERE email = %s''',[email])
    data = cursor.fetchall()
    cursor.execute(''' SELECT * FROM users''')
    users = cursor.fetchall()
    print(users)
    user_progress = []
    for user in users:
        cursor.execute(''' SELECT score FROM userscores WHERE uid=%s''', [user[0]])
        scores = cursor.fetchall()
        if len(scores) == 7:
            r = [float(scores[i][0]) for i in range(len(scores)) if i in [0,1,3,4,6]]
        elif len(scores) == 6:
            if session['questions'][2][-3] == 1:
                r = [float(scores[i][0]) for i in range(len(scores)) if i != 2]
            else:
                r = [float(scores[i][0]) for i in range(len(scores)) if i != 4]
        elif len(scores) < 5:
            r = ['NA'] * 5
        else:
            r = [float(scores[i][0]) for i in range(len(scores))]
        if user[-2] != None:
            user_progress.append([user[1]] + r + [user[-2]])
        else:
            user_progress.append([user[1]] + r + ['NA'])
        
    return render_template('admin.html', email=email, image=data[0][-1], user_progress=user_progress)
