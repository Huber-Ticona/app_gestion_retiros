from flask import Flask, url_for , request , render_template, make_response , session , jsonify, flash, send_from_directory
from flask.wrappers import Request
from flaskext.mysql import MySQL
from werkzeug.utils import redirect, secure_filename
from datetime import datetime
import os

# DEFINIENDO PARAMETROS DE ARCHIVOS A RECIBIR
UPLOAD_FOLDER = '/Users/super/Desktop/Madenco/capturador/adjuntos'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        return render_template('home.html' , usuario = usuario)
    else:
        return redirect(url_for('login'))
    

@app.route('/login' , methods = ['GET', 'POST'])   #iniciar sesión
def login():

    error = None
    if request.method == 'POST':
        nombre = request.form['nombre_usuario']
        contra = request.form['contraseña']
        

        #VALIDAR CUENTA EN DB
        cursor = mysql.get_db().cursor()
        sql = "select * from usuario where nombre = %s"
        cursor.execute( sql , ( nombre )  )
        consulta = cursor.fetchone()
        
        if consulta:
            print("usuario encontrado")
            sql = "select * from usuario where nombre = %s and contraseña = %s "
            cursor.execute( sql , ( nombre , contra )  )
            consulta2 = cursor.fetchone()
            

            if consulta2:
                #flash('You were successfully logged in')
                print("usuario y contraseña correctos.")
                session['usuario'] = nombre
                return redirect(url_for("home"))
            else:
                error = 'Invalid password'
                flash('Contraseña invalida')
                print("contra invalida")
        else:
            error = 'Invalid user'
            flash('Nombre de usuario invalido')
            print("usuario no encontrado, en la bd")
        
    
    return render_template('login.html' )
        

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
    cursor.execute("select descripcion, cantidad, retirado, unitario, total from item  where interno = %s " , interno ) #SE AGREGO EL ESTADO RETIRADO
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/subir', methods=['POST'])
@app.route('/subir/<int:folio>/<string:tipo_doc>', methods=['GET', 'POST'])
def upload_file(folio = None,tipo_doc = None):
    folio = folio
    tipo = tipo_doc
    if request.method == 'POST':
        # compruebe si la solicitud de publicación tiene la parte del archivo
        if 'file' not in request.files:
            flash('No file part')
            print(request.url)
            return redirect(request.url)
        file = request.files['file']
        #Si el usuario no selecciona un archivo, el navegador envía un
        # archivo vacío sin nombre de archivo.
        if file.filename == '':
            flash('No selected file')
            print(request.url)

            return redirect(request.url)
        if file and allowed_file(file.filename):
            nuevo_nombre = tipo + '_'+str(folio)+'_'+'adjunto_'+'1'+'.png'
            print(allowed_file(file.filename))
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return nuevo_nombre
    
@app.route('/descargar/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

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
