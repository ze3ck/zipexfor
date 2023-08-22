"""
import zipfile

# Ruta al archivo ZIP
zip_file_path = 'Search_2023-08-22 16_14_12.zip'

# Abrir el archivo ZIP
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Listar los nombres de los archivos en el archivo ZIP
    file_names = zip_ref.namelist()

    # Imprimir los nombres de los archivos
    print("=== FILES IN ZIP ===")
    for name in file_names:
        print(name)
"""
import os
import zipfile

zip_file_path = 'Search_2023-08-22 16_14_12.zip'

extract_dir = 'Extracted_files'

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    file_names = zip_ref.namelist()

    print("=== TXT FILES IN ZIP ===")
    for name in file_names:
        if name.lower().endswith('.txt'):
            print(name)
            zip_ref.extract(name, path=extract_dir)




extracted_dir = 'Extracted_files'

txt_files = [f for f in os.listdir(extracted_dir) if f.lower().endswith('.txt')]

txt_files.sort()

for txt_file in txt_files:
    txt_file_path = os.path.join(extracted_dir, txt_file)
    print(f"=== Contenido de {txt_file} ===")
    
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            print(line.strip())  
