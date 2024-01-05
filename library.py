import bcrypt  # Make sure to install the 'bcrypt' module using 'pip install bcrypt'

class Book:
    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre
        self.available = True

    def display_info(self):
        print(f"Title: {self.title}\nAuthor: {self.author}\nGenre: {self.genre}\nAvailable: {'Yes' if self.available else 'No'}\n")


class User:
    def __init__(self, username, password):
        self.username = username
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.books_read = []
        self.borrowed_log = []

    def display_borrowed_log(self):
        print(f"{self.username}'s Borrowed Books Log:")
        for log in self.borrowed_log:
            print(f"- {log}")


class Library:
    def __init__(self):
        self.books = []
        self.users = {}
        self.logged_in_user = None

    def create_account(self, username, password):
        if username not in self.users:
            self.users[username] = User(username, password)
            print(f"User '{username}' has been created.\n")
        else:
            print(f"User '{username}' already exists. Please choose a different username.\n")

    def forget_password(self, username):
        user = self.users.get(username)
        if user:
            new_password = input(f"Enter a new password for user '{username}': ")
            user.hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            print(f"Password for user '{username}' has been updated.\n")
        else:
            print(f"User '{username}' not found. Please enter a valid username.\n")

    def login(self, username, password):
        user = self.users.get(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            self.logged_in_user = user
            print(f"User '{username}' has been logged in.\n")
            return user
        else:
            print("Invalid username or password. Please try again.\n")
            return None

    def logout(self):
        self.logged_in_user = None
        print("User has been logged out.\n")

    def add_book(self, title, author, genre):
        if self.logged_in_user and self.logged_in_user.username == "admin":
            new_book = Book(title, author, genre)
            self.books.append(new_book)
            print(f"Book '{title}' added to the library.\n")
        else:
            print("Only admin can add books. Please log in as admin.\n")

    def delete_book(self, title):
        if self.logged_in_user and self.logged_in_user.username == "admin":
            for book in self.books:
                if book.title.lower() == title.lower():
                    self.books.remove(book)
                    print(f"Book '{title}' has been deleted from the library.\n")
                    return
            print(f"Book with title '{title}' not found.\n")
        else:
            print("Only admin can delete books. Please log in as admin.\n")

    def display_books(self, filter_title=None, filter_author=None, filter_genre=None):
        filtered_books = self.books

        if filter_title:
            filtered_books = [book for book in filtered_books if filter_title.lower() in book.title.lower()]
        if filter_author:
            filtered_books = [book for book in filtered_books if filter_author.lower() in book.author.lower()]
        if filter_genre:
            filtered_books = [book for book in filtered_books if filter_genre.lower() in book.genre.lower()]

        sorted_books = sorted(filtered_books, key=lambda x: x.title.lower())
        print("Library Books (Alphabetical Order):")
        for book in sorted_books:
            book.display_info()

    def lend_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower() and book.available:
                book.available = False
                self.logged_in_user.books_read.append(book.title)
                self.logged_in_user.borrowed_log.append(f"Lent '{book.title}'")
                print(f"Book '{book.title}' has been lent to {self.logged_in_user.username}.\n")
                return
        print(f"Book with title '{title}' not found or is currently not available.\n")

    def return_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower() and not book.available:
                book.available = True
                self.logged_in_user.borrowed_log.append(f"Returned '{book.title}'")
                print(f"Book '{book.title}' has been returned by {self.logged_in_user.username}.\n")
                return
        print(f"Book with title '{title}' not found or is already available.\n")

    def view_borrowed_log(self):
        if self.logged_in_user:
            self.logged_in_user.display_borrowed_log()
        else:
            print("Please log in first.\n")


def main():
    library = Library()

    while True:
        print("\nLibrary System Menu:")
        print("1. Add a Book (Admin Only)")
        print("2. Delete a Book (Admin Only)")
        print("3. Display Available Books")
        print("4. Search for Books")
        print("5. Lend a Book")
        print("6. Return a Book")
        print("7. Create User Account")
        print("8. Forget Password")
        print("9. Login")
        print("10. Logout")
        print("11. View Borrowed Books Log")
        print("12. Exit")

        choice = input("Enter your choice (1-12): ")

        if choice == "1":
            if library.logged_in_user and library.logged_in_user.username == "admin":
                title = input("Enter the title of the book: ")
                author = input("Enter the author of the book: ")
                genre = input("Enter the genre of the book: ")
                library.add_book(title, author, genre)
            else:
                print("Only admin can add books. Please log in as admin.\n")

        elif choice == "2":
            if library.logged_in_user and library.logged_in_user.username == "admin":
                title = input("Enter the title of the book to delete: ")
                library.delete_book(title)
            else:
                print("Only admin can delete books. Please log in as admin.\n")

        elif choice == "3":
            library.display_books()

        elif choice == "4":
            title_filter = input("Enter the title filter (leave blank for no filter): ")
            author_filter = input("Enter the author filter (leave blank for no filter): ")
            genre_filter = input("Enter the genre filter (leave blank for no filter): ")
            library.display_books(filter_title=title_filter, filter_author=author_filter, filter_genre=genre_filter)

        elif choice == "5":
            if library.logged_in_user:
                title = input("Enter the title of the book to lend: ")
                library.lend_book(title)
            else:
                print("Please log in first.\n")

        elif choice == "6":
            if library.logged_in_user:
                title = input("Enter the title of the book to return: ")
                library.return_book(title)
            else:
                print("Please log in first.\n")

        elif choice == "7":
            username = input("Enter a username for the new account: ")
            password = input("Enter a password for the new account: ")
            library.create_account(username, password)

        elif choice == "8":
            username = input("Enter the username for password reset: ")
            library.forget_password(username)

        elif choice == "9":
            if not library.logged_in_user:
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                library.login(username, password)
            else:
                print("You are already logged in. Logout first to log in with a different account.\n")

        elif choice == "10":
            library.logout()

        elif choice == "11":
            library.view_borrowed_log()

        elif choice == "12":
            print("Exiting the Library System. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 12.")

if __name__ == "__main__":
    main()
