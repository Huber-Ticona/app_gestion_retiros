from flask import Blueprint,abort,session,render_template,redirect,url_for,request,flash,jsonify,json,send_file,send_from_directory,current_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from .extensions import obtener_conexion
main_bp = Blueprint('main_bp', __name__ , static_folder='static' , template_folder='templates')

@main_bp.route('/')
def home():
    if "usuario" in session:
        usuario = session["usuario"]
        tipo = session['tipo']
        return render_template('home.html' , usuario = usuario,tipo_usuario = tipo)
    else:
        return redirect(url_for('auth_bp.login'))

@main_bp.route('/panel_clasico')
def panel_clasico(fecha = None):
    if "usuario" in session:
        usuario = session["usuario"]
        fecha =  datetime.now().date()

        return render_template('panel_clasico.html', usuario = usuario , fecha= str(fecha) ,tipo_usuario= session['tipo'])
    else:
        return redirect(url_for('main_bp.home'))
    
@main_bp.route('/documentos/<string:tipo>')
@main_bp.route('/documentos/<string:tipo>/<int:folio>')
@main_bp.route('/documentos/<string:tipo>/<string:tipo_orden>/<int:folio>')
def documentos(tipo = None,folio = None,tipo_orden = None):
    if "usuario" in session:
        usuario = session["usuario"]
        fecha = datetime.now().date()
        return render_template('documentos.html'  ,usuario = usuario, tipo = tipo,fecha = str(fecha), folio = folio,tipo_orden = tipo_orden)
    else:
        return redirect(url_for('login'))

@main_bp.route('/mi_cuenta')
def mi_cuenta():
    if "usuario" in session:
        usuario = session["usuario"]
        return render_template('cuenta.html' , usuario = usuario)
    else:
        return redirect(url_for('login'))

@main_bp.route('/informes')
def informes():
    if "usuario" in session:
        usuario = session["usuario"]
        fecha1 = datetime.fromisoformat('2021-01-01')
        fecha1 = fecha1.date()
        fecha2 = datetime.now()
        fecha2 = fecha2.date()

        return render_template('informes.html' , usuario = usuario, fecha1 = str(fecha1), fecha2 = str(fecha2) ,tipo_usuario= session['tipo'])
   
    else:
        return redirect(url_for('login'))

@main_bp.route('/herramientas')
def herramientas():
    if "usuario" in session:
        usuario = session["usuario"]
        fecha = datetime.fromisoformat('2021-05-10')
        fecha = fecha.date()
        return render_template('herramientas.html' , usuario = usuario, fecha = str(fecha))
    else:
        return redirect(url_for('login'))
         
    
#OBTENCION DE ITEMS X NRO INTERNO
@main_bp.route('/obt_detalle_bol_fact/<int:interno>', methods = ['POST'])
def obt_detalle_bol_fact_interno(interno):
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
            cursor = miConexion.cursor()
            cursor.execute("select descripcion, cantidad, retirado, codigo, interno, unitario, total from item  where interno = %s " , interno ) #SE AGREGO EL ESTADO RETIRADO
            detalle = cursor.fetchall()
            print(detalle)
            print(jsonify(detalle))
            return jsonify(detalle)
    finally:
        miConexion.close()

@main_bp.route('/obt_detalle_guia/<int:interno>', methods = ['POST'])
def obt_detalle_guia_interno(interno):
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
            cursor = miConexion.cursor()
            cursor.execute("select detalle , adjuntos, vinculaciones, fecha, historial_retiro from guia  where interno = %s " , interno )
            detalle = cursor.fetchall()
            print(detalle)
            print(jsonify(detalle[0]))
            return jsonify(detalle[0])
    finally:
        miConexion.close()


