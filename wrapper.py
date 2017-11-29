from flask import Flask
from flask import jsonify
from flask import request

from datetime import datetime
from elasticsearch import Elasticsearch


es = Elasticsearch(timeout=30)
app = Flask(__name__)

@app.route('/')
def hello_world():
    body = {"query": {"bool": {"must": [{"term": {"account_history.account.keyword": "1.2.282"}}, {
        "range": {"block_data.block_time": {"gte": "2015-10-26T00:00:00", "lte": "2015-10-29T23:59:59"}}}]}}}

    res = es.search(index="graphene-*", body=body)
    print("Got %d Hits:" % res['hits']['total'])

    results = []
    for hit in res['hits']['hits']:
        results.append(hit["_source"])

    return jsonify(results)

@app.route('/get_data')
def get_last_transactions():

    type = request.args.get('type')
    size = request.args.get('size')
    field = request.args.get('field')
    sort = request.args.get('sort')
    order = request.args.get('order')
    gte = request.args.get('gte')
    lte = request.args.get('lte')
    term = request.args.get('term')

    sort =  {"sort" : [ { sort : {"order" : order}}]}

    # samples
    ##@# type = aggregator
    # size = 10
    # sort =  block_data.block_time
    # field = block_data.trx_id.keyword
    # order = "desc"
    # gte = "now-1h"
    # lte = "now"

    # for data field can be account_history.account.keyword and term 1.2.282

    if type == "aggergator":
        aggs = {"aggs": { "group_by_data": { "terms": { "field": field, "size": size } } } }
        query = {"query": {"bool": {"must": [{
            "range": {"block_data.block_time": {"gte": gte, "lte": lte}}}]}}}
    elif type == "data":
        query = {"query": {"bool": {"must": [{
            "range": {"block_data.block_time": {"gte": gte, "lte": lte}}}, {"term": {field: term}}]}}}

    fromm = {"from" : 0}
    size = {"size": size}

    query = {"query": {"bool": {"must": [{
        "range": {"block_data.block_time": {"gte": gte, "lte": lte}}}]}}}

    body = sort.copy()
    body.update(aggs)
    body.update(query)
    body.update(fromm)
    body.update(size)

    res = es.search(index="graphene-*", body=body)

    results = []

    if type == "aggergator":
        for b in res['aggregations']['group_by_data']["buckets"]:
            results.append({"key": b["key"], "doc_count": b["doc_count"]})

    elif type == "data":
        for d in res["hits"]["hits"]:
            results.append(d["_source"])

    return jsonify(results)



if __name__ == '__main__':
    app.run()

