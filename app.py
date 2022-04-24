from flask import Flask, render_template, request, url_for
import pyrebase

import json

from werkzeug.utils import redirect

from Modelo.Usuario import Usuario

from Modelo.UsuarioSistema import UsuarioSistema

#Variable de configuracion
config = {
  "apiKey": "AIzaSyCkxz74SNgdH5oTPYAZ_zm2_vYQ4foC4tE",
  "authDomain": "signosvitales-67c64.firebaseapp.com",
  "databaseURL": "https://signosvitales-67c64-default-rtdb.firebaseio.com",
  "projectId": "signosvitales-67c64",
  "storageBucket": "signosvitales-67c64.appspot.com",
  "messagingSenderId": "1056196522606",
  "appId": "1:1056196522606:web:3d35df6ce793522337ac7f"
}


firebase=pyrebase.initialize_app(config)
db=firebase.database()


app = Flask(__name__)


@app.route('/inicio')
def inicio():
    lista_estacionamiento=db.child("estacionamiento").get().val()
    return render_template("inicio.html", elementos_estacionamiento=lista_estacionamiento.values())

@app.route('/')
def hello_world():
    lista=db.child("estacionamiento").get()
    try:
        lista_estacionamiento=lista.val()
        lista_indices=lista_estacionamiento.keys()
        lista_indice_final=list(lista_indices)
        return render_template("inicio.html", elementos_estacionamiento=lista_estacionamiento.values(),lista_indice_final=lista_indice_final)
    except:
        return render_template("inicio.html")


#Ruta para el registro de lugares
@app.route('/add')
def add():
    return render_template("alta_lugares.html")
#---------------------------------------------------------
#Captura de daots del formulario y guardarlos en FB
@app.route('/save_data', methods=['POST'])
def save_data():
    estacionamiento=request.form.get('estacionamiento')
    estado=request.form.get('estado')
    fecha=request.form.get('fecha')
    hora=request.form.get('hora')
    nuevo_dato=Usuario(estacionamiento,estado,fecha,hora)
    objeto_enviar= json.dumps(nuevo_dato.__dict__)

    formato = json.loads(objeto_enviar)
    db.child("estacionamiento").push(formato)

    #db.child("estacionamiento").push({"estacionamiento": estacionamiento, "estado": estado, "fecha": fecha, "hora": hora})
    return redirect(url_for('hello_world'))


@app.route('/eliminar_lugar', methods=["GET"])
def eliminar_lugar():
    id = request.args.get("id")
    db.child("estacionamiento").child(str(id)).remove()
    return redirect(url_for('hello_world'))

#-------------------------Ruta para mostrar el formulario registrar--------------------
@app.route('/actualizar_lugar/<id>')
def actualizar_lugar(id):
    lista = db.child("estacionamiento").child(str(id)).get().val()
    return render_template("formulario_actualizar.html",lista=lista,id_lugar=id)


#----------------------Ruta para modificar los valores con base al ID---------------------
@app.route('/update',methods=["POST"])
def update_lugar():
    idlugar=request.form.get('id')
    estacionamiento = request.form.get('estacionamiento')
    estado = request.form.get('estado')
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    modificar_lugar = Usuario(estacionamiento, estado, fecha, hora)

    objeto_enviar = json.dumps(modificar_lugar.__dict__)
    datos_completos = json.loads(objeto_enviar)
    db.child("estacionamiento").child(str(idlugar)).update(datos_completos)
    return redirect(url_for('hello_world'))


#----------------------Formulario de registro de usuarios del sistema---------------------
@app.route('/altausuarios')
def altausuarios():
    return render_template("alta_usuarios_sistema.html")

#------------ruta para obtener los datos del formulario y crear el usuario-------------
@app.route('/guardarusuariosistema',methods=["POST"])
def guardarusuariosistema():
    if request.method=='POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        usuario_sistema = request.form.get('usuario')
        password = request.form.get('password')
        telefono = request.form.get('telefono')
        tipo = request.form.get('tipo')

        try:
            usuario_sistema_nuevo=UsuarioSistema(nombre,correo,usuario_sistema,password,telefono,tipo)
            objeto_enviar = json.dumps(usuario_sistema_nuevo.__dict__)
            y=json.loads(objeto_enviar)
            db.child("usuarios").push(y)
        except:
            print("error")

    return render_template("alta_usuarios_sistema.html")

if __name__ == '__main__':
    app.run(debug=True)