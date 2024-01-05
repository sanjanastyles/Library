from getpass import getpass
import bcrypt

class Book:
    def __init__(self, title, author, genre, total_copies=1):
        self.title = title
        self.author = author
        self.genre = genre
        self.total_copies = total_copies
        self.available_copies = total_copies
        self.reviews = []
        self.rating = 0

    def display_info(self):
        print(f"Title: {self.title}\nAuthor: {self.author}\nGenre: {self.genre}\n"
              f"Total Copies: {self.total_copies}\nAvailable Copies: {self.available_copies}\n"
              f"Rating: {self.rating:.2f}\nReviews: {', '.join(self.reviews)}\n")

    def add_review(self, review):
        self.reviews.append(review)
        print("Review added. Thank you!\n")

    def add_rating(self, rating):
        self.rating = (self.rating + rating) / len(self.reviews)
        print(f"Rating added. Thank you!\n")

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
        self.books = {}
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
            existing_book = self.books.get(title.lower())
            if existing_book:
                existing_book.total_copies += total_copies
                existing_book.available_copies += total_copies
                print(f"Additional copies of '{title}' added to the library.\n")
            else:
                new_book = Book(title, author, genre, total_copies)
                self.books[title.lower()] = new_book
                print(f"Book '{title}' added to the library.\n")
        else:
            print("Only admin can add books. Please log in as admin.\n")

    def delete_book(self, title):
        if self.logged_in_user and self.logged_in_user.username == "admin":
            existing_book = self.books.get(title.lower())
            if existing_book:
                del self.books[title.lower()]
                print(f"Book '{title}' has been deleted from the library.\n")
            else:
                print(f"Book with title '{title}' not found.\n")
        else:
            print("Only admin can delete books. Please log in as admin.\n")

    def display_books(self):
        sorted_books = sorted(self.books.values(), key=lambda x: x.title.lower())
        print("Library Books (Alphabetical Order):")
        for book in sorted_books:
            book.display_info()

    def lend_book(self, title):
        if self.logged_in_user:
            existing_book = self.books.get(title.lower())
            if existing_book and existing_book.available_copies > 0:
                existing_book.available_copies -= 1
                self.logged_in_user.books_read.append(existing_book.title)
                self.logged_in_user.borrowed_log.append(f"Lent '{existing_book.title}'")
                print(f"Book '{existing_book.title}' has been lent to {self.logged_in_user.username}.\n")
            else:
                print(f"Book with title '{title}' not found or is currently not available.\n")
        else:
            print("Please log in first.\n")

    def return_book(self, title, rating=None, review=None):
        if self.logged_in_user:
            existing_book = self.books.get(title.lower())
            if existing_book and existing_book.available_copies < existing_book.total_copies:
                existing_book.available_copies += 1
                self.logged_in_user.borrowed_log.append(f"Returned '{existing_book.title}'")
                print(f"Book '{existing_book.title}' has been returned by {self.logged_in_user.username}.\n")
                
                if rating and 1 <= rating <= 5:
                    existing_book.add_rating(rating)

                if review:
                    existing_book.add_review(review)

            else:
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

        for book in self.books.values():
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
            print("4. Delete a Book (Admin Only)")
            print("5. Display Available Books")
            print("6. Lend a Book")
            print("7. Return a Book")
            print("8. Forget Password")
            print("9. Logout")
            print("10. View Borrowed Books Log")
        print("11. Search Books")
        print("12. Exit")

        choice = input("Enter your choice (1-12): ")

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

        elif choice == "4" and library.logged_in_user and library.logged_in_user.username == "admin":
            title = input("Enter the title of the book to delete: ")
            library.delete_book(title)

        elif choice == "5":
            library.display_books()

        elif choice == "6":
            if library.logged_in_user:
                title = input("Enter the title of the book to lend: ")
                library.lend_book(title)
            else:
                print("Please log in first.\n")

        elif choice == "7":
            if library.logged_in_user:
                title = input("Enter the title of the book to return: ")
                rating = input("Enter a rating (1-5) for the book (press Enter to skip): ")
                review = input("Enter a review for the book (press Enter to skip): ")
                rating = int(rating) if rating.isdigit() else None
                library.return_book(title, rating, review)
            else:
                print("Please log in first.\n")

        elif choice == "8" and library.logged_in_user:
            username = input("Enter the username for password reset: ")
            library.forget_password(username)

        elif choice == "9" and library.logged_in_user:
            library.logout()

        elif choice == "10" and library.logged_in_user:
            library.view_borrowed_log()

        elif choice == "11":
            keyword = input("Enter a keyword to search for: ")
            filter_option = int(input("Choose a filter option (1. Title, 2. Author, 3. Genre): "))
            search_results = library.search_books(keyword, filter_option)
            print("\nSearch Results:")
            for result in search_results:
                result.display_info()

        elif choice == "12":
            print("Exiting the Library System. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 12.")

if __name__ == "__main__":
    main()
