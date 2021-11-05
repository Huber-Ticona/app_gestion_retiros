from flask import Flask, url_for , request , render_template, make_response , session , jsonify
from flask.wrappers import Request
from flaskext.mysql import MySQL
from werkzeug.utils import redirect
from datetime import datetime

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
    if "usuario" in session:
        usuario = session["usuario"]
        return render_template('home.html' , usuario = usuario)
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

@app.route('/panel_clasico')
@app.route('/panel_clasico/<string:fecha>')
def panel_clasico(fecha = None):

    if "usuario" in session:
        usuario = session["usuario"]
        if  fecha == None:
            fecha =  datetime.now().date()
            print("Fecha de hoy: " + str(fecha))
            inicio = str(fecha) + ' 00:00'
            fin = str(fecha) + ' 23:59'
        else:
            print("Fecha recibida: " + fecha)
            inicio = str(fecha) + ' 00:00'
            fin = str(fecha) + ' 23:59'

        documentos = busqueda_docs_fecha(inicio=inicio , fin=fin) #Funcion detecta errores de DB conexion y retorna false.
        if documentos:
            boletas = documentos[0]
            facturas = documentos[1] #Si no se encontraron datos retorna una tupla vacia ().
            guias = documentos[2]
            return render_template('panel_clasico.html', usuario = usuario , boletas=boletas ,facturas=facturas, guias=guias, fecha= str(fecha) )
        else:
            return render_template('no_db_con.html')
        
    else:
        return redirect(url_for('home'))

@app.route('/obt_detalle_bol_fact/<int:interno>', methods = ['POST'])
def obt_detalle_bol_fact_interno(interno):
    cursor = mysql.get_db().cursor()
    cursor.execute("select * from item  where interno = %s " , interno )
    detalle = cursor.fetchall()
    print(detalle)
    print(jsonify(detalle))
    return jsonify(detalle)

@app.route('/obt_detalle_guia/<int:interno>', methods = ['POST'])
def obt_detalle_guia_interno(interno):
    cursor = mysql.get_db().cursor()
    cursor.execute("select JSON_EXTRACT(detalle, '$.descripciones'), JSON_EXTRACT(detalle, '$.cantidades') from guia  where interno = %s " , interno )
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

def busqueda_docs_fecha(inicio,fin):
    try:
        cursor = mysql.get_db().cursor()

        sql1 = "select * from nota_venta where folio = 0 and fecha between %s and %s "
        cursor.execute( sql1 , ( inicio , fin )  )
        boletas = cursor.fetchall()

        sql2 = "select * from nota_venta where nro_boleta = 0 and  fecha between %s and %s "
        cursor.execute(sql2 , ( inicio , fin ) )
        facturas = cursor.fetchall()

        sql3 = "select folio,interno, JSON_EXTRACT(detalle,'$.tipo_doc') ,JSON_EXTRACT(detalle, '$.doc_ref') from guia where fecha between %s and %s "
        cursor.execute(sql3 , ( inicio , fin ) )
        guias = cursor.fetchall()
        return (boletas, facturas, guias)
    except:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=5000, debug=True )
