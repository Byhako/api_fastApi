from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = 'Byhako App'
app.version = '0.1.0'

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Accion"
    },
    {
        "id": 2,
        "title": "Potter",
        "overview": "Un mago poderoso pero chillon",
        "year": "2009",
        "rating": 7.8,
        "category": "Aventura"
    }
]


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
def create_movie(
    id: int=Body(),
    title: str=Body(),
    overview: str=Body(),
    year: int=Body(),
    rating: float=Body(),
    category: str=Body()
    ):
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category,
    })
    return movies


@app.put('/movie/{id}', tags=['Movie'])
def update_movie(
    id: int,
    title: str=Body(),
    overview: str=Body(),
    year: int=Body(),
    rating: float=Body(),
    category: str=Body()
    ):
    movie_list = list(filter(lambda x: x['id'] == id, movies))
    if (len(movie_list)):
        movie = movie_list[0]
        index = movies.index(movie)
        movie['title'] = title
        movie['overview'] = overview
        movie['rating'] = rating
        movie['year'] = year
        movie['category'] = category

        movies[index] = movie

        return movie
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