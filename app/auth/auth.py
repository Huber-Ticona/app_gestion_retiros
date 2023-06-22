from flask import Blueprint, session, render_template, redirect, url_for, request, flash
from ..models.ModeloUsuario import ModeloUsuario

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])  # iniciar sesión
def login():
    print(' ------- LOGIN --------')
    if request.method == 'POST':
        nombre = request.form['nombre_usuario']
        contra = request.form['contraseña']

        consulta = ModeloUsuario.login(nombre)
        if consulta:
            print('Usuario encontrado: ', consulta)
            if consulta[8] == 'porteria':  # or consulta[8] == 'area':
                if consulta[2] == contra:
                    session['tipo'] = consulta[8]
                    session['usuario'] = consulta[10]
                    print('usuario con privilegios')
                else:
                    print('Contraseña invalida')
                    flash('Contraseña invalida')
            else:
                print('Usuario sin privilegios ')
                flash('Usuario sin privilegios -> Porteria')
        else:
            flash('Nombre de usuario invalido')
            print("usuario no encontrado, en la bd")
        return redirect(url_for('main_bp.home'))

    return render_template('login.html')


@auth_bp.route('/mi_cuenta')
def mi_cuenta():
    if "usuario" in session:
        usuario = session["usuario"]
        return render_template('cuenta.html', usuario=usuario)
    else:
        return redirect(url_for('auth_bp.login'))


@auth_bp.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('usuario', None)
    return redirect(url_for('main_bp.home'))
