from collections import defaultdict
from typing import Set, Union

import BigInters.Analyzer.Analyzer as Analyzer
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, jsonify, current_app)
from flask_cors import CORS

from BigInters.Analyzer.RiotAPI.RiotAPI import ServerException, ClientException

bp = Blueprint('MainApp', __name__)
CORS(bp)

@bp.route('/')
def index():
    return 'Index'

@bp.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if not request.is_json:
        return 'Not json'
    req = request.get_json()
    for field in ('summoner', 'matches', 'queues', 'region'):
        if field not in req or req[field] == None:
            current_app.logger.info(req)
            response = jsonify({'status': 400, 'error': 'Incorrect fields'})
            response.status_code = 400
            return response

    try:
        response = jsonify(Analyzer.run_analysis(req['summoner'], req['matches'], req['queues'], req['region']))
        response.status_code = 200
        return response
    except ClientException as e:
        print(type(e), e)
        response = jsonify({'status': 406, 'error': 'Invalid request'})
        response.status_code = 406
    except ServerException as e:
        print(type(e), e)
        response = jsonify({'status': 503, 'error': 'API Forbidden'})
        response.status_code = 503
    except Exception as e:
        response.status_code = 500
    finally:
        return response
