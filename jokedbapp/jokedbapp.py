from database import db_session
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# app-wide configuration
DEBUG = True
SECRET_KEY = "thisisasupersekritkeyunassailablewithmoderntechniques0120847119579"

# create our app and load in the config
app = Flask(__name__)
app.config.from_object(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
  app.run()
