from wtforms import form 
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, FormField,SubmitField,FieldList,TextAreaField, EmailField, PasswordField, StringField, IntegerField, DateField, DecimalField
from wtforms import validators
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Regexp, Optional, NumberRange

#Es para el inicio se sesion en auth.login
class inicioSesion(FlaskForm):
    email=EmailField('',[ validators.DataRequired(message='Campo requerido')]) 
    password=PasswordField('',[validators.DataRequired(message='Campo requerido')]) 

#Es para el registro de un nuevo usuario Cliente en auth.login
class crearUsuario(FlaskForm):
    nombre = StringField('', [validators.DataRequired(message='Campo requerido'),Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='No se permiten caracteres especiales')])
    apellido = StringField('', [validators.DataRequired(message='Campo requerido'),Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='No se permiten caracteres especiales')])  
    email2 = EmailField('', [validators.DataRequired(message='Campo requerido')])
    password2 = PasswordField('', [validators.DataRequired(message='Campo requerido')])
    
#Es para la modificaion de un usuario Cliente en usuarios.usuarioModificar
class modificarUsuario(FlaskForm):
    idUsuario=IntegerField('',[validators.number_range(min=1, max=2000,message='valor no valido')])
    nombre = StringField('', [validators.DataRequired(message='Campo requerido'),Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='No se permiten caracteres especiales')])
    apellido = StringField('', [validators.DataRequired(message='Campo requerido'),Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='No se permiten caracteres especiales')])      
    email = EmailField('', [validators.DataRequired(message='Campo requerido')])
    password = PasswordField('', validators=[Optional()])
    rol = SelectField('', choices=[('Administrador', 'Administrador'),('Vendedor', 'Vendedor'),('Cocinero', 'Cocinero'),('Cliente', 'Cliente')])  

class agregarUsuario(FlaskForm):   
    nombre = StringField('', [validators.DataRequired(message='Campo requerido'),Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='No se permiten caracteres especiales')])
    apellido = StringField('', [validators.DataRequired(message='Campo requerido'),Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='No se permiten caracteres especiales')])      
    email = EmailField('', [validators.DataRequired(message='Campo requerido')])
    password = PasswordField('', validators=[DataRequired()])
    rol = SelectField('', choices=[('Administrador', 'Administrador'),('Vendedor', 'Vendedor'),('Cocinero', 'Cocinero'),('Cliente', 'Cliente')])  
           
class nuevoUsuarioVerificacion(FlaskForm):
    codigo = IntegerField('', validators=[DataRequired()])

#Es para el registro de una nueva venta en ventas.registrar    
class nuevaVenta(FlaskForm):          
    producto = SelectField('', choices=[], validators=[validators.DataRequired(message='Seleccione un producto')])  
    presentacion = SelectField('', choices=[('Piezas', 'Piezas'),('Pre-empacada 700 gr', 'Pre-empacada 700 gr'),('Pre-empacada 1Kg', 'Pre-empacada 1Kg')], validators=[validators.DataRequired(message='Seleccione un producto')])  
    cantidad = FloatField('', [validators.DataRequired(message='Campo requerido'),validators.NumberRange(min=1, message='La cantidad no puede ser menor a 1')])

#Es para el registro de una nueva merma en mermas.nuevaMerma    
class NuevaMerma(FlaskForm):
    materia = SelectField('', coerce=int, validators=[validators.DataRequired()])
    cantidad = DecimalField('', validators=[validators.DataRequired(), validators.NumberRange(min=0.01)])
    motivo = TextAreaField('', validators=[validators.DataRequired()])        

class ProveedorNuevoForm(FlaskForm): 
    nombre = StringField('', validators=[DataRequired()])
    telefono = StringField('', validators=[DataRequired()])
    direccion = StringField('', validators=[DataRequired()])        

class ProveedorProductosForm(FlaskForm):  
    nombre_producto = StringField('', validators=[DataRequired()])
    cantidad  = DecimalField('', validators=[validators.DataRequired(), validators.NumberRange(min=0.01)])
    presentacion = SelectField('', choices=[('Kilos', 'Kilos'),('Gramos', 'Gramos'),('Litros', 'Litros'),('Mililitros', 'Mililitros'),('Piezas', 'Piezas')])  
    precio_unitario  = DecimalField('', validators=[validators.DataRequired(), validators.NumberRange(min=0.01)])

class OrdenProveedorForm(FlaskForm):  
    producto = SelectField('', choices=[], validators=[validators.DataRequired(message='Seleccione un producto')])  
    cantidad  = DecimalField('', validators=[validators.DataRequired(message='Ingrese una cantidad'), validators.NumberRange(min=0.01)])
            
class MiFormulario(FlaskForm):
    presentacion = SelectField(
        'Presentación',
        choices=[
            ('', 'Seleccionar'),  
            ('litros', 'Litros'),
            ('kilos', 'Kilos')
        ],
        validators=[DataRequired(message="Debes seleccionar una opción")],
        render_kw={
            'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer'
        }
    )
    
# Formulario para los ingredientes dentro de la receta
class IngredienteForm(FlaskForm):
    idIngrediente = SelectField('Ingrediente', coerce=int, validators=[DataRequired()])
    cantidad = DecimalField('Cantidad', validators=[DataRequired()])

# Formulario para la receta principal
class RecetaForm(FlaskForm):
    nombre = StringField('', validators=[DataRequired()])
    cantidad_produccion = IntegerField('', validators=[DataRequired()])            
    peso = FloatField('', validators=[DataRequired(message='Campo requerido')])

class RecetaIngredientesForm(FlaskForm):   
    ingrediente = SelectField('', choices=[], validators=[validators.DataRequired(message='Seleccione un ingrediente')])  
    cantidad = FloatField('', [validators.DataRequired(message='Campo requerido')])   

class RecetaImagenForm(FlaskForm):       
    imagen = FileField('', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Solo se permiten imágenes JPG, JPEG o PNG.')])      
        
# Formulario de el empaquetado
class CrearPaqueteForm(FlaskForm):
    producto_id = SelectField('Producto (Tipo Galleta)', coerce=int, validators=[DataRequired()])
    gramaje = SelectField('Gramaje del Paquete', choices=[('700', '700 gramos'), ('1000', '1 Kilo')], validators=[DataRequired()])
    cantidad_paquetes = IntegerField('Cantidad de Paquetes a Crear', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('Crear Paquetes')    