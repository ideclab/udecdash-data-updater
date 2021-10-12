# UDECDash Data Updater
UDECDash Data Updater es un componente de UDECDash, visite la wiki del repositorio para encontrar más información sobre este y otros componentes.

## Requisitos
- Python 3.9
- Supervisord 4.2
- Nodejs 14.0 a v16.0
- [Canvas Data Cli](https://github.com/instructure/canvas-data-cli "Canvas Data Cli")

## Instalación

1) Descarga el proyecto

`git clone https://github.com/xxxxx/interactive_dashboard_backend/`

2) Instala las dependencias

`pip install -r requirements.txt`

4) Compila el paquete 

`python setup.py sdist`

5) Ve a la carpera **/dist** e instala el paquete.

`pip3 install NOMBRE_DEL_ARCHIVO.tar.gz`

6) Crea un script para configurar y ejecutar la actualización de datos, puedes utilizar el fichero **main_example.py** como plantilla.

7) Envuelve el script del paso 6 en una tarea programada o cron job para automatizar el lanzamiento. Se recomienda un intervalo de 24 horas entre cada actualización.

8) Configura supervisord para ejecutar las colas de trabajo que pertenecen a IDECDash Backend, en la carpeta supervisord_config encontrarás una configuración de ejemplo.

[Ir a la documentación de Supervisord](http://supervisord.org/ "Canvas Data Cli")

**Observación:** Al agregar la configuración de supervisord no olvides modificar lo siguiente:
````
directory= PATH_TO_UDECDASH_BACKEND
stderr_logfile=PATH_TO_LOG/log_name.err.log
stdout_logfile=PATH_TO_LOG/log_name.out.log
````
*Los archivos para almacenar los log deben ser creados manualmente, tambien puedes eliminar las lineas de los logs si no deseas guardarlos.*


## Configuración
El paquete se encargará de hacer todo lo necesario para actualizar y cargar los datos, sin embargo, este debe ser llamado de algún lado. Para poder ejecutar el paquete puedes guiarte por el archivo de plantilla llamado **main_example.py**, a continuación se detallan de forma general las variables de entorno que se deben establecer.

***

Conexión a la base de datos postgresql
````
os.environ['DB_HOST'] = '127.0.0.1'
os.environ['DB_PORT'] = '5432'
os.environ['DB_NAME'] = ''
os.environ['DB_USERNAME'] = ''
os.environ['DB_PASSWORD'] = ''
````

***

Ruta al directorio data files del script Canvas Data Cli
````
os.environ['PATH_DATA_FILES'] = ''
````

***

Ruta del directorio donde se encuentra el archivo config.js que pertenece a Canvas Data Cli
````
os.environ['PATH_CANVAS_CONFIG'] = ''
````

***

Caracter concatenador de rutas que utiliza tu sistema operativo  

````
os.environ['PATH_CONCAT'] = '/'
````

***

Configuración del SMTP

**Observación:** El SMTP es utilizado para notificar administradores en caso que el proceso de actualización falle en el proceso.

````
os.environ['SMTP_USER']= ''
os.environ['SMTP_PASS']= ''
os.environ['SMTP_HOST']= ''
os.environ['SMTP_PORT']= ''
````

***

Emails de administradores que recibirán notificaciones de fallo

````
mails = ['example@example.cl']
os.environ['NOTIFICATION_EMAILS'] = os.pathsep.join(mails)
````

***

Gestionar la carga inicial. Si es true (Primera carga) no comprobará los archivos requests con los anteriores antes de insertar los nuevos, se recomienda cambiarlo a false luego de ejecutar la carga inicial y una primera actualización.
Cuando es ````False```` validará los nuevos requests con los cargados en la carga anterior -valga la redundancia- para prevenir la inserción de duplicados.

**Observación:** Aunque se inserten requests duplicados, al procesarse las interacciones no se insertarán actividades duplicadas debido a que están protegidas por una clave primaria mixta unica, por lo cual, considere esto como un segundo factor de protección.

````
os.environ['FIRST_DATA_UPDATE']= 'True'
````

***

Eliminar los archivos descargados (exceptuando requests) en la actualización de datos.

**Observación:** Durante el proceso notamos que canvas data cli hace un mal corte de registros por archivo, duplicando algunos registros que posteriormente dan excepciones en la carga automatica debido a claves unicas. Si se establece en True la siguiente propiedad se eliminarán todos los archivos y se descargarán nuevamente para asegurar así la carga unica de registros.

````
os.environ['CLEAR_DIRECTORIES_BEFORE_DOWNLOAD']= 'False'
````

***

Activa o no la descarga de nuevos archivos.

````
os.environ['ENABLE_DOWNLOAD']= 'False'
````

***

Recupera desde los archivos descargados con Canvas Data Cli solo los que poseen la extensión definida. 
os.environ['FILE_EXTENSION']='gz'

***

La contraseña del usuario que ejecutará el paquete. Esta es utilizada para detener / reanudar las instancias de supervisord.

````
os.environ['SERVER_SUDO_PASSWORD']= ''
````


***

Ruta absoluta al comando de supervisord para poder ser lanzado desde un crontab.

````
os.environ['SERVER_SUPERVISORD_COMMAND_PATH']= '/usr/bin/supervisorctl'
````

***

Ruta absoluta al comando de canvasDataCli para poder ser lanzado desde un crontab.

````
os.environ['SERVER_CANVAS_DATA_CLI_COMMAND_PATH']= '/usr/local/bin/canvasDataCli'
````


***

Ruta absoluta al directorio de UDECDash fronted. Esto permite renombrar el index para dejar el sitio en un estado de "Carga de datos".

````
os.environ['FRONTEND_DIR']= ''
````

