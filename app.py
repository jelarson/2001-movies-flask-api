# Movie App - API

# Flask app
# I want FULL CRUD functionality

# DB must contain these columns:
# id
# title
# year
# rating
# genre
# starring

# BONUS:
# Build a static front-end using Flask's render_template method

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Movie(db.Model): 
    __tablename__ = 'movies' 
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(100), nullable=False) 
    year = db.Column(db.String(4), nullable=False)
    rating = db.Column(db.String(5), nullable=False)
    genre = db.Column(db.String(20), nullable=False)
    starring = db.Column(db.String(40), nullable=False)

    def __init__(self, title, year, rating, genre, starring):
        self.title = title 
        self.year = year
        self.rating = rating
        self.genre = genre
        self.starring = starring

class MovieSchema(ma.Schema): 
    class Meta: 
        fields = ('id', 'title', 'year', 'rating', 'genre', 'starring')

movie_schema = MovieSchema() 
movies_schema = MovieSchema(many=True) 



# GET
@app.route('/movies', methods=['GET']) 
def get_movies():
    all_movies = Movie.query.all()
    result = movies_schema.dump(all_movies) 
    return jsonify(result)

# Single item GET
@app.route('/movie/<id>', methods=['GET'])
def get_movie(id):
  movie = Movie.query.get(id)
  return movie_schema.jsonify(movie)

# POST
@app.route('/movie', methods=['POST'])
def add_movie():
  title = request.json['title']
  year = request.json['year']
  rating = request.json['rating']
  genre = request.json['genre']
  starring = request.json['starring']

  new_movie = Movie(title, year, rating, genre, starring)

  db.session.add(new_movie)
  db.session.commit()

  movie = Movie.query.get(new_movie.id)

  return movie_schema.jsonify(movie)

# PUT / PATCH
@app.route('/movie/<id>', methods=['PUT'])
def movie_update(id):
  movie = Movie.query.get(id)
  title = request.json['title']
  year = request.json['year']
  rating = request.json['rating']
  genre = request.json['genre']
  starring = request.json['starring']

  movie.title = title
  movie.year = year
  movie.rating = rating
  movie.genre = genre
  movie.starring = starring

  db.session.commit()
  return movie_schema.jsonify(movie)

# Delete
@app.route('/movie/<id>', methods=['DELETE'])
def movie_delete(id):
  movie = Movie.query.get(id)
  db.session.delete(movie)
  db.session.commit()

  return movie_schema.jsonify(movie)



if __name__ == '__main__': 
    app.run(debug=True)
    app.run()

