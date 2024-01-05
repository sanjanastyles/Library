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
        self.password = password
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
            user.password = new_password
            print(f"Password for user '{username}' has been updated.\n")
        else:
            print(f"User '{username}' not found. Please enter a valid username.\n")

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
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

    def display_books(self):
        sorted_books = sorted(self.books, key=lambda x: x.title.lower())
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
        print("4. Lend a Book")
        print("5. Return a Book")
        print("6. Create User Account")
        print("7. Forget Password")
        print("8. Login")
        print("9. Logout")
        print("10. View Borrowed Books Log")
        print("11. Exit")

        choice = input("Enter your choice (1-11): ")

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
            if library.logged_in_user:
                title = input("Enter the title of the book to lend: ")
                library.lend_book(title)
            else:
                print("Please log in first.\n")

        elif choice == "5":
            if library.logged_in_user:
                title = input("Enter the title of the book to return: ")
                library.return_book(title)
            else:
                print("Please log in first.\n")

        elif choice == "6":
            username = input("Enter a username for the new account: ")
            password = input("Enter a password for the new account: ")
            library.create_account(username, password)

        elif choice == "7":
            username = input("Enter the username for password reset: ")
            library.forget_password(username)

        elif choice == "8":
            if not library.logged_in_user:
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                library.login(username, password)
            else:
                print("You are already logged in. Logout first to log in with a different account.\n")

        elif choice == "9":
            library.logout()

        elif choice == "10":
            library.view_borrowed_log()

        elif choice == "11":
            print("Exiting the Library System. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 11.")

if __name__ == "__main__":
    main()
