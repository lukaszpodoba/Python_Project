import tkinter as tk
from datetime import datetime
from tkinter import messagebox


import CollectionManager

collection_manager = CollectionManager.CollectionManager()

selected_film = None

root = tk.Tk()
root.title("Watchlist")


button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, ipadx=5, ipady=5)

search_frame = tk.Frame(root)
search_frame.pack(fill=tk.X, ipadx=5, ipady=5)

results_frame = tk.Frame(root)
results_frame.pack(fill=tk.BOTH, expand=True, ipadx=5, ipady=5)


results_listbox = tk.Listbox(results_frame)
results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)


scrollbar = tk.Scrollbar(results_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

results_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=results_listbox.yview)


results_listbox.insert(tk.END, "Results will be displayed here")

title_label = tk.Label(search_frame, text="Title:")
title_label.pack(side=tk.LEFT, padx=5, pady=5)
title_entry = tk.Entry(search_frame)
title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

director_label = tk.Label(search_frame, text="Director:")
director_label.pack(side=tk.LEFT, padx=5, pady=5)
director_entry = tk.Entry(search_frame)
director_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

genre_label = tk.Label(search_frame, text="Genre:")
genre_label.pack(side=tk.LEFT, padx=5, pady=5)
genre_entry = tk.Entry(search_frame)
genre_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

year_label = tk.Label(search_frame, text="Year:")
year_label.pack(side=tk.LEFT, padx=5, pady=5)
year_entry = tk.Entry(search_frame)
year_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)


status_var = tk.StringVar(value="All")
status_label = tk.Label(search_frame, text="Status:")
status_label.pack(side=tk.LEFT, padx=5, pady=5)
status_options = ["All", "Watched", "Unwatched"]
status_menu = tk.OptionMenu(search_frame, status_var, *status_options)
status_menu.pack(side=tk.LEFT, padx=5, pady=5)


search_button = tk.Button(search_frame, text="Search")
search_button.pack(side=tk.LEFT, padx=5, pady=5)


class MovieNotFoundError(Exception):
    pass


def perform_search():
    """
    Perform a search based on the search terms
    :return:
    """
    results_listbox.delete(0, tk.END)

    search_terms = {
        'title': title_entry.get().lower(),
        'genre': genre_entry.get().lower(),
        'director': director_entry.get().lower(),
        'year': int(year_entry.get()) if year_entry.get().isdigit() else None,
        'status': status_var.get().lower() if status_var.get().lower() != "all" else None
    }

    search_terms = {key: value for key, value in search_terms.items() if value is not None}

    try:
        results = collection_manager.search(search_terms)

        if not results:
            raise MovieNotFoundError("No movies found matching the search criteria.")

        for film in results:
            results_listbox.insert(tk.END, str(film))
    except MovieNotFoundError as e:
        results_listbox.insert(tk.END, str(e))


def update_results_listbox():
    """
    Update the results listbox with the films in the collection
    :return: None
    """
    results_listbox.delete(0, tk.END)

    for film in collection_manager.films:
        results_listbox.insert(tk.END, str(film))


def show_reviews_comments():
    """
    Show the reviews and comments for the selected film
    :return: None
    """
    if selected_film is None:
        messagebox.showinfo("No selection", "No film selected. Please select a film from the list.")
        return

    reviews_comments_window = tk.Toplevel(root)
    reviews_comments_window.title(selected_film.title)

    reviews_label = tk.Label(reviews_comments_window, text="Reviews:")
    reviews_label.pack(side=tk.TOP, padx=5, pady=5)

    reviews_text = tk.Text(reviews_comments_window, height=10, width=50)
    reviews_text.pack(side=tk.TOP, padx=5, pady=5)

    for review in selected_film.reviews:
        reviews_text.insert(tk.END, str(review) + "\n")

    clear_reviews_button = tk.Button(reviews_comments_window, text="Clear Reviews")
    clear_reviews_button.pack(side=tk.TOP, padx=5, pady=5)

    def clear_reviews():
        """
        Clear the reviews for the selected film and update the text box
        :return: None
        """
        reviews_text.config(state=tk.NORMAL)
        selected_film.reviews = []
        reviews_text.delete(1.0, tk.END)
        reviews_text.update()
        reviews_text.config(state=tk.DISABLED)

    clear_reviews_button.config(command=clear_reviews)

    comments_label = tk.Label(reviews_comments_window, text="Comments:")
    comments_label.pack(side=tk.TOP, padx=5, pady=5)

    comments_text = tk.Text(reviews_comments_window, height=10, width=50)
    comments_text.pack(side=tk.TOP, padx=5, pady=5)

    for comment in selected_film.comments:
        comments_text.insert(tk.END, comment + "\n")

    clear_comments_button = tk.Button(reviews_comments_window, text="Clear Comments")
    clear_comments_button.pack(side=tk.BOTTOM, padx=5, pady=5)

    def clear_comments():
        """
        Clear the comments for the selected film and update the text box
        :return: None
        """
        comments_text.config(state=tk.NORMAL)
        selected_film.comments = []
        comments_text.delete(1.0, tk.END)
        comments_text.update()
        comments_text.config(state=tk.DISABLED)

    clear_comments_button.config(command=clear_comments)

    reviews_text.config(state=tk.DISABLED)
    comments_text.config(state=tk.DISABLED)


