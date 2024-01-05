# Library Management Project

## Functionality:

- **User Authentication:** Users can create accounts, forget passwords, log in, and log out. Passwords are securely hashed using the bcrypt algorithm.
- **Basic User Actions:** Users can view available books, lend books, return books, and view logs of borrowed books.
- **Admin Privileges:** Admin users can add and delete books in addition to basic user actions.
- **Book Rating and Reviews:** Users can rate books when returning them and leave optional reviews.
- **Search Functionality:** Users can search for books based on titles, authors, or genres.

## Classes:

### 1. Book
- Represents a book with attributes like title, author, genre, and availability.
- Provides a method to display information about the book.

### 2. User
- Represents a user with attributes like username, hashed_password, borrowed_log (log of borrowed books), and reviews.
- Provides methods to securely handle passwords, display the borrowed books log, and store book reviews.

### 3. Library
- Manages the collection of books and user accounts.
- Provides methods for actions such as adding and deleting books, displaying available books, lending and returning books, creating user accounts, forgetting passwords, logging in, and logging out.
- Offers search functionality to find books based on user-defined criteria.

## Usage:

1. Run the script and choose from the menu options.
2. Create a user account or log in.
3. Explore basic user actions or admin privileges as per your role.
4. Rate and review books when returning them.
5. Search for books based on titles, authors, or genres.

Feel free to explore and customize the code for your needs!
