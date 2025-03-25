from flask import Blueprint, request, jsonify, abort
from .shemas import post_schema, get_schema

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

posts = []
post_id_counter = 1

@posts_bp.route('', methods=['GET'])
def get_posts():
    data = request.get_json(silent=True)

    try: 
        get_schema.load(data or {})
    except Exception as err: 
        return jsonify({ "message": err.messages })

    return jsonify(posts)

@posts_bp.route('', methods=['POST'])
def create_posts(): 
    global post_id_counter

    data = request.get_json()

    try: 
        post_schema.load(data)
    except Exception as err: 
        return jsonify({ "errors": err.messages }), 400

    if not data or 'title' not in data or 'text' not in data: 
        abort(400)

    new_post = { 
        'id': post_id_counter, 
        'title': data['title'], 
        'text': data['text'],
    }

    posts.append(new_post)
    post_id_counter += 1

    return jsonify(new_post), 201