def add_review():
    """
    Add a review to the selected film
    :return: None
    """
    if selected_film is None:
        messagebox.showinfo("No selection", "No film selected. Please select a film from the list.")
        return

    review_window = tk.Toplevel(root)
    review_window.title("Add Review")

    review_label = tk.Label(review_window, text="Select your review (1-10):")
    review_label.pack(side=tk.TOP, padx=5, pady=5)

    review_scale = tk.Scale(review_window, from_=1, to=10, resolution=0.1, orient=tk.HORIZONTAL)
    review_scale.pack(side=tk.TOP, padx=5, pady=5)

    def submit_review():
        """
        Add the review to the selected film
        :return: None
        """
        review = review_scale.get()
        collection_manager.add_review(selected_film, str(review))
        review_window.destroy()

    submit_button = tk.Button(review_window, text="Submit Review", command=submit_review)
    submit_button.pack(side=tk.TOP, padx=5, pady=5)


def add_comment():
    """
    Add a comment to the selected film
    :return: None
    """
    if selected_film is None:
        messagebox.showinfo("No selection", "No film selected. Please select a film from the list.")
        return

    comment_window = tk.Toplevel(root)
    comment_window.title("Add Review")

    comment_label = tk.Label(comment_window, text="Enter your comment:")
    comment_label.pack(side=tk.TOP, padx=5, pady=5)

    comment_entry = tk.Entry(comment_window)
    comment_entry.pack(side=tk.TOP, padx=5, pady=5)

    def submit_comment():
        """
        Add the comment to the selected film
        :return: None
        """
        comment = comment_entry.get()
        collection_manager.add_comment(selected_film, comment)
        comment_window.destroy()

    submit_button = tk.Button(comment_window, text="Submit Comment", command=submit_comment)
    submit_button.pack(side=tk.TOP, padx=5, pady=5)


def add_film():
    """
    Add a film to the collection
    :return: None
    """
    add_film_window = tk.Toplevel(root)
    add_film_window.title("Add Film")

    title_label_add = tk.Label(add_film_window, text="Title:")
    title_label_add.pack(side=tk.TOP, padx=5, pady=5)
    title_entry_add = tk.Entry(add_film_window)
    title_entry_add.pack(side=tk.TOP, padx=5, pady=5)

    director_label_add = tk.Label(add_film_window, text="Director:")
    director_label_add.pack(side=tk.TOP, padx=5, pady=5)
    director_entry_add = tk.Entry(add_film_window)
    director_entry_add.pack(side=tk.TOP, padx=5, pady=5)

    genre_label_add = tk.Label(add_film_window, text="Genre:")
    genre_label_add.pack(side=tk.TOP, padx=5, pady=5)
    genre_entry_add = tk.Entry(add_film_window)
    genre_entry_add.pack(side=tk.TOP, padx=5, pady=5)

    year_label_add = tk.Label(add_film_window, text="Year:")
    year_label_add.pack(side=tk.TOP, padx=5, pady=5)
    year_entry_add = tk.Scale(add_film_window, from_=1895, to=datetime.now().year, resolution=1, orient=tk.HORIZONTAL)
    year_entry_add.pack(side=tk.TOP, padx=5, pady=5)

    status_var_add = tk.StringVar(value="Unwatched")
    status_label_add = tk.Label(add_film_window, text="Status:")
    status_label_add.pack(side=tk.TOP, padx=5, pady=5)
    status_options_add = ["Watched", "Unwatched"]
    status_menu_add = tk.OptionMenu(add_film_window, status_var_add, *status_options_add)
    status_menu_add.pack(side=tk.TOP, padx=5, pady=5)

    rating_label = tk.Label(add_film_window, text="Rating:")
    rating_label.pack(side=tk.TOP, padx=5, pady=5)
    rating_entry = tk.Scale(add_film_window, from_=1, to=10, resolution=0.1, orient=tk.HORIZONTAL)
    rating_entry.pack(side=tk.TOP, padx=5, pady=5)

    description_label = tk.Label(add_film_window, text="Description: (optional)")
    description_label.pack(side=tk.TOP, padx=5, pady=5)
    description_entry = tk.Entry(add_film_window)
    description_entry.pack(side=tk.TOP, padx=5, pady=5)

    def submit_film():
        """
        Add the film to the collection
        :return: None
        """
        title = title_entry_add.get()
        director = director_entry_add.get()
        genre = genre_entry_add.get()
        year = int(year_entry_add.get())
        status = status_var_add.get()
        rating = float(rating_entry.get())
        description = description_entry.get()

        collection_manager.add_film(title, director, year, genre, status, rating, description)

        update_results_listbox()

        add_film_window.destroy()

    submit_button = tk.Button(add_film_window, text="Submit Film", command=submit_film)
    submit_button.pack(side=tk.TOP, padx=5, pady=5)


