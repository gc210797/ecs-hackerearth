#!/usr/bin/env python3

from flask import Flask, request, jsonify
import dao
import utils
import jwt

app = Flask(__name__)

ds = dao.DSActions('data', 'users', 'http://localhost:8000')
secret_key = "jackthegsd"


def token_required(f):
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            print(token)
            try:
                jwt.decode(token, secret_key, algorithms=['HS256'])
            except Exception as e:
                print(e)
                return jsonify({'info': 'Token is invalid'}), 403
        else:
            return jsonify({'info': 'Auth token missing'}), 403
        return f(*args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator


@app.route('/get_books', methods=['GET'])
@token_required
def get_books():
    content = request.json
    page_size = int(content['page_size'])
    page = int(content['page'])
    response = None
    token = None

    try:
        for _ in range(page):
            response = ds.get_books(content['filter'], page_size, token)
            token = response['NextToken'] if 'NextToken' in response else None
    except Exception as e:
        return jsonify({
            'info': e
        }), 500

    return jsonify(response['Items'])


@app.route('/get_book/<book_id>', methods=['GET'])
@token_required
def get_book(book_id):
    try:
        return jsonify(ds.get_book(book_id)['Item'])
    except Exception as e:
        return jsonify({
            'info': e
        }), 500


@app.route('/add_book', methods=['POST'])
@token_required
def add_book():
    content = request.json
    try:
        response = ds.add_book(utils.convert_to_dynamodb(**content))
        if response['ResponseMetadata']['HTTPStatusCode'] >= 400:
            return jsonify({
                'info': response['ResponseMetadata']
            }), response['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        return jsonify({
            'info': e
        }), 500
    return "", 200


@app.route('/update_book/<book_id>', methods=['PUT'])
@token_required
def update_book(book_id):
    content = request.json
    try:
        response = ds.update_book(book_id, content)
        if response['ResponseMetadata']['HTTPStatusCode'] >= 400:
            return jsonify({
                'info': response['ResponseMetadata']
            }), response['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        return jsonify({
            'info': e
        }), 500
    return "", 200


@app.route('/add_fav/<user_id>/<book_id>', methods=['POST'])
@token_required
def add_favourite(user_id, book_id):
    try:
        response = ds.add_favourite(user_id, book_id)
        if response['ResponseMetadata']['HTTPStatusCode'] >= 400:
            return jsonify({
                'info': response['ResponseMetadata']
            }), response['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        return jsonify({
            'info': e
        }), 500
    return "", 200


@app.route('/get_fav/<user_id>', methods=['GET'])
@token_required
def get_favourite(user_id):
    try:
        response = ds.get_favourite(user_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({
            'info': str(e)
        }), 500
    return "", 200


@app.route('/rm_fav/<user_id>/<book_id>', methods=['DELETE'])
@token_required
def remove_favourite(user_id, book_id):
    try:
        response = ds.remove_favourite(user_id, book_id)
        if response['ResponseMetadata']['HTTPStatusCode'] >= 400:
            return jsonify({
                'info': response['ResponseMetadata']
            }), response['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        return jsonify({
            'info': e
        }), 500
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
