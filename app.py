from flask import Flask, session, render_template, redirect, request, url_for, jsonify, escape

import pymysql, hashlib, ctypes

# DB 연결
db = pymysql.connect(host="localhost", user="root", password="nkhg3395!", charset="utf8")  # 기본 양식
cursor = db.cursor(pymysql.cursors.DictCursor)  # 테이블명까지 보여줌
cursor.execute('USE auction')  # 이 데이터베이스 사용할 것이다.

app = Flask(__name__)
app.secret_key = 'ABCDEF'


# @app.route('/')
# def home():
#     return render_template('login_page.html')


# 로그인
@app.route('/', methods=['GET', 'POST'])
def login_proc():
    if request.method == 'POST':
        userId = request.form['idIn']
        userPw = request.form['pwIn']

        if len(userId) == 0 or len(userPw) == 0:
            return 'ID, PW를 입력하세요.'
        else:
            sql = "SELECT * FROM sign_up"
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
                if userId == row['user_id'] and hashlib.sha256(userPw.encode()).hexdigest() == row['password']:
                    session['userId'] = userId
                    return redirect(url_for('main'))

    return render_template('login_page/login_page.html')


# 로그아웃
@app.route('/logout')
def logout():
    session.pop('userId', None)
    return redirect(url_for('login_proc'))


# 회원가입
@app.route('/register_page.html/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        result = request.form
        myid = request.form['Id']
        name = request.form['Name']
        pw = request.form['psw']
        pwr = request.form['psw-repeat']

        if pw != pwr:
            ctypes.windll.user32.MessageBoxW(0, "비밀번호를 제대로 확인하세요.", "알림", 0)
            return redirect(url_for('register'))
        else:
            sql = """
            INSERT INTO sign_up VALUES(
            NULL,
            '""" + str(myid) + """',
            '""" + str(name) + """',
            '""" + hashlib.sha256(pw.encode()).hexdigest() + """');"""

            cursor.execute(sql)

            cursor.execute('SELECT * FROM sign_up')
            value = cursor.fetchall()

            # print(value)

            db.commit()

            print("END")

        return redirect(url_for('login_proc'))

    return render_template('register_page/register_page.html')


# 메인페이지
@app.route('/main', methods=['GET', 'POST'])
def main():
    if "userId" in session:
        return render_template('main_page/main_page.html')
    else:
        return jsonify("Who are you?")


@app.route('/main/feed', methods=['GET'])
def feed_box_get():
    sql = "SELECT * FROM feed"
    cursor.execute(sql)
    data = cursor.fetchall()
    return jsonify({'feeds': data})


# # IT 페이지
# @app.route('/it', methods=['GET', 'POST'])
# def it():
#     if "userId" in session:
#         return render_template('main_page/main_page.html')
#     else:
#         return jsonify("Who are you?")
#
#
# @app.route('/it/feed', methods=['GET'])
# def feed_it_box_get():
#     sql = "SELECT * FROM feed WHERE category = 'it'"
#     cursor.execute(sql)
#     data = cursor.fetchall()
#     return jsonify({'it': data})
#
#
# # electron 페이지
# @app.route('/electron', methods=['GET', 'POST'])
# def electron():
#     if "userId" in session:
#         return render_template('trash/electron_page.html')
#     else:
#         return jsonify("Who are you?")
#
#
# @app.route('/electron/feed', methods=['GET'])
# def feed_electron_box_get():
#     sql = "SELECT * FROM feed WHERE category = 'electron'"
#     cursor.execute(sql)
#     data2 = cursor.fetchall()
#     return jsonify({'electron': data2})
#
#
# # life 페이지
# @app.route('/life', methods=['GET', 'POST'])
# def life():
#     if "userId" in session:
#         return render_template('trash/life_page.html')
#     else:
#         return jsonify("Who are you?")
#
#
# @app.route('/life/feed', methods=['GET'])
# def feed_life_box_get():
#     sql = "SELECT * FROM feed WHERE category = 'life'"
#     cursor.execute(sql)
#     data3 = cursor.fetchall()
#     return jsonify({'life': data3})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
