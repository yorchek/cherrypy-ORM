# -*- coding: utf-8 -*-
import hashlib, os
from sqlalchemy import *
from info import get_database_url

# podemos utilizar variables de entorno
try:
    url = os.environ["DATABASE_URL2"]
except KeyError: 
    # url de acceso a la base de datos
    url = get_database_url()
    # url = "postgresql+psycopg2://vomwiwzrwzmzkr:9No_s99GgPAjTg9mADFHh5Jz4A"
    # url += "@ec2-54-204-12-25.compute-1.amazonaws.com:5432/d417r6qvguin8v"

db = create_engine(url,
    connect_args={'client_encoding': 'utf8'})
db.echo = False  # Try changing this to True and see what happens
# asignamos al atributo metadata para poner por default la base de datos
metadata = MetaData(db)

# si usamos SQLite3
# db = create_engine('sqlite:///db/ruidodb.db')
# db.echo = False  # Try changing this to True and see what happens
# metadata = MetaData(db)

# en esta sección irán todas las migraciones
users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(40), nullable=False, unique=True),
    Column('name', String(50)),
    Column('password', String, nullable=False)
)

posts = Table('posts', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('name', String(50), nullable=False),
    UniqueConstraint('name', 'user_id')
)

# hacemos las migraciones
# create_all() migra las tablas aun no creadas
def migrate():
    """se hacen las migraciones de las tablas no creadas"""
    try:
        metadata.create_all()
        print "se hicieron las migraciones"
    except Exception, e:
        # evitamos que se "rompa" la ejecución del servidor
        # imprimimos si hay un error
        print e

# si queremos borrar todas las tablas
def drop():
    """Borramos toda las tablas"""
    try:
        metadata.drop_all()
        print "se borraron las tablas"
    except Exception, e:
        print e

# si queremos reiniciar la base de datos
# solo se crean las tablas
def reset():
    """Creamos de nuevo las tablas"""
    try:
        metadata.drop_all()
        metadata.create_all()
        print "se reinicio la base de datos"
        seeds()
    except Exception, e:
        print e

# define métodos auxiliares si hay modificaciones a los argumentos de alguna tabla
def passw(value):
    """Modificamos el valor de las contraseñas"""
    passhash = hashlib.sha1(value)
    return passhash.hexdigest()

# método que ingresa a la base de datos algunos elementos que son por default
def seeds():
    i = users.insert()
    i.execute(email='kuberjorg3n@hotmail.com' ,name='Yorche Chory', password=passw( 'punkrocker' ))
    # abrimos el acceso a la tabla con el método que utilizaremos

    # users.insert()

    # si solo es un elemento

    # i.execute(email='mary@example.com' ,name='Mary', password=passw( 'secret' ))

    # si son varios

    # i.execute({'name': 'John', 'age': 42},
    #     {'name': 'Susan', 'age': 57},
    #     {'name': 'Carl', 'age': 33})
    #
    # o bien podemos importar los modelos y crearlos con los métodos de cada clase
    print "termino seeds"