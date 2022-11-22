
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Hermosa10111'
app.config['MYSQL_DB'] = 'qicdatabase'
mysql = MySQL(app) #creo conexion

#settings
app.secret_key = 'msk'

if __name__ == '__main__':
    app.run(port = 3000, debug = True)


########## PANTALLA DE INICIO ##########

@app.route('/inicio')#PANTALLA DE INICIO DE LA PAGINA
def Inicio(): 
    return render_template('inicio.html')

########## fin PANTALLA DE INICIO ##########



########## PANTALLA DE CLIENTES ##########

@app.route('/clientes') # PANTALLA DE CLIENTES
def Clientes():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM clientes')
    datos = cursor.fetchall() #traer todos los datos en una variable
    return render_template('cliente.html', clientes = datos)

@app.route('/agregar_cliente', methods=['POST']) # PANTALLA DE ADICIÓN DE CLIENTE
def crearCliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO clientes (nombre, apellido, telefono, email) VALUES(%s, %s, %s, %s)', (nombre, apellido, telefono, email))
        mysql.connection.commit() #ejecuta la consulta
        flash('Cliente agregado correctamente!')
        return redirect(url_for('Clientes'))

@app.route('/editar_cliente/<id>', methods=['POST', 'GET']) # PANTALLA DE EDICIÓN DE CLIENTE
def editarCliente(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM clientes WHERE id_cliente = %s', [id])
    datos = cursor.fetchall()
    return render_template('editar_cliente.html', cliente=datos[0])

@app.route('/modificar_cliente/<id>', methods = ['POST']) # ENVÍO FORMULARIO DE EDICIÓN DE CLIENTE
def modificarClientes(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE clientes
        SET nombre = %s,
            apellido = %s,
            telefono = %s,
            email = %s
        WHERE id_cliente = %s
    """, (nombre, apellido, telefono, email, id))
    mysql.connection.commit()
    flash('Cliente actualizado correctamente!')
    return redirect(url_for('Clientes'))

@app.route('/borrar_cliente/<string:id>') # ELIMINO CLIENTE
def borrarCliente(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Cliente removido correctamente!')
    return redirect(url_for('Clientes'))

########## fin PANTALLA DE CLIENTES ##########



########## PANTALLA DE EMPLEADOS ##########

@app.route('/empleados') # PANTALLA DE EMPLEADOS
def Empleados():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM empleados')
    datos = cursor.fetchall()
    return render_template('empleados.html', empleados = datos)

@app.route('/nuevo_empleado') # PANTALLA DE ADICION DE EMPLEADO
def nuevoEmpleado():
    return render_template('nuevo_empleado.html')

@app.route('/agregar_empleado', methods=['POST']) # ENVIO FORMULACIO DE ADICION DE EMPLEADO
def crearEmpleado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        direccion = request.form['direccion']
        rol = request.form['rol']
        cuit = request.form['cuit']
        cuil = request.form['cuil']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO empleados (nombre, apellido, telefono, email, direccion, rol, cuit, cuil) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', (nombre, apellido, telefono, email, direccion, rol, cuit, cuil))
        mysql.connection.commit()
        flash('Empleado agregado correctamente!')
        return redirect(url_for('Empleados'))

@app.route('/editar_empleado/<id>', methods=['POST', 'GET']) # PANTALLA DE EDICION DE EMPLEADO
def editarEmpleado(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM empleados WHERE id_empleado = %s', [id])
    datos = cursor.fetchall()
    return render_template('editar_empleado.html', empleado=datos[0])

@app.route('/modificar_empleado/<id>', methods = ['POST']) # ENVIO FORMULARIO DE EDICION DE EMPLEADO
def modificarEmpleados(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        direccion = request.form['direccion']
        cuit = request.form['cuit']
        cuil = request.form['cuil']
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE empleados
        SET nombre = %s,
            apellido = %s,
            telefono = %s,
            email = %s,
            direccion = %s,
            cuit = %s,
            cuil = %s
        WHERE id_empleado = %s
    """, (nombre, apellido, telefono, email, direccion, cuit, cuil, id))
    mysql.connection.commit()
    flash('Empleado actualizado correctamente!')
    return redirect(url_for('Empleados'))

@app.route('/borrar_empleados/<string:id>') # ELIMINO EMPLEADO
def borrarEmpleado(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM empleados WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Empleado removido correctamente!')
    return redirect(url_for('Empleados'))

########## fin PANTALLA DE EMPLEADOS ##########


########## PANTALLA DE MESAS ##########

@app.route('/mesas')#PANTALLA DE MESAS
def Mesas():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM mesas')
    datos = cursor.fetchall() #traer todos los datos en una variable
    cursor.execute('SELECT * FROM servicios')
    servicios = cursor.fetchall()
    compararFechas()
    return render_template('mesas.html', mesas = datos, servicios = servicios)

def compararFechas(): # COMPARA FECHAS PARA DAR AVISOS DE RESERVAS PROXIMAS
    hora = datetime.now()    
    hora_ahora = hora.strftime("%H:%M")
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT servicios.id_servicio, servicios.fecha, servicios.hora_inicio, mesas.estado
                FROM mesas
                RIGHT JOIN servicios
                ON mesas.id_mesa = servicios.id_mesa
                WHERE servicios.tipo_servicio = "reserva" """)
    horarios = cursor.fetchall()
    halfhour_from_now = datetime.now() - timedelta(hours=0.5)
    hora_previa = halfhour_from_now.strftime("%H:%M") #21:20
    fiveminutes_from_now = datetime.now() - timedelta(minutes=5)
    min_previo = fiveminutes_from_now.strftime("%H:%M")
    contador = 0
    for x in horarios:
        prueba2 = horarios[contador][2]
        dt_tuple=tuple([int(x) for x in prueba2.split(':')])
        print(dt_tuple)
        print("HORARIO STRP: ",  prueba2)
        mesa = str(horarios[contador][2])
        if horarios[contador][2] >= min_previo and horarios[contador][2] <= hora_ahora and horarios[contador][3]=="ocupado":
            mensaje = "Reserva disponible: Se debera liberar la mesa " + mesa + " en menos de 5 minutos"
            flash(mensaje)
            
        if horarios[contador][2] >= hora_previa and horarios[contador][2] <= hora_ahora:
            mensaje = "La mesa " + mesa + " recibira una reserva en menos de media hora"
            flash(mensaje)
        else:
            print("no se encontro ninguna reserva proxima")
        contador+=1
    
@app.route('/agregar_mesa', methods=['POST']) # POP UP ENVIO FORMULARIO DE ADICION DE MESA 
def crearMesa():
    if request.method == 'POST':
        id_mesa = request.form['id_mesa']
        estado = request.form['estado']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO mesas (id_mesa, estado) VALUES(%s, %s)', [id_mesa, estado])
        mysql.connection.commit() #ejecuta la consulta
        flash('Mesa agregada correctamente!')
        return redirect(url_for('Mesas'))

@app.route('/borrar_mesa', methods=['POST']) # POP UP ELIMINO MESA 
def borrarMesa():
    if request.method == 'POST':
        id = request.form['id_mesa']
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM mesas WHERE id_mesa = %s', [id])
    mysql.connection.commit()
    flash('Mesa removida correctamente!')
    return redirect(url_for('Mesas'))

@app.route('/cambiar_estado_mesa/', methods = ['POST']) # POP UP CAMBIO ESTADO DE LA MESA
def modificarEstadoMesa():
    if request.method == 'POST':
        id = request.form['id_mesa']
        estado = request.form['estado']
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE mesas
        SET estado = %s
        WHERE id_mesa = %s
    """, (estado, id))
    mysql.connection.commit()
    flash('Estado de mesa modificado correctamente!')
    return redirect(url_for('Mesas'))

@app.route('/nuevo_servicio') # PANTALLA DE CREACION DE SERVICIO DE MESA / ASIGNACION DE MESA
def Servicio():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM mesas')
    datos = cursor.fetchall() #traer todos los datos en una variable
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    cursor.execute('SELECT * FROM servicios')
    servicios = cursor.fetchall()
    cursor.execute('SELECT * FROM mesas where estado = "disponible"')
    disponibles = cursor.fetchall()
    return render_template('nuevo_servicio.html', mesas = datos, clientes = clientes, disponibles = disponibles, servicios = servicios)

@app.route('/crear_servicio', methods = ['POST']) # ASIGNO MESA / ENVIO FORMULARIO DE SERVICIO DE MESA
def asignarMesa():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        id_mesa = request.form['id_mesa']
        grupo = request.form['tamano_grupo']
        senia = request.form['senia']
        estado = request.form['estado']

        if (estado == "option1"):
            estado = "disponible"
        elif (estado == "option2"):
            estado = "ocupado"
        elif(estado =="option3"): 
            estado = "no disponible"
 
        hora = datetime.now()
        hora_inicio = hora.strftime("%H:%M")
        fecha = hora.strftime("%d-%m-%Y")
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO servicios
            SET id_cliente = %s,
                id_mesa = %s,
                tipo_servicio = "mesa",
                tamano_grupo = %s,
                senia = %s,
                hora_inicio = %s,
                fecha = %s
        """, (id_cliente, id_mesa, grupo, senia, hora_inicio, fecha))
    
        cursor = mysql.connection.cursor()
        cursor.execute("""
        UPDATE mesas 
            SET estado = %s,
            senia = %s,
            id_cliente = %s
            WHERE id_mesa = %s
            """,(estado, senia, id_cliente, id_mesa))
        
    mysql.connection.commit()
    flash('Servicio creado correctamente!')
    return redirect(url_for('Mesas'))
    
@app.route('/ver_mesa/<id_mesa>', methods = ['GET']) # PANTALLA DE VISUALIZACION DE DATOS DE SERVICIO DE MESA
def verMesa(id_mesa):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM mesas WHERE id_mesa = %s', [id_mesa])
        mesa = cursor.fetchall() 
        cursor.execute('SELECT * FROM servicios WHERE id_mesa = %s AND tipo_servicio = "mesa" ', [id_mesa])
        servicio = cursor.fetchall()
        return render_template('ver_mesa.html', mesa = mesa[0], servicio = servicio[0])
            
@app.route('/editar_mesa/<id>', methods = ['POST', 'GET']) # PANTALLA DE EDICION DE DATOS DE SERVICIO DE MESA
def editarMesa(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM mesas WHERE id_mesa = %s', [id])
    datos = cursor.fetchall() 
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    cursor.execute('SELECT * FROM servicios WHERE id_mesa = %s', [id])
    servicio = cursor.fetchall()
    cursor.execute('SELECT * FROM mesas where estado = "disponible"')
    disponibles = cursor.fetchall()
    return render_template('editar_mesa.html', mesa = datos[0], servicio = servicio[0], clientes = clientes, disponibles = disponibles )

@app.route('/modificar_mesa/<id>', methods = ['POST']) # ENVIO DATOS DE FORMULARIO DE EDICION DE SERVICIO DE MESA
def modificarMesa(id):
    if request.method == 'POST':
        id_mesa = request.form['id_mesa']
        id_cliente = request.form['id_cliente']
        grupo = request.form['tamano_grupo']
        senia = request.form['senia']
        hora_inicio = request.form['hora_inicio']
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE servicios
        SET id_cliente = %s,
            id_mesa = %s,
            tamano_grupo = %s,
            senia = %s,
            hora_inicio = %s
        WHERE id_servicio = %s
    """, (id_cliente, id_mesa, grupo, senia, hora_inicio, id))

    cursor.execute("""
        UPDATE mesas
        SET senia = %s,
            id_cliente = %s
        WHERE id_mesa = %s
    """, (senia, id_cliente, id_mesa))
    
    mysql.connection.commit()
    flash('Servicio actualizado correctamente!')
    return redirect(url_for('Mesas'))

