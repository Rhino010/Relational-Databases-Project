from connect_mysql import connect_database

# Initialize a User class
class User:
    def __init__(self, library_id, name):
        self.__library_id = library_id
        self.__name = name
        self.borrowed_books = []
# Method to set an user id
    def set_id(self, new_library_id):
        self.__library_id = new_library_id
# Method to get the library id
    def get_id(self):
        return self.__library_id
# Method to set user name
    def set_name(self, new_name):
        self.__name = new_name
# Method to return the value of the user's name
    def get_name(self):
        return self.__name
# Accesses self.borrowed_books to be recalled for the user
    def get_users_books(self):
        return self.borrowed_books
# Method to add to the list of borrowed books
    def add_to_borrowed(self, book):
        self.borrowed_books.append(book)

    def remove_borrowed_book(self, book):
        self.borrowed_books.remove(book)
    
conn = connect_database()
cursor = conn.cursor()
# Declared user variable as a dictionary to track users and information about the user
users = {}

# Function to prompt the user for a user's information
def add_user():
    try:
        user_name = input("Please enter the user's name:\n")
        library_id = int(input("Please give the user's ID number:\n"))
        query = "INSERT INTO users (name, library_id) VALUES (%s, %s)"
        cursor.execute(query, (user_name, library_id))
        conn.commit()
        new_user = User(library_id, user_name)
        users[library_id] = new_user
        print(f"User with ID: {library_id} and Name: {user_name} has been added.")
    except ValueError:
        print("User ID must be a number.")
# Function to print out all of a selected user's information
def view_user_details():
    try:
        user_id = int(input("What is the users ID number?\n"))
        if user_id in users:
            user_obj = users[user_id]
            print(f"User found, ID: {user_obj.get_id()}, Name: {user_obj.get_name()}, Checked out books: {user_obj.get_users_books()}")
    except ValueError:
        print("User ID must be a number.")
# Function to print out all users currently held in the user dictionary
def show_all_users():
    if not users:
        print("There are no users at this time.")
    else:
        for id, user_obj in users.items():
            print(f"User ID: {id}, Name: {user_obj.get_name()}, Borrowed Books: {user_obj.get_users_books()}")

# Function to add a book to each instance of a user when checking out a book with the given user's id number
def user_borrowed_books(book):
    try:
        user_id = int(input("Please give the user's ID number:\n"))
        if user_id not in users:
            print("That user does not exist.")
        else:
            user_obj = users[user_id]
            user_obj.add_to_borrowed(book)
            print(f"{book} has been successfully checked out. Enjoy!")
    except ValueError:
        print("User ID must be a number.")

def user_book_return(book):
    try:
        user_id = int(input("Pleae give the user's ID number:\n"))
        if user_id not in users:
            print("That user does not exist.")
        else:
            user_obj = users[user_id]
            user_obj.remove_borrowed_book(book)
            print(f"{book} has been successfully returned. Thank you!")
    except ValueError:
        print("User ID must be a number.")

def check_valid_user(user_id):
    check_query = f"SELECT id FROM users WHERE id = {user_id}"
    cursor.execute(check_query)
    user = cursor.fetchone()
    return user




