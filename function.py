#@title `show_recipe('https://hvo.pythonanywhere.com/recipe', 'Vietnamese Beef Pho')`
from IPython.display import Javascript, display_html
from google.colab import output

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recipe</title>
    <style>
        body {
            font-family: sans-serif;
            margin: 20px;
            background-color: #f8f8f8;
            color: #333;
        }
        h1 {
            color: #d9534f; /* A nice reddish color */
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }
        .recipe-info {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .ingredients, .instructions {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        h2 {
            color: #337ab7; /* A nice blueish color */
        }
        ul {
            list-style-type: disc;
            padding-left: 20px;
        }
    </style>
</head>
<body>
</body>
</html>'''

SCRIPT = '''
fetch("ENDPOINT")
  .then((response) => response.json())
  .then((recipe) => {
    document.body.innerHTML = `
        <h1>${recipe.name}</h1>
        <div class="recipe-info">
            <img src="${recipe.image}" alt="${recipe.name}">
            <p><strong>Prep time:</strong> ${recipe.prep_time}</p>
            <p><strong>Cook time:</strong> ${recipe.cook_time}</p>
        </div>

        <div class="ingredients">
            <h2>Ingredients</h2>
            ${recipe.ingredients.map(group => `
                <h3>${Object.keys(group)[0]}</h3>
                <ul>
                    ${group[Object.keys(group)[0]].map(ingredient => `<li>${ingredient}</li>`).join('')}
                </ul>
            `).join('')}
        </div>

        <div class="instructions">
            <h2>Instructions</h2>
            ${recipe.instructions.map(group => `
                <h3>${Object.keys(group)[0]}</h3>
                <ol>
                    ${group[Object.keys(group)[0]].map(instruction => `<li>${instruction}</li>`).join('')}
                </ol>
            `).join('')}
        </div>
    `;
});
'''

def show_recipe(endpoint, dish_name, minutes_under=None):
    display_html(HTML)
    url = f'{endpoint}?name={dish_name}'
    if minutes_under:
        url += f'&minutes_under={minutes_under}'
    script = SCRIPT.replace('ENDPOINT', url)
    display(Javascript(script))

show_recipe('https://yemoe.pythonanywhere.com/recipe', 'Cheese Burger', 20)