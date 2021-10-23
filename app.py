from flask import Flask, url_for , request , render_template , session
from flask.wrappers import Request
from flaskext.mysql import MySQL

app = Flask(__name__)


# CREANDO LA CONEXION A LA BASE DE DATOS
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'huber'
app.config['MYSQL_DATABASE_PASSWORD'] = 'huber123'
app.config['MYSQL_DATABASE_DB'] = 'madenco'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def index():
    return "<p>Hola >:3 bruh! xd  !</p>"

@app.route('/login' , methods = ['GET', 'POST'])   
def login():
    return render_template('base.html')

    
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


with app.test_request_context():

    print(url_for('ordenes'))
    print(url_for('variable' , dato = 'huber ticona' ))

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=5000, debug=True )
