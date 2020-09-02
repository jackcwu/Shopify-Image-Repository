# https://www.youtube.com/watch?v=u96rVINbAUI --> MySQL tutorial
# https://www.youtube.com/watch?v=QjtW-wnXlUY --> Flask intro
# https://www.youtube.com/watch?v=6L3HNyXEais --> MySQL with Flask
# https://www.youtube.com/watch?v=-cHS4HoEFV8 --> Path variables
# https://help.pythonanywhere.com/pages/NoSuchFileOrDirectory/ --> saving stuff to file path system

##################### Logging in ###################################
# echo %PATH$
# mysql --user root -p

# py -m venv env
# env\Scripts\activate

import os
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

# UPLOAD_FOLDER ='Users/jackc/Documents/Personal Projects/images/' #'/images/'
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
imageRepository.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@imageRepository.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': # upload image to folder and add to database
        if request.form["submitButton"] == 'ADD':
            details = request.form 
            keyword = details['keyword']
            file = request.files['inputFile']

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                imagePath = os.path.join(imageRepository.config['UPLOAD_FOLDER'], filename)
                file.save(imagePath)
                
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO practice1(keyword, imagePath) VALUES(%s, %s)",(keyword, imagePath)) 
                mysql.connection.commit()
                cur.close()

            return redirect(url_for('index'))

        elif request.form["submitButton"] == 'SEARCH':
            cur = mysql.connection.cursor()
            searchTerm = request.form['search']
            count = cur.execute("SELECT * FROM practice1 WHERE keyword = %s" % ('\'' + searchTerm + '\'')) # https://stackoverflow.com/questions/48024806/flask-mysqldb-delete-from-variable-table
            
            if count > 0:
                details = cur.fetchall()
                return render_template('display.html', details=details)





            


    return render_template('index.html')


if __name__ == '__main__':
    imageRepository.run(debug=True)

