from flask import Flask, session, render_template, redirect, request, url_for, jsonify, escape

import pymysql, hashlib, ctypes

from time import sleep

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
            sleep(0)
            MS_SYSTEMMODAL = 0x00001000
            ctypes.windll.user32.MessageBoxW(0, "아이디 및 패스워드를 입력해주세요.", "알림", MS_SYSTEMMODAL)
            return redirect(url_for('login_proc'))

        else:
            sql = "SELECT * FROM sign_up"
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
                if userId == row['user_id'] and hashlib.sha256(userPw.encode()).hexdigest() == row['password']:
                    session['userId'] = userId
                    return redirect(url_for('main'))
                elif userId != row['user_id'] and hashlib.sha256(userPw.encode()).hexdigest() != row['password']:
                    sleep(0)
                    MB_SYSTEMMODAL = 0x00001000
                    ctypes.windll.user32.MessageBoxW(0, "아이디 및 패스워드가 틀렸습니다.", "알림", MB_SYSTEMMODAL)
                    return redirect(url_for('login_proc'))

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

        sql = "SELECT user_id FROM sign_up"
        cursor.execute(sql)
        id_data = cursor.fetchall()

        for idta in id_data:

            if myid == idta['user_id']:
                sleep(0)
                MS_SYSTEMMODAL = 0x00001000
                ctypes.windll.user32.MessageBoxW(0, "ID 중복 검사를 해주세요.", "알림", MS_SYSTEMMODAL)
                return redirect(url_for('register'))

        if pw != pwr:
            sleep(0)
            MB_SYSTEMMODAL = 0x00001000
            ctypes.windll.user32.MessageBoxW(0, "비밀번호가 일치하지 않습니다.", "알림", MB_SYSTEMMODAL)
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

            sleep(0)
            MB_SYSTEMMODAL = 0x00001000
            ctypes.windll.user32.MessageBoxW(0, "회원가입 완료", "알림", MB_SYSTEMMODAL)

        return redirect(url_for('login_proc'))

    return render_template('register_page/register_page.html')


# 회원가입 페이지 아이디 중복확인 GET
@app.route('/register_page.html/register/duplicate', methods=['GET'])
def duplicate():
    print("aaaaaaa")
    sql = "SELECT user_id FROM sign_up"
    cursor.execute(sql)
    dup = cursor.fetchall()
    # for dups in dup:
    #     dupc = dups

    print(dup)

    return jsonify({'dpc': dup})


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
    print(data)
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