@main_bp.route('/documentos/guias/folio/<int:folio>', methods = ['POST'])
@main_bp.route('/documentos/guias/fecha/<string:fecha1>/<string:fecha2>', methods = ['POST'])
@main_bp.route('/documentos/guias/cliente/<string:cliente>', methods = ['POST'])
def obt_guia(folio = None,fecha1 = None, fecha2= None,cliente = None):
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
            detalle = []
            print('llego a buscar guias ..')
            if folio:
                print('buscando guias x folio ....')
                sql = "SELECT folio,fecha,interno,nombre,detalle,JSON_EXTRACT(detalle,'$.monto_final'),JSON_EXTRACT(detalle,'$.estado_retiro'),JSON_EXTRACT(detalle,'$.revisor')  from guia where folio = %s"
                cursor.execute(sql , folio )
                detalle = cursor.fetchall()
                
            elif fecha1 and fecha2:
                print('buscando guias x fecha ....')
                inicio = str(fecha1) + ' 00:00'
                fin = str(fecha2) + ' 23:59'
                sql = "SELECT folio,fecha,interno,nombre,detalle,JSON_EXTRACT(detalle,'$.monto_final'),JSON_EXTRACT(detalle,'$.estado_retiro'),JSON_EXTRACT(detalle,'$.revisor')  from guia where fecha between %s and %s"
                cursor.execute( sql, (inicio, fin) )
                detalle = cursor.fetchall()
            elif cliente:
                print('buscando guias x nombre cliente ...')
                sql = "SELECT folio,fecha,interno,nombre,detalle,JSON_EXTRACT(detalle,'$.monto_final'),JSON_EXTRACT(detalle,'$.estado_retiro'),JSON_EXTRACT(detalle,'$.revisor')  from guia where nombre like '%" + cliente +"%'"
                cursor.execute( sql )
                detalle = cursor.fetchall()

            return jsonify(detalle)
    finally:
        miConexion.close()
@main_bp.route('/documentos/boletas/folio/<int:folio>', methods = ['POST'])
@main_bp.route('/documentos/boletas/fecha/<string:fecha1>/<string:fecha2>', methods = ['POST'])
@main_bp.route('/documentos/boletas/cliente/<string:cliente>', methods = ['POST'])
def obt_boleta(folio = None,fecha1 = None, fecha2= None,cliente = None):
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
            detalle = []
            print('llego a buscar guias ..')
            if folio:
                print('buscando boleta x folio ....')
                sql = "SELECT nro_boleta,fecha,interno,'Cliente Boleta',adjuntos,monto_total,estado_retiro,revisor,vinculaciones,adjuntos from nota_venta where nro_boleta = %s"
                cursor.execute(sql , folio )
                detalle = cursor.fetchall()
                #print(detalle)  
                
            elif fecha1 and fecha2:
                print('buscando boleta x fecha ....')
                inicio = str(fecha1) + ' 00:00'
                fin = str(fecha2) + ' 23:59'
                sql = "SELECT nro_boleta,fecha,interno,'Cliente Boleta',adjuntos,monto_total,estado_retiro,revisor,vinculaciones,adjuntos from nota_venta where folio = 0 and ( fecha between %s and %s) "
                cursor.execute( sql, (inicio, fin) )
                detalle = cursor.fetchall()
                #print(detalle)
            #TODAS LOS CLIENTES SON CLIENTES BOLETAS.
            '''elif cliente:
                print('buscando boleta x nombre cliente ...')
                sql = "SELECT nro_boleta,fecha,interno,'Cliente Boleta',adjuntos,monto_total,estado_retiro,revisor from nota_venta where folio = 0 and ( fecha between %s and %s) " 
                cursor.execute( sql )
                detalle = cursor.fetchall()
                print(detalle)'''

            return jsonify(detalle)
    finally:
        miConexion.close()

