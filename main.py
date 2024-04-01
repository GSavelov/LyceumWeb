import os

from flask import Flask, render_template
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route("/")
def index():
    return render_template("task.html")


def main():
    db_session.global_init('db/learners.sqlite')
    app.run(port=5050)


if __name__ == '__main__':
    main()
