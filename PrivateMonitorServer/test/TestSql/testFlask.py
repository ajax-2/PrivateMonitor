import time
from flask import Flask

app = Flask(__name__)


@app.route("/")
def main():
    time.sleep(600)
    return u"Ok"


if __name__ == "__main__":
    app.run("0.0.0.0", "5000")
