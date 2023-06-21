# flask app
from flask import Flask, render_template, request
from cppyy import include, gbl

# Configure application
app = Flask(__name__)

app.debug = True

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False # session not permanent (not saved when browser closed)
app.config["SESSION_TYPE"] = "filesystem" # store session data on filesystem

# static data

@app.route("/")
def index():
  return render_template("chat_faq.html")

from bot import chatbot_response


@app.route("/chat_faq")
def chat_faq():
  return render_template("chat_faq.html")


@app.route("/get")
def get_bot_response():
  userText = request.args.get('msg')
  return chatbot_response(userText).replace("  ", " ")

if __name__ == "__main__":
  app.run()
