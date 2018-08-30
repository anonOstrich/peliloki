from flask import redirect, render_template, request, url_for

from application import app, db, login_required
from application.genres.models import Genre, GameGenre
from application.genres.forms import GenreCreationForm
from application.games.models import Game
from application.constants import GAME_RESULTS_PER_PAGE

@app.route("/genres", methods = ["GET"])
def genres_index(page_number = 1): 
    sorted_genres = Genre.find_genres_sorted_by_number_of_games()

    return render_template("genres/list.html", genres = sorted_genres, form = GenreCreationForm())

@app.route("/genres", methods = ["POST"])
@login_required(role="ADMIN")
def genres_create(): 
    form = GenreCreationForm(request.form)
    if not form.validate():
        return render_template("genres/list.html", genres = Genre.query.all(), form=form)

    g = Genre(form.name.data)
    if Genre.query.filter_by(name=g.name).first():
        return render_template("genres/list.html", genres = Genre.query.all(),
                                error = "Samaa genreä ei voi lisätä kahdesti", form=form)

    db.session.add(g)
    db.session.commit()
    return redirect(url_for("genres_index"))


# Näkymä kaikille yhden genren peleille
@app.route("/genres/<genre_id>", methods=["GET"])
@app.route("/genres/<genre_id>/page/<page_number>", methods=["GET"])
def genres_view(genre_id, page_number = 1): 
    genre = Genre.query.filter_by(id=genre_id).first()


    if genre is None: 
        return render_template("error.html", error = "Genreä ei ole olemassa")

    games_info = Game.find_all_info({"genres": [genre.id]}, page_number = int(page_number))
    base_url = "/genres/" + str(genre_id) + "/page"
    
    return render_template("games/list.html", games_info = games_info, title = ("Genre: " + genre.name),
     page_number = int(page_number), last_page = len(games_info) < GAME_RESULTS_PER_PAGE,  base_url = base_url)