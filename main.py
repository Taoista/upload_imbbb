import os
from dotenv import load_dotenv
import requests
from pathlib import Path
import base64
import csv

def crete_folder():
    folder = Path("images")

    if not folder.exists():
        folder.mkdir()
        return folder
    else:
        return folder



def subir_imagen(url, clave_api, ruta_imagen):
    with open(ruta_imagen, "rb") as archivo:
        payload = {
            "key": clave_api
        }
        archivos = {
            "image": archivo
        }
        respuesta = requests.post(url, payload, files=archivos)
        print(respuesta)
        datos_respuesta = respuesta.json()
        if datos_respuesta["success"]:
            url_imagen = datos_respuesta["data"]["url"]
            print("Imagen subida exitosamente:", url_imagen)
            return url_imagen
        else:
            print("Error al subir la imagen:", datos_respuesta["error"]["message"])


def subir_imagenes_a_imgbb(path_images, url, clave_api):
    urls_imagenes = []
    for imagen in os.listdir(path_images):
        ruta_imagen = os.path.join(path_images, imagen)
        url_imagen = subir_imagen(url, clave_api, ruta_imagen)
        if url_imagen:
            urls_imagenes.append((imagen, url_imagen))
    return urls_imagenes

def main():
    load_dotenv()
    path_images = crete_folder()
    url = "https://api.imgbb.com/1/upload"
    clave_api = os.getenv("API_IMGBB")
    
    urls_imagenes = subir_imagenes_a_imgbb(path_images, url, clave_api)
    if urls_imagenes:
        nombre_archivo = "urls_imagenes.csv"
        with open(nombre_archivo, "w", newline="") as archivo_csv:
            escritor_csv = csv.writer(archivo_csv, delimiter=";")
            escritor_csv.writerow(["Nombre de la imagen", "URL de la imagen"])  # Encabezados de las columnas
            for nombre_imagen, url_imagen in urls_imagenes:
                escritor_csv.writerow([nombre_imagen, url_imagen])


if __name__ == "__main__":
    main()