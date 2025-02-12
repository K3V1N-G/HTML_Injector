from bs4 import BeautifulSoup
import json

def remove_img_alt(html_file, output_file, json_log):
    changes = []

    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    # Remove alt attributes from img elements and print their line numbers
    for img in soup.find_all('img'):
        if img.has_attr('alt'):
            line_num = img.sourceline
            before = str(img)
            del img['alt']
            after = str(img)

            changes.append({
                "project": html_file,
                "violation": "1.1.1.2",  # Example guideline code
                "before": before,
                "after": after,
                "linenumber": line_num
            })
    
    # Write the modified HTML back to the output file with proper formatting
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

    with open(json_log, 'w', encoding='utf-8') as json_file:
        json.dump(changes, json_file, indent=4)

# Example usage
remove_img_alt('project_1.html', 'output.html', 'changes_log.json')
