from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

gameStop = [
    {
        'id': 1,
        'name': 'god_of_war',
        'cost': 60
     },
    {
        'id': 2,
        'name': 'cuphead',
        'cost': 30
    },
    {
        'id': 3,
        'name': 'mario_odyssey',
        'cost': 60
    },
    {
        'id': 4,
        'name': 'sonic_forces',
        'cost': 1.75
    }
]


class Game(BaseModel):
    name: str
    cost: float


class UpdateGame(BaseModel):
    name: Optional[str] = None
    cost: Optional[float] = None


@app.get('/get-game/{game_id}')
def get_game(
    game_id: int = Path(
        None,
        description="Fill with ID of the game you want to view")):

    search = list(filter(lambda x: x["id"] == game_id, gameStop))

    if search == []:
        return {'Error': 'Game does not exist'}

    return {'Game': search[0]}


@app.get('/get-by-name')
def get_game(name: Optional[str] = None):

    search = list(filter(lambda x: x["name"] == name, gameStop))

    if search == []:
        return {'game': 'Does not exist'}

    return {'Game': search[0]}


@app.get('/list-gameStop')
def listar():
    return {'GameStop': gameStop}


@app.post('/create-game/{game_id}')
def create_game(game_id: int, game: Game):

    search = list(filter(lambda x: x["id"] == game_id, gameStop))

    if search != []:
        return {'Error': 'Game exists'}

    game = game.dict()
    game['id'] = game_id

    gameStop.append(game)
    return game


@app.put('/update-game/{game_id}')
def update_game(game_id: int, game: UpdateGame):

    search = list(filter(lambda x: x["id"] == game_id, gameStop))

    if search == []:
        return {'Game': 'Does not exist'}

    if game.name is not None:
        search[0]['name'] = game.name

    if game.price is not None:
        search[0]['price'] = game.price

    return search


@app.delete('/delete-game/{game_id}')
def delete_game(game_id: int):
    search = list(filter(lambda x: x["id"] == game_id, gameStop))

    if search == []:
        return {'Game': 'Does not exist'}

    for i in range(len(gameStop)):
        if gameStop[i]['id'] == game_id:
            del gameStop[i]
            break
    return {'Message': 'Game deleted successfully'}