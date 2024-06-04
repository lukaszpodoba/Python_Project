class Film:
    """
    A class to represent a film
    """

    def __init__(self, title, director, year, genre, status, rating, description):
        self.title = title
        self.director = director
        self.year = year
        self.genre = genre
        self.status = status
        self.rating = rating
        self.description = description

        self.reviews = []
        self.comments = []

    def __str__(self):
        return f"{self.title} ({self.year}) by {self.director} {self.rating}/10 {self.genre}"


    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def director(self):
        return self.__director

    @director.setter
    def director(self, director):
        self.__director = director

    @property
    def genre(self):
        return self.__genre

    @genre.setter
    def genre(self, genre):
        self.__genre = genre

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, rating):
        self.__rating = rating

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, year):
        self.__year = year

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def reviews(self):
        return self.__reviews

    @reviews.setter
    def reviews(self, reviews):
        self.__reviews = reviews

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, comments):
        self.__comments = comments
