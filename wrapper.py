from flask import Flask
from flask import jsonify
from flask import request

from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, query, Q, DocType, utils
from elasticsearch_dsl.exceptions import IllegalOperation

from flasgger import Swagger

es = Elasticsearch(timeout=60)
app = Flask(__name__)
from flask_cors import CORS, cross_origin
CORS(app)

app.config['SWAGGER'] = {
    'title': 'Bitshares ES API',
    'uiversion': 2
}
Swagger(app, template_file='wrapper.yaml')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

@app.route('/get_account_history')
def get_account_history():

    account_id = request.args.get('account_id', False)
    operation_type = request.args.get('operation_type', False)
    from_ = request.args.get('from_', 0)
    size = request.args.get('size', 10)
    from_date = request.args.get('from_date', "2015-10-10")
    to_date = request.args.get('to_date', "now")
    sort_by = request.args.get('sort_by', "-block_data.block_time")
    type = request.args.get('type', "data")
    agg_field = request.args.get('agg_field', "operation_type")

    if type != "data":
        s = Search(using=es, index="bitshares-*")
    else:
        s = Search(using=es, index="bitshares-*", extra={"size": size, "from": from_})

    q = Q()
    if account_id and operation_type:
        q = Q("match", account_history__account=account_id) & Q("match", operation_type=operation_type)
    elif account_id and not operation_type:
        q = Q("match", account_history__account=account_id)
    elif not account_id and operation_type:
        q = Q("match", operation_type=operation_type)

    range_query = Q("range", block_data__block_time={'gte': from_date, 'lte': to_date})
    s.query = q & range_query

    if type != "data":
        s.aggs.bucket('per_field', 'terms', field=agg_field, size=size)

    s = s.sort(sort_by)

    #print s.to_dict()

    response = s.execute()
    #print response
    results = []
    #print s.count()
    if type == "data":
        for hit in response:
            results.append(hit.to_dict())
    else:
        for field in response.aggregations.per_field.buckets:
            results.append(field.to_dict())

    return jsonify(results)


@app.route('/get_single_operation')
def get_single_operation():

    operation_id = request.args.get('operation_id', "1.11.0")

    s = Search(using=es, index="bitshares-*", extra={"size": 1})

    q = Q("match", account_history__operation_id=operation_id)

    s.query = q
    response = s.execute()
    results = []
    for hit in response:
        results.append(hit.to_dict())

    return jsonify(results)

@app.route('/is_alive')
def is_alive():
    find_string = datetime.utcnow().strftime("%Y-%m")
    from_date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

    s = Search(using=es, index="bitshares-" + find_string)
    s.query = Q("range", block_data__block_time={'gte': from_date, 'lte': "now"})
    s.aggs.metric("max_block_time", "max", field="block_data.block_time")

    json_response = {
        "server_time": datetime.utcnow(),
        "head_block_timestamp": None,
        "head_block_time": None
    }

    try:
        response = s.execute()
        if response.aggregations.max_block_time.value is not None:
            json_response["head_block_time"] = str(response.aggregations.max_block_time.value_as_string)
            json_response["head_block_timestamp"] = response.aggregations.max_block_time.value
            json_response["deltatime"] = abs((datetime.utcfromtimestamp(json_response["head_block_timestamp"] / 1000) - json_response["server_time"]).total_seconds())
            if json_response["deltatime"] < 30:
                json_response["status"] = "ok"
            else:
                json_response["status"] = "out_of_sync"
                json_response["error"] = "last_block_too_old"
        else:
            json_response["status"] = "out_of_sync"
            json_response["deltatime"] = "Infinite"
            json_response["query_index"] = find_string
            json_response["query_from_date"] = from_date
            json_response["error"] = "no_blocks_last_24_hours"
    except NotFoundError:
        json_response["status"] = "out_of_sync"
        json_response["deltatime"] = "Infinite"
        json_response["error"] = "index_not_found"
        json_response["query_index"] = find_string

    return jsonify(json_response)

@app.route('/get_trx')
def get_trx():

    trx = request.args.get('trx', "738be2bd22e2da31d587d281ea7ee9bd02b9dbf0")
    from_ = request.args.get('from_', 0)
    size = request.args.get('size', 10)

    s = Search(using=es, index="bitshares-*", extra={"size": size, "from": from_})

    q = Q("match", block_data__trx_id=trx)

    s.query = q
    response = s.execute()
    results = []
    for hit in response:
        results.append(hit.to_dict())

    return jsonify(results)



if __name__ == '__main__':
    app.run()

