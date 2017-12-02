from flask import Flask
from flask import jsonify
from flask import request

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

es = Elasticsearch(timeout=30)
app = Flask(__name__)

@app.route('/get_account_history')
def get_account_history():
    account_id = request.args.get('account_id')
    from_ = request.args.get('from')
    size = request.args.get('size')
    sort_by = request.args.get('sort_by')

    s = Search(using=es, index="graphene-*", extra={"size": size}) \
        .query("match", account_history__account=account_id) \
        .extra(from_=from_) \
        .sort(sort_by)

    response = s.execute()
    #print response
    results = []
    print s.count()
    for hit in response:
        results.append(hit.to_dict())
        #print(hit.meta.score, hit.account_history.account)
    return jsonify(results)

if __name__ == '__main__':
    app.run()

