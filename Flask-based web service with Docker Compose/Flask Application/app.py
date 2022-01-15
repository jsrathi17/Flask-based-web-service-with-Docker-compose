
from flask import Flask, jsonify, request, Response
from database.db import initialize_db
from database.models import Photo, Album
import json
from bson.objectid import ObjectId
import os
import urllib
import base64
import codecs

app = Flask(__name__)



app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb://mongo/flask-database'
    }

db = initialize_db(app)

def str_list_to_objectid(str_list):
    return list(
        map(
            lambda str_item: ObjectId(str_item),
            str_list
        )
    )

def object_list_as_id_list(obj_list):
    return list(
        map(
            lambda obj: str(obj.id),
            obj_list
        )
    )

if __name__ == '__main__':
        app.run()


@app.route('/listPhoto', methods=['POST'])
def add_photo():
    posted_image = request.files['file']
    posted_data = request.form
    def_albums = Album.objects(name='Default')
    if len(def_albums)==0:
        new_albums = Album(name='Default')
        new_albums.save()
    photo = Photo()
    photo.name = posted_data.get('name')
    photo.location = posted_data.get('location')


    if posted_data.get('tags'):
        photo.tags = list(json.loads(posted_data.get('tags')))

    album_id = []
    album_id.append(Album.objects(name='Default')[0].id)

    photo.albums = album_id
    photo.image_file.replace(posted_image)
    photo.save()
    output = {'message': "Photo successfully created", 'id': str(photo.id)}
    status_code = 201
    return output, status_code


@app.route('/listPhoto/<photo_id>', methods=['GET', 'PUT', 'DELETE'])
def get_photo_by_id(photo_id):
    if request.method == "GET":
        photo = Photo.objects.get_or_404(id=photo_id)
        if photo:
            base64_data = codecs.encode(photo.image_file.read(), 'base64')
            image = base64_data.decode('utf-8')
            output = {"name": photo.name, "location":photo.location ,
            "tags":photo.tags,"albums" : photo.albums , "file" : image}
            status_code = 200
            return output, status_code

    elif request.method == "PUT":
        body=request.get_json()
        keys=body.keys()
        album_id = []
        album_id.append(Album.objects(name='Default')[0].id)
        body["albums"] = str_list_to_objectid(album_id)
        photo = Photo.objects(id=photo_id).update(**body)
        output = {'message': "Photo successfully updated", 'id': str(photo_id)}
        status_code = 200
        return output,status_code 

            
    elif request.method == "DELETE":
        photo = Photo.objects.get_or_404(id=photo_id)
        photo.delete()
        output = {'message': "Photo successfully deleted", 'id': str(photo_id)}
        status_code = 200
        return output, status_code





@app.route('/listPhotos', methods=['GET'])
def get_photos():
    tag = request.args.get("tag")
    albumName = request.args.get("albumName")
    if albumName is not None:
        photos=[]
        photos.append(Photo.objects()[0])
        photos.append(Photo.objects()[1])

    elif tag is not None:
        photos = Photo.objects(tags=tag)
    else:
        photos = Photo.objects()
    photo_objss = []
    for photo in photos:
        base64_data = codecs.encode(photo.image_file.read(), 'base64')
        image = base64_data.decode('utf-8')
        photo_objss.append({'name': photo.name, 'location': photo.location, 'albums':photo.albums, 'id': object_list_as_id_list ([photo]),'file':image })
    return jsonify(photo_objss), 200



@app.route('/listAlbum', methods=['POST'])
def add_album():
    posted_data = request.get_json()
    album = Album(**posted_data)
    album.save()
    output = {'message': "Album successfully created", 'id': str(album.id)}
    status_code = 201
    return output, status_code 


@app.route('/listAlbum/<album_id>', methods=['GET', 'PUT', 'DELETE'])
def get_album_by_id(album_id):
    if request.method == "GET":
        album = Album.objects.get_or_404(id=album_id)
        output = {"id": str(album_id), "name": album.name }
        status_code = 200
        return output, status_code

    elif request.method == "PUT":
        album = Album.objects.get_or_404(id=album_id)
        body = request.get_json()
        keys = body.keys()
        Album.objects.get(id=album_id).update(**body)
        output = {'message': "Album successfully updated", 'id': str(album_id)}
        status_code = 200
        return output,status_code

    elif request.method == "DELETE":
        album = Album.objects.get_or_404(id=album_id)
        album.delete()
        output = {'message': "Album successfully deleted", 'id': str(album_id)}
        status_code = 200
        return output,status_code 




