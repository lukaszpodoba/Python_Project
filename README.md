# Python Watchlist

## Overview
Watchlist is a desktop application built in Python for managing a personal movie collection. It allows users to browse, search, add, edit, and delete movies. Additionally, the app supports adding reviews and comments to individual films, generating statistics (e.g., average rating, genre counts), and exporting the movie collection data to a text file.
## Key Components & Technologies
- **Language & Environment**:
  - **Python**: The entire application is developed in Python.
  - **Tkinter**: Used for creating the graphical user interface (GUI), including windows, buttons, text fields, and more.
- **Object-Oriented Architecture**:
  - The project leverages classes, encapsulation, and property decorators to maintain clean, modular code.


## Main Modules
- **Film (Film.py)**:
  - Represents a single movie with attributes like title, director, release year, genre, watch status, rating, and description.
  - Maintains lists for reviews and comments (each with a timestamp), showcasing encapsulation using `@property` and setters.
- **CollectionManager (CollectionManager.py)**:
  - Manages the movie collection by creating, modifying, and deleting `Film` instances.
  - Provides methods such as `add_film`, `remove_film`, and `search` to perform basic operations.
  - Implements `add_review` and `add_comment` methods that automatically attach the current date and time to entries.
- **User Interface (GUI.py)**:
  - Constructs the main application window divided into several sections: a search bar, a results area (Listbox), and an action panel with various buttons.
  - Allows users to filter movies by title, director, genre, year, and status (“Watched” or “Unwatched”).
  - Facilitates movie management through additional pop-up windows for adding, editing, and deleting films.
  - Supports adding reviews (with a rating slider) and comments, and includes functionality to clear these lists.
  - Features include generating statistics and exporting collection data to a text file (`film_collection.txt`).

 
## Functionalities & Design
- **Separation of Concerns**: The application separates data management (handled by the Film and CollectionManager classes) from the GUI logic, which simplifies maintenance and future enhancements.
- **Comprehensive Operations**: Supports a full data lifecycle (create, read, update, delete), along with additional functionalities like searching, reviewing, comment management, statistical analysis, and data export.
- **User-Friendly Interface**: The use of Tkinter ensures an intuitive and interactive user experience.





