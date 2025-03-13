from bs4 import BeautifulSoup
import os

projects = [
    "project_1.html", "project_2.html", "project_3.html", "project_4.html", 
    "project_5.html", "project_6.html", "project_7.html", "project_8.html", 
    "project_9.html", "project_10.html"
]

def run_prettify():
    for html_file in projects:
        name, ext = os.path.splitext(html_file)
        output_file = f"pretty_files/{name}_pretty{ext}"
        html_file = 'original_files/' + html_file
        
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'lxml')
        
            
            print(output_file)
            
            with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(soup.prettify())