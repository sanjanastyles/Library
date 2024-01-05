# Library Management System

## Introduction
This code implements a simple library system with features such as user account management, book management, borrowing and returning books, and data backup and restoration. Below are the key features and functionalities of the code.

## Classes
### 1. Book
- Represents a book in the library.
- Attributes:
  - `title`: Title of the book.
  - `author`: Author of the book.
  - `genre`: Genre of the book.
  - `total_copies`: Total copies of the book.
  - `available_copies`: Available copies of the book.
  - `reviews`: List of reviews for the book.
  - `rating`: Average rating of the book.

### 2. User
- Represents a user in the library system.
- Attributes:
  - `username`: User's username.
  - `hashed_password`: Hashed password for user authentication.
  - `security_questions`: List of security questions.
  - `security_answers`: Dictionary mapping security questions to their answers.
  - `email`: User's email address.
  - `reset_code`: Reset code for password reset.
  - `reset_code_expiry`: Expiry time for the reset code.
  - `borrowed_log`: List of borrowed books.

### 3. Library
- Manages the overall library system.
- Attributes:
  - `books`: Dictionary storing books in the library.
  - `users`: Dictionary storing user information.
  - `logged_in_user`: Currently logged-in user.

## Features
### User Management
1. **Create User Account**
   - Allows users to create a new account with a unique username, email, and password.
   - Collects security questions and answers during account creation.

2. **Login**
   - Validates user credentials (username and password) for login.
   - Differentiates between regular users and the admin user.

3. **Forget Password**
   - Initiates password reset for a user by providing options based on email or security questions.

### Book Management
4. **Add Book (Admin Only)**
   - Allows the admin to add new books to the library, specifying title, author, genre, and total copies.

5. **Delete Book (Admin Only)**
   - Allows the admin to delete books from the library based on the title.

6. **Display Available Books**
   - Shows the list of available books in alphabetical order with details such as title, author, genre, copies, rating, and reviews.

### Borrowing and Returning Books
7. **Lend a Book**
   - Allows users to borrow books if they are logged in and if the book is available.

8. **Return a Book**
   - Allows users to return a borrowed book, optionally providing a rating and review.

9. **View Borrowed Books Log**
   - Displays the borrowing history of the currently logged-in user.

### Search Books
10. **Search Books**
    - Allows users to search for books based on title, author, or genre.
    - Users can choose the search filter option (title, author, genre) during the search.

### Data Backup and Restoration (Admin Only)
11. **Backup Data**
    - Allows the admin to create a backup of the library's data in a JSON file.

12. **Restore Backup Data**
    - Allows the admin to restore the library's data from a previously created backup file.

### Miscellaneous
13. **Logout**
    - Logs out the currently logged-in user.

14. **Exit**
    - Exits the library system.

## Usage
- Run the script to start the library system.
- Follow the menu prompts to interact with the system.
- Admin functionalities are accessible by logging in as the admin user.
- The script allows users to create accounts, log in, borrow and return books, search for books, and perform other library-related tasks.

## Note
- Some features, such as email sending for password reset, are marked as "TODO" and need implementation.
- The backup and restore features are commented out, but they can be uncommented and used if needed.

## Disclaimer
- This is a simplified implementation for educational purposes and may lack certain real-world considerations and security measures.
