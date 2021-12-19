# -*- coding: utf-8 -*-

# api
from flask import Flask
from flask_restful import ( Api, Resource )

# face detection
from cv2 import ( CascadeClassifier, imread, cvtColor, COLOR_BGR2GRAY )

# database connection
from mysql.connector import connect

app = Flask(__name__)
api = Api(app)

class GetFace(Resource):
  def __init__(self):
    self.config = {
        'user'    : 'root',
        'password': 'Pa$$w0rd!',
        'host'    : '127.0.0.1',
        'database': 'db_name',
        'raise_on_warnings': True
    }
    self.cnx    = connect(**self.config)
    self.cursor = self.cnx.cursor()
    self.face   = CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

  def get(self, user_id):
    self.query = f'SELECT * FROM users WHERE id="{user_id}" limit 1'
    self.cursor.execute(self.query)

    for self.content in self.cursor:
      self.response = {
        'id'   : self.content[0],
        'name' : self.content[1],
        'email': self.content[2],
        'image': self.content[4],
      }

    self.image   = imread(f"img/{self.response['image']}")
    self.convert = cvtColor(self.image, COLOR_BGR2GRAY)
    self.count   = self.face.detectMultiScale(self.convert, scaleFactor=1.1, minNeighbors=5)

    print(self.response, {'convert': self.convert, 'face': len(self.count)})

    return {'result': True if len(self.count) == 1 else False}

api.add_resource(GetFace, '/<int:user_id>')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)
