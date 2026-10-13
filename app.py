from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Krithika this is final hello project!"                   
@app.route("/new")
def new():
    return "FINAL CHECK"            
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)