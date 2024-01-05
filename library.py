from getpass import getpass
import bcrypt

class Book:
    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre
        self.available = True
        self.rating = 0
        self.reviews = []

    def display_info(self):
        print(f"Title: {self.title}\nAuthor: {self.author}\nGenre: {self.genre}\n"
              f"Available: {'Yes' if self.available else 'No'}\n"
              f"Rating: {self.rating:.1f} ({len(self.reviews)} reviews)\n")

    def add_review(self, review):
        self.reviews.append(review)
        print("Review added. Thank you!\n")

    def calculate_average_rating(self, new_rating):
        total_rating = self.rating * len(self.reviews)
        total_rating += new_rating
        self.rating = total_rating / (len(self.reviews) + 1)


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

    def return_book(self, title, rating=0, review=""):
        for book in self.books:
            if book.title.lower() == title.lower() and not book.available:
                book.available = True
                self.logged_in_user.borrowed_log.append(f"Returned '{book.title}'")
                if rating > 0:
                    book.add_review(review)
                    book.calculate_average_rating(rating)
                print(f"Book '{book.title}' has been returned by {self.logged_in_user.username}.\n")
                return
        print(f"Book with title '{title}' not found or is already available.\n")

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
        if not library.logged_in_user:
            print("\nWelcome to the Library System!")
            print("1. Create User Account")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ")

            if choice == "1":
                username = input("Enter a username for the new account: ")
                password = getpass("Enter a password for the new account: ")
                library.create_account(username, password)

            elif choice == "2":
                username = input("Enter your username: ")
                password = getpass("Enter your password: ")
                library.login(username, password)

            elif choice == "3":
                print("Exiting the Library System. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 3.")

        else:
            print("\nLibrary System Menu:")
            print("1. Display Available Books")
            print("2. Lend a Book")
            print("3. Return a Book")
            print("4. View Borrowed Books Log")
            print("5. Search for Books")
            print("6. Logout")

            if library.logged_in_user.username == "admin":
                print("Admin Privileges:")
                print("7. Add a Book")
                print("8. Delete a Book")

            print("9. Exit")

            choice = input("Enter your choice (1-9): ")

            if choice == "1":
                library.display_books()

            elif choice == "2":
                title = input("Enter the title of the book to lend: ")
                library.lend_book(title)

            elif choice == "3":
                title = input("Enter the title of the book to return: ")
                rating = int(input("Enter your rating for the book (0-5): "))
                review = input("Enter your review for the book (optional): ")
                library.return_book(title, rating, review)

            elif choice == "4":
                library.view_borrowed_log()

            elif choice == "5":
                keyword = input("Enter the keyword to search for: ")
                print("Filter Options:")
                print("1. Title")
                print("2. Author")
                print("3. Genre")
                filter_option = int(input("Enter the filter option (1-3): "))
                filtered_books = library.search_books(keyword, filter_option)
                if filtered_books:
                    print("Search Results:")
                    for book in filtered_books:
                        book.display_info()
                else:
                    print("No matching books found.\n")

            elif choice == "6":
                library.logout()

            elif choice == "7" and library.logged_in_user.username == "admin":
                title = input("Enter the title of the book: ")
                author = input("Enter the author of the book: ")
                genre = input("Enter the genre of the book: ")
                library.add_book(title, author, genre)

            elif choice == "8" and library.logged_in_user.username == "admin":
                title = input("Enter the title of the book to delete: ")
                library.delete_book(title)

            elif choice == "9":
                print("Exiting the Library System. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()
