from bs4 import BeautifulSoup
import requests
from tkinter import *
from pathlib import Path
import os

"""A GUI application that creates a list of the top 100 movies scraped from Empire Online and allows the user to delete
them individually until they have marked off all movies."""

# Colors
DARK = "#222831"
MID = "#393E46"
BLUE = "#00ADB5"
WHITE = "#EEEEEE"


class MovieList:
    """A class to handle all the movies and GUI"""
    def __init__(self):
        """Create window, header, and reset button."""
        self.list = []
        self.movie_objects = []
        self.button_objects = []

        # Window config
        self.window = Tk()
        self.window.minsize(400, 400)
        self.window.config(bg=MID, pady=20, padx=20)
        self.window.title("Movies to Watch App")

        self.header = Label(text=f"Movies to Watch: {len(self.list)}", bg=MID, font=("arial", 20, "bold"), fg=BLUE)
        self.header.grid(column=0, row=0, padx=5, pady=15, columnspan=12)
        reset = Button(text="Reset List", fg=BLUE, bg=DARK, font=("georgia", 12, "bold"), command=self.reset)
        reset.grid(column=13, row=0)
        self.get_movies()

    def reset(self):
        """Removes movie file to restart list."""
        os.remove("movies.txt")
        self.get_movies()

    def delete_entry(self, num):
        """Remove the item from movie list and remove its corresponding label and button."""
        item = self.list[num]
        self.list.remove(item)
        delete_button = self.button_objects[num]
        label_title = self.movie_objects[num]
        label_title.grid_forget()
        delete_button.grid_forget()
        self.update_list()

    def update_list(self):
        """Open the movie list file and rewrite it with the removed movies. Remove all previous buttons and labels."""
        with open(file="movies.txt", mode="w") as file:
            for movie in self.list:
                file.writelines(movie)
        self.display_movies()

    def get_movies(self):
        """Use beautiful soup to scrape the top 100 list of movies from Empire Online if the movie list file has not
         been created. If it has, check its entries and add them into the movie list."""
        try:
            with open(file="movies.txt", mode="r") as file:
                content = file.readlines()
            self.list = content
            self.display_movies()

        except FileNotFoundError:
            if not Path("to_do.txt").exists():
                url = "https://www.empireonline.com/movies/features/best-movies-2/"
                response = requests.get(url=url).text
                soup = BeautifulSoup(markup=response, features="html.parser")
                titles = soup.find_all(name="h3")

                movie_list = [title.getText() for title in titles]
                movie_list = movie_list[::-1]
                with open(file="movies.txt", mode="w") as file:
                    for item in movie_list:
                        file.writelines(item + "\n")
                with open(file="movies.txt", mode="r") as file:
                    content = file.readlines()
                self.list = content
            self.display_movies()

    def display_movies(self):
        """Removes previous button and labels(if they exist). Create labels & buttons for each movie in the movie list,
         maximum 15 entries per column. Add these to corresponding movie and button lists for easy deletion."""
        for each in self.movie_objects:
            each.grid_forget()
        for each in self.button_objects:
            each.grid_forget()
        self.header.config(text=f"Movies to Watch: {len(self.list)}")
        count = 1
        column = 2
        column_jump = [21, 41, 61, 81,]
        for movie in self.list:
            movie_title = Label(text=movie, bg=MID, fg=BLUE, anchor="nw", font=("arial", 10, "bold"), wraplength=300)
            movie_title.grid(column=column, row=count, padx=1, sticky="w")
            delete_button = Button(text="Delete", fg=BLUE, bg=DARK, font=("georgia", 8, "bold"),
                            command=lambda num=self.list.index(movie): self.delete_entry(num))
            delete_button.grid(column=column-1, row=count, pady=3, padx=5, sticky="e")

            count += 1
            if count in column_jump:
                column += 2
                count = 1
            self.movie_objects.append(movie_title)
            self.button_objects.append(delete_button)


m_list = MovieList()
m_list.window.mainloop()
