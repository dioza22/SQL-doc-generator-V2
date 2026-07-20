
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
        {"name": "CustomerID",  "data_type": "INT",      "nullable": False, "length": None},
        {"name": "Email",       "data_type": "VARCHAR",  "nullable": True,  "length": 255},
        {"name": "CreatedAt",   "data_type": "DATETIME", "nullable": False, "length": None},
        {"name": "PhoneNumber", "data_type": "VARCHAR",  "nullable": True,  "length": 20},
        {"name": "IsActive",    "data_type": "BIT",      "nullable": False, "length": None},
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

if __name__ == "__main__":
        main()