@app.route('/terminar_servicio/<id_mesa> <id_cliente>', methods = ['GET','POST']) # TERMINO SERVICIO DE MESA, BORRO DATOS DE SERVICIO Y LOS ENVIO A ARCHIVO
def terminarServicio(id_mesa, id_cliente):
    hora_fin = datetime.now().strftime("%H:%M")
    cursor = mysql.connection.cursor()
    cursor.execute(""" 
        SELECT id_servicio FROM servicios WHERE id_mesa = %s AND id_cliente = %s AND tipo_servicio = 'mesa'  
    """, (id_mesa, id_cliente))
    id_servicioR = cursor.fetchone()
    id_servicio = str(id_servicioR)
    characters = "(','`)"
    id_servicio = ''.join(x for x in id_servicio if x not in characters)

    cursor.execute(""" 
    UPDATE servicios
        SET hora_fin = %s
        WHERE id_servicio = %s
    """, (hora_fin, id_servicio))
    
    cursor.execute(""" 
    INSERT INTO archivo_servicios
        SELECT * FROM servicios 
        WHERE id_servicio = %s
    """, [id_servicio])
    
    cursor.execute("""
        DELETE FROM `qicdatabase`.`servicios` WHERE (`id_servicio` = %s);
    """, [id_servicio])

    cursor.execute(""" 
    UPDATE mesas
        SET estado = 'disponible',
        senia = Null,
        id_cliente = Null
        WHERE id_mesa = %s
    """, [id_mesa])
    mysql.connection.commit()
    flash('Servicio finalizado correctamente!')
    return redirect(url_for('Mesas'))