@main_bp.route('/documentos/facturas/folio/<int:folio>', methods = ['POST'])
@main_bp.route('/documentos/facturas/fecha/<string:fecha1>/<string:fecha2>', methods = ['POST'])
@main_bp.route('/documentos/facturas/cliente/<string:cliente>', methods = ['POST'])
def obt_factura(folio = None,fecha1 = None, fecha2= None,cliente = None):
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
            detalle = []
            print('llego a buscar facturas ..')
            if folio:
                print('buscando factura x folio ....')
                sql = "SELECT folio,fecha,interno,nombre,adjuntos,monto_total,estado_retiro,revisor,vinculaciones,adjuntos from nota_venta where folio = %s"
                cursor.execute(sql , folio )
                detalle = cursor.fetchall()
                #print(detalle)  
                
            elif fecha1 and fecha2:
                print('buscando factura x fecha ....')
                inicio = str(fecha1) + ' 00:00'
                fin = str(fecha2) + ' 23:59'
                sql = "SELECT folio,fecha,interno,nombre,adjuntos,monto_total,estado_retiro,revisor,vinculaciones,adjuntos from nota_venta where nro_boleta = 0 and ( fecha between %s and %s) "
                cursor.execute( sql, (inicio, fin) )
                detalle = cursor.fetchall()
                #print(detalle)
            elif cliente:
                print('buscando factura x nombre cliente ...')
                sql = "SELECT folio,fecha,interno,nombre,adjuntos,monto_total,estado_retiro,revisor,vinculaciones,adjuntos from nota_venta where nro_boleta = 0 and nombre like  '%" + cliente +"%'" 
                cursor.execute( sql )
                detalle = cursor.fetchall()
                #print(detalle)

            return jsonify(detalle)
    finally:
        miConexion.close()

@main_bp.route('/documentos/creditos/folio/<int:folio>', methods = ['POST'])
@main_bp.route('/documentos/creditos/fecha/<string:fecha1>/<string:fecha2>', methods = ['POST'])
@main_bp.route('/documentos/creditos/cliente/<string:cliente>', methods = ['POST'])
def obt_creditos(folio = None,fecha1 = None, fecha2= None,cliente = None):
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
            detalle = []
            print('llego a buscar creditos ..')
            if folio:
                print('buscando creditos x folio ....')
                sql = "SELECT folio,fecha,interno,nombre,detalle,JSON_EXTRACT(detalle, '$.monto_final'),JSON_EXTRACT(detalle, '$.observacion'),JSON_EXTRACT(detalle, '$.motivo'),JSON_EXTRACT(detalle, '$.tipo_doc'),JSON_EXTRACT(detalle, '$.doc_ref') from nota_credito where folio = %s"
                cursor.execute(sql , folio )
                detalle = cursor.fetchall()
                #print(detalle)  
                
            elif fecha1 and fecha2:
                print('buscando creditos x fecha ....')
                inicio = str(fecha1) + ' 00:00'
                fin = str(fecha2) + ' 23:59'
                sql = "SELECT folio,fecha,interno,nombre,detalle,JSON_EXTRACT(detalle, '$.monto_final'),JSON_EXTRACT(detalle, '$.observacion'),JSON_EXTRACT(detalle, '$.motivo'),JSON_EXTRACT(detalle, '$.tipo_doc'),JSON_EXTRACT(detalle, '$.doc_ref')  from nota_credito where fecha between %s and %s "
                cursor.execute( sql, (inicio, fin) )
                detalle = cursor.fetchall()
                #print(detalle)
            elif cliente:
                print('buscando creditos x nombre cliente ...')
                sql = "SELECT folio,fecha,interno,nombre,detalle,JSON_EXTRACT(detalle, '$.monto_final'),JSON_EXTRACT(detalle, '$.observacion'),JSON_EXTRACT(detalle, '$.motivo'),JSON_EXTRACT(detalle, '$.tipo_doc'),JSON_EXTRACT(detalle, '$.doc_ref') from nota_credito where nombre like  '%" + cliente +"%'" 
                cursor.execute( sql )
                detalle = cursor.fetchall()
                #print(detalle)

            return jsonify(detalle)
    finally:
        miConexion.close()

