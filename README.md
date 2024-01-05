# Library Management System

This is a simple library management system implemented in Python. It allows users to perform various actions such as adding and deleting books, lending and returning books, creating user accounts, and more. The system consists of three main classes: `Book`, `User`, and `Library`.

## Functionality:

- **Admin Privileges:** Only the admin user can add and delete books.
- **User Authentication:** Users can create accounts, forget passwords, log in, and log out.
- **Book Management:** Admin can add and delete books. Users can view available books, lend books, and return books.
- **User Logs:** Users can view logs of books they have borrowed.

## Classes:

### 1. Book
- Represents a book with attributes like title, author, genre, and availability.
- Provides a method to display information about the book.

### 2. User
- Represents a user with attributes like username, password, and borrowed_log (log of borrowed books).
- Provides methods to display the borrowed books log.

### 3. Library
- Manages the collection of books and user accounts.
- Provides methods for actions such as adding and deleting books, displaying available books, lending and returning books, creating user accounts, forgetting passwords, logging in, and logging out.

## Usage:

1. Run the script and choose from the menu options.
2. Admin login is required for adding and deleting books.
3. Users can create accounts, log in, and perform book-related actions.

Feel free to explore and customize the code for your needs!
