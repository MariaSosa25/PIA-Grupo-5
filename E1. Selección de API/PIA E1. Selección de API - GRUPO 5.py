# Semana 1 PIA
# Grupo 5

import requests

# Función que conecta el programa con el API de NEO de la NASA
# Determina si el asteroide es peligroso o no
def determinar_peligro(asteroid_id):
    API_KEY= "0AMkNAnXRuPBPKGLJWGrqDFQfcb4qbniMnvQVc0x"
    url= f"https://api.nasa.gov/neo/rest/v1/neo/{asteroid_id}?api_key={API_KEY}"
    respuesta= requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        nombre = datos["name"]
        print(f"Nombre del asteroide {asteroid_id}: {nombre}")
        es_peligroso = datos["is_potentially_hazardous_asteroid"]
        if es_peligroso==True:
            print(f"{nombre} es un asteroide potencialmente peligroso.")
        else:
            print(f"{nombre} NO es un asteroide potencialmente peligroso.")
    else:
        print("Error")

# Programa inicial
print("""¡Bienvenido!
Este programa tiene como objetivo proporcionar datos relevantes sobre objetos NEO (Near Earth Objects).
Elija una opción de nuestro menú para comenzar.
""")
menu = """
-------------------------------------Menú-------------------------------------
| 1. Determinar si un asteroide es potencialmente peligroso (se necesita id) |
| 2. Lista de asteroides mas cercanos a la Tierra                            |
| 3. Datos adicionales sobre NEOs (se necesita id)                           |
| 4. Salir                                                                   |
------------------------------------------------------------------------------
"""
while True:
    print(menu)
    # Aquí se valida que el usuario no ingrese caracteres que no sean enteros
    try:
        op = int(input("Ingrese opción deseada: "))
    except ValueError as e:
        print(e)
    finally:
        if op==1:
            # Ejemplos de id: 2001566, 2001221, 2001580…
            asteroid_id= int(input("Ingresar ID: "))
            determinar_peligro(asteroid_id)
            input("Presiona la tecla enter para continuar. :D")
        elif op==2:
            pass
        elif op==3:
            pass
        elif op==4:
            print("Salida del usuario.\nHASTA LUEGO!")
            break
        else:
            print("Opcion invalida. ¡Pruebe de nuevo!")
