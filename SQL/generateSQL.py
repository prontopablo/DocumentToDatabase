import uuid

with open('inputForSQL.txt', 'r') as f:
    lines = f.readlines()

# initialize variables to hold data
region = ""
province = ""
town = ""
name = ""
harvard_short_list_text = ""

with open('output.sql', 'w', encoding='utf-8') as out:
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # check if line has the expected format
        if ": " not in line:
            if harvard_short_list_text:
                # concatenate multi-line harvard_short_list_text
                harvard_short_list_text += " " + line.replace("'", "''")
            else:
                print(f"Skipping invalid line: {line}")
            continue

        key, value = line.split(": ", 1)  # limit the split to only one occurrence of ": "
        if key == "Name":
            name = value.replace("'", "''")
        elif key == "Region":
            region = value.replace("'", "''")
        elif key == "Province":
            province = value.replace("'", "''")
        elif key == "Town":
            town = value.replace("'", "''")
        elif key == "harvard_short_list_text":
            # concatenate multi-line harvard_short_list_text
            harvard_short_list_text = value.replace("'", "''")
            while True:
                if not lines:
                    break
                next_line = lines.pop(0).strip()
                if not next_line or next_line[0].isalpha():
                    break
                harvard_short_list_text += " " + next_line.replace("'", "''")

            if not harvard_short_list_text:
                harvard_short_list_text = "NULL"
            else:
                harvard_short_list_text = "'" + harvard_short_list_text + "'"

            # generate UUID for site
            id = str(uuid.uuid4())

            # write SQL INSERT statement to output file for items_root table
            out.write(f"INSERT INTO items_root (internal_id, name) VALUES ('{id}', '{name}');\n")
            
            # insert new rows in items_location_data, items_harvard_long_list, items_map_data, items_handbook_data, and items_protected_monuments_data tables
            out.write(f"INSERT INTO items_location_data (id, town, region, province) VALUES ('{id}', '{town}', '{region}', '{province}');\n")
            out.write(f"INSERT INTO items_harvard_list_data (id, short_list_text) VALUES ('{id}', {harvard_short_list_text});\n")
            out.write(f"INSERT INTO items_map_data (id) VALUES ('{id}');\n")
            out.write(f"INSERT INTO items_handbook_data (id) VALUES ('{id}');\n")
            out.write(f"INSERT INTO items_protected_monuments_data (id) VALUES ('{id}');\n")
