""" Set of valid SQL data types for column definitions. """
VALID_TYPES: set[str] = {
    "INT", "BIGINT", "SMALLINT", "TINYINT",
    "DECIMAL", "NUMERIC", "FLOAT", "REAL",
    "VARCHAR", "NVARCHAR", "CHAR", "NCHAR", "TEXT",
    "DATETIME", "DATE", "TIME", "DATETIME2",
    "BIT", "UNIQUEIDENTIFIER", "VARBINARY", "XML",
}

""" Set of SQL data types that require a length specification. """
TYPES_WITH_LENGTH: set[str] = {"VARCHAR", "NVARCHAR", "CHAR", "NCHAR", "DECIMAL", "NUMERIC"}

""" Maximum allowed length for a column name in SQL Server. """
MAX_COLUMN_NAME_LENGTH: int = 128

# ----- Utility Functions -----
def parse_data_type(data_type: str) -> tuple[str, int | None]:
    """Parses the data type string to extract the base type and length if present.
    Normalizes raw SQL data types into:
    'varchar(255)' → ('VARCHAR', 255)
    'int'          → ('INT', None)
    'DECIMAL(18,2)'→ ('DECIMAL', 18)   # Only keep the precision part for simplicity
    """
    cleaned_type = data_type.strip().upper()
    
    if "(" not in cleaned_type:
        return cleaned_type, None
    
    base = cleaned_type[:cleaned_type.index("(")]
    inside = cleaned_type[cleaned_type.index("(") + 1:cleaned_type.index(")")]
    #For types like DECIMAL(18,2), we only take the first part (precision)
    length = inside.split(",")[0].strip()

    if length.isdigit():
        return base, int(length)
    
    return base, None  # Return None if length is not a valid integer

def validate_column(column: dict) -> list[str]:
    """Validates a column definition dictionary and returns a list of error messages if any."""
    errors: list[str] = []
    
    # Validate column name
    name = column.get("name", "")
    if not name:
        errors.append("Column name is missing.")
    elif len(name) > MAX_COLUMN_NAME_LENGTH:
        errors.append(f"Column name '{name}' exceeds maximum length of {MAX_COLUMN_NAME_LENGTH}.")
    elif " " in name:
        errors.append(f"Column name '{name}' contains spaces, which is not allowed.")

    # Validate data type
    data_type = column.get("data_type", "")
    base_type, _ = parse_data_type(data_type) if data_type else ("", None)
    if not data_type:
        errors.append(f"Data type for column '{name}' is missing.")
    else:
        base_type, length = parse_data_type(data_type)
        if base_type not in VALID_TYPES:
            errors.append(f"Invalid data type '{base_type}' for column '{name}'.")
        elif base_type in TYPES_WITH_LENGTH and length is None:
            errors.append(f"Data type '{base_type}' for column '{name}' requires a length specification.")
    
    return errors

def normalize_columns(column: dict) -> dict:
    """
    Normalizes and cleans the data types of columns in the provided dictionary.
    Returns a new dictionary with normalized data types and lengths without modifying the original input.
    """
    data_type, length = parse_data_type(column.get("data_type", ""))

    if data_type in TYPES_WITH_LENGTH and length is None:
        if data_type in {"VARCHAR", "NVARCHAR"}:
            length = 255  # Default length for VARCHAR and NVARCHAR
        elif data_type in {"CHAR", "NCHAR"}:
            length = 1  # Default length for CHAR and NCHAR

    return {
        "name": column.get("name", "").strip(),
        "data_type": data_type,
        "length": length,
        "nullable": column.get("nullable", True),  # Default to True if not specified
        "default": column.get("default", None),
    }

