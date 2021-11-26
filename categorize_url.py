from pymongo import MongoClient

client = MongoClient()
db = client.moovle

def homepage():
    db.pages.update(
        {'url': {'$regex': 'https?://[^/]+$'}, 'category': {'$exists': False}},
        {'$set': {'category': 'homepage'}},
        multi=True
    )

def movie():
    db.pages.update(
        {
            '$or': [
                {'url': {'$regex': 'https?://www.imdb.com/title/[^/]+/$'}},
                {'url': {'$regex': 'https?://www.rottentomatoes.com/m/[^/]+/$'}},
                {'url': {'$regex': 'https?://www.movies.com/[^/]+/m[^/]+/$'}},
                {'url': {'$regex': 'https?://www.allmovie.com/movie/'}},
                {'url': {'$regex': 'https?://letterboxd.com/film/[^/]+/$'}},
                {'url': {'$regex': 'https?://www.metacritic.com/movie/[^/]+/$'}},
                {'url': {'$regex': 'https?://www.themoviedb.org/movie/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/film/'}},
            ],
            'category': {'$exists': False}
        },
        {'$set': {'category': 'movie'}},
        multi=True
    )

def news():
    db.pages.update(
        {
            '$or': [
                {'url': {'$regex': 'https?://www.imdb.com/news/ni[^/]+/$'}},
                {'url': {'$regex': 'https?://editorial.rottentomatoes.com/article/'}},
                {'url': {'$regex': 'https?://www.movies.com/movie-news/'}},
            ],
            'category': {'$exists': False}
        },
        {'$set': {'category': 'news'}},
        multi=True
    )

def person():
    db.pages.update(
        {
            '$or': [
                {'url': {'$regex': 'https?://www.rottentomatoes.com/celebrity/'}},
                {'url': {'$regex': 'https?://www.allmovie.com/artist/'}},
                {'url': {'$regex': 'https?://letterboxd.com/actor/'}},
                {'url': {'$regex': 'https?://www.metacritic.com/person/'}},
                {'url': {'$regex': 'https?://www.themoviedb.org/person/'}},
                {'url': {'$regex': 'https?://www.imdb.com/name/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/actor/'}},
                {'url': {'$regex': 'https?://letterboxd.com/producer/'}},
                {'url': {'$regex': 'https?://www.movies.com/actors/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/producer/'}},
            ],
            'category': {'$exists': False}
        },
        {'$set': {'category': 'person'}},
        multi=True
    )

def guide():
    db.pages.update(
        {
            '$or': [
                {'url': {'$regex': 'https?://editorial.rottentomatoes.com/guide/'}},
            ],
            'category': {'$exists': False}
        },
        {'$set': {'category': 'guide'}},
        multi=True
    )

def gallery():
    db.pages.update(
        {
            '$or': [
                {'url': {'$regex': 'https?://editorial.rottentomatoes.com/gallery/'}},
                {'url': {'$regex': 'https?://www.imdb.com/gallery/'}},
            ],
            'category': {'$exists': False}
        },
        {'$set': {'category': 'gallery'}},
        multi=True
    )

def uncategorized():
    db.pages.update(
        {
            '$or': [
                {'url': {'$regex': 'https?://www.allmovie.com/characteristic/'}},
                {'url': {'$regex': 'https?://www.allmovie.com/genre/'}},
                {'url': {'$regex': 'https?://www.rottentomatoes.com/browse/'}},
                {'url': {'$regex': 'https?://www.imdb.com/search/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/[^/]+/$'}, 'title': {'$regex': 'profile'}},
                {'url': {'$regex': 'https?://letterboxd.com/[^/]+/$'}, 'title': {'$regex': 'profile'}},
                {'url': {'$regex': 'https?://editorial.rottentomatoes.com/tag/'}},
                {'url': {'$regex': 'https?://www.imdb.com/chart/'}},
                {'url': {'$regex': 'https?://www.imdb.com/list/'}},
                {'url': {'$regex': 'https?://www.themoviedb.org/account/'}},
                {'url': {'$regex': 'https?://feedback.letterboxd.com/users/'}},
                {'url': {'$regex': 'https?://www.allmovie.com/subgenre/'}},
                {'url': {'$regex': 'https?://www.imdb.com/poll/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/editor/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/writer/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/costumes/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/composer/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/production-design/'}},
                {'url': {'$regex': 'https?://letterboxd.com/editor/'}},
                {'url': {'$regex': 'https?://letterboxd.com/writer/'}},
                {'url': {'$regex': 'https?://letterboxd.com/costumes/'}},
                {'url': {'$regex': 'https?://letterboxd.com/composer/'}},
                {'url': {'$regex': 'https?://letterboxd.com/production-design/'}},
                {'url': {'$regex': 'https?://letterboxd.com/[^/]+/list/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/[^/]+/list/'}},
            ],
            'category': {'$exists': False}
        },
        {'$set': {'category': None}},
        multi=True
    )

