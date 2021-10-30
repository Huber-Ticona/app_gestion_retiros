from flask import Flask, url_for , request , render_template, make_response , session
from flask.wrappers import Request
from flaskext.mysql import MySQL
from werkzeug.utils import redirect

app = Flask(__name__)


# CREANDO LA CONEXION A LA BASE DE DATOS
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'huber'
app.config['MYSQL_DATABASE_PASSWORD'] = 'huber123'
app.config['MYSQL_DATABASE_DB'] = 'madenco'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
app.secret_key="madenco"

@app.route('/')
def home():
    if "usuario" in session:
        usuario = session["usuario"]
        return render_template('home.html' , nombre = usuario)
    else:
        return render_template('home.html' )
    

@app.route('/login' , methods = ['GET', 'POST'])   #iniciar sesión
def login():
    if request.method == 'POST':
        nombre = request.form['nombre_usuario']
        contra = request.form['contraseña']
        session['usuario'] = nombre
        return redirect(url_for("home"))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('usuario', None)
    return redirect(url_for('home'))

@app.route('/panel-clasico')
def panel_clasico():
    return render_template('panel_clasico.html')
    
@app.route('/mostrar/ordenes/')
def ordenes():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM clave')
    usuarios = cursor.fetchall()

    print(usuarios)
    print(type(usuarios))
    return 'usuarios '

    #test push

@app.route('/variable/<dato>')
def variable(dato):
    return f"hola, el dato es: {dato}"

@app.errorhandler(404)
def not_found():
    """Page not found."""
    return make_response(render_template("404.html"), 404)

with app.test_request_context():

    print(url_for('home'))
    print(url_for('variable' , dato = 'huber ticona' ))

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=5000, debug=True )
