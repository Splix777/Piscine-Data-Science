import os


if __name__ == "__main__":
    print(
        """
        What is a piscine?
        
        Much like the selection piscine, the project is split in
        many smaller projects (modules), and with each day a
        new notion on the language/paradigm/technology
        you chose to workon. Validating a piscine requires more than
        just a day or two of investment. To ensure that this
        piscine is done correctly, it is recommended that you take
        note of everything listed below:•You can’t validate the
        piscine if you work only on one or two projects.
        
            •Trying to turn in every day: even if something isn’t finished,
            it’s better to try and turn it in.•At least one week of work:
            going into the piscine shouldn’t be taken lightly.
            
            •Each initialized depot will be automatically closed after
            one day.
            
            •You have two days to complete the required peer-evaluations
            in each module.•It is possible to retry your modules without waiting.
            
        What is your username? """,
        end="",
    )
    user = input()
    os.system("clear")

    print(f"""    Which Module are you evaluating {user}?
        1. Data Engineering & Data Warehouse
        2. Data Analyst
        3. Data Science part 1
        4. Data Science part 2
        Select a module: """, end="")

    module = int(input())
    os.system("clear")

    if 1 <= module <= 4:
        os.system(f'python3 ./data-science-{module}/main.py')
    else:
        print("Invalid module selection. Please select a module between 1 and 5.")

