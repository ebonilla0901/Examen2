from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
import pyodbc

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


conn = pyodbc.connect('DRIVER={SQL Server};SERVER=QS44\MILTONQS44;DATABASE=examen2;UID=examen;PWD=12345678')
cursor = conn.cursor()
cursor.execute("SELECT IdUsuario, Nombre, contrasena FROM Usuarios")
rows= cursor.fetchall()
users = []
for row in rows:
    
    Id = row.IdUsuario
    Nombre = row.Nombre
    contrasena = row.contrasena
    users.append(User(id = Id, username = Nombre, password = contrasena))
    

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
       
        for user in users:
            if user.username == username and user.password == password:
                session['user_id'] = user.id
                return redirect(url_for('profile'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')


if __name__ == '__main__':
   app.run(port=5000)