########## fin PANTALLA DE MESAS ##########



########## PANTALLA DE RESERVAS ##########

@app.route('/reservas') # PANTALLA DE RESERVAS
def Reservas():
    fecha = datetime.now().strftime("%d-%m-%Y")
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT clientes.nombre, clientes.apellido, servicios.*
                FROM clientes
                RIGHT JOIN servicios
                ON clientes.id_cliente = servicios.id_cliente
                WHERE tipo_servicio = "reserva" 
                """)
    tser = cursor.fetchall()
    cursor.execute("""SELECT clientes.nombre, clientes.apellido, servicios.*
                FROM clientes
                RIGHT JOIN servicios
                ON clientes.id_cliente = servicios.id_cliente
                WHERE tipo_servicio = "reserva" AND fecha =%s
                """, [fecha])
    ser = cursor.fetchall()
    return render_template('reservas.html', todas = tser, servicios = ser)

@app.route('/nueva_reserva') # PANTALLA DE CREACIÓN DE RESERVA
def nuevaReserva():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM servicios')
    res = cursor.fetchall()
    cursor.execute('SELECT * FROM clientes')
    cli = cursor.fetchall()
    cursor.execute('SELECT * FROM mesas')
    mes = cursor.fetchall() 
    return render_template('nueva_reserva.html', reservas = res, clientes = cli, mesas = mes)

@app.route('/crear_reserva', methods = ['POST']) # ENVÍO FORMULARIO DE CREACIÓN DE RESERVA 
def crearReserva():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        id_mesa = request.form['id_mesa']
        grupo = request.form['tamano_grupo']
        senia = request.form['senia']
        hora_inicio = request.form['hora_inicio']
        fecha = request.form['fecha']
        fecha = datetime.strptime(fecha, '%Y-%m-%d').strftime('%d-%m-%Y')
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO servicios
            SET id_cliente = %s,
                id_mesa = %s,
                tipo_servicio = "reserva",
                tamano_grupo = %s,
                senia = %s,
                hora_inicio = %s,
                fecha = %s
        """, (id_cliente, id_mesa, grupo, senia, hora_inicio, fecha))    
        print(fecha)
    mysql.connection.commit()
    flash('Servicio creado correctamente!')
    return redirect(url_for('Reservas'))

