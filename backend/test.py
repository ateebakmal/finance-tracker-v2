print("running this file")
name = "uq__categories__profile_id__category_name_lower"
parts = name.split("__")
        
print(parts)
table,cols = parts[1], parts[2:]
print(table)
print(f'{table} with this {" ".join(cols)} already exists')