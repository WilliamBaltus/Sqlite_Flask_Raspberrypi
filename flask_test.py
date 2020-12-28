from flask import Flask, render_template

app = Flask(__name__) #instance of flask

@app.route('/') #index page
def index():
    return render_template('index.html')


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=False) #zero's allow for all request on local network to ping to this localhost, listens on port 5000