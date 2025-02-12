import json
from bs4 import BeautifulSoup
import os
from bs4 import Comment

def remove_img_alt(soup, html_file):
    changes = []
    for img in soup.find_all('img'):
        if img.has_attr('alt'):
            line_number = img.sourceline
            before = str(img)  # Store original tag
            del img['alt']
            after = str(img)  # Store modified tag

            # Log the change
            changes.append({
                "violation": "1.1.1.2",  # Example guideline code
                "before": before,
                "after": after,
                "linenumber": line_number
            })
    
    return changes

def remove_iframe_alt(soup, html_file):
    changes = []
    for iframe in soup.find_all('iframe'):
        if iframe.has_attr('title'):
            line_number = iframe.sourceline
            before = str(iframe)  # Store original tag
            del iframe['title']
            after = str(iframe)  # Store modified tag

            # Log the change
            changes.append({
                "violation": "1.1.1.1",
                "before": before,
                "after": after,
                "linenumber": line_number
            })
    
    return changes

def empty_label_input(soup, html_file):
    changes = []
    count = 0

    for label in soup.find_all('label'):
        if count == 1:
            break
        associated_element = soup.find(id=label['for'])

        if associated_element:
            if associated_element.name == 'input':
                line_number = label.sourceline
                before = str(label)
                label.string = ""
                after = str(label)

                changes.append({
                    "violation": "1.3.1.1",
                    "before": before,
                    "after": after,
                    "linenumber": line_number
                })
        
        count += 1
        
    return changes
        
def remove_label_input(soup, html_file):
    changes = []

    for label in soup.find_all('label'):
        total_elements = len(soup.find_all(id=label['for']))
        associated_element = soup.find(id=label['for'])

        if associated_element:
            if associated_element.name == 'input':
                line_number = label.sourceline
                before = str(label)
                id = label['for']

                comment = Comment(f"""
    Label for input element \"{id}\" removed 
    """)

                label.insert_before(comment)
                label.decompose()
                after = f"<!--Label for input element \"{id}\" removed -->"

                changes.append({
                    "violation": "1.3.1.2",
                    "before": before,
                    "after": after,
                    "linenumber": line_number
                })
        
    return changes   

def update_html(projects, json_log):
    changes = {}

    # Load existing JSON if it exists
    if os.path.exists(json_log):
        with open(json_log, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                # Ensure JSON is a dictionary, convert from list if necessary
                if isinstance(data, list):
                    changes = {}  # Reset to dictionary format
                elif isinstance(data, dict):
                    changes = data
            except json.JSONDecodeError:
                changes = {}  # Reset if file is empty or malformed

    # Read the HTML file
    for html_file in projects:
        name, ext = os.path.splitext(html_file)
        output_file = f"output_files/{name}_output{ext}"
        input_file = 'pretty_files/' + html_file

        with open(input_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # Track changes specific to this file
        modification_functions = [remove_iframe_alt, remove_img_alt, remove_label, empty_label]

        file_changes = []
        for func in modification_functions:
            file_changes.extend(func(soup, input_file))

        # Update the JSON structure
        changes[input_file] = file_changes

        # Write the modified HTML back to the output file with proper formatting
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        # Save changes to a JSON file
        with open(json_log, 'w', encoding='utf-8') as json_file:
            json.dump(changes, json_file, indent=4)

projects = ['project_1_pretty.html', 'project_2_pretty.html']

# Example usage
update_html(projects, 'changes_log.json')
