from flask import Flask, jsonify, request,render_template,Response
from flask import Flask, render_template, request, jsonify
from azure.storage.blob import BlobServiceClient
import os
import time
import uuid
    
app = Flask(__name__)

connection_string = "DefaultEndpointsProtocol=https;AccountName=snowflakeazuredemo103;AccountKey=VoHCO6c56mSSGnGf0EzaNgv9n8y1KeV+8a7qBHqNgbvCfQRYHiPvJea38bD6ZVsGYaklkZ0Fzbet+AStRDyCXg==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "snowflake-demo"
path = "/"
copied_items = []
pre_path = []
post_path = []

@app.route('/')
def index():
    file_list = populate_files()
    return render_template('index.html', file_list=file_list)

@app.route('/selected_value', methods=['POST'])
def selected_value():
    selected_value = request.json.get('selectedValue')
    global path
    path = selected_value
    pre_path.insert(0, path)
    file_list = populate_files()
    return jsonify({'success': True, 'selected_value': selected_value, 'file_list': file_list})

@app.route('/update_dropdown', methods=['POST'])
def update_dropdown():
    data = request.json
    folder = data.get('name')
    global path
    if folder[2:].find(".") != -1:
        new_value = path
        file_list = populate_files()
        return jsonify({'success': True, 'newValue': new_value, 'file_list': file_list})
    else:
        path += folder[2:] + '/'
        new_value = path
        pre_path.insert(0, path)
        file_list = populate_files()
        return jsonify({'success': True, 'newValue': new_value, 'file_list': file_list})

@app.route('/pre_tab', methods=['POST'])
def pre_tab():
    global path
    if len(pre_path) > 1:
        path = pre_path.pop(1)
        post_path.insert(0, path)
        file_list = populate_files()
        return jsonify({'success': True, 'newValue': path, 'file_list': file_list})
    else:
        file_list = populate_files()
        return jsonify({'success': True, 'newValue': path, 'file_list': file_list})

@app.route('/next_tab', methods=['POST'])
def next_tab():
    global path
    if len(post_path) > 1:
        path = post_path.pop(1)
        file_list = populate_files()
        return jsonify({'success': True, 'newValue': path, 'file_list': file_list})
    elif len(post_path) == 1:
        path = post_path.pop(0)
        file_list = populate_files()
        return jsonify({'success': True, 'newValue': path, 'file_list': file_list})
    else:
        file_list = populate_files()
        return jsonify({'success': True, 'newValue': path, 'file_list': file_list})

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})

    # Upload the file to Azure Blob Storage
    container_client = blob_service_client.get_container_client(container_name)
    blob_name = os.path.join(path, file.filename)
    blob_client = container_client.get_blob_client(blob=blob_name)
    blob_client.upload_blob(file)

    file_list = populate_files()
    return jsonify({'success': True, 'file_list': file_list})

def populate_files():
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

    table_lists = []
    for file in files:
        file_path = os.path.join(path, file)
        blob_client = container_client.get_blob_client(blob=file_path)

        properties = blob_client.get_blob_properties()
        modified_date = properties.last_modified
        size = properties.size

        if file.find(".") != -1:
            file_name = "📄" + ' ' + file
        else:
            file_name = "📁" + ' ' + file

        files_detail = {}
        files_detail['name'] = file_name
        files_detail['modified_date'] = str(modified_date.strftime("%d-%m-%Y %H:%M"))
        files_detail['size'] = str(size) + ' KB'
        table_lists.append(files_detail)

    return table_lists


# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

  return Response(render_template('result.html',data=['No items']))

    


if __name__ == '__main__':
    #app.run(host='0.0.0.0',port = 5050 )
    app.run(debug=True)
