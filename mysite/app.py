import os
from flask import Flask, request, send_from_directory, render_template

app = Flask(__name__, static_url_path='/static',template_folder='templates')
app.config['UPLOAD_FOLDER'] ="/mysite/uploads"
# Folder where uploaded files will be stored

# Initialize the list to store uploaded filenames
uploaded_files = []

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('upload.html',uploaded_files=uploaded_files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'You Dumb..'

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # os.chmod(filename, 0o666)

        uploaded_files.append(file.filename)# Add the uploaded filename to the list
        return 'File uploaded successfully'

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        # Remove the file from the uploaded_files list
        if filename in uploaded_files:
            uploaded_files.remove(filename)

        # Remove the file from the file system
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        return 'File deleted successfully'
    except Exception as e:
        return 'Error deleting the file: ' + str(e)

# @app.route('/file_list')
# def file_list():
#     # Return the list of uploaded files as HTML
#     return '\n'.join([f'<li>{file}</li>' for file in uploaded_files])

# from flask import render_template_string

@app.route('/file_list')
def file_list():
      # Render the list of uploaded files as HTML
    file_links = [f'<li><a href="/download/{file}" download="{file}">{file}</a> <button type="button" class="delete-button" onclick="deleteFile(\'{file}\')">Delete</button></li>' for file in uploaded_files]
    return '\n'.join(file_links)






@app.route('/download/<filename>')
def download_file(filename):
    # Construct the full path to the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # print("File Path:", file_path)

    # Check if the file exists
    if os.path.exists(file_path):

        # print("File Found")
        # Set the appropriate content type and headers for downloads
        response = send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
        return response
    else:
        print("File Not Found")
        return 'File not found', 404


if __name__ == '__main__':
    app.run(debug=True)
