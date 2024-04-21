import sqlite3

secret_key = "pich2sampleple"

# 関数：テーブルの作成
def create():
    dbname = "users.db"
    # データベース接続
    conn = sqlite3.connect(dbname)

    # データベースを操作するためのカーソル作成
    cur = conn.cursor()

    # テーブルの作成
    cur.execute(
        "CREATE TABLE users(id INTEGER PRIMARY KEY,username STRING,pass STRING)"
    )

    # テーブルへのデータ挿入
    users = [
        (0,"admin","qwerty"),
        (1,"cguf0082","Doshisha"),
        (2,"ISDL","test")
    ]
    cur.executemany("INSERT INTO users values(?,?,?)",users)
    conn.commit()   # データベースへの反映

    # データベースとの接続遮断
    cur.close()
    conn.close()

# 関数：データの追加
def add(id,username,pwd):
    dbname = "users.db"
    # データベース接続
    conn = sqlite3.connect(dbname)

    # データベースを操作するためのカーソル作成
    cur = conn.cursor()
    
    # 追加要素の初期化と格納
    add = ()
    add = (id,username,pwd)

    # テーブルにデータを追加
    cur.execute("INSERT INTO users values(?,?,?)",add)
    conn.commit()

    # データベースとの接続遮断
    cur.close()
    conn.close()

# 関数：データの削除
def delete(id):
    dbname = "users.db"
    # データベース接続
    conn = sqlite3.connect(dbname)

    # データベースを操作するためのカーソル作成
    cur = conn.cursor()

    # データの削除
    cur.execute("DELETE FROM users WHERE id ='" + str(id) +"'")
    conn.commit()

    # データベースとの接続遮断
    cur.close()
    conn.close()

#関数：データの更新
def update(id,username,pwd):
    dbname = "users.db"
    # データベース接続
    conn = sqlite3.connect(dbname)

    # データベースを操作するためのカーソル作成
    cur = conn.cursor()

    # データの更新
    cur.execute("UPDATE users SET username ='"+username+"',pass ='" +pwd+ "' WHERE id = '"+ str(id)+"'")
    conn.commit()

    # データベースとの接続遮断
    cur.close()
    conn.close()

# 関数：テーブルの削除
def drop():
    dbname = "users.db"
    # データベース接続
    conn = sqlite3.connect(dbname)

    # データベースを操作するためのカーソル作成
    cur = conn.cursor()

    # テーブルの削除
    cur.execute("DROP TABLE users")
    # conn.commit()

    # データベースとの接続遮断
    cur.close()
    conn.close()
