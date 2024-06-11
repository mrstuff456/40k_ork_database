import sqlite3

DATABASE = 'Orks.db'


def menu():
    print("welcome to the 40k ork unit database.")
    print("please select an option:")
    print("1: search for a unit by it's name.")
    user_input = input("")

    if user_input == '1':
        searchunitname()


def searchunitname():
    search = input("Please enter your search term or type 'exit' to cancel: ")
    if search != "exit":
        with sqlite3.connect(DATABASE) as db:
            cursor = db.cursor()
            sql = f"SELECT name FROM unit WHERE name LIKE '%{search}%'"
            cursor.execute(sql)
            results = cursor.fetchall()

            if not results:
                print(f"Sorry, there were no units matching '{search}'")
                searchunitname()
            else:
                counter = 1
                for i in results:
                    print(f"| {counter:<2} | {i[0]:<40}|")
                    counter += 1

                print("To bring up full unit data, enter the number that coresponds to the desired unit, or type 'exit' to cancel:")
                while True:
                    try:
                        user_input = input("")
                        new_input = int(user_input)
                        break
                    except ValueError:
                        print('please enter a valid input')

                search = results[new_input - 1][0]
                print("")
                print(search)
                sql = f"SELECT * FROM unit WHERE name = '{search}'"
                cursor.execute(sql)
                results = cursor.fetchall()
                

    if search == "exit":
        menu()


menu()
