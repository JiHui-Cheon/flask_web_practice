from flask import Flask, render_template, request, redirect
from data import Articles
import pymysql
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.debug = True


db = pymysql.connect(
  host='localhost',
  port = 3306,
  user = 'root',
  passwd = '2643',
  db = 'practice'
)

@app.route('/', methods = ['GET'])
def index():
    # return "Hello World!!"
    return render_template("index.html", data = "JIHUI")

@app.route('/about')
def about():
    return render_template("about.html", hello = "안녕")

@app.route('/articles')
def articles():
    cursor = db.cursor()
    sql = 'SELECT * FROM topic;'
    cursor.execute(sql)
    topics = cursor.fetchall()
    db.commit()
    # articles = Articles()
    # print(articles[0]['author'])

    return render_template("articles.html", articles = topics)

@app.route('/article/<int:id>')
def article(id):
    cursor = db.cursor()
    sql = 'SELECT * FROM topic WHERE id={}'.format(id)
    cursor.execute(sql)
    topic = cursor.fetchonte()
    print(topic)
    # articles = Articles()
    # article = articles[id-1]
    # print("articles[id-1]")
    return render_template("article.html", article = topic)

@app.route('/add_articles', methods = ["GET","POST"])
def add_articles():
    cursor = db.cursor()
    if request.method == "POST":
        author = request.form['author']
        title = request.form['title']
        desc = request.form['desc']

        sql = "INSERT INTO `topic` (`title`, `desc`, `author`) VALUES (%s, %s, %s);"
        input_data = [title, desc, author]
        # print(request.form['desc'])

        cursor.execute(sql, input_data)
        db.commit()
        return redirect("/articles")
    else:
        return render_template("add_articles.html")

@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    cursor = db.cursor()
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        author = request.form['author']
        print(id)
        sql = 'UPDATE topic SET title = %s, body = %s, author = %s WHERE id = {};'.format(id)
        input_data = [title, desc, author]
        cursor.execute(sql, input_data)
        db.commit()
        # print(request.form['title'])
        return redirect('/articles')
    
    else:
        sql = "SELECT * FROM topic WHERE id = {}".format(id) # db아이디임.
        cursor.execute(sql)
        topic = cursor.fetchone()
        # print(topic[1])
        return render_template("edit_article.html", article = topic)

@app.route('/delete/<int:id>', methods = ["POST"])
def delete(id):
    cursor = db.cursor()
    sql = 'DELETE FROM topic WHERE id = {};'.format(id) 
    cursor.execute(sql)
    db.commit()
    return redirect("/articles")

@app.route('/register', methods = ["POST", "GET"])
def register():
    cursor = db.cursor()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        print(id)
        sql = "INSERT INTO `users` (`name`, `email`, `username`, `password`) VALUES (%s, %s, %s, %s);"
        input_data = [name, email, username, password]
        cursor.execute(sql, input_data)
        db.commit()
        # print(request.form['title'])
        return redirect('/')
    
    else:
        # sql = "SELECT * FROM users WHERE id = {}".format(id) # db아이디임.
        # cursor.execute(sql)
        # users = cursor.fetchone()
        # # print(topic[1])
        return render_template("register.html")        
    
                   

if __name__ == '__main__':
    app.run()