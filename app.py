from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
# from function import functions

from transcription_summarization import transcribe,summarize
from utils import *
app = Flask(__name__)
app.secret_key='veryrandsoemthingslfak;domthing'

# Home page
@app.route('/')
def index():
    return render_template('dashboard.html')

# Specify the upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create the upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    # Check if the 'audio_file' file input field is present in the form
    if 'audio_file' not in request.files:
        return "No file part"

    audio_file = request.files['audio_file']
    audio_bytes = audio_file.read()
    transcription , transcription_id = transcribe(audio_bytes)
    print(transcription)
    summary = summarize(transcription_id, context = "The caller is contacting a first responder with an emergency distress call")
    address = get_address(transcription_id)
    coords = get_coords(address)
    session['details']={'summary':summary, 'address':address,'coords':coords,'transcription':transcription,'transcription_id': transcription_id}
    # transcription = summary = address= ''
    # Check if the file is empty
    # if audio_file.filename == '':
    #     return "No selected file"

    # # Save the uploaded file to the 'uploads' folder
    # upload_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
    # audio_file.save(upload_path)

    # transcribe(audio_file)

    return render_template('transcription.html',transcription=transcription, summary = summary,coords=coords, address=address)
@app.route('/analysis', methods=['GET','POST'])
def analysis():
    data = session['details']
    category = get_category(data['transcription'])
    nearest = get_nearest(category, data['coords'][0], data['coords'][1])
    severity = get_severity(data['transcription_id'])
    analysis_data = {'category':category, 'nearest': nearest, 'severity':severity}
    return render_template('analysis.html',analysis_data=analysis_data)
    
if __name__ == '__main__':
    app.run(debug=True)
