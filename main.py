from fastapi import FastAPI, Path, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from model import Movie
from typing import List
from data import movies

app = FastAPI()
app.title = 'Byhako App'
app.version = '0.1.0'


@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hola Ruben jajaj</h1>')


@app.get('/movies', tags=['Movie'], response_model=List[Movie])
def get_movie():
    return JSONResponse(
        content=movies,
        status_code=status.HTTP_200_OK
        )


@app.get('/movie/{id}', tags=['Movie'], response_model=List[Movie])
def get_movie(id: int=Path(ge=1, le=2000)):
    list_movies = list(filter(lambda x: x['id'] == id, movies))
    return JSONResponse(
        content=list_movies,
        status_code=status.HTTP_200_OK
        )


@app.get('/movie/', tags=['Movie'], response_model=List[Movie])
def get_movies_by_category(category: str=Query(min_length=5, max_length=15)):
    list_movies = list(filter(lambda x: x['category'] == category, movies))
    return JSONResponse(
        content=list_movies,
        status_code=status.HTTP_200_OK
        )


@app.post('/movie', tags=['Movie'])
def create_movie(movie: Movie):
    movies.append(movie.model_dump())
    return JSONResponse(
        content=movies,
        status_code=status.HTTP_201_CREATED
        )


@app.put('/movie/{id}', tags=['Movie'])
def update_movie(id: int, new_movie: Movie):
    movie_list = list(filter(lambda x: x['id'] == id, movies))
    if (len(movie_list)):
        movie = movie_list[0]
        index = movies.index(movie)
        movies[index] = new_movie

        return JSONResponse(
            content=new_movie,
            status_code=status.HTTP_202_ACCEPTED
            )
    else:
        return JSONResponse(
            content={ 'message': 'Movie not found' },
            status_code=status.HTTP_404_NOT_FOUND
            )


@app.delete('/movie/{id}', tags=['Movie'], response_model=dict)
def delete_movie(id: int):
    movie_list = list(filter(lambda x: x['id'] == id, movies))
    if (len(movie_list)):
        movie = movie_list[0]
        movies.remove(movie)

        return JSONResponse(
            content={ 'message': 'Movie deleted' },
            status_code=status.HTTP_200_OK
            )
    else:
        return JSONResponse(
            content={ 'message': 'Movie not found' },
            status_code=status.HTTP_404_NOT_FOUND
            )
