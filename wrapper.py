from flask import Flask
from flask import jsonify
from flask import request

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, query, Q, DocType, utils
from elasticsearch_dsl.exceptions import IllegalOperation

es = Elasticsearch(timeout=30)
app = Flask(__name__)

@app.route('/get_account_history')
def get_account_history():

    account_id = request.args.get('account_id') if 'account_id' in request.args else False
    operation_type = request.args.get('operation_type') if 'operation_type' in request.args else False
    from_ = request.args.get('from_') if 'from_' in request.args else 0
    size = request.args.get('size') if 'size' in request.args else 10
    from_date = request.args.get('from_date') if 'from_date' in request.args else "2015-10-10"
    to_date = request.args.get('to_date') if 'to_date' in request.args else "now"
    sort_by = request.args.get('sort_by') if 'sort_by' in request.args else "-block_data.block_time"
    type = request.args.get('type') if 'type' in request.args else "data"
    agg_field = request.args.get('agg_field') if 'agg_field' in request.args else "operation_type"

    s = Search(using=es, index="graphene-*", extra={"size": size, "from": from_})

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
        s.aggs.bucket('per_field', 'terms', field=agg_field)

    s = s.sort(sort_by)

    print s.to_dict()

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

if __name__ == '__main__':
    app.run()