def process_columns(raw_columns: list[dict]) -> tuple[list[dict], list[str]]:
    """
    Processes a list of column definitions, normalizing them and collecting any validation errors.
    Returns a tuple containing the list of normalized columns and a list of error messages.
    """
    normalized_columns = []
    errors = []

    for i, column in enumerate(raw_columns):
        col_errors = validate_column(column)
        if col_errors:
            column_name = f"Column '{column.get("name", f"column{i}")}'"
            for warning in col_errors:
                errors.append(f"{column_name}: {warning}")
            continue  # Skip adding this column to normalized_columns due to validation errors
        else:
            normalized_columns.append(normalize_columns(column))

    return normalized_columns, errors

def main()  -> None:
    """Main function to demonstrate column processing and validation."""
    raw_columns = [
        {"name": "CustomerID",      "data_type": "int",           "nullable": False},
        {"name": "Email Address",   "data_type": "varchar(255)",  "nullable": True},   # espace dans nom
        {"name": "CreatedAt",       "data_type": "datetime2",     "nullable": False},
        {"name": "",                "data_type": "INT",           "nullable": False},   # nom vide
        {"name": "Score",           "data_type": "DECIMAL(18,4)", "nullable": True},
        {"name": "Notes",           "data_type": "nvarchar",      "nullable": True},   # longueur manquante
        {"name": "Status",          "data_type": "MYSTERY_TYPE",  "nullable": False},  # type inconnu
        {"name": "IsActive",        "data_type": "BIT",           "nullable": False},
        {"name": "ProfilePicture",  "data_type": "VARBINARY(1024)","nullable": True},
        {"name": "Description",     "data_type": "TEXT",          "nullable": True},
        {"name": "CreatedBy",       "data_type": "VARCHAR(50)",   "nullable": False},
        {"name": "UpdatedAt",       "data_type": "DATETIME",      "nullable": True},
        {"name": "IsDeleted",       "data_type": "BIT",           "nullable": False},
        {"name": "LastLogin",       "data_type": "DATETIME2",     "nullable": True},
        {"name": "UserRole",        "data_type": "VARCHAR(20)",   "nullable": False},
        {"name": "ProfileURL",      "data_type": "NVARCHAR(2083)","nullable": True},  # longueur max URL
        {"name": "Bio",             "data_type": "TEXT",          "nullable": True},
        {"name": "Preferences",     "data_type": "XML",           "nullable": True},
        {"name": "SessionToken",    "data_type": "UNIQUEIDENTIFIER","nullable": False},
        {"name": "LastPurchaseDate","data_type": "DATE",          "nullable": True},
        {"name": "LoyaltyPoints",   "data_type": "INT",           "nullable": False},
        {"name": "ReferralCode",    "data_type": "CHAR(10)",      "nullable": True},
        {"name": "SubscriptionType","data_type": "VARCHAR(20)",   "nullable": False},
        {"name": "IsPremiumMember",  "data_type": "BIT",          "nullable": False},
        {"name": "ProfileVisibility","data_type": "VARCHAR(10)",  "nullable": False},
        {"name": "NotificationPrefs","data_type": "VARCHAR(50)",  "nullable": True},
        {"name": "ThemePreference",  "data_type": "VARCHAR(20)",  "nullable": True},
        {"name": "",                 "data_type": "",             "nullable": True},   # nom et type vide]
    ]
    normalized_columns, warnings = process_columns(raw_columns)

    if warnings:
        print(f"⚠️  {len(warnings)} warnings found :\n")
        for warning in warnings:
            print(f" ⚠️  {warning}")
        print()
    else:
        print("All columns are valid.")

    print(f"✅ {len(normalized_columns)} valid columns processed over {len(raw_columns)}.\n")
    print(f"  {'Name':<20} {'Data Type':<15} {'Length':<10} {'Nullable'}")
    print("  " + "-" * 55)
    for col in normalized_columns:
        lenght_str = str (col["length"]) if col["length"] is not None else "-"
        nullable_str = "YES" if col["nullable"] else "NO"
        print(f"  {col['name']:<20} {col['data_type']:<15} {lenght_str:<10} {nullable_str}")
        
if __name__ == "__main__":
    main()