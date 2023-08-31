import os
import zipfile
import mysql.connector

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


# Función para insertar datos en la base de datos
def insert_data_into_database(db_connection, file_id, keyword, content):
    with db_connection.cursor() as cursor:
        insert_query = """
        INSERT INTO datos_salientes (archivo_id, keyword, content)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (file_id, keyword, content))
    db_connection.commit()


# Menu
def menu_ordenar_archivos():
    output_file = "dumpData.txt"

    print("-" * 30)
    print("1) Extraer, formatear y almacenar archivos")

    opcion = input("> ")

    if opcion == "1":
        ordenar_archivos_txt()
    else:
        print("Opción no válida. Por favor, seleccione 1, 2 o 3.")


# inicio de procesamiento de datos
def ordenar_archivos_txt(db_connection):
    zip_file_path = "Search 2023-08-22 16_14_12.zip"
    extract_dir = "Extracted_files"

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        file_names = zip_ref.namelist()

        print("=== TXT FILES IN ZIP ===")
        for name in file_names:
            if name.lower().endswith(".txt"):
                print(name)
                zip_ref.extract(name, path=extract_dir)

    extracted_dir = "Extracted_files"
    output_file = "dumpData.txt"

    # Nuevas asignaciones de palabras clave
    keyword_mappings = {
        "Username": ["USER", "Login", "Username"],
        "Password": ["Password", "PASS"],
        "Url": ["URL", "Host"],
    }

    # Procesar datos
    def find_keywords_and_content_in_file(file_path, keyword_mappings):
        found_data = []
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                for keyword, keywords_list in keyword_mappings.items():
                    found_keywords = [kw for kw in keywords_list if kw in line]
                    if found_keywords:
                        found_data.append((keyword, line.strip()))
                        break
        return found_data

    # Ordenar la salida de los datos pertinentes
    with open(output_file, "w", encoding="utf-8") as out_f:
        txt_files = [f for f in os.listdir(extracted_dir) if f.lower().endswith(".txt")]
        txt_files.sort()

        for txt_file in txt_files:
            txt_file_path = os.path.join(extracted_dir, txt_file)
            found_data = find_keywords_and_content_in_file(
                txt_file_path, keyword_mappings
            )
            # Setear salida de datos para que sea legible
            if found_data:
                file_id = os.path.splitext(txt_file)[0]
                for keyword, content in found_data:
                    insert_data_into_database(db_connection, file_id, keyword, content)


def main():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="critdb",
    )

    create_table_query = """
    CREATE TABLE IF NOT EXISTS datos_salientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        archivo_id VARCHAR(255),
        keyword VARCHAR(255),
        content TEXT
    )
    """
    with db_connection.cursor() as cursor:
        cursor.execute(create_table_query)
    db_connection.commit()

    ordenar_archivos_txt(db_connection)

    db_connection.close()


if __name__ == "__main__":
    main()
