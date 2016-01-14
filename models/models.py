# -*- coding: utf-8 -*-
import os
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, validates
from sqlalchemy.pool import StaticPool
from info import get_database_url

Base = declarative_base()

# podemos utilizar variables de entorno
try:
    url = os.environ["DATABASE_URL2"]
    print "se conecto con las variables"
except KeyError: 
    #url = get_database_url()
    # url = "postgresql+psycopg2://vomwiwzrwzmzkr:9No_s99GgPAjTg9mADFHh5Jz4A"
    # url += "@ec2-54-204-12-25.compute-1.amazonaws.com:5432/d417r6qvguin8v"

#engine = create_engine(url, 
#    connect_args={'client_encoding': 'utf8'})
#engine.echo = True
#engine.connect()

# Si estamos utilizando sqlite3
 engine = create_engine('sqlite:///models/db/ruidodb.db',
     connect_args={'check_same_thread':False},
     poolclass=StaticPool)
 engine.echo = True  # Try changing this to True and see what happens
 engine.connect()

# creamos una nueva session
# mantendremos la misma sesion para todas las tablas
Session = sessionmaker(bind=engine)
session = Session()

# definimos nuestros objetos
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(Integer, nullable=False, unique=True)
    name = Column(String)
    password = Column(String, nullable=False)

    # Aquí ponemos las relaciones entre tablas
    # cascade="save-update, merge, delete"
    posts = relationship("Post", cascade="save-update,delete")

    # Aquí pueden ir algunasas validaciones
    @validates('email')
    def validate_email(self, key, address):
        if User.find_by_email(address) is not None:
            raise ValueError("email")
        return address

    @validates('password')
    def validate_password(self, key, password):
        if password:
            return password
        raise ValueError("password")

    # Ejemplo por si se quiere imprimir un objeto
    def __repr__(self):
        return "<User(email='%s', name='%s')>" % (self.email, self.name)

    # Si se quieren sobreescribir algunos métodos
    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception, e:
            session.rollback()

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception, e:
            session.rollback()

    def update(self, name=None, password=None, post=None):
        if name and self.name != name:
            self.name = name
        if password and self.password != password:
            self.password = password
        # si se quiere agregar en una relacion User ('parent') - Post ('child')
        if post and post not in self.posts:
            session.add(post)
            self.posts.append(post)
        try:
            session.commit()
        except Exception, e:
            session.rollback()

    @staticmethod
    def find(value):
        """Método que regresa un usuario 
        pasandole el id de la tabla correspondiente"""
        return session.query(User).get(value)

    @staticmethod
    def find_by_email(value):
        try:
            return session.query(User).filter_by(email=value).one()
        except Exception, e:
            session.rollback()
            return None

    @staticmethod
    def all():
        return session.query(User).all()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)

    def __repr__(self):
        return "<Post(user_id='%s', name='%s')>" % (self.user_id, self.name)

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception, e:
            session.rollback()

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception, e:
            session.rollback()

    def update(self, name=None):
        if name and self.name != name:
            self.name = name
        try:
            session.commit()
        except Exception, e:
            session.rollback()

    @staticmethod
    def find_by(user_id=None, name=None):
        try:
            if user_id:
                return session.query(Post).filter_by(user_id=user_id).all()
            elif name:
                return session.query(Post).filter_by(name=name).all()
        except Exception, e:
            return None
        
# otro_user = User(email='otro2@example.com', name='otro', password='otropassword')
# otro_user.save()

# for i in xrange(1,3):
#     post = Post(user_id=otro_user.id, name=("post"+str(i)))
#     post.save()

# print otro_user.posts

# first_user = User.find(1)
# first_user.delete()
# print Post.find_by(user_id=1)