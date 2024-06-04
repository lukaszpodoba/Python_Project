from datetime import datetime

from Film import Film


class CollectionManager:
    """
    A class to manage a collection of films
    """

    def __init__(self):
        self.films = [
            Film("Inception", "Christopher Nolan", 2010, "Sci-Fi", "Unwatched", 8.8,
                 "A thief who steals corporate..."),
            Film("The Dark Knight", "Christopher Nolan", 2008, "Action", "Unwatched", 9.0,
                 "When the menace known as the..."),
            Film("Interstellar", "Christopher Nolan", 2014, "Sci-Fi", "Watched", 8.6,
                 "Earth's future has been riddled..."),
            Film("The Shawshank Redemption", "Frank Darabont", 1994, "Drama", "Watched", 9.3,
                 "Two imprisoned..."),
            Film("The Godfather", "Francis Ford Coppola", 1972, "Crime", "Watched", 9.2,
                 "The aging patriarch of an..."),
            Film("The Godfather: Part II", "Francis Ford Coppola", 1974, "Crime", "Unwatched", 9.0,
                 "The early life and career of..."),
            Film("It", "Andy Muschietti", 2017, "Horror", "Unwatched", 7.3,
                 "In the summer of 1989, a group of bullied kids band together to destroy a shape-shifting monster, which disguises itself as a clown and preys on the children of Derry, their small Maine town."),
            Film("Dune", "Denis Villeneuve", 2021, "Sci-Fi", "Unwatched", 8.3,
                 "Feature adaptation of Frank Herbert's science fiction novel, about the son of a noble family entrusted with the protection of the most valuable asset and most vital element in the galaxy.")
        ]

    @staticmethod
    def add_review(film, review):
        """
        Add a review to a film
        :param film: The film to review
        :param review: The review to add
        :return: None
        """
        film.reviews.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + review + "/10")

    @staticmethod
    def add_comment(film, comment):
        """
        Add a comment to a film
        :param film: The film to comment on
        :param comment: The comment to add
        :return: None
        """
        film.comments.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + comment)

    def add_film(self, title, director, year, genre, status, rating, description=""):
        """
        Add a film to the collection
        :param title: The title of the film
        :param director: The director of the film
        :param year: The year the film was released
        :param genre: The genre of the film
        :param status: The status of the film
        :param rating: The rating of the film
        :param description: The description of the film
        :return: None
        """
        if not title or not director or not year or not genre:
            return "Title, director, year, and genre are required."

        film = Film(title, director, year, genre, status, rating, description)
        self.films.append(film)

    def remove_film(self, film):
        """
        Remove a film from the collection
        :param film: The film to remove
        :return: None
        """
        if film in self.films:
            self.films.remove(film)
        else:
            print("Film not found in the list.")

    def search(self, search_terms):
        """
        Search for films in the collection
        :param search_terms: A dictionary of search terms
        :return: A list of films that match the search terms
        """
        results = []
        for film in self.films:
            if all((str(value) == str(getattr(film, key)).lower() if key == 'status' else str(value) in str(getattr(film, key)).lower())
                   for key, value in search_terms.items() if value):
                results.append(film)
        return results
