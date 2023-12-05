let ingredientCount = 2;

function addIngredientField() {
    const ingredientContainer = document.getElementById('ingredient_container')
    const ingredient = document.createElement('div')
    ingredient.classList.add('ingredient_container')
    const newIngerdient = document.createElement('div')
    newIngerdient.classList.add('ingredient', 'input-container')

    ingredient.appendChild(newIngerdient)

    newIngerdient.innerHTML = '<input type="text" name="ingredient" id="ingredient" placeholder="Ingredient ' + ingredientCount + '">'
    ingredientContainer.appendChild(ingredient)
    ingredientCount++

    if (ingredientCount >= 3) {
        const removeIngredientButton = document.getElementById('remove_ingredient')
        removeIngredientButton.style.display = 'block'
    }

    console.log(ingredientCount)
}


function removeIngredientField() {
    const ingredientContainer = document.getElementById('ingredient_container')
    const lastIngredient = ingredientContainer.lastElementChild
    if (lastIngredient) {
        ingredientContainer.removeChild(lastIngredient)
        ingredientCount--
    }
    if (ingredientCount < 3) {
        const removeIngredientButton = document.getElementById('remove_ingredient')
        removeIngredientButton.style.display = 'none'
    }

}


function openMenu() {
    document.getElementById("create_recipe").style.display = "block";
    document.querySelector(".popup-container").classList.add("open");
    document.querySelector(".closeMenu-btn").style.display = "block";
}

function openEditMenu() {
    document.getElementById("edit_recipe").style.display = "block";
    document.querySelector(".popup-container").classList.add("open");
    document.querySelector(".closeMenu-btn").style.display = "block";
}

function openEditUserMenu() {
    document.getElementById("edit_user").style.display = "block";
    document.querySelector(".popup-container").classList.add("open");
    document.querySelector(".closeMenu-btn").style.display = "block";
}

function closeMenu() {
    document.getElementById("create_recipe").style.display = "none";
    document.querySelector(".popup-container").classList.remove("open");
    document.querySelector(".closeMenu-btn").style.display = "none";
}

function closeEditMenu() {
    document.getElementById("edit_recipe").style.display = "none";
    document.querySelector(".popup-container").classList.remove("open");
    document.querySelector(".closeMenu-btn").style.display = "none";
}

function closeEditUserMenu() {
    document.getElementById("edit_user").style.display = "none";
    document.querySelector(".popup-container").classList.remove("open");
    document.querySelector(".closeMenu-btn").style.display = "none";
}

function openDropdownMenu() {
    let menuBtn = document.querySelector('.toggle_btn');
    let menuBtnIcon = document.querySelector('.toggle_btn i');
    let dropDownMenu = document.querySelector('.dropdown_menu');
    let pageLinks = document.querySelectorAll('.nav_but');
    function openDropDown() {
        dropDownMenu.classList.toggle('open');
        const menuIsOpen = dropDownMenu.classList.contains('open');
        menuBtnIcon.classList = menuIsOpen ? 'fa-solid fa-xmark' : 'fa-solid fa-bars';
    }
    menuBtn.onclick = openDropDown;
    pageLinks.forEach((nav_but) => {
        nav_but.onclick = openDropDown;
    })
}

document.addEventListener('DOMContentLoaded', openDropdownMenu)