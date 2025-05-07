# Semana 2 PIA
# Grupo 5

import requests
import re

# Esta función permite validar, mediante expresiones regulares, que el usuario ingrese únicamente digitos en el ID
# Evita errores en las solicitudes a la API
def validar_id(asteroid_id):
    return re.fullmatch(r"\d+", asteroid_id) is not None

class Manejo_de_api:

    # Función que conecta el programa con el API de NEO de la NASA
    # Determina si el asteroide es peligroso o no
    def determinar_peligro(API_KEY, asteroid_id):
        url= f"https://api.nasa.gov/neo/rest/v1/neo/{asteroid_id}?api_key={API_KEY}"
        respuesta= requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            nombre = datos["name"]
            print(f"\nNombre del asteroide {asteroid_id}: {nombre}")
            es_peligroso = datos["is_potentially_hazardous_asteroid"]
            if es_peligroso==True:
                print(f"\n{nombre} es un asteroide potencialmente peligroso.")
            else:
                print(f"\n{nombre} NO es un asteroide potencialmente peligroso.")
        else:
            print(f"Error {respuesta.status_code}: no se pudo conectar con la API. Verifica que el ID sea válido.")

    # Esta función permite que el usuario visualice datos de un asteroide
    # Le da la opción de crear un archivo txt con los datos
    def consultar_datos(API_KEY, asteroid_id):
        url= f"https://api.nasa.gov/neo/rest/v1/neo/{asteroid_id}?api_key={API_KEY}"
        respuesta= requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            # Evaluación de limpieza de datos:
            # Los datos obtenidos del JSON están bien estructurados y no presentan campos ruidosos o inconsistencias.
            # Por lo tanto, no se requiere limpieza adicional.

            # Se crea un diccionario 
           # Se crea un diccionario 
            datos_detallados = dict()
            datos_detallados["NOMBRE"]= datos["name"]
            datos_detallados["ID"]= datos["id"]
            datos_detallados["MAGNITUD_ABSOLUTA_H"]= datos["absolute_magnitude_h"]
            datos_detallados["DIÁMETRO_ESTIMADO"]= datos["estimated_diameter"]["kilometers"] # Datos compuestos de otro dict

            nombre = datos.get("name_limited", datos["name"])

            # Se imprime el diccionario
            for x,y in datos_detallados.items():
                print(f"\n{x} --> {y}")
                print("__________")
            while True:
                opcion= int(input(f"\nDesea guardar la información de {nombre} en un archivo de texto? [1-Si/2-No]: "))
                if opcion==1:
                    with open (f"Datos_{asteroid_id}.txt","w") as file:
                        for x,y in datos_detallados.items():
                            file.write(f"{x} --> {y}.\n")
                    print("Listo!")
                    break
                elif opcion==2:
                    print("Regresando al menú principal…")
                    break
                else:
                    print("Opcion invalida. ¡Pruebe de nuevo!")
        else:
            print(f"Error {respuesta.status_code}: no se pudo conectar con la API. Verifica que el ID sea válido.")

    # Esta función permite al usuario buscar la cantidad de IDs que desee según un intervalo propuesto.
    # Regresa una lista de IDs
    def lista_ids(API_KEY, inicial, final):
        while True:
            if inicial < 0 or inicial > final or final > 39312:
                print("\nRango inválido. Intenta con un intervalo válido dentro de 0 y 39312")
                try:
                    inicial = int(input("Introducir valor inicial del intervalo: "))
                    final = int(input("Introducir valor final del intervalo: "))
                except ValueError:
                    print("Por favor ingrese solo números.")
            else:
                break
        asteroides_totales = []
        page = 0
        while len(asteroides_totales) <= final:
            url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?page={page}&size=100&api_key={API_KEY}"
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                nuevos = datos["near_earth_objects"]
                # Evaluación de limpieza de datos:
                # La API ya proporciona una lista clara de objetos con campos estructurados.
                # No se identificaron errores, valores nulos o datos redundantes, por lo que no fue necesaria una limpieza adicional.

                asteroides_totales.extend(nuevos)
                
                total_pages = datos["page"]["total_pages"]
                current_page = datos["page"]["number"]

                if current_page >= total_pages - 1:
                    break

                # Se navega mediante las páginas del API para obtener los IDs solicitados por el usuario
                page += 1
            else:
                print(f"Error {respuesta.status_code}: no se pudo conectar con la API. Verifica que el ID sea válido.")
                return

        # Se imprime la lista de los IDs encontrados    
        print("\nIDs disponibles en el intervalo solicitado:")
        for i in range(inicial, final + 1):
            asteroide = asteroides_totales[i]
            if (inicial == 0):
                print(f"{i+1}. ID: {asteroide['id']} | Nombre: {asteroide['name']}")
            else:
                print(f"{i}. ID: {asteroide['id']} | Nombre: {asteroide['name']}")
            
# Programa inicial
API_KEY= "0AMkNAnXRuPBPKGLJWGrqDFQfcb4qbniMnvQVc0x"
print("""¡Bienvenido!
Este programa tiene como objetivo proporcionar datos relevantes sobre objetos NEO (Near Earth Objects).
Elija una opción de nuestro menú para comenzar.
""")
menu = """
-------------------------------------Menú-------------------------------------
| 1. Determinar si un asteroide es potencialmente peligroso (se necesita ID) |
| 2. Consultar sobre NEOs (se necesita ID)                                   |
| 3. Consultar IDs en la base de datos                                       |
| 4. Salir                                                                   |
------------------------------------------------------------------------------
"""
while True:
    print(menu)
    # Aquí se valida que el usuario no ingrese caracteres que no sean enteros
    try:
        op = int(input("Ingrese opción deseada: "))
    except ValueError:
        print("La opción debe de ser un número. ¡Pruebe de nuevo!")
    else:
        if op==1:
            # Ejemplos de id: 2001566, 2001221, 2001580…
            asteroid_id= input("Ingresar ID: ")
            # Se valida el ID con expresiones regulares
            if validar_id(asteroid_id):
                Manejo_de_api.determinar_peligro(API_KEY, asteroid_id)
            else:
                print("ID inválido. Debe contener solo dígitos.")
            input("\nPresiona la tecla enter para continuar. :D")
        elif op==2:
            asteroid_id= input("Ingresar ID: ")
            # Se valida el ID con expresiones regulares
            if validar_id(asteroid_id):
                Manejo_de_api.consultar_datos(API_KEY, asteroid_id)
            else:
                print("ID inválido. Debe contener solo dígitos.")
            input("\nPresiona la tecla enter para continuar. :D")
        elif op==3:
            print("El sistema de datos cuenta con 39312 elementos, por esta razón le recomendamos visualizar pocas IDs a la vez!")
            print("Tenga en cuenta que, entre mayores sean los números, más se tardará en procesar la información.")
            # Se validan los intervalos haciendo uso de excepciones
            try:
                inicial = int(input("Introducir valor inicial del intervalo: "))
                final = int(input("Introducir valor final del intervalo: "))
            except ValueError:
                print("Por favor ingrese solo números.")
                input("\nPresiona la tecla enter para continuar. :D")
            else:
                print("Buscando IDs…")
                Manejo_de_api.lista_ids(API_KEY, inicial, final)
                input("\nPresiona la tecla enter para continuar. :D")
        elif op==4:
            print("Salida del usuario.\nHASTA LUEGO!")
            break
        else:
            print("Opcion invalida. ¡Pruebe de nuevo!")
