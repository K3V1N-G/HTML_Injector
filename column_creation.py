import json

with open("changes_log.json", "r") as file:
    json_data = json.load(file)

line_nums = []
code_snippets = []

for key, nested_lists in json_data.items():  # Loop through dictionary values
            for inner_list in nested_lists:  # Extract first-level lists
                for entry in inner_list:  # Extract dictionaries inside the list
                    if "linenumber" in entry:
                        if "label_line" in entry:
                            line_nums.append([entry['linenumber'], entry['label_line']])
                        else:
                            line_nums.append(entry['linenumber'])
                    if "after" in entry:
                        code_snippets.append(repr(entry["after"]))
        



nums_file = "line_numbers.txt"
code_file = "code_snippets.txt"

with open(nums_file, "w") as file:
    file.write("\n".join(map(str, line_nums)))  # Convert numbers to strings and save

with open(code_file, "w") as file2:
    file2.write("\n".join(map(str, code_snippets)))