def edit_film():
    """
    Edit the selected film
    :return: None
    """
    if selected_film is None:
        messagebox.showinfo("No selection", "No film selected. Please select a film from the list.")
        return

    film_to_edit = selected_film

    edit_film_window = tk.Toplevel(root)
    edit_film_window.title("Edit Film")

    title_label_edit = tk.Label(edit_film_window, text="Title:")
    title_label_edit.pack(side=tk.TOP, padx=5, pady=5)
    title_entry_edit = tk.Entry(edit_film_window)
    title_entry_edit.insert(0, film_to_edit.title)
    title_entry_edit.pack(side=tk.TOP, padx=5, pady=5)

    director_label_edit = tk.Label(edit_film_window, text="Director:")
    director_label_edit.pack(side=tk.TOP, padx=5, pady=5)
    director_entry_edit = tk.Entry(edit_film_window)
    director_entry_edit.insert(0, film_to_edit.director)
    director_entry_edit.pack(side=tk.TOP, padx=5, pady=5)

    genre_label_edit = tk.Label(edit_film_window, text="Genre:")
    genre_label_edit.pack(side=tk.TOP, padx=5, pady=5)
    genre_entry_edit = tk.Entry(edit_film_window)
    genre_entry_edit.insert(0, film_to_edit.genre)
    genre_entry_edit.pack(side=tk.TOP, padx=5, pady=5)

    year_label_edit = tk.Label(edit_film_window, text="Year:")
    year_label_edit.pack(side=tk.TOP, padx=5, pady=5)
    year_entry_edit = tk.Scale(edit_film_window, from_=1895, to=datetime.now().year, resolution=1, orient=tk.HORIZONTAL)
    year_entry_edit.set(film_to_edit.year)
    year_entry_edit.pack(side=tk.TOP, padx=5, pady=5)

    status_var_edit = tk.StringVar(value=film_to_edit.status)
    status_label_edit = tk.Label(edit_film_window, text="Status:")
    status_label_edit.pack(side=tk.TOP, padx=5, pady=5)
    status_options_edit = ["Watched", "Unwatched"]
    status_menu_edit = tk.OptionMenu(edit_film_window, status_var_edit, *status_options_edit)
    status_menu_edit.pack(side=tk.TOP, padx=5, pady=5)

    rating_label = tk.Label(edit_film_window, text="Rating:")
    rating_label.pack(side=tk.TOP, padx=5, pady=5)
    rating_entry = tk.Scale(edit_film_window, from_=1, to=10, resolution=0.1, orient=tk.HORIZONTAL)
    rating_entry.set(film_to_edit.rating)
    rating_entry.pack(side=tk.TOP, padx=5, pady=5)

    description_label = tk.Label(edit_film_window, text="Description: (optional)")
    description_label.pack(side=tk.TOP, padx=5, pady=5)
    description_entry = tk.Entry(edit_film_window)
    description_entry.insert(0, film_to_edit.description)
    description_entry.pack(side=tk.TOP, padx=5, pady=5)

    def submit_film():
        """
        Update the film with the new data
        :return: None
        """
        film_to_edit.title = title_entry_edit.get()
        film_to_edit.director = director_entry_edit.get()
        film_to_edit.genre = genre_entry_edit.get()
        film_to_edit.year = int(year_entry_edit.get())
        film_to_edit.status = status_var_edit.get()
        film_to_edit.rating = float(rating_entry.get())
        film_to_edit.description = description_entry.get()

        update_results_listbox()

        edit_film_window.destroy()

    submit_button = tk.Button(edit_film_window, text="Submit Changes", command=submit_film)
    submit_button.pack(side=tk.TOP, padx=5, pady=5)


def delete_film():
    """
    Delete the selected film
    :return: None
    """
    if selected_film is None or not results_listbox.curselection():
        messagebox.showinfo("No selection", "No film selected. Please select a film from the list.")
        return

    collection_manager.remove_film(selected_film)
    results_listbox.delete(results_listbox.curselection()[0])


