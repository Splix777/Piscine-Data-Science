import os


def main():
    print("""
Introduction

ETL, which stands for extract, transform and load, is a data integration process that
combines data from multiple data sources into a single, consistent data store that is
loaded into a data warehouse

Data Source  Data Source
|           |
    |           |
    |           |
    V           V
    ETL Process
    |           |
    |           |
    |           |
    V           V
Data Warehouse  Data Warehouse

Press Any Key to Continue""")

    exercise_script("""
Exercise 00: Show me your DB
Files to submit: None
Allowed Functions: pgadmin, Postico, dbeaver or what you want to see the dbeasily

•Find a way to see the db easily with a software

•The software chosen must be easy to file and to use for the search of an ID

Press Any Key to Continue""")

    exercise_script("""
Exercise 01: customers table
Files to submit: customers_table.*
Allowed Functions: All

•You have to join all the data_202*_*** tables together in a table called "customers"

Press Any Key to Continue""")

    exercise_script("""
Exercise 02: remove duplicates
Files to submit: remove_duplicates.*
Allowed Functions: All

•You must delete the duplicate rows in the "customers" table.

For exemple:
event_time           event_type        product_id
2022-10-01 00:00:32, remove_from_cart, 5779403
2022-10-01 00:00:33, remove_from_cart, 5779403

Press Any Key to Continue""")

    exercise_script("""
Exercise 03: fusion
Files to submit: fusion.*
Allowed Functions: All

•You must combine the "customers" tables with "items" in the "customers" table

Press Any Key to Continue""")

    print("Do you want to run the exercises? (y/n)")
    response = input()
    os.system("clear")
    if response == "y":
        os.system("python3 data-science-1/ex03/warehouse/main.py")
    else:
        print("Goodbye")


def exercise_script(text: str):
    input()
    os.system("clear")

    print(text, end="")


if __name__ == "__main__":
    main()
