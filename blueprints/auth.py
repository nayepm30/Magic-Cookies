from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash, session
from flask_login import login_user, login_required, logout_user
from models import db, Usuario
from flask_mail import Message
import random
import forms

auth = Blueprint('auth', __name__)

@auth.route("/", methods=['GET', 'POST'])
def index():
    
    return render_template("index.html")

@auth.route("/login", methods=['GET', 'POST'])
def login():
    flash("")
    create_form = forms.inicioSesion(request.form)
    create_form2 = forms.crearUsuario(request.form)
    accion = request.form.get('accion')
 
    if request.method == 'POST':
        if accion == 'inicioSesion' and create_form.validate():
            usu = create_form.email.data.strip()
            pas = create_form.password.data.strip()

            sesion = Usuario.query.filter_by(email=usu).first()

            if sesion and sesion.check_password(pas):
                login_user(sesion)
                flash("Inicio de sesión exitoso.", "success")
                if sesion.rol == "Cliente":
                    return redirect(url_for('carrito.mostrar_galletas'))  
                else:
                    return redirect(url_for('inicio.dashboard'))  
            else:
                flash("Usuario o contraseña incorrectos.", "danger")

        elif accion == 'crearCuenta' and create_form2.validate():
            if Usuario.query.filter_by(email=create_form2.email2.data.strip()).first():
                flash("El correo electrónico ya está registrado.", "warning")
            else:
             
                session['nuevo_usuario'] = {
                    'nombre': create_form2.nombre.data.strip(),
                    'apellido': create_form2.apellido.data.strip(),
                    'email': create_form2.email2.data.strip(),
                    'password': create_form2.password2.data.strip()
                }

           
                codigo = str(random.randint(100000, 999999))
                session['codigo_verificacion'] = codigo

                mail = current_app.extensions['mail']
                msg = Message('Código de verificación - MagicCookies',
                            recipients=[session['nuevo_usuario']['email']])
                msg.body = f'Tu código de verificación es: {codigo}'
                mail.send(msg)

                return redirect(url_for('auth.verificacion'))
        else:
            flash("Error al registrar el usuario.", "danger")

    return render_template("login.html", form=create_form, form2=create_form2)

@auth.route("/verificacion", methods=['GET', 'POST'])
def verificacion():
    create_form = forms.nuevoUsuarioVerificacion(request.form)    
    if request.method == 'POST':
        codigo = str(create_form.codigo.data).strip()
        codigo_esperado = str(session.get('codigo_verificacion', '')).strip()   
         
        if codigo == codigo_esperado:
            datos = session.get('nuevo_usuario')
            if datos:
                nuevoUsuario = Usuario(
                    nombre=datos['nombre'],
                    apellido=datos['apellido'],
                    email=datos['email'],
                    rol="Cliente"
                )
                nuevoUsuario.set_password(datos['password'])

                db.session.add(nuevoUsuario)
                db.session.commit()

                # Limpiar sesión
                session.pop('nuevo_usuario', None)
                session.pop('codigo_verificacion', None)

                flash("Cuenta verificada y creada correctamente.", "success")
                return redirect(url_for('auth.login'))
        else:
            flash("Código incorrecto. Intenta de nuevo.", "danger")

    return render_template("loginVerificacion.html", form=create_form)

@auth.route("/logout")
@login_required
def logout():    
    logout_user()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('auth.index'))
 
@auth.route("/enviar_correo")
def enviar_correo():    
    mail = current_app.extensions['mail']
    
    msg = Message('Asunto del correo',
                  recipients=['torrestristan360@gmail.com'])
    msg.body = 'Hola, este es un correo de prueba enviado con Flask-Mail.'
    mail.send(msg)
    return 'Correo enviado correctamente'