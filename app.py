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

xd = 'xd'
@app.route('/')
def home():
    print(xd)
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
    if "usuario" in session:
        usuario = session["usuario"]

        cursor = mysql.get_db().cursor()
        cursor.execute("select * from nota_venta where folio = 0 and fecha between '2021-05-07 00:00' and '2021-05-07 23:59' ")
        boletas = cursor.fetchall()
        cursor.execute("select * from nota_venta where nro_boleta = 0 and  fecha between '2021-05-07 00:00' and '2021-05-07 23:59' ")
        facturas = cursor.fetchall()

        return render_template('panel_clasico.html' , nombre = usuario, boletas=boletas ,facturas = facturas)
    else:
        return redirect(url_for('home'))
    
@app.route('/mostrar/ordenes/')
def ordenes():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM clave')
    usuarios = cursor.fetchall()

    print(usuarios)
    print(type(usuarios))
    return redirect(url_for('home'))

with app.test_request_context():

    print(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=5000, debug=True )
