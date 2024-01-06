from getpass import getpass
import bcrypt
import json
import random
import string
from datetime import datetime, timedelta
import re


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
              f"Rating: {self.rating:.2f}\nReviews: {', '.join(map(str, self.reviews))}\n")

    def add_review(self, review):
        self.reviews.append(review)
        print("Review added. Thank you!\n")

    def add_rating(self, rating):
        if isinstance(rating, (int, float)) and 1.0 <= rating <= 5.0:
            self.reviews.append(rating)
            self.rating = sum(self.reviews) / len(self.reviews)
            print(f"Rating of {rating} added. Thank you!\n")
        else:
            print("Invalid rating. Please enter a number between 1 and 5.")



class User:
    def __init__(self, username, hashed_password, security_questions=None, security_answers=None, email=None):
        self.username = username
        self.hashed_password = hashed_password
        self.security_questions = security_questions or []
        self.security_answers = dict(zip(security_questions, security_answers)) if security_questions and security_answers else {}
        self.email = email
        self.reset_code = None
        self.reset_code_expiry = None
        self.borrowed_log = []

    def display_borrowed_log(self):
        print(f"{self.username}'s Borrowed Books Log:")
        for log in self.borrowed_log:
            print(f"- {log}")

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password)

    def generate_reset_code(self):
        self.reset_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.reset_code_expiry = datetime.now() + timedelta(minutes=15)

    def reset_password(self, new_password):
        self.hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        self.reset_code = None
        self.reset_code_expiry = None
        print(f"Password for user '{self.username}' has been updated.\n")

    def initiate_password_reset(self):
        if self.email:
            self.generate_reset_code()
            self.send_reset_email()
            print(f"Password reset initiated. Check your email for instructions.\n")
        else:
            print(f"User '{self.username}' does not have a registered email.\n")

    def send_reset_email(self):
        # TODO: Implement email sending mechanism with reset link or code
        # For simplicity, print the reset code in the console
        print(f"Reset code for {self.username}: {self.reset_code}")

    def initiate_password_reset_security_questions(self):
        if self.security_questions and self.security_answers:
            self.verify_identity_and_reset_password()
        else:
            print(f"Security questions are not set for user '{self.username}'. Password reset failed.\n")

    def verify_identity_and_reset_password(self):
        if not self.security_questions or not self.security_answers:
            print(f"Security questions are not set for user '{self.username}'. Password reset failed.\n")
            return

        shuffled_questions = list(self.security_questions)
        random.shuffle(shuffled_questions)

        print("Answer the following security questions to verify your identity:")
        for i, question in enumerate(shuffled_questions, 1):
            answer = input(f"{i}. {question}: ")
            original_answer = self.security_answers.get(question, "")
            if answer.lower() != original_answer.lower():
                print("Incorrect answer. Password reset failed.\n")
                return

        new_password = getpass("Enter a new password for your account: ")
        self.reset_password(new_password)