@main_bp.route('/documentos/ordenes/<string:tipo>/folio/<int:folio>', methods = ['POST'])
@main_bp.route('/documentos/ordenes/<string:tipo>/fecha/<string:fecha1>/<string:fecha2>', methods = ['POST'])
@main_bp.route('/documentos/ordenes/<string:tipo>/cliente/<string:cliente>', methods = ['POST'])
def obt_ordenes(folio = None,tipo = None,fecha1 = None, fecha2= None,cliente = None):
    miConexion = obtener_conexion()
    #Sanitizar valores , analisis futuro.
    try:
        with miConexion.cursor() as cursor:
            detalle = []
            print('llego a buscar orden de: ' + tipo + ' ...')
            if folio:
                print('buscando orden x folio ....')
                sql = "SELECT nro_orden,fecha_orden,telefono,nombre,detalle, JSON_EXTRACT(detalle, '$.creado_por'),despacho,JSON_EXTRACT(extra, '$.estado'),tipo_doc ,nro_doc from orden_"+ tipo +" where nro_orden = " + str(folio) 
                cursor.execute(sql ) 
                detalle = cursor.fetchall()
                print(detalle)  
                
            elif fecha1 and fecha2:
                print('buscando orden x fecha ....')
                inicio = str(fecha1) + ' 00:00'
                fin = str(fecha2) + ' 23:59'
                sql = "SELECT nro_orden,fecha_orden,telefono,nombre,detalle, JSON_EXTRACT(detalle, '$.creado_por'),despacho,JSON_EXTRACT(extra, '$.estado'),tipo_doc ,nro_doc from orden_"+ tipo +" where fecha_orden between '"+ inicio + "' and  '" + fin +"'"
                cursor.execute( sql )
                detalle = cursor.fetchall()
                #print(detalle)
            elif cliente:
                print('buscando orden x nombre cliente ...')
                sql = "SELECT nro_orden,fecha_orden,telefono,nombre,detalle, JSON_EXTRACT(detalle, '$.creado_por'),despacho,JSON_EXTRACT(extra, '$.estado'),tipo_doc ,nro_doc  from orden_"+ tipo +" where nombre like  '%" + cliente + "%'" 
                cursor.execute( sql )
                detalle = cursor.fetchall()
                #print(detalle)

            return jsonify(detalle)
    finally:
        miConexion.close()

#OBTENCION DE DATOS DE DOCUMENTO (BOLETA,FACTURA Y GUIA)
def busqueda_docs_fecha(inicio,fin):
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
        #cursor = miConexion.cursor()

            sql1 = "select interno,vendedor,folio,monto_total,nro_boleta,nombre,vinculaciones,adjuntos,estado_retiro,revisor,despacho,fecha,historial_retiro from nota_venta where folio = 0 and fecha between %s and %s "
            cursor.execute( sql1 , ( inicio , fin )  )
            boletas = cursor.fetchall()

            sql2 = "select interno,vendedor,folio,monto_total,nro_boleta,nombre,vinculaciones,adjuntos,estado_retiro,revisor ,despacho,fecha,historial_retiro from nota_venta where nro_boleta = 0 and  fecha between %s and %s "
            cursor.execute(sql2 , ( inicio , fin ) )
            facturas = cursor.fetchall()

            sql3 = "select folio, interno,JSON_EXTRACT(detalle, '$.vendedor'),JSON_EXTRACT(detalle, '$.monto_final'), JSON_EXTRACT(detalle, '$.estado_retiro'),vinculaciones, JSON_EXTRACT(detalle, '$.tipo_doc'),despacho from guia where fecha between %s and %s "
            cursor.execute(sql3 , ( inicio , fin ) )
            guias = cursor.fetchall()
            return (boletas, facturas, guias)
    except:
        return False
    finally:
        miConexion.close()
