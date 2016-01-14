# -*- coding: utf-8 -*-
import sqlite3

class ConSQLite:
    """ Clase de ejemplo de conexión por medio de sqlite3
        por si se requieren consultas no soportadas por algún ORM
        solo hay dos tipos de consultas: modifican elementos de la base
        y las que solo ven algún elemento sin modificarlo """

    # Como su nombre lo indica solo para consultas
    def consultar(self, sql):
        try:
            conn = sqlite3.connect("models/db/ruidodb.db")
        except:
            print "No se puede conectar"

        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
        except:
            rows = None
        finally:
            try:
                cur.close()
                conn.close()
            except:
                print "no se puede desconectar consulta"

        # asignamos por default que si hay u error o no hay elementos es None
        if(rows is not None and len(rows) == 0):
            rows = None

        return rows

    # Método que se utilizara para insertar, actualizar y eliminar información de la base de datos
    # es actualizar porque actualiza la base
    def actualizar(self, sql):
        # si queremos alguna bandera para saber si se realizo correctamente
        n = 1
        try:
            conn = sqlite3.connect("models/db/ruidodb.db")
        except:
            print "no se puede conectar"
        
        try:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
        except psycopg2.DatabaseError, e:
            # si queremos manejar los errores
            print e.pgcode
            print e.pgerror
            n = -1
        finally :
            try:
                cur.close()
                conn.close()
            except:
                print "no se puede desconectar actualiza"
        return n