class Library:
    def __init__(self):
        self.books = {}
        self.users = {}
        self.logged_in_user = None

    def create_account(self, username, password, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Invalid email format. Please enter a valid email address.\n")
            return
        
        if username not in self.users:
            confirm_password = getpass("Confirm password for the new account: ")

            if password == confirm_password:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                # Set up security questions
                print("Set up security questions:")
                questions = [
                    "What is your favorite color?",
                    "What is the name of your first pet?",
                    "In which city were you born?"
                ]
                answers = [getpass(f"{question}: ") for question in questions]  # Collect user's answers to security questions securely using getpass

                self.users[username] = User(username, hashed_password, questions, answers, email)  # Create a new user with the provided username, hashed password, and security question answers
                print(f"User '{username}' has been created with security questions.\n")
            else:
                print("Passwords do not match. Please try again.\n")
        else:
            print(f"User '{username}' already exists. Please choose a different username.\n")

    def initiate_password_reset_email(self, username):
        user = self.users.get(username)
        if user and user.email:
            user.initiate_password_reset()
        else:
            print(f"User '{username}' not found or does not have a registered email.\n")

    def initiate_password_reset_security_questions(self, username):
        user = self.users.get(username)
        if user and user.security_questions and user.security_answers:
            user.verify_identity_and_reset_password()
        else:
            print(f"Security questions are not set for user '{username}'. Password reset failed.\n")

    def forget_password(self, username):
        user = self.users.get(username)
        if user:
            recovery_choice = input("Choose a recovery option (1. Email, 2. Security Questions): ")

            if recovery_choice == "1" and user.email:
                self.initiate_password_reset_email(username)
            elif recovery_choice == "2" and user.security_questions and user.security_answers:
                self.initiate_password_reset_security_questions(username)
            else:
                print("Invalid recovery option or not enough information. Password reset failed.\n")
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
            print(f"Title: {book.title}\nAuthor: {book.author}\nGenre: {book.genre}\n"
                  f"Total Copies: {book.total_copies}\nAvailable Copies: {book.available_copies}\n"
                  f"Rating: {book.rating:.2f}\nReviews: {', '.join(book.reviews)}\n")

    def lend_book(self, title):
        if self.logged_in_user:
            existing_book = self.books.get(title.lower())
            if existing_book and existing_book.available_copies > 0:
                existing_book.available_copies -= 1
                self.logged_in_user.borrowed_log.append(f"Lent '{existing_book.title}'")  # Logs the lending of the book with the specified title in the user's borrowing history.
                print(f"Book '{existing_book.title}' has been lent to {self.logged_in_user.username}.\n")
            else:
                print(f"Book with title '{title}' not found or is currently not available.\n")
        else:
            print("Please log in first.\n")

    def return_book(self, title, rating=None, review=None):
        if self.logged_in_user:
            existing_book = self.books.get(title.lower())
            if existing_book:
                self.logged_in_user.borrowed_log.append(f"Returned '{existing_book.title}'")
                print(f"Book '{existing_book.title}' has been returned by {self.logged_in_user.username}.\n")

                if rating is not None:
                    try:
                        rating = float(rating)
                        if 1.0 <= rating <= 5.0:
                            existing_book.add_rating(rating)
                        else:
                            raise ValueError("Invalid rating. Please enter a number between 1 and 5.")
                    except ValueError as e:
                        print(str(e))
                else:
                    print("No rating provided. Rating skipped.")

                if review:
                    existing_book.add_review(review)
                else:
                    print("No review provided. Review skipped.\n")

                existing_book.available_copies += 1  # Update available copies
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
                match_found = keyword.lower() in book.title.lower()  # Check if the keyword is present in the book title (case-insensitive)
            elif filter_option == 2:  # Author filter
                match_found = keyword.lower() in book.author.lower()
            elif filter_option == 3:  # Genre filter
                match_found = keyword.lower() in book.genre.lower()

            if match_found:
                filtered_books.append(book)

        return filtered_books

    def backup_data(self, filename="library_backup.json"):
        # Prepare data to be stored in the backup file
        data = {
            "books": {title: {"author": book.author, "genre": book.genre, "total_copies": book.total_copies, "available_copies": book.available_copies} for title, book in self.books.items()},
            "users": {username: {"hashed_password": user.hashed_password, "security_questions": user.security_questions, "security_answers": user.security_answers, "email": user.email} for username, user in self.users.items()},
            "logged_in_user": self.logged_in_user.username if self.logged_in_user else None
        }
        with open(filename, 'w') as file:
            json.dump(data, file)
        print(f"Data backed up to {filename}.\n")

    def restore_data(self, filename="library_backup.json"):
        try:
            with open(filename, 'r') as file:  # Attempt to open and read the backup file
                data = json.load(file)  # Load data from the backup file as a JSON object

            self.books = {title: Book(title, book["author"], book["genre"], book["total_copies"])  # Restore books from the backup data
                          for title, book in data["books"].items()}

            self.users = {username: User(username, user["hashed_password"], user["security_questions"], user["security_answers"], user["email"])  # Restore users from the backup data
                          for username, user in data["users"].items()}

            if data["logged_in_user"] and data["logged_in_user"] in self.users:  # Check if a logged-in user is present in the backup data
                self.logged_in_user = self.users[data["logged_in_user"]]  # Set the logged-in user to the one in the backup data
                print(f"Data restored from {filename}. Welcome back, {self.logged_in_user.username}!\n")
            else:
                print(f"Data restored from {filename}.\n")
        except FileNotFoundError:
            print(f"No backup file '{filename}' found.\n")  # Handle the case where the backup file is not found


def main():
    library = Library()

    # library.restore_data("library_backup.json")

    while True:
        if library.logged_in_user:
            print(f"\nWelcome, {library.logged_in_user.username}!\n")
            if library.logged_in_user.username == "admin":
                print("4. Add a Book (Admin Only)")
                print("5. Delete a Book (Admin Only)")
                print("12. Backup Data")
                print("13. Restore Backup Data (Admin Only)")
        print("Library System Menu:")
        if not library.logged_in_user:
            print("1. Create User Account")
            print("2. Login")
            print("3. Forget Password")
        else:
            print("6. Display Available Books")
            print("7. Lend a Book")
            print("8. Return a Book")
            print("9. Logout")
            print("10. View Borrowed Books Log")
        print("11. Search Books")
        print("14. Exit")

        choice = input("Enter your choice (1-14): ")

        if choice == "1" and not library.logged_in_user:
            username = input("Enter a username for the new account: ")
            email = input("Enter your email address: ")

            # Validate email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print("Invalid email format. Please enter a valid email address.\n")
                continue  # Restart the loop if the email format is invalid

            password = getpass("Enter a password for the new account: ")
            library.create_account(username, password, email)

        elif choice == "2" and not library.logged_in_user:
            username = input("Enter your username: ")
            password = getpass("Enter your password: ")
            user = library.login(username, password)

        elif choice == "3":
            username = input("Enter the username for password reset: ")
            library.forget_password(username)

        elif choice == "4" and library.logged_in_user and library.logged_in_user.username == "admin":
            title = input("Enter the title of the book: ")
            author = input("Enter the author of the book: ")
            genre = input("Enter the genre of the book: ")
            total_copies = int(input("Enter the total number of copies: "))
            library.add_book(title, author, genre, total_copies)

        elif choice == "5" and library.logged_in_user and library.logged_in_user.username == "admin":
            title = input("Enter the title of the book to delete: ")
            library.delete_book(title)

        elif choice == "6":
            library.display_books()

        elif choice == "7":
            if library.logged_in_user:
                title = input("Enter the title of the book to lend: ")
                library.lend_book(title)
            else:
                print("Please log in first.\n")

        elif choice == "8":
            if library.logged_in_user: 
                title = input("Enter the title of the book to return: ")
                rating = input("Enter a rating (1-5) for the book (press Enter to skip): ")
                review = input("Enter a review for the book (press Enter to skip): ")
                rating = float(rating) if rating.isdigit() else None
                library.return_book(title, rating, review)
            else:
                print("Please log in first.\n")

        elif choice == "9" and library.logged_in_user:
            library.logout()

        elif choice == "10" and library.logged_in_user:
            library.view_borrowed_log()

        elif choice == "11":
            while True:
                try:
                    filter_option = int(input("Choose a filter option (1. Title, 2. Author, 3. Genre, 0. Exit): "))
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue  # Restart the loop if there is an error

                if filter_option == 0:  # User wants to exit the search loop
                    print("Exiting the search. Returning to the main menu.")
                    break
                elif filter_option in [1, 2, 3]: # Process the valid input
                    keyword = input("Enter a keyword to search for: ")
                    search_results = library.search_books(keyword, filter_option)
                    print("\nSearch Results:")
                    for result in search_results:
                        result.display_info()
                    break
                else:
                    print("Invalid input. Please enter a valid number (0, 1, 2, or 3) to exit or choose a filter option.")


        elif choice == "12" and library.logged_in_user and library.logged_in_user.username == "admin":
            # Backup data before exiting
            library.backup_data("library_backup.json")
            print("Exiting the Library System. Goodbye!")
            break

        elif choice == "13" and library.logged_in_user and library.logged_in_user.username == "admin":
            library.restore_data()
            break

        elif choice == "14":
            print("Exiting the Library System. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 12.")

if __name__ == "__main__":
    main()