#obt 2
@main_bp.route('/obtener/docs/<string:fecha>')
def obt_docs(fecha):
    print("Fecha recibida: " + fecha)
    inicio = str(fecha) + ' 00:00'
    fin = str(fecha) + ' 23:59'

    documentos = busqueda_docs_fecha(inicio,fin)
    if documentos:
        l_bol = documentos[0]
        l_fact = documentos[1]
        l_guia = documentos[2]
        #print(l_guia)
        return render_template('body_panel.html' , boletas = l_bol,facturas = l_fact,guias = l_guia)
    else:
        return render_template('no_db_con.html')
    
#ACTUALIZAR DATOS
@main_bp.route('/actualizar/nota_venta/item', methods=['POST'])
def actualizar_nota_venta():
    dato = request.json
    estado = None
    print('----- datos update -------')
    print(dato[0])
    print(dato[1])
    print(dato[2])
    print('----- datos historial --------')
    #historial
    fecha = datetime.now()
    detalle = {
        "revisor": session['usuario'],
        "fecha": str(fecha.strftime("%d-%m-%Y %H:%M:%S")),
        "descripciones":dato[3],
        "antes": dato[4],
        "despues": dato[5]
    }
    historial = json.dumps(detalle)
    print(historial)

    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
            # Se actualiza el estado de retiro
            sql = 'update nota_venta set estado_retiro = %s where interno = %s'
            cursor.execute(sql , (dato[0] , dato[2]) )
            # Se actualiza el revisor
            sql = 'update nota_venta set revisor = %s where interno = %s'
            cursor.execute(sql , (session['usuario'] , dato[2]) )
            #miConexion.commit()
            # Crea la consulta
            sql = 'update item set retirado = %s where codigo = %s and interno = %s'
            cursor.executemany(sql , dato[1] )
            # connection is not autocommit by default. So you must commit to save
            # your changes.

            #historial
            sql = 'select historial_retiro,interno from nota_venta where interno = %s'
            cursor.execute(sql, dato[2])
            lista = cursor.fetchone()
            if lista[0] == None:
                print('--------creando historial ----------')
                lista_historial = []
                lista_historial.append(historial)                
                detalle2 = {
                    "lista_historial" : lista_historial
                }
                nuevo_historial = json.dumps(detalle2)
                sql = 'update nota_venta set historial_retiro = %s where interno = %s'
                cursor.execute(sql , ( nuevo_historial , dato[2]) )
            else:
                print('--------actualizando historial ----------')
                aux_historial = json.loads(lista[0])
                try:
                    aux_historial['lista_historial'].append(historial)
                    nuevo_historial = json.dumps(aux_historial)
                    sql = 'update nota_venta set historial_retiro = %s where interno = %s'
                    cursor.execute(sql , ( nuevo_historial , dato[2]) )
                except KeyError:
                    print(' llave "lista_historial" no encontrado. Historial NO creado')
                    
            miConexion.commit()
            return jsonify(data = True, message = "Cantidad retirada actualizada")
    except:
        return jsonify(data = False, message = "Error al actualizar cantidades. Consulte a su operador")
    finally:
        miConexion.close()
        

