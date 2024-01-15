import sqlite3,os
from flask import Flask,flash,render_template,redirect,url_for,request,g,session
from datetime import timedelta

# テーブル作成スクリプトのインポート
import create_table as table

app = Flask(__name__)

app.secret_key = "pich2sampleple"
app.permanent_session_lifetime = timedelta(minutes=5)


# 関数：データベース接続・カーソルの作成
def get_cursor():
    if 'db' not in g:
        g.db = sqlite3.connect('users.db') 
        g.cursor = g.db.cursor()
    return g.cursor

#関数：ユーザ追加処理
def add_user(new_user,new_pass):
    cur = get_cursor()

    # sql文
    sql_u = """SELECT id FROM users where username='""" + new_user + """'"""
    sql_p = """SELECT id FROM users where pass='""" + new_pass + """'"""
        
    # print(cur.execute(sql_u).fetchone())

    if cur.execute(sql_u).fetchone() is not None or cur.execute(sql_p).fetchone() is not None:    # 既存ユーザor 既存パスワード
        flash("it's already used\nPlease enter another one")
        return redirect("/administrator")
    else:       # 新規登録
        cur.execute("SELECT MAX(id) FROM users")
        num = cur.fetchone()[0]
        table.add(num+1,new_user,new_pass)
        flash(new_user+" is registered")
        return redirect('/administrator')

# 関数：ユーザ情報の更新
def update(new_username,new_pwd):
    cur = get_cursor()

    # sql文
    sql_u = """SELECT id FROM users where username='""" + new_username + """'"""
    sql_p = """SELECT id FROM users where pass='""" + new_pwd + """'"""
    
    if cur.execute(sql_u).fetchone() is not None or cur.execute(sql_p).fetchone() is not None:    # 既存ユーザor 既存パスワード
        flash("it's already used. Please enter another one")
        return redirect("/login")
    else:       # 情報更新
        cur.execute("SELECT id FROM users where username='"+session["user"]+"'")
        user_id = cur.fetchone()[0]

        table.update(user_id,new_username,new_pwd)
        session["user"] = new_username
        flash("Change User's Info")
    return redirect("/login")

# ログイン画面
@app.route("/",methods=["GET","POST"])
def index():
    # users.dbが無ければ作成
    if not os.path.exists("users.db"):
        table.create()

    # ログイン画面更新時
    if request.method == "GET":
        return render_template("index.html")
    # ログイン実行時
    if request.method == "POST":
        # 入力されたユーザ名/パスワードの変数格納
        username = request.form["username"]
        pwd = request.form["pass"]

        # 入力無しの場合
        if username == '' or pwd == '':
            flash("Enter username & password")
            return redirect('/')

        # カーソルの取得
        cur = get_cursor() 

        # データテーブル確認
        sql = """SELECT id FROM users where username='""" + username + """'"""
        if  cur.execute(sql).fetchone() is None:             # データなし
            flash("Not registered")
            return redirect('/')
        elif len(cur.execute(sql).fetchone()) != 0  :        # データあり
            cur.execute("SELECT * FROM users where username='" + username + "'")
            user_info = cur.fetchall()[0]
    
            # ユーザ名/パスワード照合（パスワードの復号処理を追加したい）
            if username == user_info[1]:
                if pwd == user_info[2]:
                    session.permanent = True
                    session["user"] = username
                    return redirect('login')
                else:
                    flash("Wrong password")
                    return redirect('/')
            
        return render_template('index.html')

# ログイン処理
@app.route("/login",methods=["GET","POST"])
def login():
    # 不正操作防止策
    if "user" not in session:
        flash("You have to login to access the login-page")
        return redirect('/')
    
    # Login as Administrator
    if session["user"] == "admin":
        return redirect('/administrator')
    
    # ユーザ情報更新
    if request.method == "POST":
        if request.form["username"] != "" and request.form["pass"] != "":
            update(request.form["username"],request.form["pass"])
        else :
            flash("Enter new username/pass")
    return render_template("login.html")

# ログアウト処理
@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect('/')

# ユーザ削除
@app.route("/delete")
def delete_this():
    # 不正操作防止策
    if "user" not in session:
        flash("You have to login as Administrator")
        return redirect('/')
    
    cur = get_cursor()

    cur.execute("SELECT id FROM users where username='"+session["user"]+"'")
    user_id = cur.fetchone()[0]
    table.delete(user_id)

    flash("Delete User:"+session["user"])
    return redirect("/")

# admin（管理者）接続時の処理
@app.route("/administrator",methods=["GET","POST"])
def admin():
    # 不正操作防止策
    if "user" not in session:
        flash("You have to login as Administrator")
        return redirect('/')
    
    if request.method =="POST":        
        if request.form["username"] != "" and request.form["pass"] != "":       # ユーザ追加
            add_user(request.form["username"],request.form["pass"])
        else:                                                                   # 入力なし
            flash("Enter username & password")
        return redirect("/administrator")

    return render_template("admin.html")

# admin権限による全登録ユーザの削除
@app.route("/administrator/delete_all")
def delete_all():
    # 不正操作防止策
    if "user" not in session:
        flash("You have to login as Administrator")
        return redirect('/')
    
    if session["user"] == "admin":
        cur = get_cursor()

        cur.execute("SELECT MAX(id) FROM users")
        id_max = cur.fetchone()[0]
        for id in range(1,id_max+1): # admin以外のユーザ削除
            table.delete(id)

        flash("Deleted all registered Users")
        return redirect("/administrator")
    else:
        flash("You're not Administrator")
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)