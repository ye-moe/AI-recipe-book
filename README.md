# AI-recipe-book

Recipe Generator
We would like to build a website that can automatically generate recipes with images for any given dish name. Here is a sample of how the website should look. In order to properly show the recie on the page, we need to build a backend that can generate the following JSON for any given dish name:

`
{
    name:  <the name of the dish>,
    image: <base64 encoded png>,
    prep_time: <the time needed to prepare the dish>,
    cook_time: <the time needed to cook the dish>,
    ingredients: [
        {<name of the cooking part>: [list of ingredients]},
        ...
    ],
    instructions: [
        {<name of the cooking part>: [list of instructions]},
    ],
}
`

To make our website to be general enough, we will make use of Vertex AI for generating the recipe instructions, and Imagen 3 for generating the illustrative images. Both are from Google Cloud Platform (GCP).

You are asked to setup the following publicly available endpoints either on PythonAnywhere or on GCP (e.g. using Cloud Run/Functions):

https://SERVER/id : returns your "EMPLID_LastName", e.g. 00000000_Vo
https://SERVER/recipe?name=DISH_NAME&minutes_under=MIN : returns the recipe for DISH_NAME in the above JSON format. The recipe should be prepared under MIN minutes if MIN is provided.
* SERVER should be either USERNAME.pythonanyhwere.com; or PROJECT.cloudfunction.net.

You could use the function show_recipe() below to test your endpoint on Google Colab (should wait for a few seconds).