@app.route('/ver_reserva/<id>', methods = ['GET']) # PANTALLA DE VISUALIZACIÓN DE DATOS DE RESERVA
def verReserva(id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM servicios WHERE id_servicio = %s', [id])
        servicio = cursor.fetchall()
        return render_template('ver_reserva.html', servicio = servicio[0])

@app.route('/editar_reserva/<id>', methods = ['POST', 'GET']) # PANTALLA DE EDICIÓN DE RESERVA
def editarReserva(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM servicios WHERE id_servicio = %s', [id])
    datos = cursor.fetchall()
    cursor.execute('SELECT id_mesa FROM mesas')
    mesas = cursor.fetchall()
    cursor.execute('SELECT id_cliente FROM clientes')
    clientes = cursor.fetchall()
    return render_template('editar_reserva.html', servicio = datos[0], clientes = clientes, mesas = mesas )

@app.route('/modificar_reserva/<id>', methods = ['POST']) # ENVIO FORMULARIO DE EDICIÓN DE RESERVA
def modificarReserva(id):
    if request.method == 'POST':
        id_mesa = request.form['id_mesa']
        id_cliente = request.form['id_cliente']
        grupo = request.form['tamano_grupo']
        senia = request.form['senia']
        hora_inicio = request.form['hora_inicio']
        fecha = request.form['fecha']
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE servicios
        SET id_cliente = %s,
            id_mesa = %s,
            tamano_grupo = %s,
            senia = %s,
            hora_inicio = %s,
            fecha = %s
        WHERE id_servicio = %s
    """, (id_cliente, id_mesa, grupo, senia, hora_inicio, fecha, id))
    mysql.connection.commit()
    flash('Reserva actualizada correctamente!')
    return redirect(url_for('Reservas'))

@app.route('/borrar_reserva/<id>', methods=['GET','POST']) # ELIMINO RESERVA
def borrarReserva(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM servicios WHERE id_servicio = %s', [id])
    mysql.connection.commit()
    flash('Reserva removida correctamente!')
    return redirect(url_for('Reservas'))

@app.route('/iniciar_reserva/<id_servicio>', methods=['GET','POST']) # VERIFICO ESTADO DE MESA EN MODULO MESAS Y ACTUALIZO EL SERVICIO DE RESERVA A MESA
def iniciarReserva(id_servicio):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id_mesa FROM servicios WHERE id_servicio = %s', [id_servicio])
    id_mesa = cursor.fetchone()
    cursor.execute('SELECT estado FROM mesas WHERE id_mesa = %s', [id_mesa])
    estado = cursor.fetchone()
    cursor.execute('SELECT senia, id_cliente FROM servicios WHERE id_servicio = %s', [id_servicio])
    datos = cursor.fetchall()
    print(datos)
    characters = "(','`)"
    id_mesa=str(id_mesa)
    id_mesa= ''.join(x for x in id_mesa if x not in characters)
    estado = ''.join(x for x in estado if x not in characters)
    if (estado == "ocupado"):
        flash("Debe desocupar la mesa de la reserva antes de poder iniciar el servicio")
    elif(estado =="no disponible"):
        flash("La mesa seleccionada no se encuentra disponible actualmente. Seleccionar otra.")
    elif(estado =="disponible"):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE servicios
            SET tipo_servicio = "mesa"
            WHERE id_servicio = %s
            """, [id_servicio])
        cursor.execute("""
        UPDATE mesas
        SET estado = "ocupado"
            senia = %s,
            id_cliente = %s
        WHERE id_mesa = %s
        """, (datos[0],datos[1],id_mesa))
        mysql.connection.commit()
        flash('Reserva iniciada correctamente!')
    return redirect(url_for('Reservas'))

########## fin PANTALLA DE RESERVAS ##########



########## PANTALLA DE ARCHIVOS ##########

@app.route('/archivos') #PANTALLA DE ARCHIVOS
def Archivos():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM archivo_servicios')
    datos = cursor.fetchall() 
    return render_template('archivos.html', servicios = datos)

########## fin PANTALLA DE ARCHIVOS ##########



### PANTALLA INICIO DE SESION 
"""@app.route('/inicio_sesion')
def InicioSesion():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM login')
    datos = cursor.fetchall() #traer todos los datos en una variable
    return render_template('login.html', datos = datos)


@app.route('/iniciar_sesion')
def VerificarSesion():
    if request.method == 'POST':
        user = request.form['usuario']
        contrasenia = request.form['contrasenia']
        rol = request.form['rol']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM login WHERE usuario == %s and pass = %s and rol == %s', (user, contrasenia, rol))
    datos = cursor.fetchall() #traer todos los datos en una variable
    if (datos == 1):
        if (rol == "usuario"):
            return render_template('pag_usuario.html')
        elif(rol == "admin"):
            return render_template('pag_admin.html')
    else:
        flash('Usuario o contraseña incorrecto.')
"""
    



