import sqlite3

DATABASE = 'Orks.db'


def menu():
    '''
    This function is the menu that the user will be presented with that allows them to interact with the program
    and run the variuos functions that the program has.
    '''
    #present the user with the possible function options.
    print("welcome to the 40k ork unit database.")
    print("please select an option:")
    print("0: exit the program.")
    print("1: search for a unit by it's name.")
    print("2: Print out all data in the database.")
    print("3: print all data in the database sorted by a certain stat.")
    #take the user's option
    user_input = input("")

    #check the user input and run the corresponding function
    if user_input == "0":
        exit()
    elif user_input == '1':
        searchunitname()
    elif user_input == '2':
        printall()
    elif user_input == '3':
        printallsorted()
    #deny any input that does not fit within any option above and rerun the menu command
    else:
        print("Please enter a valid input")
        menu()

def searchunitname():
    '''
    This function will allow the user to enter a search term and produce a list of units which name match the search
    the user will then be able to enter a number that corresponds to a unit and will produce the full stats for that unit
    '''
    #promt the user to input a search term in which will be run through the database
    search = input("Please enter your search term or type 'exit' to cancel: ")
    if search != "exit":
        with sqlite3.connect(DATABASE) as db:
            #set the sql query
            cursor = db.cursor()
            sql = f"SELECT name FROM unit WHERE name LIKE '%{search}%'"
            cursor.execute(sql)
            results = cursor.fetchall()
            #allow the user to retry if no results are found
            if not results:
                print(f"Sorry, there were no units matching '{search}'")
                searchunitname()
            else:
                #format the data in a way that looks good and assign a number to each result
                counter = 1
                for i in results:
                    print(f"| {counter:<2} | {i[0]:<40}|")
                    counter += 1

                print("To bring up full unit data, enter the number that coresponds to the desired unit, or type 'exit' to cancel:")
                while True:
                    try:
                        #promt the user to select a unit's name by inputting the number assigned next to it
                        user_input = input("")
                        if user_input == "exit":
                            menu()
                        new_input = int(user_input)
                        break
                    except ValueError: #catch the code from breaking if the user does not input ann integer
                        print('please enter a valid input')

                # print out the selceted unit's results in a nice way for the user to read
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

                #promt the user with options of waht do do now
                print("press enter to go back to menu, or type 'exit' to exit the program")
                user_input = input("")

                #exit the program if the usser types 'exit'
                if user_input == "exit":
                    exit()
                else:
                    menu()

                

    if search == "exit":
        menu()

def printall():
    '''
    This function will print out everything inside of the database and format/print the data in a nice way.
    '''
    #connect to; the database
    with sqlite3.connect(DATABASE) as db:
        #set up the SQL statement
        cursor = db.cursor()
        sql = "SELECT * FROM unit;"
        #execute the sql query
        cursor.execute(sql)
        #fetch the results of the sql query
        results = cursor.fetchall()
        #print the results in a nice format
        print("| ID | Name                                    | M  | T  | SV | W  | LD | OC |")
        print("------------------------------------------------------------------------------")
        for result in results:
            print(f"| {result[0]:<3}| {result[1]:<40}| {result[2]:<3}| {result[3]:<3}| {result[4]:<3}| {result[5]:<3}| {result[6]:<3}| {result[7]:<3}|")
        #promt the user with the option to return to enu or eit the program
        user_input = input("Press enter to go back to menu, or type 'exit' to exit the program:")
        #exit the program if the user types 'exit'
        if user_input == 'exit':
            exit()
        menu()

def printallsorted():
    '''
    This function will promt the user with a choice of stat and ascending and descending category, the program will then
    print all data in the database in the format of that sorted stat
    '''
    #connect to the database
    with sqlite3.connect(DATABASE) as db:
        #promt the user
        user_input = input("what stat do you want the data to be sorted by? (Name, M, T, S, W, LD, OC)")
        user_input = user_input.capitalize()

        #set the input given by the user to the corresponding collum name
        while True:
            if user_input == 'Name':
                stat = 'name'
                break
            elif user_input == 'M':
                stat = 'movement'
                break
            elif user_input == 'T':
                stat = 'toughness'
                break
            elif user_input == 'S':
                stat = 'save'
                break
            elif user_input == 'W':
                stat = 'wounds'
                break
            elif user_input == 'LD':
                stat = 'leadership'
                break
            elif user_input == 'OC':
                stat = 'objective control'
                break
            else:
                #deny any invalid input and let the user try again
                print("Please enter a valid input (Name, M, T, S, W, LD, OC)")
                user_input = input("")
        #ask the user in which order they want the data sorted
        user_input = input("Do you want it to be sorted ascending (lowest to highest) or desending? (highest to lowest) (A/D).")
        user_input = user_input.capitalize()
        while True:
            #set the user input to its SQL counterpart
            if user_input == 'A':
                order = 'ASC'
                break
            elif user_input == 'D':
                order = 'DESC'
                break
            else:
                print("Please enter a valid input. (A/D)")
                user_input = input("")
        #initialise the SQL query
        cursor = db.cursor()
        sql = f"SELECT * FROM unit ORDER BY {stat} {order};"
        #execue the sql query and get its results
        cursor.execute(sql)
        results = cursor.fetchall()
        #print the data in a nice readable way
        print("| ID | Name                                    | M  | T  | SV | W  | LD | OC |")
        print("------------------------------------------------------------------------------")
        for result in results:
            print(f"| {result[0]:<3}| {result[1]:<40}| {result[2]:<3}| {result[3]:<3}| {result[4]:<3}| {result[5]:<3}| {result[6]:<3}| {result[7]:<3}|")
        user_input = input("Press enter to go back to menu, or type 'exit' to exit the program:")

        if user_input == "exit":
            exit()
        else:
            menu()

#call the menu function to start the code
menu()
