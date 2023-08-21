import os
import multiprocessing
from bs4 import BeautifulSoup
import re

def search_text_in_file(file_path, target_text):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')
            return target_text.lower() in soup.get_text().lower()
    except Exception as e:
        print(f"Error while processing a file {file_path}: {e}")
    return False

def search_in_folder(folder_path, target_text):
    matching_files = []
    with multiprocessing.Pool() as pool:
        tasks = [(os.path.join(root, file), target_text) for root, _, files in os.walk(folder_path) for file in files if file.endswith(".html")]
        results = pool.starmap(search_text_in_file, tasks)
        
        for file_path, result in zip([task[0] for task in tasks], results):
            if result:
                matching_files.append(os.path.normpath(file_path))

    return matching_files

def main():
    folder_path = input("Enter the path to the folder to search for: ")

    if not os.path.isdir(folder_path):
        print("The specified path is not a folder")
        return
    
    target_text = input("Enter search text: ")
    matching_files = search_in_folder(folder_path, target_text)
    matching_files = sorted(matching_files, key=lambda x: [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', x)])
    
    if matching_files:
        print("The text is found in the following files:")
        for file in matching_files:
            print(file)
    else:
        print("Text not found in any file")

if __name__ == "__main__":
    main()
