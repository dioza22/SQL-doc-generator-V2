from datetime import datetime

#Cleaning up whitespace from strings

raw:str = "  user_id  "

print(raw.strip())
print(raw.lstrip())
print(raw.rstrip())

#Case sensitivity in strings

col:str = "CreatedAt"

print(col.lower())
print(col.upper())

#Searching for substrings

dtype:str = "VARCHAR(255)"

print(dtype.find("CHAR"))
print(dtype.startswith("VAR"))
print(dtype.endswith("55)"))
print(dtype.count("A"))
print("RCH" in dtype)

#Replacement
messy:str = "  user__id__column  "

print(messy.replace("__", "_").strip())

# ---Splitting strings---
csv_line:str = "id,name,email,created_at,created_by"

parts:list[str] = csv_line.split(",")

print(parts)
print(f"{parts[0]} | {parts[1]} | {parts[2]} | {parts[3]} | {parts[4]} | {parts[-1]}")

#-------------------------------------------#

col_name:str = "created_at"
col_type:str = "DATETIME"
col_len:int = 255
col_price:float = 1000.222

#Formatting strings with f-strings
print(f"{col_name:<20}")
print(f"{col_name:>20}")
print(f"{col_name:^20}")

#Number formatting
print(f"{col_len:05d}")
print(f"{col_price:.2f}")
print(f"{col_price:,.3f}")

#Combined
print(f"{col_name:<20} | {col_type:<15} | {col_len:>5} ")

#Division in Python
print(f"Division 10 / 3 = {10/3:.5f}")
print(f"Floor division  10 // 3 = {10//3}")
print(f"Modulo 10 % 3 = {10%3}")
print(f"Power 2**10= {2**10}")

#Type conversion
print(int("1987"))
print(float("1987.22"))
print(str(1987))
print(int(1987.22))

#Secure type conversion with try-except
raw:str = "  1987 "
if raw.strip().isdigit():
    length:int = int(raw.strip())
    print(f"Length is : {length}")

#--------------------------------#

def generate_report_header (db_name:str, server:str, schema_count:int) -> str:
    timestamp:str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    lines = [
        f"Documentation Report for Database: {db_name.upper()}",
        "",
        f"**Server** : {server}",
        f"**Schemas analysed** : {schema_count}",
        f"**Generated at** : {timestamp}",
        "",
        "____",
        ""
    ]
    return "\n".join(lines) 

def generate_table_header (table_name:str, schema_name:str, column_count:int) -> str:
    lines = [
        f"{schema_name}.{table_name}",
        "",
        f"**Columns** : {column_count:,}",
        "",
        f"| {'Column Name':<25} | {'Type':<15} | {'Nullable':<10} |",
        f"|{'-' * 27}|{'-' * 17}|{'-'*12}|",
    ]
    return "\n".join(lines)

def generate_column_doc (column_name:str, data_type:str, is_nullable:bool) -> str:
    nullable_status:str = "NULL" if is_nullable else "NOT NULL"
    return f"| {column_name:<25} | {data_type:<15} | {nullable_status:<10} |"

def main() -> None:
    db_name:str = "AdventureWorks"
    server:str = "SQL_PROD_01"
    schema_count:int = 5
    print(generate_report_header(db_name, server, schema_count))
    print(generate_table_header("Employee", "HumanResources", 125))
    print(generate_column_doc("EmployeeID", "INT", False))
    print(generate_column_doc("EmployeeName", "VARCHAR(255)", True))
    print(generate_column_doc("Address", "VARCHAR(255)", True))
    print(generate_column_doc("DateOfBirth", "Date", True))
    print(generate_column_doc("SSN", "VARCHAR(255)", False))
    print(generate_column_doc("MaritalStatus", "VARCHAR(255)", False))

if __name__ == "__main__":
    main()