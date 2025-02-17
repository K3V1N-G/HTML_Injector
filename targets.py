import json
from bs4 import BeautifulSoup
import os
from bs4 import Comment
import random
from bs4.element import NavigableString


def insert_font(soup, html_file):
    changes = []
    num_to_inject = 4
    i = 0

    for p in soup.find_all('p'):
        if i > num_to_inject:
            break

        line_number = p.sourceline
        before = str(p)  # Store original tag
        p.name = 'font'
        after = str(p)  # Store modified tag

        # Log the change
        changes.append({
            "guideline": "font element used",
            "violation": "1.4.4.1",  # Example guideline code
            "before": before,
            "after": after,
            "linenumber": line_number
        })
        
        i += 1
    
    return changes

def insert_bold(soup, html_file):
    changes = []
    num_to_inject = 4
    i = 0

    for strong in soup.find_all('strong'):
        if i > num_to_inject:
            break

        line_number = strong.sourceline
        before = str(strong)  # Store original tag
        strong.name = 'b'
        after = str(strong)  # Store modified tag

        # Log the change
        changes.append({
            "guideline": "b (bold) element used",
            "violation": "1.4.4.3",  # Example guideline code
            "before": before,
            "after": after,
            "linenumber": line_number
        })
        
        i += 1
    
    return changes

def insert_ital(soup, html_file):
    changes = []
    num_to_inject = 4
    i = 0

    for ital in soup.find_all('em'):
        if i > num_to_inject:
            break

        line_number = ital.sourceline
        before = str(ital)  # Store original tag
        ital.name = 'i'
        after = str(ital)  # Store modified tag

        # Log the change
        changes.append({
            "guideline": "i (italic) element used",
            "violation": "1.4.4.2",  # Example guideline code
            "before": before,
            "after": after,
            "linenumber": line_number
        })
        
        i += 1
    
    return changes

def update_title(soup, html_file):
    odds = random.random()
    changes = []
    for title in soup.find_all('title'):
        line_number = title.sourceline
        before = str(title)  # Store original tag
        if odds > .5:

            comment = Comment(f"""
            Title element removed 
            """)

            title.insert_before(comment)
            title.decompose()
            after = f"<!--Title element removed -->"
        else:
            title.string = Comment("Text for title element removed")
            after = str(title)

        changes.append({
            "guideline": "title element is empty or document is missing title element",
            "violation": "2.4.2.1",
            "before": before,
            "after": after,
            "linenumber": line_number
        })
    
    return changes

def remove_img_alt(soup, html_file):
    changes = []

    num_to_inject = 4
    i = 0

    for img in soup.find_all('img'):
        if i > num_to_inject:
            break
        if img.has_attr('alt'):
            line_number = img.sourceline
            before = str(img)  # Store original tag
            del img['alt']
            after = str(img)  # Store modified tag

            # Log the change
            changes.append({
                "guideline": "img element missing alt attribute",
                "violation": "1.1.1.2",  # Example guideline code
                "before": before,
                "after": after,
                "linenumber": line_number
            })
        
            i += 1
    
    return changes

def remove_a_text(soup, html_file):
    changes = []

    num_to_inject = 4
    i = 0

    for a in soup.find_all('a'):
        if i > num_to_inject:
            break
        if len(list(a.children)) == 1:
            line_number = a.sourceline
            before = str(a)

            a.string = Comment("Text for anchor element removed")

            after = str(a)

            changes.append({
                "guideline": "anchor contains no text",
                "violation": "2.4.4.1",  # Example guideline code
                "before": before,
                "after": after,
                "linenumber": line_number
            })

            i += 1
    
    return changes

def remove_iframe_alt(soup, html_file):
    changes = []

    num_to_inject = 4
    i = 0

    for iframe in soup.find_all('iframe'):
        if i > num_to_inject:
            break
        if iframe.has_attr('title'):
            line_number = iframe.sourceline
            before = str(iframe)  # Store original tag
            del iframe['title']
            after = str(iframe)  # Store modified tag

            guideline = "iframe element missing alt attribute"
            # Log the change
            changes.append({
                "guideline": "iframe element missing alt attribute",
                "violation": "1.1.1.1",
                "before": before,
                "after": after,
                "linenumber": line_number
            })

            i += 1
    
    return changes

