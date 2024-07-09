from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from model import Movie
from data import movies

app = FastAPI()
app.title = 'Byhako App'
app.version = '0.1.0'


@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hola Ruben jajaj</h1>')


@app.get('/movies', tags=['Movie'])
def get_movie():
    return movies


@app.get('/movie/{id}', tags=['Movie'])
def get_movie(id: int):
    return list(filter(lambda x: x['id'] == id, movies))


@app.get('/movie/', tags=['Movie'])
def get_movies_by_category(category: str):
    return list(filter(lambda x: x['category'] == category, movies))


@app.post('/movie', tags=['Movie'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies


@app.put('/movie/{id}', tags=['Movie'])
def update_movie(id: int, new_movie: Movie):
    movie_list = list(filter(lambda x: x['id'] == id, movies))
    if (len(movie_list)):
        movie = movie_list[0]
        index = movies.index(movie)
        movies[index] = new_movie

        return new_movie
    else:
        return 'Movie not found'


@app.delete('/movie/{id}', tags=['Movie'])
def delete_movie(id: int):
    movie_list = list(filter(lambda x: x['id'] == id, movies))
    if (len(movie_list)):
        movie = movie_list[0]
        movies.remove(movie)

        return 'Movie deleted'
    else:
        return 'Movie not found'