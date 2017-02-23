# -*- coding: utf-8 -*-

from flask import Flask, json, request, current_app
from werkzeug.wrappers import Response

from models import Comment, SAMPLE_SIZE, search, suggest
from views.utils import ApiResponse
from views.exceptions import ApiException


class ApiFlask(Flask):
    def make_response(self, rv):
        if isinstance(rv, dict):
            if 'r' not in rv:
                rv['r'] = 1
            rv = ApiResponse(rv)
        if isinstance(rv, ApiResponse):
            return rv.response_to()
        return Flask.make_response(self, rv)

json_api = ApiFlask(__name__)
PER_PAGE = 20


@json_api.errorhandler(ApiException)
def api_error_handler(error):
    return error.to_result()


@json_api.errorhandler(403)
@json_api.errorhandler(404)
@json_api.errorhandler(500)
def error_handler(error):
    if hasattr(error, 'name'):
        mas = error.name
        code = error.code
    else:
        msg = error.message
        code = 500
    return ApiResponse({'message': msg}, status=code)


@json_api.route('/comments')
def home():
    sort = request.args.get('sort', 'star')
    start = request.args.get('start', 0, type=int)
    limit = request.args.get('limit', PER_PAGE, type=int)

    if sort == 'star':
        comments = Comment.order_by_star(start, limit)
    else:
        comments = []
    return {
        'comments': [comment.to_dict() for comment in comments],
        'has_more': start + limit < SAMPLE_SIZE
    }


@json_api.route('/search', methods=['GET', 'POST'])
def search_view():
    subject_id = request.form.get('subject_id', '')
    type = request.form.get('type', 'movie')
    comment = search(subject_id, type)
    print comment
    return {
        'comment': [comment.to_dict()]
    }


@json_api.route('/suggest', methods=['GET', 'POST'])
def suggest_view():
    text = request.form.get('text', '')
    start = request.form.get('start', 0, type=int)
    limit = request.form.get('limit', 20, type=int)
    items = suggest(text)
    items = items[start: start + limit]
    return {'items': items}

