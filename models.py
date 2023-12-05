from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    instructions = db.Column(db.Text)
    servings = db.Column(db.Integer)
    difficulty = db.Column(db.String(50))
    cuisine = db.Column(db.String(50))
    image = db.Column(db.String(500))
    category = db.Column(db.String(100))
    ingredients = db.relationship('Ingredient', secondary='recipe_ingredients', backref='recipes', lazy=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ratings = db.relationship('UserRating', cascade="all, delete", backref='recipe', lazy=True)

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    profile_info = db.Column(db.String(500))
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    favourites = db.relationship('Recipe', secondary='user_favourites', backref='users', lazy=True)
    ratings = db.relationship('UserRating', cascade="all, delete", backref='user', lazy=True)

class UserFavourite(db.Model):
    __tablename__ = 'user_favourites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

class UserRating(db.Model):
    __tablename__ = 'user_ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete="CASCADE"))
    rating = db.Column(db.Integer)
    review = db.Column(db.String(500))
