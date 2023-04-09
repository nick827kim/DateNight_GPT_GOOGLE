from flask import Flask, render_template, request
import os
import openai
import requests

app = Flask(__name__)


openai.api_key = INSERT YOUR GPT API KEY HERE

def chat_gpt(message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        max_tokens=75,
        n=1,
        stop=None,
        temperature=0.3,
    )

    return response.choices[0].text.strip()

def generate_restaurant_suggestion(person1, person2, location, price, age):
    prompt = f"Give me a list of exactly 3 popular restaurants in {location} for a couple in their {age} with a budget of ${price}, where person 1 wants {person1} and person 2 wants {person2}."
    restaurant_list = chat_gpt(prompt)
    return restaurant_list

def get_restaurant_details(restaurant_name, location):
    api_key = ENTER GOOGLE API KEY HERE
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={restaurant_name}+in+{location}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["results"]:
        restaurant = data["results"][0]
        return {
            "name": restaurant["name"],
            "address": restaurant["formatted_address"],
            "rating": restaurant.get("rating", "N/A"),
            "place_id": restaurant["place_id"]
        }
    return None

def get_map_image(address, api_key):
    map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={address}&zoom=15&size=600x300&maptype=roadmap&markers=color:red%7Clabel:%7C{address}&key={api_key}"
    return map_url


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggest', methods=['POST'])
def suggest():
    person1 = request.form['person1']
    person2 = request.form['person2']
    location = request.form['location']
    price = request.form['price']
    age = request.form['age']

    restaurant_list = generate_restaurant_suggestion(person1, person2, location, price, age)
    restaurants = []
    api_key = "ENTER GOOGLE API KEY HERE"

    for restaurant_name in restaurant_list.split(","):
        restaurant_details = get_restaurant_details(restaurant_name.strip(), location)
        if restaurant_details:
            restaurant_details["map_image"] = get_map_image(restaurant_details["address"], api_key)
            restaurants.append(restaurant_details)

    return render_template('suggestion.html', restaurants=restaurants)


if __name__ == '__main__':
    app.run(debug=True)

