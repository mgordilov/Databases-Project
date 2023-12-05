from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from models import (
    Recipe,
    Ingredient,
    RecipeIngredient,
    User,
    UserFavourite,
    UserRating,
    db,
)

app = Flask(__name__)
app.config.from_object('config')

with app.app_context():
    db.init_app(app)
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'


@app.route('/')
def index():
    return render_template('index.html', recipes=Recipe.query.all())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))







# SIGN-UP AND LOGIN(OUT) ACTIONS
@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_call():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        flash('Username/email already exists')
        return redirect(url_for('signup_page'))

    user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_call():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        flash('Please fill out all fields')
        return redirect(url_for('login_page'))

    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No such user existing!')
        return redirect(url_for('login_page'))
    if password != user.password:
        flash('Invalid password')
        return redirect(url_for('login_page'))
    login_user(user)

    return redirect(url_for('dashboard', username=user.username))

@app.route('/logout', methods=['GET'])
@login_required
def logout_call():
    logout_user()
    flash('Successfully logged out!')
    return redirect(url_for('index'))

@app.route('/account/<username>')
@login_required
def dashboard(username):
    if username == current_user.username:
        user = User.query.filter_by(username=username).first()
        favorite_recipes = user.favourites
        return render_template('dashboard.html', user=User.query.filter_by(username=username).first(), recipes=Recipe.query.filter_by(author_id=current_user.id).all(), favourites = favorite_recipes)
    else:
        return redirect(url_for('index'))

@app.route('/account/<username>/edit', methods=['POST'])
@login_required
def edit_account(username):
    username = request.form.get('username')
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    personal_info = request.form.get('personal_info')

    user = User.query.get(current_user.id)
    user.username = username
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.profile_info = personal_info

    db.session.commit()
    return redirect(url_for('dashboard', username=user.username))





@app.route('/create-recipe', methods=['POST'])
def create_recipe_call():
    if not current_user.is_authenticated:
        flash('Please login first')
        return redirect(url_for('login_page'))
    else:
        name = request.form.get('name')
        description = request.form.get('description')
        ingredient_names = request.form.getlist('ingredient')
        prep_time = request.form.get('prep_time')
        cook_time = request.form.get('cook_time')
        instructions = request.form.get('instructions')
        servings = request.form.get('servings')
        difficulty = request.form.get('difficulty')
        cuisine = request.form.get('cuisine')
        image = request.form.get('image')
        
        recipe = Recipe(name=name, description=description, prep_time=prep_time, cook_time=cook_time, instructions=instructions, servings=servings, difficulty=difficulty, cuisine=cuisine, image=image, author_id=current_user.id)

        for ingredient_name in ingredient_names:
            ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
            if not ingredient:
                ingredient = Ingredient(name=ingredient_name)
            recipe.ingredients.append(ingredient)

        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('catalogue'))

@app.route('/recipe/<int:recipe_id>/edit', methods=['POST'])
def edit_recipe_call(recipe_id):
    name = request.form.get('name')
    description = request.form.get('description')
    prep_time = request.form.get('prep_time')
    cook_time = request.form.get('cook_time')
    instructions = request.form.get('instructions')
    servings = request.form.get('servings')
    difficulty = request.form.get('difficulty')
    cuisine = request.form.get('cuisine')
    image = request.form.get('image')
    
    recipe = Recipe.query.get(recipe_id)
    recipe.name = name
    recipe.description = description
    recipe.prep_time = prep_time
    recipe.cook_time = cook_time
    recipe.instructions = instructions
    recipe.servings = servings
    recipe.difficulty = difficulty
    recipe.cuisine = cuisine
    recipe.image = image
    db.session.commit()
    return redirect(url_for('recipe_page', recipe_id=recipe_id))

@app.route('/recipe/<int:recipe_id>/delete', methods=['GET'])
@login_required
def delete_recipe_page(recipe_id):
    if current_user.id == Recipe.query.get(recipe_id).author_id:
        return render_template('delete.html', recipe=Recipe.query.get(recipe_id))
    flash('You are not authorized to delete this recipe')
    return redirect(url_for('recipe_page', recipe_id=recipe_id))

@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe_call(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('dashboard', username=current_user.username))



@app.route('/recipe/<int:recipe_id>/like', methods=['POST', 'GET'])
def like_recipe(recipe_id):
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        recipe = Recipe.query.get(recipe_id)
        if recipe not in user.favourites:
            user.favourites.append(recipe)
            db.session.commit()
            return(redirect(url_for('recipe_page', recipe_id=recipe_id)))
        else:
            user.favourites.remove(recipe)
            db.session.commit()
            return(redirect(url_for('recipe_page', recipe_id=recipe_id)))
    else:
        flash('Please login first')
        return redirect(url_for('login_page'))


@app.route('/recipe/<int:recipe_id>/review', methods=['POST'])
def review(recipe_id):
    if current_user.is_authenticated:
        rating = request.form.get('rating')
        review = request.form.get('review')

        recipe = Recipe.query.get(recipe_id)
        user_rating = UserRating.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
        if user_rating:
            user_rating.rating = rating
            user_rating.review = review
            db.session.commit()
        else:
            user_rating = UserRating(user_id=current_user.id, recipe_id=recipe_id, rating=rating, review=review)
            db.session.add(user_rating)
            db.session.commit()
        return redirect(url_for('recipe_page', recipe_id=recipe_id, user_rating=user_rating))
    else:
        flash('Please login to leave a review')
        return redirect(url_for('login_page'))
        


@app.route('/recipe/<int:recipe_id>')
def recipe_page(recipe_id):
    return render_template('recipe.html', recipe=Recipe.query.get(recipe_id), user_rating=UserRating.query.filter_by(recipe_id=recipe_id).all(), ingredients=Recipe.query.get(recipe_id).ingredients)



@app.route('/catalogue')
def catalogue():
    return render_template('catalogue.html', recipes=Recipe.query.all())

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)