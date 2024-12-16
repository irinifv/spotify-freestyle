# spotify-freestyle

A web app that allows users to search for Spotify artists, visualize popularity, and explore related artists.

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Add your Spotify API credentials to a `.env` file.
4. Run the app: `python app/main.py`.

## Features
- Search for artists.
- Visualize artist popularity.
- Explore related artists and albums.


## Usage
Run the web app (then view in the browser at http://localhost:5000/):

```sh
# Mac OS:
FLASK_APP=web_app flask run

# Windows OS:
# ... if `export` doesn't work for you, try `set` instead
# ... or set FLASK_APP variable via ".env" file
export FLASK_APP=web_app
flask run
```



## Testing

Run tests:

```sh
pytest
```

## Old Code Bin
```
main.py
from app import create_app

# Create the Flask app using the factory function
app = create_app()

if __name__ == "__main__":
    # Run the app in debug mode
    app.run(debug=True)
```
