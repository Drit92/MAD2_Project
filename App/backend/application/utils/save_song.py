import os 
from flask import current_app 
from werkzeug.utils import secure_filename 
ALLOWED_EXTENSIONS = {'mp3', 'ogg', 'wav'} 



SONG_UPLOAD_FOLDER = '../static/songs/'  

def save_song(song_file):
    filename = secure_filename(song_file.filename)
    file_path = os.path.join(current_app.config['SONG_UPLOAD_FOLDER'], filename)

    song_file.save(file_path)
    return file_path
