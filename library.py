from getpass import getpass
import bcrypt

class Book:
    def __init__(self, title, author, genre, total_copies=1):
        self.title = title
        self.author = author
        self.genre = genre
        self.total_copies = total_copies
        self.available_copies = total_copies

    def display_info(self):
        print(f"Title: {self.title}\nAuthor: {self.author}\nGenre: {self.genre}\n"
              f"Total Copies: {self.total_copies}\nAvailable Copies: {self.available_copies}\n")

    def add_review(self, review):
        self.reviews.append(review)
        print("Review added. Thank you!\n")

    def calculate_average_rating(self, new_rating):
        total_rating = self.rating * len(self.reviews)
        total_rating += new_rating
        self.rating = total_rating / (len(self.reviews) + 1)


class User:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password
        self.books_read = []
        self.borrowed_log = []

    def display_borrowed_log(self):
        print(f"{self.username}'s Borrowed Books Log:")
        for log in self.borrowed_log:
            print(f"- {log}")

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password)


class Library:
    def __init__(self):
        self.books = []
        self.users = {}
        self.logged_in_user = None

    def create_account(self, username, password):
        if username not in self.users:
            confirm_password = getpass("Confirm password for the new account: ")

            if password == confirm_password:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                self.users[username] = User(username, hashed_password)
                print(f"User '{username}' has been created.\n")
            else:
                print("Passwords do not match. Please try again.\n")
        else:
            print(f"User '{username}' already exists. Please choose a different username.\n")


    def forget_password(self, username):
        user = self.users.get(username)
        if user:
            new_password = getpass(f"Enter a new password for user '{username}': ")
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

    def add_book(self, title, author, genre, total_copies=1):
        if self.logged_in_user and self.logged_in_user.username == "admin":
            existing_book = next((book for book in self.books if book.title.lower() == title.lower()), None)
            if existing_book:
                existing_book.total_copies += total_copies
                existing_book.available_copies += total_copies
                print(f"Additional copies of '{title}' added to the library.\n")
            else:
                new_book = Book(title, author, genre, total_copies)
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
        if self.logged_in_user:
            for book in self.books:
                if book.title.lower() == title.lower() and book.available_copies > 0:
                    book.available_copies -= 1
                    self.logged_in_user.books_read.append(book.title)
                    self.logged_in_user.borrowed_log.append(f"Lent '{book.title}'")
                    print(f"Book '{book.title}' has been lent to {self.logged_in_user.username}.\n")
                    return
            print(f"Book with title '{title}' not found or is currently not available.\n")
        else:
            print("Please log in first.\n")

    def return_book(self, title):
        if self.logged_in_user:
            for book in self.books:
                if book.title.lower() == title.lower() and book.available_copies < book.total_copies:
                    book.available_copies += 1
                    self.logged_in_user.borrowed_log.append(f"Returned '{book.title}'")
                    print(f"Book '{book.title}' has been returned by {self.logged_in_user.username}.\n")
                    return
            print(f"Book with title '{title}' not found or is already available.\n")
        else:
            print("Please log in first.\n")

    def view_borrowed_log(self):
        if self.logged_in_user:
            self.logged_in_user.display_borrowed_log()
        else:
            print("Please log in first.\n")

    def search_books(self, keyword, filter_option):
        filtered_books = []

        for book in self.books:
            match_found = False

            if filter_option == 1:  # Title filter
                match_found = keyword.lower() in book.title.lower()
            elif filter_option == 2:  # Author filter
                match_found = keyword.lower() in book.author.lower()
            elif filter_option == 3:  # Genre filter
                match_found = keyword.lower() in book.genre.lower()

            if match_found:
                filtered_books.append(book)

        return filtered_books


def main():
    library = Library()

    while True:
        if library.logged_in_user:
            print(f"\nWelcome, {library.logged_in_user.username}!\n")
        print("Library System Menu:")
        if not library.logged_in_user:
            print("1. Create User Account")
            print("2. Login")
        else:
            print("3. Add a Book (Admin Only)")
            print("4. Display Available Books")
            print("5. Lend a Book")
            print("6. Return a Book")
            print("7. Forget Password")
            print("8. Logout")
            print("9. View Borrowed Books Log")
        print("10. Exit")

        choice = input("Enter your choice (1-10): ")

        if choice == "1" and not library.logged_in_user:
            username = input("Enter a username for the new account: ")
            password = getpass("Enter a password for the new account: ")
            library.create_account(username, password)

        elif choice == "2" and not library.logged_in_user:
            username = input("Enter your username: ")
            password = getpass("Enter your password: ")
            user = library.login(username, password)


        elif choice == "3" and library.logged_in_user and library.logged_in_user.username == "admin":
            title = input("Enter the title of the book: ")
            author = input("Enter the author of the book: ")
            genre = input("Enter the genre of the book: ")
            total_copies = int(input("Enter the total number of copies: "))
            library.add_book(title, author, genre, total_copies)

        elif choice == "4":
            library.display_books()

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

        elif choice == "7" and library.logged_in_user:
            username = input("Enter the username for password reset: ")
            library.forget_password(username)

        elif choice == "8" and library.logged_in_user:
            library.logout()

        elif choice == "9" and library.logged_in_user:
            library.view_borrowed_log()

        elif choice == "10":
            print("Exiting the Library System. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 10.")

if __name__ == "__main__":
    main()
