from flask import Flask, jsonify, request,render_template,Response
import flask

    
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

  return Response(render_template('result.html',data=['No items']))

    


if __name__ == '__main__':
    #app.run(host='0.0.0.0',port = 5050 )
    app.run(debug=True)
