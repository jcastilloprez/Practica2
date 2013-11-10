#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from web import form
from web.contrib.template import render_mako
import dbm
        
urls = (
	'/', 'inicio',
	'/logout', 'logout',
	'/registro', 'registro',
	'/insercion', 'insercion',
	'/datos', 'datos',
	'/modificar', 'modificar',
	'/cambio', 'cambio',
	'/alumno', 'alumno'
)

#Para poder usar sesiones con web.py
web.config.debug = False

app = web.application(urls, globals())

session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'usuario':''})

#Templates de mako
render = render_mako(
	directories = ['templates'],
	input_encoding = 'utf-8',
	output_encoding = 'utf-8')

form_p2 = form.Form(
	form.Textbox("nick", form.notnull, description="Nick de Github"),
	form.Textbox("nombre", form.notnull, description="Nombre de alumno"),
	form.Textbox("apellidos", form.notnull, description="Apellidos del alumno"),
	form.Textbox("dni", form.notnull, form.regexp('^([0-9]{8}[A-Z])$', 'Formato de DNI incorrecto'), description="DNI del alumno"),
	form.Textbox("correo", form.notnull, form.regexp('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', 'Formato de correo electrónico incorrecto'), description="Correo electrónico"),
	form.Dropdown("dia", [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31], description="Dia de nacimiento"),
	form.Dropdown("mes", ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'], description="Mes de nacimiento"),
	form.Dropdown("anio", [1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013], description="Año de nacimiento"),
	form.Button("Mandar datos"),
	validators = [form.Validator("Fecha de nacimiento incorrecta", lambda i: (((str(i.mes) == 'febrero') and ((int(i.dia) <= 28) and ((int(i.anio) % 4) != 0) or (int(i.dia) <= 29) and ((int(i.anio) % 4) == 0))) or ((int(i.dia) <= 31) and ((str(i.mes) == 'enero') or (str(i.mes) == 'marzo') or (str(i.mes) == 'julio') or (str(i.mes) == 'agosto') or (str(i.mes) == 'octubre') or (str(i.mes) == 'diciembre'))) or ((int(i.dia) <= 30) and ((str(i.mes) == 'abril') or (str(i.mes) == 'junio') or (str(i.mes) == 'septiembre') or (str(i.mes) == 'noviembre')))))]
)

login_form = form.Form(
	form.Textbox ('usuario', form.notnull, description='Usuario: '),
	form.Password ('contrasenia', form.notnull, description='Contraseña: '),
	form.Button ('Ingresar'),
)

datos_form = form.Form(
	form.Textbox ('nombre', form.notnull, description='Nick de Github para visualizar datos de un alumno: '),
	form.Button ('Entrar'),
)

modi_form = form.Form(
	form.Textbox ('nombre', form.notnull, description='Nick de Github para modificar datos de un alumno: '),
	form.Button ('Entrar'),
)

def correct_password ():
	return 'admin'

def comprueba_identificacion ():
	usuario = session.usuario
	return usuario

class logout:
	def GET(self):
		usuario = session.usuario
		session.kill()
		return 'Adios ' + usuario

class inicio:
	def GET(self):
		usuario = comprueba_identificacion () #Comprobamos que el usuario esté identificado, sino le pedimos al usuario que se identifique
		if usuario: 
			return web.seeother('/registro')
		else:
			form = login_form()
			return render.login(form = form, usuario = usuario, mensaje = '')

	def POST(self):
		form = login_form()
		if not form.validates():
			return render.login(form = form, usuario = '', mensaje = '')

		i = web.input()
		usuario = i.usuario
		password = i.contrasenia

		if password == correct_password ():
			session.usuario = usuario
			return web.seeother('/registro')
		else:
			form = login_form()	
			return render.login(form = form, usuario = '', mensaje = 'Solamente el administrador puede acceder a esta parte')
	
class registro:
	def GET(self):
		usuario = comprueba_identificacion ()
		form = form_p2()
		if usuario:
			return render.index(form = form, usuario = usuario, mensaje = '')
		else:
			return web.seeother('/')

class insercion:
	def GET(self):
		usuario = comprueba_identificacion ()
		form = form_p2()
		return render.registro(form = form, usuario = usuario)

	def POST(self):
		usuario = comprueba_identificacion ()
		form = form_p2()
		if not form.validates():
			return render.registro(form = form, usuario = usuario)
		else:
			db = dbm.open(form.d.nick, 'c')

			db['nick'] = form.d.nick
			db['nombre'] = form.d.nombre
			db['apellidos'] = form.d.apellidos
			db['dni'] = form.d.dni
			db['correo'] = form.d.correo
			db['dia'] = form.d.dia
			db['mes'] = form.d.mes
			db['anio'] = form.d.anio

			db.close()

			return render.index(form = form, usuario = usuario, mensaje = 'Registro de alumno realizado correctamente')

class datos:
	def GET(self):
		usuario = comprueba_identificacion ()
		form = datos_form()
		return render.datos(form = form, usuario = usuario)

	def POST(self):
		usuario = comprueba_identificacion ()
		form = datos_form()

		if not form.validates():
			return render.datos(form = form, usuario = usuario)
		else:
			try:
				db = dbm.open(form.d.nombre, 'r')

				nick = db['nick']
				nombre = db['nombre']
				apellidos = db['apellidos']
				dni = db['dni']
				correo = db['correo']
				dia = db['dia']
				mes = db['mes']
				anio = db['anio']
				nacimiento = dia + '/' + mes + '/' + anio

				db.close()

				return render.visualizar(form = form, usuario = usuario, nick = nick, nombre = nombre, apellidos = apellidos, dni = dni, correo = correo, nacimiento = nacimiento)
			except:
				return render.index(form = form, usuario = usuario, mensaje = 'Nick de Github de alumno no existente en la base de datos')

class alumno: 
	def GET(self):
		usuario = comprueba_identificacion ()
		form = datos_form()
		formi = login_form()
		return render.alumno(form = form, usuario = usuario, formi = formi)

	def POST(self):
		usuario = comprueba_identificacion ()
		form = datos_form()
		formi = login_form()

		if not form.validates():
			return render.alumno(form = form, usuario = usuario, formi = formi)
		else:
			try:
				db = dbm.open(form.d.nombre, 'r')

				nick = db['nick']
				nombre = db['nombre']
				apellidos = db['apellidos']
				dni = db['dni']
				correo = db['correo']
				dia = db['dia']
				mes = db['mes']
				anio = db['anio']
				nacimiento = dia + '/' + mes + '/' + anio

				db.close()

				return render.visu(formi = formi, usuario = usuario, nick = nick, nombre = nombre, apellidos = apellidos, dni = dni, correo = correo, nacimiento = nacimiento)
			except:
				return render.inicio(formi = formi, usuario = usuario, mensaje = 'Nick de Github de alumno no existente en la base de datos')

class modificar:
	def GET(self):
		usuario = comprueba_identificacion ()
		form = modi_form()
		return render.modificar(form = form, usuario = usuario)

	def POST(self):
		usuario = comprueba_identificacion ()
		form = modi_form()	
		formi = form_p2()

		if not form.validates():
			return render.modificar(form = form, usuario = usuario)	
		else:
			try:
				db = dbm.open(form.d.nombre, 'r')

				nick = db['nick']
				nombre = db['nombre']
				apellidos = db['apellidos']
				dni = db['dni']
				correo = db['correo']
				dia = db['dia']
				mes = db['mes']
				anio = db['anio']
	
				formi.nick.value = nick
				formi.nombre.value = nombre
				formi.apellidos.value = apellidos
				formi.dni.value = dni
				formi.correo.value = correo
				formi.dia.value = int(dia)
				formi.mes.value = mes
				formi.anio.value = int(anio)	

				db.close()

				return render.modi(formi = formi, usuario = usuario)
			except:
				return render.index(form = form, usuario = usuario, mensaje = 'Nick de Github de alumno no existente en la base de datos')
		
class cambio:
	def POST(self):
		usuario = comprueba_identificacion ()
		form = form_p2()
		if not form.validates():
			return render.modi(form = form, usuario = usuario)
		else:
			db = dbm.open(form.d.nick, 'w')

			db['nick'] = form.d.nick
			db['nombre'] = form.d.nombre
			db['apellidos'] = form.d.apellidos
			db['dni'] = form.d.dni
			db['correo'] = form.d.correo
			db['dia'] = form.d.dia
			db['mes'] = form.d.mes
			db['anio'] = form.d.anio

			db.close()

			return render.index(form = form, usuario = usuario, mensaje = 'Registro de alumno realizado correctamente')

if __name__ == "__main__":
    app.run()
