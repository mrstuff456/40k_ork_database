import sqlite3

DATABASE = 'Orks.db'


def menu():
    '''
    This function is the menu that the user will be presented with that allows them to interact with the program
    and run the variuos functions that the program has.
    '''
    print("welcome to the 40k ork unit database.")
    print("please select an option:")
    print("0: exit the program")
    print("1: search for a unit by it's name.")
    user_input = input("")

    if user_input == "0":
        exit()
    elif user_input == '1':
        searchunitname()
    else:
        print("Please enter a valid input")
        menu()


def searchunitname():
    '''
    This function will allow the user to enter a search term and produce a list of units which name match the search
    the user will then be able to enter a number that corresponds to a unit and will produce the full stats for that unit
    '''
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
                        if user_input == "exit":
                            menu()
                        new_input = int(user_input)
                        break
                    except ValueError:
                        print('please enter a valid input')

                search = results[new_input - 1][0]
                print("")
                print("unit stats for", search)
                sql = f"SELECT * FROM unit WHERE name = '{search}'"
                cursor.execute(sql)
                results = cursor.fetchall()
                results = results[0]
                print("Unit ID:", results[0])
                print("Movement:", results[2])
                print("Toughness:", results[3])
                print("Save:", results[4])
                print("Wounds:", results[5])
                print("Leadership:", results[6])
                print("Objective Control:", results[7])
                print("")

                print("press enter to go back to menu, or type 'exit' to exit the program")
                user_input = input("")

                if user_input == "exit":
                    exit()
                else:
                    menu()

                

    if search == "exit":
        menu()


menu()
