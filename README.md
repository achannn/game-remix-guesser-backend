# Game Remix Guesser

This is the server for the Game Remix Guesser app. It's a FastAPI Python app run using a WSGI, preferably `uvicorn`. The Python app communicates with a postgres database so as to be able to quickly generate Questions and check Answers.

See `Dockerfile`, `docker-compose.yml`, and `requirements.txt` for more information on libraries and technologies.

## Terms

A "remix" is a musician's reinterpretation of a song. In this case, all songs are from videogames. "To remix" a song is to remake it in your own style, while maintaining enough musical elements so that the original song is still recognizable.

Ocremix is a more than 10 years old website where artists have been uploading remixes of videogame music. The url is https://ocremix.org.

## Gameplay

Send a `GET` to `/game` to receive a `Question`. A `Question` is a dictionary (object) with the properties `choices` and `question`.

```JSON
{
  "choices": [
    {
      "origin_game": "Bonk's Adventure",
      "public_id": 141005297
    },
    {
      "origin_game": "Ecco the Dolphin",
      "public_id": 343436227
    },
    {
      "origin_game": "OutRun",
      "public_id": 745909131
    },
    {
      "origin_game": "Shinobi",
      "public_id": 526338364
    }
  ],
  "question": {
    "remix_youtube_url": "www.youtube.com/embed/0Wqrz01KU2Q",
    "secret_id": 963516206
  }
}
```


`Question.choices` is a list (array) of four `Choice`s. A `Choice` is a dictionary with the properties `origin_game`, which indicates a real videogame title, and `public_id`, which is an id to identify that `Choice` against a `Remix`'s matching `public_id`. Learn more about `Remix`es below.

`Question.question` is a dictionary with the properties `remix_youtube_url`, which is a URL to a youtube video of a `Remix` song, and `secret_id`, an id to identify a `Choice` against a `Remix`.

In order to "win," the user must listen to the youtube video linked in the `Question.question.remix_youtube_url`, then decide which game had the song that has been remixed. When they decide, create a `Answer` object consisting of the `secret_id` from `Question.question` and the `public_id` of the given `choice`.

Send the `Answer` object as the body of a `POST` to `/game` and the server will respond either with a `200` if the answer is correct, or a `422` if the answer is incorrect. If the answer is correct, the server will also send a `CorrectAnswerPackage` with the `origin_game` indicating the game which contained the original song, the `remix_artist` indicating the user that uploaded the remix to Ocremix, `ocremix_remix_url` linking to the remix on ocremix.org, and `original_song_title` indicaating the title of the song that was remixed to create the remix.

Guesses are unlimited. No points are tracked.

A `Remix` is an internal (not exposed to clients) Class that represents an Ocremix "Remix," such as https://ocremix.org/game/48/donkey-kong-country-2-diddys-kong-quest-snes . Each Remix has an id, a youtube video of the song itself, a `remix_title` of the song's "remix" name (different from the original song name), a `remix_artist_id` of the Ocremix User who uploaded it, a `remix_original_song_id` referring to an `OriginalSong` of which the `Remix` is a remix, and a `public_id` and `secret_id`.

Learn more about the various database models in `app/models.py`.

## Limitations

### Cheating

`publid_id` and `secret_id`s are both generated once (on app instantiation, using `randint`) and remain the same forever. If the app goes undeployed for a while, it would be possible for someone to create their own map of `public_id`s that match `secret_id`s. However, this is functionally identical to someone simply creating a map of each song to each origin game title, so it doesn't really matter (this is the equivalent of passing a test by memorizing the textbook).

Also, because answer checking doesn't use any kind of session ID, someone could simply send a `POST` request as illustrated above using another device other than the browser tab playing the game, to check answers. I don't know why anybody would be taking this game that seriously but just keep an eye out if you're playing with a buddy and they look to have `curl` open on their phone.

### Dependency on Youtube

This only works because all songs are hosted on Youtube. There are over 4,000 songs that I found, far more than I can afford to host. If Youtube ever takes any songs down, the app simply won't work anymore.


## Development

The app can be run in python directly, but I don't recommend it. Instead, use docker. If you do use docker, make sure environment variables in `.env` are visible to python.

Ensure docker is installed on your machine. Ensure your version of docker is recent enough to be able to do `docker compose` commands. If you can't do this, ensure `docker-compose` is also installed. Ideally, install these things are installed in a way that doesn't require using `sudo` do run docker commands.

Copy `example.env` to `.env`.

Then, do:

```bash
docker compose up
```

Any changes you make to `/app` files should automatically trigger a restart of the fastapi server running in docker.

### Database Changes

There's no Alembic yet, so any changes that modify database tables (add / remove columns) require a tear-down of the docker volume. From the backend folder, do

```bash
docker volume ls
```

Look for volumes with `mysql` in the name. For each of those volumes, do

```bash
docker volume rm {volume_name}
```

### Docker Issues

Docker is hard (for me) to clean up after properly.

With any bugs, a good first step is to just TOTALLY whipe out docker. It can persist code in unexpected ways.

Make sure the the image is properly deleted:

```bash
docker image ls
```

Get the image ID for the api / backend, then copy into:

```bash
docker image rmi {id}
```

Make sure the volume is properly deleted:


```bash
docker volume ls
```

Copy the volume name, then paste into:

```bash
docker volume rm {name}
```