@main_bp.route('/actualizar/guia/item', methods=['POST'])
def actualizar_guia():
    dato = request.json
    print('----- datos update -------')
    print(dato[0])
    print(dato[1])
    print(dato[2])
    print('----- datos historial --------')
    #historial
    fecha = datetime.now()
    detalle = {
        "revisor": session['usuario'],
        "fecha": str(fecha.strftime("%d-%m-%Y %H:%M:%S")),
        "descripciones":dato[3],
        "antes": dato[4],
        "despues": dato[5]
    }
    historial = json.dumps(detalle)
    print(historial)

    nuevo = json.dumps(dato[1]) #items retirados
    nuevo = nuevo[1: len(nuevo) - 1]

    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
    
            '''sql = "SELECT JSON_EXTRACT( detalle , '$.retirado') from guia where interno = %s"
            cursor.execute(sql, dato[2])
            registro = cursor.fetchone()
            print(registro)'''

            #if registro[0]:#Si existe registro del retiro y revisor anteriormente **MODIFICADO ya que el agente capturador, otorga dichos parametros en la creacion
            print("tiene registrado retiros, comenzando a actualizar...")
            sql = "SELECT JSON_REPLACE(detalle, '$.retirado', JSON_ARRAY("+ nuevo +"),'$.estado_retiro', %s,'$.revisor', %s ) from guia where interno = %s"
            cursor.execute(sql, (dato[0], session['usuario'] , dato[2] ))
            resultado = cursor.fetchone()
            #print(resultado)

            '''else:
                print("no tiene registrado retiros y revisor, creando registros ...")
                sql = "SELECT JSON_INSERT( detalle , '$.retirado', JSON_ARRAY("+ nuevo +"),'$.estado_retiro', %s, '$.revisor', %s ) from guia where interno = %s"
                cursor.execute(sql, (estado , session['usuario'], dato[2] ))
                resultado = cursor.fetchone()
                print(resultado)'''

            sql2 = "UPDATE guia SET detalle = %s where interno = %s"
            cursor.execute(sql2 , (resultado, dato[2]))

            # ACTUALIZANDO EL HISTORIAL
            sql = 'select historial_retiro,interno from guia where interno = %s'
            cursor.execute(sql, dato[2])
            lista = cursor.fetchone()
            if lista[0] == None:
                print('--------creando historial ----------')
                lista_historial = []
                lista_historial.append(historial)                
                detalle2 = {
                    "lista_historial" : lista_historial
                }
                nuevo_historial = json.dumps(detalle2)
                sql = "UPDATE guia SET historial_retiro = %s where interno = %s"
                cursor.execute(sql , ( nuevo_historial , dato[2]) )
            else:
                print('--------actualizando historial ----------')
                aux_historial = json.loads(lista[0])
                try:
                    aux_historial['lista_historial'].append(historial)
                    nuevo_historial = json.dumps(aux_historial)
                    sql = "UPDATE guia SET historial_retiro = %s where interno = %s"
                    cursor.execute(sql , ( nuevo_historial , dato[2]) )
                except KeyError:
                    print(' llave "lista_historial" no encontrado. Historial NO creado')

            miConexion.commit()

            return jsonify(data = True, message = "GUIA: Cantidad retirada actualizada")
    except:
        return jsonify(data = False, message = "GUIA: Error al actualizar cantidades. Consulte a su operador")
    finally:
        miConexion.close()

@main_bp.route('/estadisticas/generales' , methods=['POST'] )
def obt_estadistica_general():
    x_ventas = [0,0,0]
    x_guias = [0,0,0] #[NO RETIRADO, INCOMPLETO, COMPLETO]
    #CONSULTAS
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
            cursor.execute("SELECT estado_retiro, count(*) FROM nota_venta group by estado_retiro") #SE AGREGO EL ESTADO RETIRADO
            ventas = cursor.fetchall()
            print(ventas)
            if ventas != ():
                for item in ventas:
                    if item[0] == 'NO RETIRADO':
                        x_ventas[0] = item[1]
                    elif item[0] == 'INCOMPLETO':
                        x_ventas[1] = item[1]
                    elif item[0] == 'COMPLETO':
                        x_ventas[2] = item[1]
                    print(x_ventas)

            cursor.execute("SELECT JSON_EXTRACT(detalle, '$.estado_retiro'), count(*) FROM guia group by JSON_EXTRACT(detalle, '$.estado_retiro')") #SE AGREGO EL ESTADO RETIRADO
            guias = cursor.fetchall()
            print(guias)
            if guias != ():
                
                for item in guias:
                    print(item)
                    if item[0] == '"NO RETIRADO"':
                        x_guias[0] = item[1]
                    elif item[0] == '"INCOMPLETO"':
                        x_guias[1] = item[1]
                    elif item[0] == '"COMPLETO"':
                        x_guias[2] = item[1]
                    print(x_guias)

            return jsonify( estado = True, ventas = x_ventas,
                            guias = x_guias)
    
    finally:
        miConexion.close() 

