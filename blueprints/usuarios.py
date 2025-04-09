from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Usuario
import forms
from utils import role_required
from werkzeug.security import generate_password_hash

usuarios = Blueprint('usuarios', __name__)

@usuarios.route("/usuarios", methods=['GET', 'POST'])
@login_required
@role_required('Administrador')
def usuario():
    
    usuarios = Usuario.query.all()

    return render_template('usuarios/usuarios.html', usuarios=usuarios)

@usuarios.route("/usuariosNuevo", methods=['GET', 'POST'])
@login_required
@role_required('Administrador')
def usuarioNuevo():
    create_form = forms.agregarUsuario(request.form)

    if request.method == 'POST' and create_form.validate():
        email_existente = Usuario.query.filter_by(email=create_form.email.data).first()
        if email_existente:
            flash('El correo ya está registrado, ingrese otro.', 'danger')
            return render_template('usuarios/usuariosNuevo.html', form=create_form)
        
        hashed_password = generate_password_hash(create_form.password.data)

        usuario = Usuario(
            nombre=create_form.nombre.data,
            apellido=create_form.apellido.data,
            email=create_form.email.data,
            password=hashed_password,
            rol=create_form.rol.data
        )

        db.session.add(usuario)
        db.session.commit()
        flash('Usuario registrado.', 'success')
        return redirect(url_for('usuarios.usuario'))

    return render_template('usuarios/usuariosNuevo.html', form=create_form)

@usuarios.route("/usuariosModificar", methods=['GET', 'POST'])
@login_required
@role_required('Administrador')
def usuarioModificar():
    create_form = forms.modificarUsuario(request.form)

    if request.method == 'GET':
        idUsuario = request.args.get('idUsuario')
        usuario = db.session.query(Usuario).filter(Usuario.idUsuario == idUsuario).first()
        create_form.idUsuario.data = idUsuario
        create_form.nombre.data = str.rstrip(usuario.nombre)
        create_form.apellido.data = usuario.apellido    
        create_form.email.data = usuario.email
        create_form.password.data = usuario.password
        create_form.rol.data = usuario.rol

    if request.method == 'POST':
        idUsuario = create_form.idUsuario.data
        usuario = db.session.query(Usuario).filter(Usuario.idUsuario == idUsuario).first()

        
        email_existente = db.session.query(Usuario).filter(
            Usuario.email == create_form.email.data,
            Usuario.idUsuario != idUsuario
        ).first()

        if email_existente:
            flash('El correo electrónico ya está registrado en otro usuario.', 'error')
            return render_template('usuarios/usuariosModificar.html', form=create_form)

        usuario.nombre = str.rstrip(create_form.nombre.data)
        usuario.apellido = create_form.apellido.data       
        usuario.email = create_form.email.data
            
        if create_form.password.data:
            usuario.set_password(create_form.password.data)

        usuario.rol = create_form.rol.data

        db.session.add(usuario)
        db.session.commit()
        flash('Usuario modificado.', 'success')
        return redirect(url_for('usuarios.usuario'))

    return render_template('usuarios/usuariosModificar.html', form=create_form)


@usuarios.route("/usuariosEliminar/<int:idUsuario>", methods=['GET', 'POST'])
@login_required
@role_required('Administrador')
def usuarioEliminar(idUsuario):
    usuario = Usuario.query.get_or_404(idUsuario)

    db.session.delete(usuario)
    db.session.commit()    
    flash('Usuario eliminado.', 'success')
    return redirect(url_for('usuarios.usuario'))
    