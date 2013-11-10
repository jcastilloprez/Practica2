Práctica 2: Aislamiento de una aplicación web usando una jaula chroot
=========
**Crear una mini-aplicación web (un hola mundo o un simple formulario) y aislarlo en una jaula chroot.**

## Objetivo

El principal objetivo que nos pide esta práctica es familiarizarnos con la creación, configuración y manejo de jaulas chroot, para restringir a los usuarios a ciertas aplicaciones o autorizar el acceso de una aplicación a cierto usuario.

## Introducción 

Voy a crear una pequeña aplicación web en Python que va a consistir en una pequeña página web en donde podemos visualizar todos los datos previamente guardados insertando nuestro nick de GitHub. Ahora bien, si somos el administrador del sistema podremos además insertar nuevos alumnos y modificar sus datos.
Dicha aplicación va a estar alojada en una jaula de un sistema debianita y el acceso a dicha jaula sólo va a estar permitido a un usuario que vamos a crear y al usuario root. 

## Documentación 

Para la creación de la jaula voy a utilizar la herramienta “debootstrap”, tal y como vimos en el ejercicio 3 de este tema. El sistema operativo que voy a instalar en dicha jaula es la última versión estable del sistema debianita “Wheezy”.  

Como la herramienta debootstrap ya la tenemos instalada de un ejercicio de este tema nos saltamos el paso de instalar dicha herramienta. Si dicha herramienta no estuviera instalada, su instalación es tan fácil como acceder a la consola e instalarla con: `sudo apt-get install debootstrap` 

El siguiente paso es instalar el sistema operativo e aislarlo en la jaula con la orden: 

`sudo debootstrap --arch=i386 wheezy /seguro/jaulas/p2 http://ftp.us.debian.org/debian`

Una vez que termine el proceso de instalación, para probar que el sistema operativo mínimo se ha instalado correctamente accedemos con la herramienta chroot a dicha jaula y vemos que está todo completo. 

![Práctica 2 - Foto 1](http://ubuntuone.com/2hAhuBAGmpy7FPtPSgk1ZE)

Ahora voy a crear un usuario y configurar la jaula para que sólo el usuario creado y “root” puedan acceder a la jaula. El usuario se crea con “adduser” y el proceso de su creación lo podemos ver a continuación: 

![Práctica 2 - Foto 2](http://ubuntuone.com/5vdhb5hhpVoBPFBcOQTfDV)

Para configurar la jaula voy a hacer uso de la herramienta “schroot”, que como no la tengo instalada en mi sistema lo instalo con: `sudo apt-get install schroot`

A continuación, configuramos el acceso a dicha jaula  para que sólo por parte del usuario creado anteriormente y “root” puedan acceder a ella, para ello, creamos el fichero de configuración de schroot que se va a encontrar en “/etc/schroot/chroot.d/wheezy.conf” y lo rellenamos tal y como se muestra a continuación: 

![Práctica 2 - Foto 3](http://ubuntuone.com/7CtMukLsvrBvMEBsZlsuLl)

Para probar que podemos acceder a dicha jaula con dicho usuario hacemos lo siguiente:

![Práctica 2 - Foto 4](http://ubuntuone.com/32SzeDr3mfpBZp4uA7KCC0)

El siguiente paso es instalar los paquetes necesarios y configurar la jaula para que pueda servir páginas web realizadas con python, ya que mi aplicación web va a estar realizada en dicho lenguaje. Para ello accedemos a la jaula con: `sudo chroot /seguro/jaulas/p2` y la configuramos un poco montando los sistemas de ficheros proc y devpts: 

> ```
> mount -t proc proc /proc
> mount devpts /dev/pts -t devpts
> ```

Una vez montados dichos sistemas, procedemos a la instalación de todos los paquetes que vamos a necesitar para arrancar nuestra aplicación de python: 

> ```
> apt-get install python
> apt-get install python-web2py
> apt-get install python-mako
> ```

A la hora de la instalación del paquete “python-web2py” me salta un error de que el paquete no funciona perfectamente. Para solucionar este error lo que he realizado ha sido bajarme dicho paquete de los repositorios de GitHub e instalarlo de dicho repositorio. Las ordenes para dicho proceso son las siguientes:

> ```
> apt-get install git
> git clone git://github.com/webpy/webpy.git
> cd webpy/
> python setup.py install
> ```

Una vez realizado lo anterior ya no nos da ningún error y ya funciona el paquete perfectamente. Solamente queda copiar la aplicación de nuestra máquina anfitriona a la jaula, para ello utilizamos la siguiente orden:

`sudo cp -r ./p2-iv/ /seguro/jaulas/p2/home/`

Una vez copiada la aplicación en la jaula sólo queda lanzarla en ejecución. Para ello accedemos al directorio en donde la hemos copiado y la lanzamos con la siguiente orden: `python p2-iv.py 6666`
Muy importante indicarle un puerto distinto al puerto 8080, ya que en mi caso el puerto 8080 ya lo tengo ocupado con el servidor Apache y si no le indico un número de puerto la aplicación no se lanza. 

![Práctica 2 - Foto 5](http://ubuntuone.com/6pBhpVYXTjzt0eiwEVXDGi)

Una vez lanzada la aplicación, nos vamos a un navegador web e insertamos la url que no acaba de dar el lanzamiento de la aplicación, que en mi caso es http://0.0.0.0:6666/ y nos mostrará la página de inicio de mi aplicación.

![Práctica 2 -  Foto 6](http://ubuntuone.com/24mjCCdB78HiIi6CjBWHmF)

Si no somos los administradores de la página lo único que nos permite la aplicación es visualizar los datos de los alumnos, insertando el nick de GitHub.

![Práctica 2 - Foto 7](http://ubuntuone.com/68f1Iq8knY7zv4N163SvEZ)

Una vez que insertemos el nick nos aparecerá todos los datos guardados correspondientes a dicho alumno. 

![Práctica 2 - Foto 8](http://ubuntuone.com/7F3OHqs9Hi5y6NjDFjwmIS)

Ahora bien si somos el administrador del sistema, el diseño de la página se ve alterado un poco y nos da también las opciones de insertar un nuevo alumno o de modificar los datos de un alumno. 

![Práctica 2 - Foto 9](http://ubuntuone.com/6Bca8sqnwuYLcS8nSiwfsp)

Si deseamos registrar un nuevo alumno, lo único que tiene que hacer el administrador es rellenar el formulario que muestra la página y guardar sus datos. Estos datos se van guardando en ficheros en el sistema, teniendo un fichero cada alumno con el nombre de su nick de GitHub.

![Práctica 2 - Foto 10](http://ubuntuone.com/6y9b0iwu9JF0SJPPuESde5)

Si por el contrario, lo que queremos es que el administrador modifique los datos de un alumno, lo que tiene que hacer es insertar el nick de GitHub de dicho alumno

![Práctica 2 - Foto 11](http://ubuntuone.com/3d9a4NtM9UhPLB7PaXKBjn)

y modificar el formulario que aparece relleno con los datos de dicho alumno.

![Práctica 2 - Foto 12](http://ubuntuone.com/6lIokFhZycK4wej0grcjpX)

Si volvemos a visualizar los datos de dicho alumno podemos apreciar que los cambios han sido aceptados.

![Práctica 2 - Foto 13](http://ubuntuone.com/4CaviafA7x4q82a3j5ZKDV)
