from flask import Blueprint, request, jsonify, abort
from .shemas import post_schema, get_schema
from db import posts_db
from marshmallow import ValidationError

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('', methods=['GET'])
def get_posts():
    '''
    Route to get existing posts
    '''

    data = request.get_json(silent=True)

    try: 
        get_schema.load(data or {})
    except ValidationError as err: 
        return jsonify({ "message": err.messages }), 400

    posts = list(posts_db.find({}, { "_id": 0 }))

    return jsonify(posts), 200


@posts_bp.route('', methods=['POST'])
def create_posts(): 
    '''
    Route to create a new post
    '''

    data = request.get_json()

    try: 
        post_schema.load(data)
    except ValidationError as err: 
        return jsonify({ "errors": err.messages }), 400

    new_post = { 
        'title': data['title'], 
        'text': data['text'],
    }

    result = posts_db.insert_one(new_post)

    # Cannot turn ObjectId into JSON
    new_post['_id'] = str(result['_id'])

    return jsonify(new_post), 201

