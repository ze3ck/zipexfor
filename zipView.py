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

# Extración y salida, junto con palabras claves a buscar dentro de los txt
extracted_dir = 'Extracted_files'

output_file = 'dumpData.txt'

keywords = ['Username', 'Password', 'URL']

def find_keywords_and_content_in_file(file_path, keywords):
    found_data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            for keyword in keywords:
                if keyword in line:
                    found_data.append((keyword, line.strip()))
    return found_data

with open(output_file, 'w', encoding='utf-8') as out_f:
    txt_files = [f for f in os.listdir(extracted_dir) if f.lower().endswith('.txt')]
    txt_files.sort()
    
    for txt_file in txt_files:
        txt_file_path = os.path.join(extracted_dir, txt_file)
        found_data = find_keywords_and_content_in_file(txt_file_path, keywords)
        
        if found_data:
            file_id = os.path.splitext(txt_file)[0]  # Obtener la ID del archivo de origen
            out_f.write(f"Archivo: {file_id}.txt\n")
            for keyword, content in found_data:
                out_f.write(f"  {keyword}: {content}\n")


print("Análisis completado. Los resultados se han almacenado en 'dumpData.txt'.")
