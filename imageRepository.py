# https://www.youtube.com/watch?v=u96rVINbAUI --> MySQL tutorial
# https://www.youtube.com/watch?v=QjtW-wnXlUY --> Flask intro
# https://www.youtube.com/watch?v=6L3HNyXEais --> MySQL with Flask
# https://www.youtube.com/watch?v=-cHS4HoEFV8 --> Path variables

##################### Logging in ###################################
# echo %PATH$
# mysql --user root -p

# py -m venv env
# env\Scripts\activate

from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
import yaml
from werkzeug.utils import secure_filename

imageRepository = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
imageRepository.config['MYSQL_HOST'] = db['mysql_host']
imageRepository.config['MYSQL_USER'] = db['mysql_user']
imageRepository.config['MYSQL_PASSWORD'] = db['mysql_password']
imageRepository.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(imageRepository)

UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
imageRepository.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@imageRepository.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch Form Data
        userDetails = request.form 
        path = userDetails['path']
        name = 'cat.jpg'
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO images(path, name) VALUES(%s, %s)",(path, name)) # change user
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    imageRepository.run(debug=True)

