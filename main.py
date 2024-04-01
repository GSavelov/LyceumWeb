import os

from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route("/")
def index():
    return render_template("task.html")


def main():
    app.run(port=5050)


if __name__ == '__main__':
    main()
