import os
import csv
import io
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
  os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
  files = request.files.getlist('file')
  if not files or files == [None]:
    return jsonify({"error": "No files part in the request"}), 400
  
  results = []
  for file in files:
    if file.filename == '':
      results.append({"filename": "", "error": "No file selected"})
      continue
    
    if file and file.filename.endswith('.csv'):
      filename = secure_filename(file.filename)
      
      try:
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.reader(stream)
        
        headers = next(csv_reader)
        
        data = []
        for row in csv_reader:
          data.append(dict(zip(headers, row)))
          
        results.append({
          "filename": filename,
          "message": "File parsed successfully",
          "data": data
        })
      
      except Exception as e:
        results.append({
          "filename": filename,
          "error": f"Failed to parse CSV file: {e}"
        })
    
  else:
    results.append({
      "filename": filename,
      "error": "Invalid file type. Only csv files are allowed"
    })
  return jsonify(results), 200
  
if __name__ == '__main__':
  app.run(debug=True)