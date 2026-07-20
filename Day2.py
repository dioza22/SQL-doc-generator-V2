from datetime import datetime
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