def review():
    db.pages.update(
        {
            '$or': [
                {'url': {'$regex': 'https?://letterboxd.com/reviews/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/reviews/'}},
                {'url': {'$regex': 'https?://letterboxd.com/[^/]+/film/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/[^/]+/film/'}},
            ],
            'category': {'$exists': False}
        },
        {'$set': {'category': 'review'}},
        multi=True
    )

def series():
    db.pages.update(
        {
            '$or': [
                {'url': {'$regex': 'https?://www.rottentomatoes.com/tv/'}},
                {'url': {'$regex': 'https?://www.themoviedb.org/tv/'}},
            ],
            'category': {'$exists': False}
        },
        {'$set': {'category': 'series'}},
        multi=True
    )

def event():
    db.pages.update(
        {
            '$or': [
                {'url': {'$regex': 'https?://www.imdb.com/[^/]+/'}, 'title': {'$regex': 'festival', '$options': '$i'}},
            ],
            'category': {'$exists': False}
        },
        {'$set': {'category': 'event'}},
        multi=True
    )

def blog():
    db.pages.update(
        {
            '$or': [
                {'url': {'$regex': 'https?://www.allmovie.com/blog/'}},
                {'url': {'$regex': 'https?://feedback.letterboxd.com/forums/'}},
            ],
            'category': {'$exists': False}
        },
        {'$set': {'category': 'blog'}},
        multi=True
    )

def company():
    db.pages.update(
        {
            '$or': [
                {'url': {'$regex': 'https?://www.imdb.com/company/'}},
            ],
            'category': {'$exists': False}
        },
        {'$set': {'category': 'company'}},
        multi=True
    )

def detail():
    db.pages.update(
        {
            '$or': [
                {'url': {'$regex': 'https?://www.metacritic.com/movie/[^/]+/details/'}},
                {'url': {'$regex': 'https?://letterboxd.com/film/[^/]+/genres/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/film/[^/]+/genres/'}},
                {'url': {'$regex': 'https?://letterboxd.com/film/[^/]+/details/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/film/[^/]+/details/'}},
                {'url': {'$regex': 'https?://letterboxd.com/film/[^/]+/likes/'}},
                {'url': {'$regex': 'https?://www.letterboxd.com/film/[^/]+/likes/'}},
            ],
            'category': {'$exists': False}
        },
        {'$set': {'category': 'detail'}},
        multi=True
    )

def trailer():
    db.pages.update(
        {
            '$or': [
                {'url': {'$regex': 'trailers?', '$options': '$i'}}
            ],
            'category': {'$exists': False}
        },
        {'$set': {'category': 'trailer'}},
        multi=True
    )

def remove_not_related():
    db.pages.remove(
        {
            '$or': [
                {'url': {'$regex': '/api/', '$options': '$i'}},
                {'url': {'$regex': 'https?://feedback.letterboxd.com/admin/', '$options': '$i'}},
            ],
            'category': {'$exists': False}
        }
    )

homepage()
movie()
person()
news()
guide()
gallery()
series()
event()
blog()
company()
detail()
trailer()
uncategorized()
remove_not_related()
review()