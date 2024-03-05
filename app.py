from flask import Flask, jsonify, request,render_template,Response
from flask import Flask, render_template, request, jsonify
from azure.storage.blob import BlobServiceClient
import os
import time
import uuid

connection_string = "DefaultEndpointsProtocol=https;AccountName=snowflakeazuredemo103;AccountKey=VoHCO6c56mSSGnGf0EzaNgv9n8y1KeV+8a7qBHqNgbvCfQRYHiPvJea38bD6ZVsGYaklkZ0Fzbet+AStRDyCXg==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "snowflake-demo"

path = "/"

container_client = blob_service_client.get_container_client(container_name)
blobs = container_client.list_blobs(name_starts_with=path)

files = []
path_list = path.split('/')
path_list.remove('')

for blob in blobs:
    parts = blob.name.split('/')
    if len(parts) > len(path_list):
        break
    else:
        files.append(parts[len(path_list) - 1])
    
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
