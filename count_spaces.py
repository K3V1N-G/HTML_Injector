from bs4 import BeautifulSoup

input = 'pretty_files/project_7_pretty.html'
with open(input, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')


for finder in soup.find_all('a'):
    if len(list(finder.children)) < 100:
        line_number = finder.sourceline
        print(len(list(finder.children)))
        print(str(finder))
            
        before = str(finder)
        after = str(finder)