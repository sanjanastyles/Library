# Library Management System

This is a comprehensive library management system implemented in Python. The system allows users to perform various actions such as creating accounts, logging in, adding and deleting books, lending and returning books, rating and reviewing books, and more. The project employs secure password management using the bcrypt algorithm for user authentication.

## Key Features:
- **Secure User Authentication:** Implemented with bcrypt, ensuring password security for user accounts.
- **Admin Privileges:** Exclusive access for admin users to add, delete, and manage books, maintaining control over the library.
- **Book Management with Multiple Copies:** Supports multiple copies of the same book, each tracked separately, facilitating efficient book inventory management.
- **User Logs:** Users can view logs of their borrowed books, providing insights into their reading history.
- **Rating and Reviews:** Users can rate and leave reviews when returning books, enhancing the interactive user experience.
- **Search and Filters:** A search option with filters allows users to find specific books based on titles, authors, or genres.
- **Dynamic User Interface:** The menu dynamically adjusts based on user roles, displaying admin-specific options only to the admin user.
- **Structured Codebase:** Organized into classes (Book, User, and Library), promoting code modularity and readability.
- **Relevant Data Structures and Algorithms:** Utilizes data structures and algorithms for efficient book searches and user log management.

## Classes:

### 1. Book
- Represents a book with attributes like title, author, genre, and availability.
- Provides methods to display information, add reviews, and calculate average ratings.

### 2. User
- Represents a user with attributes like username, hashed_password, and borrowed_log (log of borrowed books).
- Provides methods for securely handling passwords, displaying the borrowed books log, and managing ratings and reviews.

### 3. Library
- Manages the collection of books and user accounts.
- Provides methods for actions such as adding and deleting books, displaying available books, lending and returning books, creating user accounts, forgetting passwords, logging in, and logging out. Admin-specific functionalities are available only to the admin user.

## Usage:

1. Run the script and choose from the menu options.
2. Create an account or log in to access user-specific features.
3. Admin login is required for adding and deleting books.
4. Users can explore available books, lend, return, rate, and review books.
5. Admins can manage the book collection and view user logs.

Feel free to explore and customize the code for your needs!
