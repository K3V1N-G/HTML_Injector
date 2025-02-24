from bs4 import BeautifulSoup
import os
import json

projects = [
    "project_1.html", "project_2.html", "project_3.html", "project_4.html", 
    "project_5.html", "project_6.html", "project_7.html", "project_8.html", 
    "project_9.html", "project_10.html", "project_11.html", "project_12.html", 
    "project_13.html", "project_14.html", "project_15.html"
]

def check_img(soup, html_file):
    count = 0
    changes = []
    expected_num = 5
    missing_alt = 0
    remaining = expected_num

    for i in soup.find_all("img"):
        if i.get('alt'):
            if count < expected_num:
                remaining -= 1
            count += 1
        else:
            missing_alt += 1

    changes.append({
                "element": "img",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
                "missing alt text": missing_alt
            })
        
    return changes

def check_iframe(soup, html_file):
    count = 0
    changes = []
    expected_num = 5
    missing_alt = 0
    remaining = expected_num

    for i in soup.find_all("iframe"):
        if i.get('title'):
            if count < expected_num:
                remaining -= 1
            count += 1
        else:
            missing_alt += 1

    changes.append({
                "element": "iframe",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
                "missing alt text": missing_alt
            })
        
    return changes            

def check_input(soup, html_file):
    count = 0
    changes = []
    expected_num = 10
    no_label = 0
    remaining = expected_num

    for i in soup.find_all("input"):
        id = i.get('id')
        associated_label = soup.find('label', {'for': id})
        if associated_label:
            if count < expected_num:
                remaining -= 1
            count += 1
        else:
            no_label += 1

    changes.append({
                "element": "input",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
                "missing label": no_label
            })
        
    return changes 

def check_select(soup, html_file):
    count = 0
    changes = []
    expected_num = 10
    no_label = 0
    remaining = expected_num

    for i in soup.find_all("select"):
        id = i.get('id')
        associated_label = soup.find('label', {'for': id})
        if associated_label:
            if count < expected_num:
                remaining -= 1
            count += 1
        else:
            no_label += 1

    changes.append({
                "element": "select",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
                "missing label": no_label
            })
        
    return changes 

def check_button(soup, html_file):
    count = 0
    changes = []
    expected_num = 5
    no_label = 0
    remaining = expected_num

    for i in soup.find_all("button"):
        associated_label = i.text
        if associated_label:
            if count < expected_num:
                remaining -= 1
            count += 1
        else:
            no_label += 1

    changes.append({
                "element": "button",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
                "missing label": no_label
            })
        
    return changes

#reverse of select and input functions
def check_labels(soup, html_file):
    count = 0
    changes = []
    expected_num = 20
    no_element = 0
    remaining = expected_num
    line_num = 0
    other_label = 0

    for i in soup.find_all("label"):
        id = i.get('for')
        associated_label_input = soup.find('input', {'id': id})
        associated_label_select = soup.find('select', {'id': id})
        test = soup.find(True, {'id': id})
        if associated_label_input or associated_label_select:
            if count < expected_num:
                remaining -= 1
            count += 1
        elif test:
            other_label += 1
        else:
            no_element += 1

    changes.append({
                "element": "label",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
                "missing associated element": no_element,
                "labels for non-relevant elements": other_label
            })
        
    return changes 

def check_paragraph(soup, html_file):
    count = 0
    changes = []
    expected_num = 10
    remaining = expected_num

    for i in soup.find_all("p"):
        if count < expected_num:
            remaining -= 1
        count += 1

    changes.append({
                "element": "p",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
            })
        
    return changes

def check_emphasis(soup, html_file):
    count = 0
    changes = []
    expected_num = 5
    remaining = expected_num

    for i in soup.find_all("em"):
        if count < expected_num:
            remaining -= 1
        count += 1

    changes.append({
                "element": "em",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
            })
        
    return changes

def check_strong(soup, html_file):
    count = 0
    changes = []
    expected_num = 5
    remaining = expected_num

    for i in soup.find_all("strong"):
        if count < expected_num:
            remaining -= 1
        count += 1

    changes.append({
                "element": "strong",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
            })
        
    return changes

def check_html(soup, html_file):
    count = 0
    changes = []
    expected_num = 1
    missing_lang = 0
    remaining = expected_num

    for i in soup.find_all("html"):
        if i.get('lang'):
            if count < expected_num:
                remaining -= 1
            count += 1
        else:
            missing_lang += 1

    changes.append({
                "element": "html",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
                "missing lang attribute": missing_lang
            })
        
    return changes

def check_title(soup, html_file):
    count = 0
    changes = []
    expected_num = 1
    empty_label = 0
    remaining = expected_num

    for i in soup.find_all("title"):
        if i.text:
            if count < expected_num:
                remaining -= 1
            count += 1
        else:
            empty_label += 1

    changes.append({
                "element": "title",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
                "missing label text": empty_label
            })
        
    return changes

def check_anchor(soup, html_file):
    count = 0
    changes = []
    expected_num = 5
    empty_label = 0
    remaining = expected_num

    for i in soup.find_all("a"):
        if len(list(i.children)) == 1:
            if i.text:
                if count < expected_num:
                    remaining -= 1
                count += 1
            else:
                empty_label += 1

    changes.append({
                "element": "a",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
                "missing label text": empty_label
            })
        
    return changes

def check_onfocus(soup, html_file):
    count = 0
    changes = []
    expected_num = 5
    missing_other = 0
    remaining = expected_num

    for i in soup.find_all(True):
        if i.get('onmouseover'):
            if i.get('onfocus'):
                if count < expected_num:
                    remaining -= 1
                count += 1
            else:
                missing_other += 1

    changes.append({
                "element": "onmouseover/onfocus",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
                "missing onfocus": missing_other
            })
        
    return changes

def check_onblur(soup, html_file):
    count = 0
    changes = []
    expected_num = 5
    missing_other = 0
    remaining = expected_num

    for i in soup.find_all(True):
        if i.get('onmouseout'):
            if i.get('onblur'):
                if count < expected_num:
                    remaining -= 1
                count += 1
            else:
                missing_other += 1

    changes.append({
                "element": "onmouseover/onfocus",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
                "missing onblur": missing_other
            })
        
    return changes

def check_onkeydown(soup, html_file):
    count = 0
    changes = []
    expected_num = 5
    missing_other = 0
    remaining = expected_num

    for i in soup.find_all(True):
        if i.get('onmousedown'):
            if i.get('onkeydown'):
                if count < expected_num:
                    remaining -= 1
                count += 1
            else:
                missing_other += 1

    changes.append({
                "element": "onmousedown/onkeydown",
                "valid elements": f"{count}/{expected_num}",
                "remaining": remaining,
                "missing onkeydown": missing_other
            })
        
    return changes


def run_validation(projects, json_log):
    changes = {}

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


    for file in projects:
        name, ext = os.path.splitext(file)
        html_file = 'original_files/' + file
        
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'lxml')
            
            element_functions = [check_img, check_iframe, check_input, check_select, check_button, check_labels, check_paragraph, check_emphasis, check_strong, check_html, check_title, check_anchor, check_onfocus, check_onblur, check_onkeydown]

            data = []

            for func in element_functions:
                 data.extend(func(soup, html_file))

            changes[name] = data

                # Save changes to a JSON file
            with open(json_log, 'w', encoding='utf-8') as json_file:
                json.dump(changes, json_file, indent=4)


run_validation(projects, 'validation_log.json')