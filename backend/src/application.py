import time
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
from api import search, hello

PORT=5001


application = Flask(__name__)
CORS(application)

# logger.info('Initializing application...')

parser = reqparse.RequestParser()
parser.add_argument('domain_id', type=int)


class Hello(Resource):
    def get(self):
        return hello.get_hello()


class Search(Resource):
    def get(self):
        return {"result": "OK",
                "articles": search.get_articles(1, 2)
        }


api = Api(application)
api.add_resource(Hello, '/hello')
api.add_resource(Search, '/search')

if __name__ == '__main__':
    application.run(port=PORT, debug=True)

