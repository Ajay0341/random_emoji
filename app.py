from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import random, os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emojis.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Emoji(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emoji = db.Column(db.String(10))

    def _repr_(self):
        return f'<Emoji {self.emoji}>'


# Set the path to the media folder
media_folder = 'static/media/'  # Replace with the actual path to your media folder

# Create the media folder if it doesn't exist
if not os.path.exists(media_folder):
    os.makedirs(media_folder)

@app.route('/')
def index():
    images = os.listdir(media_folder)
    random_image = random.choice(images)
    image_path = os.path.join(media_folder, random_image)
    return render_template('show.html', image_path=image_path)


@app.route('/file-upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            # Generate a secure filename
            filename = secure_filename(file.filename)

            # Save the file to the media folder
            file.save(os.path.join(media_folder, filename))

        return redirect(url_for('index'))
    return render_template('file_upload.html')


if __name__ == '__main__':
    app.run(debug=True) 