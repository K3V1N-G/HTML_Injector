import json
from bs4 import BeautifulSoup
import os
from bs4 import Comment
import random
import targets
import prettify


prettify.run_prettify()

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

        if os.path.exists(input_file):
            with open(input_file, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
        else:
            continue

        # Track changes specific to this file
        modification_functions = [targets.remove_iframe_alt, targets.remove_img_alt, targets.update_label_input, targets.update_label_select, targets.update_label_button, targets.insert_font, targets.insert_ital, targets.insert_bold, targets.update_mouse_attr, targets.insert_marquee, targets.update_title, targets.remove_a_text, targets.update_html_lang]

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

projects = ['project_1_pretty.html', 'project_2_pretty.html', 'project_3_pretty.html', 'project_4_pretty.html', 'project_5_pretty.html', 'project_6_pretty.html', 'project_7_pretty.html', 'project_8_pretty.html', 'project_9_pretty.html', 'project_10_pretty.html', 'project_11_pretty.html', 'project_12_pretty.html', 'project_13_pretty.html', 'project_14_pretty.html', 'project_15_pretty.html']

# run the program
update_html(projects, 'changes_log.json')