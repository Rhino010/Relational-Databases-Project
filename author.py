from connect_mysql import connect_database

conn = connect_database()
cursor = conn.cursor()
# Creating a class named authors to hold author names and short bios about them
class Author:
    def __init__(self, name, bio):
        self.__name = name
        self.__bio = bio
# Method to set the author's name
    def set_name(self, new_name):
        self.__name = new_name
# Method to retrieve the authors name from an instance
    def get_name(self):
        return self.__name
# Method to set the author's bio
    def set_bio(self, new_bio):
        self.__bio = new_bio
# Method to retrieve the author's bio from the authors dictionary
    def get_bio(self):
        return self.__bio
# Created an authors dictionary
authors = {}
# Function to add an author to the dictionary
def add_author():
    name = input("Enter the author's name:\n")
    bio = input("Enter some information about the author:\n")
    query = "INSERT INTO authors (name, biography) VALUES (%s, %s)"
    cursor.execute(query, (name, bio))
    conn.commit()
    temp_author = Author(name, bio)
    authors[name] = temp_author
    print(f"Author: {name}, has been added.")
# Function to search the authors dictionary for a specific author
def find_author():
    author_name = input("What is the author's name you are lookin for?\n")
    if author_name in authors:
        author_obj = authors[author_name]
        print(f"Name: {author_obj.get_name()}, Bio: {author_obj.get_bio()}")
    else:
        print("We do not have any information on that author.")
# Function to print out all authors from the authors dictionary
def show_all_authors():
    if not authors:
        print("This directory is currently empty.")
    else:
        for name, author_obj in authors.items():
            print(f"Author Name: {name}, Bio: {author_obj.get_bio()}")


