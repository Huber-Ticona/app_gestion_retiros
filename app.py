from flask import Flask, url_for , request , render_template, make_response , session , jsonify
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
        return redirect(url_for('login'))
    

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
        cursor = mysql.get_db().cursor()
        cursor.execute("select * from nota_venta where folio = 0 and fecha between '2021-05-07 00:00' and '2021-05-07 23:59' ")
        boletas = cursor.fetchall()

        cursor.execute("select * from nota_venta where nro_boleta = 0 and  fecha between '2021-05-07 00:00' and '2021-05-07 23:59' ")
        facturas = cursor.fetchall()
        
        cursor.execute("select folio, JSON_EXTRACT(detalle, '$.tipo_doc') ,JSON_EXTRACT(detalle, '$.doc_ref') from guia where fecha between '2021-10-18 00:00' and '2021-10-18 23:59'")
        guias = cursor.fetchall()

        return render_template('panel_clasico.html' , boletas=boletas ,facturas=facturas, guias=guias)
    else:
        return redirect(url_for('home'))

@app.route('/obt_detalle_bol_fact/<int:interno>', methods = ['POST'])
def obt_detalle_interno(interno):
    cursor = mysql.get_db().cursor()
    cursor.execute("select * from item  where interno = %s " , interno )
    detalle = cursor.fetchall()
    print(detalle)
    print(jsonify(detalle))
    return jsonify(detalle)


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