@main_bp.route('/estadisticas/pendientes/<string:fecha1>/<string:fecha2>')
def obt_pendientes(fecha1 = None , fecha2 = None):

    inicio = str(fecha1) + ' 00:00'
    fin = str(fecha2) + ' 23:59'
    print('Pendientes Desde: '+ inicio + ' - Hasta: ' + fin)
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
            sql1= "SELECT interno,vendedor,folio,monto_total,nro_boleta,nombre,vinculaciones,adjuntos,estado_retiro,revisor, despacho,fecha,historial_retiro from nota_venta where (estado_retiro = 'NO RETIRADO' OR estado_retiro = 'INCOMPLETO' ) and nro_boleta = 0 AND (fecha between '"+ inicio +"' and '"+ fin +"')"
            cursor.execute(sql1) 
            facturas = cursor.fetchall()

            sql2 = "SELECT interno,vendedor,folio,monto_total,nro_boleta,nombre,vinculaciones,adjuntos,estado_retiro,revisor,despacho,fecha,historial_retiro from nota_venta where (estado_retiro = 'NO RETIRADO' OR estado_retiro = 'INCOMPLETO' ) and folio = 0 AND (fecha between '"+ inicio +"' and '"+ fin +"')"
            cursor.execute(sql2) 
            boletas = cursor.fetchall()

            sql3 = "SELECT folio, interno,JSON_EXTRACT(detalle, '$.vendedor'),JSON_EXTRACT(detalle, '$.monto_final'), JSON_EXTRACT(detalle, '$.estado_retiro'),vinculaciones , JSON_EXTRACT(detalle, '$.tipo_doc'),despacho from guia where ( JSON_EXTRACT(detalle, '$.estado_retiro') = 'NO RETIRADO' OR JSON_EXTRACT(detalle, '$.estado_retiro') = 'INCOMPLETO' ) AND (fecha between '"+ inicio +"' and '"+ fin +"')"
            cursor.execute(sql3)
            guias = cursor.fetchall()

            #datos = []
            #datos.append(boletas)
            #datos.append(facturas)
            #datos.append(guias)
            return render_template('body_panel.html' , boletas = boletas,facturas = facturas ,guias = guias)

    finally:
        miConexion.close() 
@main_bp.route('/estadisticas/flujo-diario/<string:fecha1>/<string:fecha2>')
def obt_flujo_diario(fecha1 = None, fecha2 = None):

    inicio = str(fecha1) + ' 00:00'
    fin = str(fecha2) + ' 23:59'
    ventas = []
    guias = []
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
            sql1= "SELECT * from nota_venta WHERE fecha between %s and %s "
            cursor.execute(sql1, ( inicio, fin )) 
            ventas = cursor.fetchall()

            sql3 = "SELECT * from guia where fecha between %s and %s "
            cursor.execute(sql3 , ( inicio , fin ))
            guias = cursor.fetchall()

            return jsonify(
                ventas = ventas,
                guias = guias
            )


    finally:
        miConexion.close() 


@main_bp.route('/estadisticas/despachos-atrasados' ,methods = ['POST'])
def despachos_atrasados():
    ventas = []
    guias = []
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
            sql1= "SELECT * from nota_venta where estado_retiro != 'COMPLETO' AND despacho = 'SI' "
            cursor.execute(sql1) 
            ventas = cursor.fetchall()  

            sql3 = "SELECT * from guia where despacho is not null and despacho !='NO' and detalle->'$.estado_retiro' = 'NO RETIRADO' "
            cursor.execute(sql3 )
            guias = cursor.fetchall()

            return jsonify(
                ventas = ventas,
                guias = guias
            )
    finally:
        miConexion.close()
