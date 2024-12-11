from connect_mysql import connect_database
from user import check_valid_user
from datetime import date, datetime

conn = connect_database()
cursor = conn.cursor()

# Creation of a class named Book to hold a books title, the author, the genre, the publication year, and set its original
# availability to True under the assumption that a book will not be entered into the program until they have it.
class Book:
    def __init__(self, title, author_id, isbn, publication_date):
        self.__title = title
        self.__author_id = author_id
        self.__isbn = isbn
        self.__publication_date = publication_date
        self.availability = True
# Retrieves the title from an instance of the Book class
    def get_title(self):
        return self.__title
# Retrieves an author from a Book class instance
    def get_author(self):
        return self.__author_id
# Retrieves book isbn for 
    def get_isbn(self):
        return self.__isbn
# Retrieves the publication year from a Book class instance
    def get_publication_year(self):
        return self.__publication_date
# Method to toggle the availability of a book when called without needing explicit True or False inputs from user
    def set_availability(self):
        if not self.availability:
            self.availability = True
        else:
            self.availability = False
# Method to return a specific books avaialability. False means unavailable while True is available.
    def get_availability(self):
        return self.availability
# Method to display all books from a given instance.
    def show_all_books(self):
        if self.availability == True:
            print(f"Title: {self.__title}, Author: {self.__author_id}, ISBN: {self.__isbn}, Publish Year: {self.__publication_date}, Available: 'YES'")
        else:
            print(f"Title: {self.__title}, Author: {self.__author_id}, ISBN: {self.__isbn}, Publish Year: {self.__publication_date}, Available: 'NO'")
    

# Function to add a book to library_books dictionary
def add_book():
    title = input("What is the title of the book?\n")
    author_id = int(input("What is the corresponding author id number?\n"))
    isbn = int(input("What is the ISBN number of this book?\n"))
    publication_date = input("What is the publication date as (YYYY-MM-DD)?\n")
    new_book = Book(title, author_id, isbn, publication_date)
    query = "INSERT INTO books (title, author_id, isbn, publication_date, availability) VALUES (%s ,%s, %s, %s, True)"
    cursor.execute(query, (title, author_id, isbn, publication_date))
    conn.commit()
    print(f"'{title}' has been successfully added.")

# Function to reset a books availability to False in the library_books dictionary
def borrow_book(book_id):
    book_check_query = "SELECT id, title FROM books WHERE id = %s AND availability = 1"
    cursor.execute(book_check_query, (book_id, ))
    book = cursor.fetchone()
    if book:
        print(book)
        choice = input(f"{book[1]}, with book ID {book[0]}, is currently available to check out. Would you like to rent this? Type 'Yes' or 'No'.").lower()
        if choice == 'yes':
            try:
                user_id = int(input("Enter the user's ID:\n"))
                if check_valid_user(user_id):
                    today = input("Enter today's date as 'YYYY-MM-DD'\n")
                    update_borrowed_books = f"INSERT INTO borrowed_books (user_id, book_id, borrow_date) VALUES ({user_id}, {book[0]}, {today})"
                    cursor.execute(update_borrowed_books)
                    conn.commit()
                    print(f"User with ID {user_id} has successfully checked out {book[1]}")
                else:
                    print("There is no user with that ID, please try again.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Transaction canceled")        
    else:
        print("That particular book is currently unavailable.")
# Function to set the availability to True for a book after function is called
def return_book(book):
    try:
        if book in library_books and library_books[book].get_availability() == False:
            library_books[book].set_availability()
        elif book not in library_books:
            print("Sorry that book does not belong to this library.")
    except Exception as e:
        print(f"Error occurred: {e}")
# Function to finc a particular book in the dictionary library_books and show whether it is currently available or not.
def find_book():
    try:
        book = input("What is the book title?\n")
        if book in library_books and library_books[book].get_availability() == True:
            print(f"Book: {book}, Available to check out: 'YES' ")
        elif book in library_books and library_books[book].get_availability() == False:
            print(f"Book: {book}, Available to check out: 'NO' ")
        else:
            print("This library does not carry that title.")
    except Exception as e:
        print(f"Error occurred: {e}")
# Function to print out all the books in the library_books dictionary and display all books with all information had on them.
def show_all_books():
    if not library_books:
        print("No books currently in the library.")
    else:
        print("\nHere is a list of books we keep:")
        for book in library_books.values():
            book.show_all_books()



