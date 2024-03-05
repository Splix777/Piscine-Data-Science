import os


def main():
    print("""
Introduction
        
In the next two modules, you will see the role of a data engineer.
This second step is important to understand. The data engineer
"cleans" the data and transforms it in order to have data ready
to be analyzed by analysts/data scientists.

The next module involves data cleansing. This second step is
important to under-stand the data engineer "cleans" the data
and transforms it. The objective is to have data ready to be
analyzed by analysts/data scientists.

We are at the end of February 2022, it’s your first day in a
company selling items on the Internet. Before leaving on
a trip your boss gives you the sales of the last 4 months.
You will have to exploit them and propose solutions to
increase the turnover of the company.

Press Any Key to Continue""")

    exercise_script("""
Exercise 00: Create PostgreSQL Database
Files to submit: None
Allowed Functions: All

For this exercise you can use directly postgres
if installed in your campus or if you go through a
VM, otherwise you have to use docker compose.

•The username is your student login
•The name of the DB is piscineds
•The password is "mysecretpassword"

We must be able to connect to your postgres database with this command:

psql -U your_login -d piscineds -h localhost -W
mysecretpassword

Open another terminal and run the following command:
docker exec -it db bash
    
    Then run the following command:
    psql -U your_login -d piscineds -h localhost -W
    
    When prompted for a password, enter "mysecretpassword"

Press Any Key to Continue""")

    exercise_script("""
Exercise 01: Show me your DB
Files to submit: None
Allowed Functions: pgadmin, Postico, dbeaver or what you want to see the dbeasily

•Find a way to visualize the db easily with a software

•The chosen software must help you to easily find and
manipulate data using its own corresponding ID

Open a browser preferably chrome and go to the following address:
http://localhost:5050

Login with the following credentials:
email: admin@admin.com
password: 123

Press Any Key to Continue""")

    exercise_script("""
To connect to a PostgreSQL database, using pgadmin, you can follow the steps below:
•Click on the "Add New Server" button.
•Enter the following information in the General Tab:
    •Name: piscineds
•Enter the following information in the Connection Tab:
    •Host name/address: db
    •Port: 5432
    •Maintenance database: piscineds
    •Username: fsalazar
    •Password: mysecretpassword
•Click on the "Save" button.

Press Any Key to Continue""")

    exercise_script("""
Exercise 02: First table
Files to submit: table.*
Allowed Functions: All

•Create a postgres table using the data from a CSV from the ’customer’
folder. Name the tables according to the CSV’s name but without the file extension,
for example : "data_2022_oct"

•The name of the columns must be the same as the one in the CSV files and have
the appropriate type, beware you should have at least 6 different data types

•A DATETIME as the first column is mandatory

Press Any Key to Continue""")

    exercise_script("""
Exercise 03: Second table
Files to submit: automatic_table.*
Allowed Functions: All

•We are at the end of February 2022, you should be able to create tables with data
extracted from a CSV.
•Now, in addition, retrieve all the CSV from the ’customer’ folder automatically and
name the tables according to the CSV’s name but without the file extension, for
example : "data_2022_oct"

Below is an example of the expected directory structure:
$> ls -alR
total XX
drwxrwxr-x 2 eagle eagle 4096 Fev 42 20:42 .
drwxrwxr-x 5 eagle eagle 4096 Fev 42 20:42 ..
drwxrwxr-x 2 eagle eagle 4096 Jan 42 20:42 customer
drwxrwxr-x 2 eagle eagle 4096 Jan 42 20:42 items

./customer:
total XX
drwxrwxr-x 2 eagle eagle 4096 Fev 42 20:42 .
drwxrwxr-x 5 eagle eagle 4096 Fev 42 20:42 ..
-rw-rw-r-- 1 eagle eagle XXXX Mar 42 20:42 data_2022_dec.csv
-rw-rw-r-- 1 eagle eagle XXXX Mar 42 20:42 data_2022_nov.csv
-rw-rw-r-- 1 eagle eagle XXXX Mar 42 20:42 data_2022_oct.csv
-rw-rw-r-- 1 eagle eagle XXXX Mar 42 20:42 data_2023_jan.csv

./items:
...

Press Any Key to Continue""")

    exercise_script("""
Exercise 04: tems table
Files to submit: items_table.*
Allowed Functions: All

•You have to create the table "items" with the same columns as in the "item.csv" file
•You have to create at least 3 data types in the table

Below is an example of the expected directory structure:
$> ls -alR
total XX
drwxrwxr-x 2 eagle eagle 4096 Fev 42 20:42 .
drwxrwxr-x 5 eagle eagle 4096 Fev 42 20:42 ..
drwxrwxr-x 2 eagle eagle 4096 Jan 42 20:42 customer
drwxrwxr-x 2 eagle eagle 4096 Jan 42 20:42 items

./customer:
...

./items:
total XX
drwxrwxr-x 2 eagle eagle 4096 Fev 42 20:42 .
drwxrwxr-x 5 eagle eagle 4096 Fev 42 20:42 ..
-rw-rw-r-- 1 eagle eagle XXXX Mar 42 20:42 items.csv

Press Any Key to Continue""")

    exercise_script("""
Now that we've understood the exercise, let's start by creating the database.
This might take a while, so be patient.
Do you want to continue? (y/n) """)
    
    response = input()
    os.system("clear")
    if response == "y":
        os.system("python3 data-science-0/ex04/main.py")
    else:
        print("Goodbye")


def exercise_script(text: str):
    input()
    os.system("clear")

    print(text, end="")


if __name__ == "__main__":
    main()
