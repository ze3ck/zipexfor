import os
import zipfile

BOLD = "\033[1m"
END = "\033[0m"

banner = r"""
{}     
  _____          ___     ___        
 |_  (_)_ __ ___| __|_ _| __|__ _ _ 
  / /| | '_ \___| _|\ \ / _/ _ \ '_|
 /___|_| .__/   |___/_\_\_|\___/_|  
       |_|                                                                                                     
                                {}

""".format(
    BOLD, END
)
print(banner)


def menu_ordenar_archivos():
    output_file = "dumpData.txt"
    
    print("-"*30)
    print("1) Extraer, formatear y almacenar archivos")
    print("2) Mostrar archivo almacenado")
    print("3) Salir")
    
    opcion = input("> ")

    if opcion == "1":
        ordenar_archivos_txt()
    elif opcion == "2":
        mostrar_archivo(output_file)
    elif opcion == "3":
        salir()
    else:
        print("Opción no válida. Por favor, seleccione 1, 2 o 3.")


def ordenar_archivos_txt():
    # Aquí iría el código para ordenar archivos TXT
    zip_file_path = "Search_2023-08-22 16_14_12.zip"
    extract_dir = "Extracted_files"

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        file_names = zip_ref.namelist()

        print("=== TXT FILES IN ZIP ===")
        for name in file_names:
            if name.lower().endswith(".txt"):
                print(name)
                zip_ref.extract(name, path=extract_dir)

    # Extracción y salida, junto con palabras clave a buscar dentro de los txt
    extracted_dir = "Extracted_files"

    output_file = "dumpData.txt"

    keywords = ["Username", "Password", "URL"]

    def find_keywords_and_content_in_file(file_path, keywords):
        found_data = []
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                found_keywords = []
                for keyword in keywords:
                    if keyword in line:
                        found_keywords.append(keyword)
                if found_keywords:
                    found_data.append((', '.join(found_keywords), line.strip()))
        return found_data

    with open(output_file, "w", encoding="utf-8") as out_f:
        txt_files = [f for f in os.listdir(extracted_dir) if f.lower().endswith(".txt")]
        txt_files.sort()

        for txt_file in txt_files:
            txt_file_path = os.path.join(extracted_dir, txt_file)
            found_data = find_keywords_and_content_in_file(txt_file_path, keywords)

            if found_data:
                file_id = os.path.splitext(txt_file)[
                    0
                ]  # Obtener la ID del archivo de origen
                out_f.write(f"\nArchivo: {file_id}.txt\n")
                for keyword, content in found_data:
                    out_f.write(f" {content}\n")
                    

    print("Análisis completado. Los resultados se han almacenado en 'dumpData.txt'.")

def mostrar_archivo(file_path):
    print("Mostrando archivo:")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print(f"El archivo '{file_path}' no fue encontrado.")

def salir():
    print("Saliendo...")

menu_ordenar_archivos()
