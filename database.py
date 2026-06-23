movies = {}

def add_movie(key, message_id):
    movies[key] = message_id

def get_movie(key):
    return movies.get(key)
