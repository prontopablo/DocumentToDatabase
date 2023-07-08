#!/usr/bin/python3

import os, json
import pandas as pd
import postgres
from uuid import uuid4
from supabase import create_client


def client():
    url: str = os.environ.get("URL")
    key: str = os.environ.get("KEY")
    return create_client(url, key)


def value_exists(roww, key, na_support=True, no_support=False, none_support=False):
    value = roww[key]
    result = value is None or pd.isna(value)

    if na_support:
        result = result or value == "NA"

    if no_support:
        result = result or value == "No"

    if none_support:
        result = result or value == "none"

    return not result


# Row value or default
def rvod(roww, key, default, na_support=True, no_support=False, none_support=False):
    if not value_exists(roww, key, na_support=na_support, no_support=no_support, none_support=none_support):
        return default
    return roww[key]

print("Reading input file")
data=pd.read_csv('input-data/nigels_sample_data_tivoli.tsv', sep='\t')

items_root = []
items_location_data = []
items_harvard_list_data = []
items_map_data = []
items_handbook_data = []
items_protected_monuments_data = []

print("Formatting and correcting data before insert")
for index, row in data.iterrows():
    internal_id = uuid4()

    alt_names = []
    if value_exists(row, "alt name 1"):
        alt_names.append(row["alt name 1"])

    if value_exists(row, "alt name"):
        alt_names.append(row["alt name"])

    notes = []
    if value_exists(row, "Notes"):
        notes.append(row["Notes"])

    photograph_links = None
    if value_exists(row, "links to photographs"):
        photograph_links = row["links to photographs"].split(";")

    items_root.append((
        str(internal_id),
        rvod(row, "Name", "TODO"),
        alt_names,
        None,
        None,
        rvod(row, "known damage (text)", None),
        notes,
        rvod(row, 'Period', "") + " : " + rvod(row, 'Period 2', ""),
        photograph_links,
        rvod(row, "damage bibliography? (reference or no)", None)
    ))

    items_location_data.append((
        str(internal_id),
        rvod(row, "town", None),
        rvod(row, "country", None),
        rvod(row, "region", None),
        rvod(row, "province", None),
        "point",
        []
    ))

    items_harvard_list_data.append((
        str(internal_id),
        rvod(row, "Harvard long list stars (0-4)", None),
        rvod(row, "Harvard long list text", None),
        rvod(row, "Harvard short list text", None)
    ))

    # Normalise No/Na/Null differences (Make them all null)
    acls_location_type = rvod(row, "ACLS map church/palace or house/monument/cultural institution or NA", None)

    # Remove uncertainty marker
    if acls_location_type is not None and acls_location_type.endswith("?"):
        acls_location_type = acls_location_type[0:len(acls_location_type)-1]

    items_map_data.append((
        str(internal_id),
        rvod(row, "ACLS map name or none", None, no_support=True),
        acls_location_type,
        rvod(row, "ACLS map stars (4-0)", None),
        rvod(row, "ACLS map grid reference", None),
        rvod(row, "ACLS map address", None, none_support=True),
        rvod(row, "ACLS map text", None),
        None,  # ACLS Map Links
        rvod(row, "CA Atlas map title/none", None, no_support=True),
        rvod(row, "CA Atlas church/palace ot house/monuments/cultural institutions", None),
        rvod(row, "CA Atlas stars (4-0)", None),
        rvod(row, "CA Atlas grid reference", None),
        rvod(row, "CA Atlas address", None, none_support=True),
        rvod(row, "CA Atlas text", None),
        None  # CA Map links
    ))

    zone_volume_items = rvod(row, "Zone HB vol no or none", "", no_support=True).split(" ")
    zone_volume_number = None
    zone_volume_text = None
    if zone_volume_items is not None and len(zone_volume_items) == 2:
        zone_volume_number = zone_volume_items[0]
        zone_volume_text = zone_volume_items[1]

    zone_aux_text = rvod(row, "Zone HB auxiliary list no or none", "No", no_support=False)
    zone_aux_bool = True if zone_aux_text == "Yes" else False

    items_handbook_data.append((
        str(internal_id),
        rvod(row, "CA Handbook 17A/17B/None", None, no_support=True),
        rvod(row, "CA HB church/palace or house/monument/cultural institution", None),
        rvod(row, "CA HB stars (4-0)", None),
        rvod(row, "CA HB address", None, none_support=True),
        rvod(row, "CA HB text", None),
        zone_volume_text,
        zone_volume_number,
        zone_aux_bool,
        rvod(row, "Zone HB text", None, no_support=True)
    ))

    items_protected_monuments_data.append((
        str(internal_id),
        rvod(row, "LPM (vol no or none)", None, no_support=True),
        rvod(row, "LPM stars (4-0)", None),
        rvod(row, "LPM military grid", None),
        rvod(row, "LPM text", None)
    ))

print("Connecting to the database")
connection = postgres.db_connect()

# Wipe all old rows, as we generate new IDs.
print("Cleaning old data")
postgres.wipe_database_table(connection, "items_root")
postgres.wipe_database_table(connection, "items_location_data")
postgres.wipe_database_table(connection, "items_harvard_list_data")
postgres.wipe_database_table(connection, "items_map_data")
postgres.wipe_database_table(connection, "items_handbook_data")
postgres.wipe_database_table(connection, "items_protected_monuments_data")
connection.commit()

print("Inserting rows")
# Insert rows
for item in items_root:
    postgres.insert_root_item(connection, item)

for item in items_location_data:
    postgres.insert_location_item(connection, item)

for item in items_harvard_list_data:
    postgres.insert_harvard_item(connection, item)

for item in items_map_data:
    postgres.insert_map_item(connection, item)

for item in items_handbook_data:
    postgres.insert_hb_data_item(connection, item)

for item in items_protected_monuments_data:
    postgres.insert_lpm_data(connection, item)

with open('out/out.json', 'w') as json_file:
    json_file.write(json.dumps(items_map_data, indent=2))

print("Closing db connection")
connection.close()

print("Done")
