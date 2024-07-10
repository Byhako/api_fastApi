from fastapi import Depends, FastAPI, Path, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from model import JWTBearer, Movie, User
from typing import List
from data import movies
from jwt_manager import create_token

app = FastAPI()
app.title = 'Byhako App'
app.version = '0.1.0'


# LOGIN
@app.post('/login', tags=['Auth'])
def login(user: User):
    if user.email == 'toto@mail.com' and user.password == 'toto':
        token: str = create_token(user.model_dump())
        return JSONResponse(
            content={ 'token': token },
            status_code=status.HTTP_202_ACCEPTED
            )
    else:
        return JSONResponse(
            content={ 'token': None },
            status_code=status.HTTP_401_UNAUTHORIZED
            )

@app.get('/logout', tags=['Auth'])
def logout():
    return 'OK'

@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hola Ruben jajaj</h1>')


@app.get(
    '/movies',
    tags=['Movie'],
    response_model=List[Movie],
    dependencies=[Depends(JWTBearer())]
)
def get_movie() -> List[Movie]:
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