def update_label_input(soup, html_file):
    changes = []
    count = 0
    for input in soup.find_all('input'):
        if count > 9:
            break
        associated_label = soup.find('label', {'for': input.get('id')})

        if associated_label:
            if count % 2 == 0:
                line_number = associated_label.sourceline
                before = str(associated_label)
                id = input['id']
                associated_label.string = Comment("Text removed from input element \"{id}\" label")
                after = str(associated_label)

                changes.append({
                    "guideline": "input element has no text in label",
                    "violation": "1.3.1.1",
                    "before": before,
                    "after": after,
                    "linenumber": line_number
                })
            else:
                line_number = associated_label.sourceline
                before = str(associated_label)
                id = input['id']

                comment = Comment(f"""
                Label for input element \"{id}\" removed 
                """)

                associated_label.insert_before(comment)
                associated_label.decompose()
                after = f"<!--Label for input element \"{id}\" removed -->"

                changes.append({
                    "guideline": "input element is missing a label",
                    "violation": "1.3.1.2",
                    "before": before,
                    "after": after,
                    "linenumber": line_number
                })
            count += 1
        
        
    return changes

def update_label_select(soup, html_file):
    changes = []
    count = 0
    for select in soup.find_all('select'):
        if count > 9:
            break
        associated_label = soup.find('label', {'for': select.get('id')})

        if associated_label:
            if count % 2 == 0:
                line_number = associated_label.sourceline
                before = str(associated_label)
                id = select['id']
                associated_label.string = Comment(f"Text removed from select element \"{id}\" label")
                after = str(associated_label)

                changes.append({
                    "guideline": "select element has no text in label",
                    "violation": "1.3.1.3",
                    "before": before,
                    "after": after,
                    "linenumber": line_number
                })
            else:
                line_number = associated_label.sourceline
                before = str(associated_label)
                id = select['id']

                comment = Comment(f"""
                Label for select element \"{id}\" removed 
                """)

                associated_label.insert_before(comment)
                associated_label.decompose()
                after = f"<!--Label for select element \"{id}\" removed -->"

                changes.append({
                    "guideline": "select element is missing a label",
                    "violation": "1.3.1.3",
                    "before": before,
                    "after": after,
                    "linenumber": line_number
                })
            count += 1
        
        
    return changes

def update_label_button(soup, html_file):
    changes = []
    count = 0
    for button in soup.find_all('button'):
        if count > 4:
            break

        line_number = button.sourceline
        before = str(button)
        id = button['id']
        button.string = Comment(f"Text removed from button element \"{id}\"")
        after = str(button)

        changes.append({
            "guideline": "button element has no text in label",
            "violation": "1.3.1.5",
            "before": before,
            "after": after,
            "linenumber": line_number
        })
        
        count += 1
        
        
    return changes

def update_mouse_attr(soup, html_file):
    changes = []
    count = 0
    num_to_inject = 4

    for mouse in soup.find_all(True):
        if count > 4:
            break


        if mouse.has_attr('onmouseover') and mouse.has_attr('onfocus'):
            count += 1
            line_number = mouse.sourceline
            before = str(mouse)
            del(mouse['onfocus'])
            after = str(mouse)

            changes.append({
            "guideline": "onmouseover event handler missing onfocus event",
            "violation": "2.1.1.1",
            "before": before,
            "after": after,
            "linenumber": line_number
            }) 
        if mouse.has_attr('onmouseout') and mouse.has_attr('onblur'):
            count += 1
            line_number = mouse.sourceline
            before = str(mouse)
            del(mouse['onblur'])
            after = str(mouse)

            changes.append({
            "guideline": "onmouseout event handler missing onblur event",
            "violation": "2.1.1.2",
            "before": before,
            "after": after,
            "linenumber": line_number
            })          
        if mouse.has_attr('onmousedown') and mouse.has_attr('onkeydown'):
            count += 1
            line_number = mouse.sourceline
            before = str(mouse)
            del(mouse['onkeydown'])
            after = str(mouse)

            changes.append({
            "guideline": "onmousedown event handler missing onkeydown event",
            "violation": "2.1.1.3",
            "before": before,
            "after": after,
            "linenumber": line_number
            })
        


    return changes


def insert_marquee(soup, html_file):
    changes = []
    num_to_inject = 4
    i = 0

    for p in soup.find_all('p'):
        if i > num_to_inject:
            break

        line_number = p.sourceline
        before = str(p)  # Store original tag
        p.name = 'marquee'
        p['behavior'] = "scroll"
        p['direction'] = "left"
        after = str(p)  # Store modified tag

        # Log the change
        changes.append({
            "guideline": "marquee element used",
            "violation": "2.2.2.1",  # Example guideline code
            "before": before,
            "after": after,
            "linenumber": line_number
        })
        
        i += 1
    
    return changes