@main_bp.route('/despachos_atrasados_defecto', methods=['POST'])
def atraso():
    print('---- OBTENIENDO DESPACHOS ATRASADOS X 3 DIAS -----')
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
            sql =  '''SELECT COUNT(*) 
                FROM nota_venta
                WHERE nro_boleta = 0 and despacho = "SI" AND (DATEDIFF(NOW(), fecha) >= 3) and estado_retiro != "COMPLETO" '''
            cursor.execute(sql) 
            facturas = cursor.fetchone()

            sql =  '''SELECT COUNT(*) 
                FROM nota_venta
                WHERE folio = 0 and despacho = "SI" AND (DATEDIFF(NOW(), fecha) >= 3) and estado_retiro != "COMPLETO" '''
            cursor.execute(sql) 
            boletas = cursor.fetchone()

            sql = '''SELECT count(*)
                FROM guia
                WHERE despacho = "SI" AND (DATEDIFF(NOW(), fecha) >= 3) and detalle->"$.estado_retiro" != "COMPLETO" '''
            cursor.execute(sql) 
            guias = cursor.fetchone()

            return jsonify(
                len_boletas = boletas,
                len_facturas = facturas,
                len_guias = guias
            )


    finally:
        miConexion.close()
####### ADJUNTAR IMAGEN A DOCUMENTO VENTA #########
ALLOWED_EXTENSIONS = {'pdf','png', 'jpg', 'jpeg'}  # Extensiones permitidas

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/subir', methods=['POST'])
@main_bp.route('/subir/<int:folio>/<string:tipo_doc>/<int:interno>', methods=['GET', 'POST'])
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
            miConexion = obtener_conexion()
            try:
                with miConexion.cursor() as cursor:
                    adjuntos = None
                    
                    if tipo == "GUIA":
                        tabla = "guia"
                    else:
                        tabla = "nota_venta"
                    
                    sql1 = "SELECT adjuntos from "+ tabla +" where interno = %s"
                    cursor.execute( sql1 , ( interno )  )
                    adjuntos = cursor.fetchone()
                    
                    
                    print(adjuntos)
                    
                    if adjuntos[0] != None: #Si existe adjuntos del documento
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
                        print("no tiene adj")
                        new_adjuntos = []
                        nuevo_nombre = tipo + '_'+str(folio)+'_'+'adjunto_1.' + extension[1] 
                        new_adjuntos.append(nuevo_nombre)
                        new_adjuntos = json.dumps(new_adjuntos)
                        print(type(new_adjuntos))

                    sql2 = "update "+ tabla +" set adjuntos = %s where interno = %s"
                    cursor.execute( sql2 , ( new_adjuntos, interno )  )
                    miConexion.commit()
                    #SE ALMACENA LOCALMENTE
                    filename = secure_filename(nuevo_nombre)
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    return jsonify(
                        data = nuevo_nombre,
                        category="success",
                        message = tipo_doc + ": Imagen adjuntada con exito"
                    )
            except:
                print('error de excepcion encontrado')
                return jsonify(
                    message="error de excepcion interna",
                    category="error"
                )
            finally:
                miConexion.close()
            
        else:
            return jsonify(
                    message="formato invalido",
                    category="error"
                )

        
@main_bp.route('/descargar/<name>')
def download_file(name):
    print('upload folder: ',current_app.config["UPLOAD_FOLDER"])
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)
########

@main_bp.route('/releases')
def releases():
    print('root_path: ', current_app.root_path )
    print('upload_folder: ', current_app.config["UPLOAD_FOLDER"] )
    print('RELEASE_FOLDER: ', current_app.config["RELEASE_FOLDER"] )
    print('PROYECTO ROOT: ',current_app.config["PROYECT_ROOT"])

    releases = os.listdir(current_app.config["RELEASE_FOLDER"])
    latest_release = max(releases)
    return render_template('releases.html', latest_release=latest_release,releases=releases)

@main_bp.route('/releases/<filename>')
def download_release(filename):
    try:
        return send_from_directory(current_app.config["RELEASE_FOLDER"], filename,as_attachment=True)
    except FileNotFoundError:
        abort(404)
