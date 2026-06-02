name:str = "Mamadou"
age:int = 30
is_active:bool = True

print(f"My name is {name}, I am {age} years old and my active status is {is_active}.")
print(f"Type of name is {type(name)}, type of age is {type(age)}, and type of is_active is {type(is_active)}.")

username:str = input("Enter your user name:")
print(f"Hello, {username}!")
age_input:str = input("Enter your age:")
try:
    age:int = int(age_input)
    print(f"You are {age} years old.")
except  ValueError:
    print("Invalid input for age. Please enter a number.")

def describe_column(column_name:str, data_type:str, is_nullable:bool) -> str:
    nullable_status:str = "NULL" if is_nullable else "NOT NULL" 
    return f"{column_name:<20} {data_type:<15} {nullable_status}"

def get_column_from_user() -> tuple[str, str, bool]:
    name = input("Enter column name: ")
    data_type = input("Enter data type: ")
    nullable_input = input("Is the column nullable? (y/n): ").strip().lower()
    is_nullable = nullable_input in ["y", "yes"]
    return name, data_type, is_nullable

def main() -> None:
    columns = [
        ("id", "INT", False),
        ("name", "VARCHAR(255)", False),
        ("email", "VARCHAR(255)", True),
        ("created_at", "TIMESTAMP", False),
        ("created_by", "VARCHAR(255)", False)
    ]

    print(f"{'Column Name':<20} {'Data Type':<15} {'Nullable'}")
    print("-" * 50)
    for column in columns:
        print(describe_column(*column))
    
    name, data_type, is_nullable = get_column_from_user()
    print("\n-----SQL Documentation Generator V2.0-----")
    print(f"{'Column Name':<20} {'Data Type':<15} {'Nullable'}")
    print("-" * 50)
    print(describe_column(name, data_type, is_nullable))

if __name__ == "__main__":    
    main()