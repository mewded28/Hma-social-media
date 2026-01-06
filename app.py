from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "pysocial_secret_key" 

users = [
    {
        "username": "admin", 
        "age": 30, 
        "posts": ["Welcome! This is the starting post."] 
    }
]

def get_all_posts():
    feed = [] 
    for user in users:
        for post in user['posts']:
            feed.append({"user": user['username'], "text": post})
    return feed

@app.route('/') 
def login_page():
    if "user" in session:
        return redirect('/feed')
    return render_template('login.html')

@app.route('/login_action', methods=['POST']) 
def login_action():
    uname = request.form.get('username').strip().lower()
    uage = request.form.get('age')

    if not uname or not uage:
        return "Fields are required.", 400

    found_user = None 
    for u in users:
        if u['username'] == uname:
            found_user = u
            break 
    
    if not found_user:
        try:
            new_user = {"username": uname, "age": int(uage), "posts": []}
            users.append(new_user)
        except ValueError:
            return "Invalid age.", 400
    
    session["user"] = uname
    return redirect('/feed')

@app.route('/feed') 
def feed_page():
    if "user" not in session:
        return redirect('/') 
    
    posts = get_all_posts()
    return render_template('feed.html', username=session["user"], feed=posts)

@app.route('/post', methods=['POST']) 
def post():
    if "user" not in session:
        return redirect('/')

    content = request.form.get('content').strip()
    
    if content:
        for u in users:
            if u['username'] == session["user"]:
                u['posts'].insert(0, content)
                break
                
    return redirect('/feed')

@app.route('/logout') 
def logout():
    session.pop("user", None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
