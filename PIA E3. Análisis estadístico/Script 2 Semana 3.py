# Segundo Script de semana 3
import re
from statistics import mean

# Lectura y validación de IDs y nombres
def leer_ids_nombres(ruta_ids):
    asteroides = []
    patron = re.compile(r'ID:\s*(\d+)\s*\|\s*Nombre:\s*(.+)')

    with open(ruta_ids, 'r') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue  # Saltar líneas vacías
            match = patron.search(linea)
            if match:
                id_ = match.group(1)
                nombre = match.group(2)
                asteroides.append({
                    "ID": id_,
                    "Nombre": nombre
                })
            else:
                print(f"[Advertencia] Línea no válida: {linea}")

    return asteroides

# Lectura y validación de datos de un asteroide
def leer_datos_asteroide(ruta_datos):
    patron_linea = re.compile(r'-->\s*(.+?)\.?$')
    valores = []

    with open(ruta_datos, 'r') as archivo:
        for linea in archivo:
            match = patron_linea.search(linea)
            if match:
                valor = match.group(1).strip()
                valores.append(valor)
            else:
                print(f"[Advertencia] Línea no válida: {linea.strip()}")

    # Se valida que no hayan mas de 5 datos
    if len(valores) < 5:
        ValueError("Faltan datos para construir el diccionario del asteroide.")

    datos = {
        "Nombre": valores[0],
        "ID": valores[1],
        "Magnitud_Absoluta_H": float(valores[2]),
        "Diámetro_Estimado_(km)": eval(valores[3]),
    }

    return datos

def operaciones(estructura_visualizacion):
    print("Si desea hacer operaciones con los datos recabados de su script, elija la opción deseada.")
    menu2= """
    --------------------------------------------------------
    | 1. Encontrar promedio del diámetro del NEO           |
    | 2. Convertir magnitud absoluta H a luminosidad solar |
    | 3. No quiero realizar operaciones                    |
    --------------------------------------------------------
    """
    while True:
        print(menu2)
        op1= int(input("Ingrese opción deseada: "))
        # Operacion 1 usando statistics module
        if op1==1:
            valores= list()
            mini= estructura_visualizacion["Diámetro_estimado (km)"]["estimated_diameter_min"]
            valores.append(mini)
            maxi= estructura_visualizacion["Diámetro_estimado (km)"]["estimated_diameter_max"]
            valores.append(maxi)
            print(f"El diámetro promedio del NEO es {mean(valores)} km.")
        # Operacion 2
        elif op1==2:
            H= estructura_visualizacion["Magnitud_Absoluta_H"]
            lumi= (1.08* 10**11) * (10*(-0.4 * H))
            print(f"{H} es equivalente a {lumi} luminosidad solar.")
        elif op1==3:
            print("Regresando al menú principal...")
            break
        else:
            print("Opcion invalida. ¡Pruebe de nuevo!")

# Codigo principal
print("Bienvenido! Este programa tiene el propósito de visualizar y manejar los datos de NEOs.")
menu= """
-------------------------------------Menú-------------------------------------
| 1. Visualizar archivo .txt de NEO determinada                              |
| 2. Consultar listas de IDs guardada                                        |                                      |
| 3. Salir                                                                   |
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
            # Uso del script 1
            # Se solicita ID al usuario
            id_usuario = input("\nIngresa el ID del asteroide que deseas analizar: ").strip()
            # Se construye una ruta al archivo de datos
            ruta_datos = f"Datos_{id_usuario}.txt"
            try:
                info_detallada = leer_datos_asteroide(ruta_datos)

                # Preparación para visualización
                estructura_visualizacion = {
                    "ID": info_detallada["ID"],
                    "Nombre": info_detallada["Nombre"],
                    "Magnitud_Absoluta_H": info_detallada["Magnitud_Absoluta_H"],
                    "Diámetro_estimado (km)": info_detallada["Diámetro_Estimado_(km)"]
                    }
                print("\nDatos Detallados para Visualización")
                print()
                for x,y in estructura_visualizacion.items():
                    print(f"{x} : {y}")
                    
            except FileNotFoundError:
                print(f"\n[Error] No se encontró el archivo: {ruta_datos}")
            except ValueError as e:
                print(f"\n[Error] {e}")
            operaciones(estructura_visualizacion)

        elif op==2:   
            # Se Lee lista de asteroides y datos de un asteroide
            ruta_ids = "Asteroides_IDs.txt"
            lista_info = leer_ids_nombres(ruta_ids)

            print("\nLista de Asteroides")
            for i in lista_info:
                print(i)

        elif op==3:
            print("Salida del usuario.\nHASTA LUEGO!")
            break
        else:
            print("Opcion invalida. ¡Pruebe de nuevo!")
            
