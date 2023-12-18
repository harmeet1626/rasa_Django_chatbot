# Chatbot - Zoya

Zoya is a chatbot powered by Rasa Open Source.


## Run Locally

Clone the project

```bash
  git clone https://github.com/ranjeetsps/rasa_chatbot.git
```

Go to the project directory

```bash
  cd rasa_chatbot
```
Create a Virtual Environment of python 3.8


Install dependencies

```bash
  pip install -r requirements.txt
```

Start the django server

```bash
  python manage.py runserver
```

Open a new terminal & Navigate to app_rasa folder

```bash
  cd app_rasa
```

Start the Rasa server

```bash
  rasa run -m models --enable-api  --endpoints endpoints.yml --cors "*" --debug

```

Open a new terminal into app_rasa folder

```bash
  rasa run actions
```


## Main Features

- NLP understanding
- Ticket Raising
- Document Sharing
- Text to speech
- Table booking in a restaurant
- Cancel the reservation
- User based history 



## Tech Stack

**Client:** Html, CSS, Javascript, JQuery, Bootstrap, Django Jinja Templating

**Server:** Python, DJango Rest Framework, Rasa open Source, Mysql database, Google Translator APis.

## Authors

- [@ranjeetsps](https://www.github.com/ranjeetsps)
- [@riteshsp](https://www.github.com/riteshsp)
- [@harmeet1626](https://www.github.com/harmeet1626)

