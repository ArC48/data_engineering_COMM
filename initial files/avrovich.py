from pprint import pprint

from fastavro import writer, reader, parse_schema
import json
#
# # Step 1: Define a simple JSON record
# json_data = [
#     {"name": "Alice", "age": 30, "city": "Berlin"},
#     {"name": "Bob", "age": 25, "city": "Paris"},
#     {"name": "Charlie", "age": 35, "city": "Rome"}
# ]
# """-----------------------------------------------------------------"""
#
# # Step 2: Define an Avro schema (as Python dict)
schema = {
    "type": "record",
    "name": "Person",
    "namespace": "elguja.avro",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "age", "type": "int"},
        {"name": "city", "type": "string"}
    ]
}
#
#
# # Step 3: Parse the schema
# parsed_schema = parse_schema(schema)
#
# pprint(parsed_schema)
#
#
# # Step 4: Write the data to an Avro file
# avro_filename = "people.avro"
# # WB means - Write Binary
# with open(avro_filename, "wb") as out:
#     writer(out, parsed_schema, json_data)
#
#
# print(f"✅ Avro file '{avro_filename}' created successfully.\n")
#

avro_filename = "people.avro"
# RB = Read Binary
# FO = File Out
with open(avro_filename, "rb") as fo:
    records = reader(fo)



# Step 6: Extract the schema from an existing Avro file
with open(avro_filename, "rb") as fo:
    avro_reader = reader(fo)
    extracted_schema = avro_reader.writer_schema


print("\n🧩 Extracted Schema:")
print(json.dumps(extracted_schema, indent=2))