def show_description():
    """
    Show the description of the selected film
    :return: None
    """
    if selected_film is None:
        messagebox.showinfo("No selection", "No film selected. Please select a film from the list.")
        return

    description_window = tk.Toplevel(root)
    description_window.title(selected_film.title)

    description_label = tk.Label(description_window, text="Description:")
    description_label.pack(side=tk.TOP, padx=5, pady=5)

    description_text = tk.Text(description_window, height=10, width=50)
    description_text.pack(side=tk.TOP, padx=5, pady=5)

    description_text.insert(tk.END, selected_film.description)

    description_text.config(state=tk.DISABLED)


def show_statistics():
    """
    Show statistics about the film collection
    :return: None
    """
    genre_counts = {}

    total_rating = 0
    num_films = 0

    review_counts = {}

    for film in collection_manager.films:
        if film.genre in genre_counts:
            genre_counts[film.genre] += 1
        else:
            genre_counts[film.genre] = 1

        total_rating += film.rating
        num_films += 1

        review_counts[film.title] = len(film.reviews)

    average_rating = round(total_rating / num_films, 2) if num_films else 0

    most_reviewed_film = max(review_counts, key=review_counts.get) if review_counts else "None"

    stats_window = tk.Toplevel(root)
    stats_window.title("Statistics")

    tk.Label(stats_window, text="Number of films in each genre:").pack()
    for genre, count in genre_counts.items():
        tk.Label(stats_window, text=f"{genre}: {count}").pack()

    tk.Label(stats_window, text=f"Average rating of films: {average_rating}").pack()
    tk.Label(stats_window, text=f"Most reviewed film: {most_reviewed_film}").pack()


def import_information():
    """
    Import film information from a file
    :return: None
    """
    with open('film_collection.txt', 'w') as f:
        for film in collection_manager.films:
            f.write(f"Title: {film.title}\n")
            f.write(f"Director: {film.director}\n")
            f.write(f"Year: {film.year}\n")
            f.write(f"Genre: {film.genre}\n")
            f.write(f"Status: {film.status}\n")
            f.write(f"Rating: {film.rating}\n")
            f.write(f"Description: {film.description}\n")
            f.write(f"Reviews: {', '.join(film.reviews)}\n")
            f.write(f"Comments: {', '.join(film.comments)}\n")
            f.write("\n")
    messagebox.showinfo("Success", "Film collection has been exported to film_collection.txt")


def on_film_select(event):
    """
    Handle the selection of a film in the results listbox
    :param event: The event that triggered the function
    :return: None
    """
    global selected_film

    if results_listbox.curselection():
        index = results_listbox.curselection()[0]
        selected_film = collection_manager.films[index]
    else:
        selected_film = None


results_listbox.bind('<<ListboxSelect>>', on_film_select)

search_button.config(command=perform_search)


button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X, ipadx=5, ipady=5)


group1_frame = tk.Frame(button_frame)
group1_frame.pack(side=tk.LEFT, padx=20, pady=5)
group2_frame = tk.Frame(button_frame)
group2_frame.pack(side=tk.LEFT, padx=20, pady=5)
group3_frame = tk.Frame(button_frame)
group3_frame.pack(side=tk.LEFT, padx=20, pady=5)


show_reviews_button = tk.Button(group1_frame, text="Show Reviews/Comments", command=show_reviews_comments)
show_reviews_button.pack(side=tk.LEFT, padx=5, pady=5)

add_review_button = tk.Button(group1_frame, text="Add Review", command=add_review)
add_review_button.pack(side=tk.LEFT, padx=5, pady=5)

add_comment_button = tk.Button(group1_frame, text="Add Comment", command=add_comment)
add_comment_button.pack(side=tk.LEFT, padx=5, pady=5)

add_film_button = tk.Button(group2_frame, text="Add Film", command=add_film)
add_film_button.pack(side=tk.LEFT, padx=5, pady=5)

edit_film_button = tk.Button(group2_frame, text="Edit Film", command=edit_film)
edit_film_button.pack(side=tk.LEFT, padx=5, pady=5)

delete_film_button = tk.Button(group2_frame, text="Delete Film", command=delete_film)
delete_film_button.pack(side=tk.LEFT, padx=5, pady=5)

show_description_button = tk.Button(group3_frame, text="Show Description", command=show_description)
show_description_button.pack(side=tk.LEFT, padx=5, pady=5)

show_statistics_button = tk.Button(group3_frame, text="Show Statistics", command=show_statistics)
show_statistics_button.pack(side=tk.LEFT, padx=5, pady=5)

import_info_button = tk.Button(group3_frame, text="Import Information", command=import_information)
import_info_button.pack(side=tk.LEFT, padx=5, pady=5)


root.mainloop()
