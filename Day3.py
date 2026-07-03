
columns = ["user_id","name","created_at","phone","email"]

print(columns[0])
print(columns[-1])

print(columns[1:3])
print(columns[2:])
print(columns[1:4])
print(columns[:3])

columns.append("address")
columns.insert(2,"updated_at")
columns.remove("email")
popped = columns.pop()
print(len(columns))
print("email" in columns)
print(columns)

columns.sort()
sorted_copy = sorted(columns)
print(sorted_copy)
print(columns)

for col in columns:
    print(col)

for i, col in enumerate(columns):
    print(f"{i} | {col}")

column = {
    "name": "user_id",
    "data_type": "INT",
    "nullable": "FALSE",
    "length": "None",
    "identity": "TRUE",
    "description": "The unique user identity"

}

print(column["name"])
print(column.get("data_type"))
print(column.get("default", "N/A"))

column["identity"] = "FALSE"
column["default"] = "GETDATE()"

print("data_type" in column)
print("default_value" in column)

for key in column:
    print(key)

for key, value in column.items():
    print(f"{key} : {value}")

print(list(column.keys()))
print(list(column.values()))

del column["description"]
removed = column.pop("identity")

columns = [
    {"name": "CustomerID", "data_type": "INT", "nullable": "FALSE", "length": "None", "identity": "TRUE", "description": "The unique customer id"},
    {"name": "Email", "data_type": "VARCHAR", "nullable": "TRUE", "length": "255", "identity": "FALSE", "description": "The user email"},
    {"name": "Name", "data_type": "VARCHAR", "nullable": "TRUE", "length": "255", "identity": "FALSE", "description": "The user name"},
    {"name": "Phone", "data_type": "VARCHAR", "nullable": "TRUE", "length": "20", "identity": "FALSE", "description": "The user phone number"},
    {"name": "user_id", "data_type": "INT", "nullable": "FALSE", "length": "None", "identity": "TRUE", "description": "The unique user id"},
    {"name": "Address", "data_type": "VARCHAR", "nullable": "TRUE", "length": "255", "identity": "FALSE", "description": "The user address"},
    {"name": "IsActive", "data_type": "BIT", "nullable": "FALSE", "length": "None", "identity": "FALSE", "description": "Define the status of user"}
]

#Filter not nullable columns
not_nullable = [col for col in columns if not col["nullable"]]
varchar_columns = [col for col in columns if col["data_type"]=="VARCHAR"]

#Tansformer .Select() in LINQ
names_only = [col["name"] for col in columns]
print(names_only)

#Filter with transformers .Select with .Where() in LINQ
nullable_names = [col["name"] for col in columns if col["nullable"]]
print(nullable_names)

#Sort by key
sorted_columns = sorted(columns, key=lambda col: col["name"])
sorted_by_type = sorted(columns, key=lambda col: (col["data_type"], col["name"]))

print(sorted_columns)

print(sorted_by_type)

#Counting
nullable_count = sum(1 for col in columns if col["nullable"]=="TRUE")
print(f"{nullable_count} columns are nullable of {len(columns)} total columns")

def format_data_type(data_type:str, length:str | None) -> str:
    """Formats the SQL data type with length if provided."""
    if length is not None and length != "None":
        return f"{data_type}({length})"
    return data_type

def generate_columns_table(columns:list[dict]) -> str:
    """Generates a formatted table of columns from a list of dictionaries 
    representing table columns and returns a complete Markdown table.
    """
    #Header of the table
    header = f"| {'Column name':<25} | {'Data type':<15} | {'Nullable':<10} |"
    separator = f"|{'-'*27}|{'-'*17}|{'-'*12}|"

    #Rows of the table
    rows = []
    for col in columns:
        data_type_formatted = format_data_type(col["data_type"], col.get("length"))
        null_str = "YES" if col["nullable"] == "TRUE" else "NO"
        row = f"| {col['name']:<25} | {data_type_formatted:<15} | {null_str:<10} |"
        rows.append(row)

    # Combine all parts into the final table
    table = "\n".join([header, separator] + rows)
    return table

def generate_table_summary(table_name:str, columns:list[dict]) -> str:
    """Generates a summary of the table stats including the table name, total columns, and nullable columns."""
    total_columns = len(columns)
    nullable_count = sum(1 for col in columns if col["nullable"] == "TRUE")
    not_nullable = total_columns - nullable_count
    varchar_count = sum(1 for col in columns if col["data_type"] == "VARCHAR")
    lines = [
        f"**Total columns:** : {total_columns} ",
        f"**Nullable columns:** : {nullable_count} | **Not nullable columns:** : {not_nullable} ",
        f"**VARCHAR columns:** : {varchar_count} "
    ]
    return "\n".join(lines)

def main():
    columns = [
        {"name": "CustomerID",  "dtype": "INT",      "nullable": False, "length": None},
        {"name": "Email",       "dtype": "VARCHAR",  "nullable": True,  "length": 255},
        {"name": "CreatedAt",   "dtype": "DATETIME", "nullable": False, "length": None},
        {"name": "PhoneNumber", "dtype": "VARCHAR",  "nullable": True,  "length": 20},
        {"name": "IsActive",    "dtype": "BIT",      "nullable": False, "length": None},
    ]
    print("## Sales.Customers\n")
    print(generate_table_summary("Customers", columns))
    print()
    print(generate_columns_table(columns))
    print()

    # Bonus : afficher uniquement les colonnes nullable
    nullable_cols = [c for c in columns if c["nullable"]]
    print(f"\n### Colonnes nullable ({len(nullable_cols)})\n")
    print(generate_columns_table(nullable_cols))