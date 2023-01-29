"""UIP - PROGRAMACIÓN IV - DICCIONARIO DEL SLANG PANAMEÑO

Actividad: Elaborar una aplicación de línea de comandos en Python que sirva cuyo
propósito sea mantener un diccionario de palabras del slang panameño (xopa, mopri, otras).

Las palabras y su significado deben ser almacenadas dentro de una base de datos SQLite.
Las opciones dentro del programa deben incluir como mínimo: a) Agregar nueva palabra,
b) Editar palabra existente, c) Eliminar palabra existente, d) Ver listado de palabras,
e) Buscar significado de palabra, f) Salir"""

import sqlite3
import sys

try:

    databaseName = "prodDictionary.db"

    def getConnection():
        return sqlite3.connect(databaseName)

    def createTables():
        tables = ["CREATE TABLE IF NOT EXISTS dictionary (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT NOT NULL, meaning TEXT NOT NULL)"]
        connection = getConnection()
        cursor = connection.cursor()
        for table in tables:
            cursor.execute(table)

    def principal():
        createTables()
        menu = """
    \n__________________________________________
            DICCIONARIO DE SLANG PANAMEÑO
    a) Agregar nueva palabra
    b) Editar palabra existente
    c) Eliminar palabra existente
    d) Ver listado de palabras
    e) Buscar significado de palabra
    f) Salir
    __________________________________________
    Selecciona una opción: """

        option = ""
        while option != "f":
            option = input(menu).lower()
            if option == "a":
                word = input("Ingresa la palabra: ")
                # Comprobar si la palabra ya existe
                possibleMeaning = getMeaning(word)
                if possibleMeaning:
                    print(f"La palabra '{word}' ya existe")
                # Si no existe:
                else:
                    meaning = input("Ingresa el significado: ")
                    addWord (word, meaning)
                    print(f"Palabra agregada: {word}")
            if option == "b":
                word = input("Ingresa la palabra que quieres editar: ")
                newMeaning = input("Ingresa el nuevo significado: ")
                editWord (word, newMeaning)
                print(f"Palabra actualizada: {word}")
            if option == "c":
                word = input("Ingresa la palabra a eliminar: ")
                removeWord(word)
                print(f"Palabra eliminada: {word}")
            if option == "d":
                words = getWords()
                print("=== Lista de palabras ===")
                for word in words:
                    # Al leer desde la base de datos se devuelven los datos como arreglo, por lo que hay que imprimir el primer elemento
                    print(word[0])
            if option == "e":
                word = input("Ingresa la palabra de la cual quieres saber el significado: ")
                meaning = getMeaning(word)
                if meaning:
                    print(f"El significado de '{word}' es: {meaning[0]}")
                else:
                    print(f"Palabra '{word}' no encontrada")
        else:
            print("\nEl programa ha finalizado")
            sys.exit()

    #MÉTODO PARA AGREGAR PALABRA
    def addWord(word, meaning):
        connection = getConnection()
        cursor = connection.cursor()
        statement = "INSERT INTO dictionary (word, meaning) VALUES (?, ?)"
        cursor.execute(statement, [word, meaning])
        connection.commit()

    #MÉTODO PARA EDITAR PALABRA
    def editWord(word, newMeaning):
        connection = getConnection()
        cursor = connection.cursor()
        statement = "UPDATE dictionary SET meaning = ? WHERE word = ?"
        cursor.execute(statement, [newMeaning, word])
        connection.commit()

    #MÉTODO PARA ELIMINAR PALABRA
    def removeWord(word):
        connection = getConnection()
        cursor = connection.cursor()
        statement = "DELETE FROM dictionary WHERE word = ?"
        cursor.execute(statement, [word])
        connection.commit()

    #MÉTODO PARA OBTENER PALABRAS
    def getWords():
        connection = getConnection()
        cursor = connection.cursor()
        query = "SELECT word FROM dictionary"
        cursor.execute(query)
        return cursor.fetchall()

    #MÉTODO PARA OBTENER SIGNIFICADO DE UNA PALABRA
    def getMeaning(word):
        connection = getConnection()
        cursor = connection.cursor()
        query = "SELECT meaning FROM dictionary WHERE word = ?"
        cursor.execute(query, [word])
        return cursor.fetchone()

    #GARANTIZAR QUE LA FUNCIÓN 'principal' SOLO SE EJECUTE CUANDO EL ARCHIVO SE EJECUTA COMO PROGRAMA PRINCIPAL Y NO CUANDO SE IMPORTA COMO MÓDULO
    if __name__ == '__main__':
        principal()

#MANEJO DE EXCEPCIONES
except ValueError:
    print("ExceptionError - ValueError: Database not connected")

except TypeError:
    print("ExceptionError - TypeError: Database not connected")

except TimeoutError:
    print("ExceptionError - Timeout: Database not connected")

finally:
    # CIERRE DE CONEXION A BASE DE DATOS SQLITE
    connection = getConnection()
    getConnection().close