from flask import Flask, json, url_for , request , render_template, make_response , session , jsonify, flash, send_from_directory
from flask.wrappers import Request
import pymysql
from werkzeug.utils import redirect, secure_filename
from datetime import datetime
import os

# DEFINIENDO PARAMETROS DE ARCHIVOS A RECIBIR
UPLOAD_FOLDER = '/Users/super/Desktop/Madenco/capturador/adjuntos'
ALLOWED_EXTENSIONS = {'pdf','png', 'jpg', 'jpeg'} 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# CREANDO LA CONEXION A LA BASE DE DATOS
miConexion = pymysql.connect( host='localhost',
            user= 'huber', passwd='huber123', db='madenco' )

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
        cursor = miConexion.cursor()
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

#OBTENCION DE ITEMS X NRO INTERNO
@app.route('/obt_detalle_bol_fact/<int:interno>', methods = ['POST'])
def obt_detalle_bol_fact_interno(interno):
    cursor = miConexion.cursor()
    cursor.execute("select descripcion, cantidad, retirado, codigo, interno, unitario, total from item  where interno = %s " , interno ) #SE AGREGO EL ESTADO RETIRADO
    detalle = cursor.fetchall()
    print(detalle)
    print(jsonify(detalle))
    return jsonify(detalle)

@app.route('/obt_detalle_guia/<int:interno>', methods = ['POST'])
def obt_detalle_guia_interno(interno):
    cursor = miConexion.cursor()
    cursor.execute("select detalle from guia  where interno = %s " , interno )
    detalle = cursor.fetchall()
    print(detalle)
    print(jsonify(detalle))
    return jsonify(detalle)

#ALMACENADO DE ARCHIVOS.
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/subir', methods=['POST'])
@app.route('/subir/<int:folio>/<string:tipo_doc>/<int:interno>', methods=['GET', 'POST'])
def upload_file(folio = None,tipo_doc = None,interno = None):
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
            print(file.filename)
            extension = (file.filename).split('.')

            # SE CONSULTA LOS ADJUNTOS DEL DOCUMENTO
            cursor = miConexion.cursor()

            adjuntos = None
            sql1 = "SELECT adjuntos from nota_venta where interno = %s"
            cursor.execute( sql1 , ( interno )  )
            adjuntos = cursor.fetchone()
            
            
            print(adjuntos)
            try:
                if adjuntos[0] != None:
                    print('tiene '+ str(len(adjuntos[0])) +'adjuntos')
                   
                    estructura = '{ "adj": '+ adjuntos[0] + '}'
                    data = json.loads(estructura)
                    print(type(data))
                    print(type(data["adj"]))
                    
                    nuevo_nombre = tipo + '_'+str(folio)+'_'+'adjunto_'+ str(len(data["adj"]) + 1)+'.' + extension[1]
                    data["adj"].append(nuevo_nombre)
                    print(data["adj"])

                    new_adjuntos = json.dumps(data["adj"])
                else:
                    new_adjuntos = []
                    nuevo_nombre = tipo + '_'+str(folio)+'_'+'adjunto_1.' + extension[1] 
                    new_adjuntos.append(nuevo_nombre)
                    new_adjuntos = json.dumps(new_adjuntos)
                    print(type(new_adjuntos))

                sql2 = "update nota_venta set adjuntos = %s where interno = %s"
                cursor.execute( sql2 , ( new_adjuntos, interno )  )
                miConexion.commit()
                #SE ALMACENA LOCALMENTE
                filename = secure_filename(nuevo_nombre)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return jsonify(
                    data = nuevo_nombre,
                    category="success"
                )
            except:
                print('error de excepcion encontrado')
                return jsonify(
                    message="error de excepcion interna",
                    category="error"
                )
            
            
        else:
            return jsonify(
                    message="formato invalido",
                    category="error"
                )

            
    
@app.route('/descargar/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

#OBTENCION DE DATOS DE DOCUMENTO (BOLETA,FACTURA Y GUIA)
def busqueda_docs_fecha(inicio,fin):
    try:
        cursor = miConexion.cursor()

        sql1 = "select interno,vendedor,folio,monto_total,nro_boleta,nombre,vinculaciones,adjuntos,estado_retiro from nota_venta where folio = 0 and fecha between %s and %s "
        cursor.execute( sql1 , ( inicio , fin )  )
        boletas = cursor.fetchall()

        sql2 = "select interno,vendedor,folio,monto_total,nro_boleta,nombre,vinculaciones,adjuntos,estado_retiro from nota_venta where nro_boleta = 0 and  fecha between %s and %s "
        cursor.execute(sql2 , ( inicio , fin ) )
        facturas = cursor.fetchall()

        sql3 = "select folio,interno,JSON_EXTRACT(detalle, '$.vendedor'),JSON_EXTRACT(detalle, '$.monto_final') ,JSON_EXTRACT(detalle,'$.tipo_doc') ,JSON_EXTRACT(detalle, '$.doc_ref') from guia where fecha between %s and %s "
        cursor.execute(sql3 , ( inicio , fin ) )
        guias = cursor.fetchall()
        return (boletas, facturas, guias)
    except:
        return False

#ACTUALIZAR DATOS
@app.route('/actualizar/nota_venta/item', methods=['POST'])
def actualizar_nota_venta():
    dato = request.json
    estado = None
    if dato[0]:
        print("retirado completo")
        estado = "COMPLETO"
        
    else:
        print("retirado incompleto")
        estado = "INCOMPLETO"
    print(dato[1])
    print(dato[2])
    try:
        cursor = miConexion.cursor()
        sql = 'update nota_venta set estado_retiro = %s where interno = %s'
        cursor.execute(sql , (estado , dato[2]) )
        #miConexion.commit()
        # Crea la consulta
        sql = 'update item set retirado = %s where codigo = %s and interno = %s'
        cursor.executemany(sql , dato[1] )
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        miConexion.commit()
        return jsonify(data = True, message = "Cantidad retirada actualizada")
    except:
        return jsonify(data = False, message = "Error al actualizar cantidades. Consulte a su operador")


@app.route('/actualizar/guia/<int:interno>', methods=['POST'])
def actualizar_guia(interno = None):
    print(interno)


if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=5000, debug=True )
