## Install packages

`pip install --require-virtualenv -r requirements.txt`

## Starting the server

#### ⚠️ Your terminal should be inside "app" before attempting to launch the server
#### If you need to use another port, add the flag `--port`
#### Add flag `--reload` to refresh the server at each code change

`granian --interface asgi main:app`

## Testing

Run tests using :

`pytest app`

## Developer tools

### Linter
https://docs.astral.sh/ruff/linter/

`ruff check app --watch`

### Format
https://docs.astral.sh/ruff/formatter/

`ruff format app`