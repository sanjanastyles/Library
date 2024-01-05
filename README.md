# Library Management System

This Python-based Library Management System provides a versatile platform for managing books, user accounts, and interactions within a library setting. The system incorporates secure user authentication, admin privileges, book management, and user logs. Passwords are securely hashed using the bcrypt algorithm for enhanced security.

## Functionality:

- **Admin Privileges:** Only the admin user can add and delete books, ensuring control over the library's catalog.
- **User Authentication:** Users can create accounts, forget passwords, log in, and log out. Passwords are securely hashed using the bcrypt algorithm.
- **Book Management:** Admin can add and delete books. Users can view available books, lend books, and return books. The system now supports multiple copies of the same book, each tracked separately.
- **User Logs:** Users can view logs of books they have borrowed. For added transparency, users can also view the average rating and reviews for each book.
- **Rating and Reviews:** Users can rate books and leave reviews when returning them. Admins can view ratings and reviews during book management.

## Classes:

### 1. Book
- Represents a book with attributes like title, author, genre, total_copies, and available_copies.
- Provides a method to display information about the book.
- Supports multiple copies and tracks their availability separately.

### 2. User
- Represents a user with attributes like username, hashed_password, books_read, and borrowed_log.
- Provides methods to securely handle passwords, display the borrowed books log, and leave reviews.

### 3. Library
- Manages the collection of books and user accounts.
- Provides methods for actions such as adding and deleting books, displaying available books, lending and returning books, creating user accounts, forgetting passwords, logging in, and logging out.
- Implements search functionality for books based on title, author, or genre.

## Usage:

1. Run the script and choose from the menu options.
2. Admin login is required for adding and deleting books.
3. Users can create accounts, log in, and perform book-related actions.

Feel free to explore and customize the code for your needs!
