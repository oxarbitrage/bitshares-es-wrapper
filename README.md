# Bitshares ElasticSearch Wrapper

Wrapper for final user applications to interact with account data from the bitshares blockchain stored by  `bitshares-core` with `elasticsearch-plugin` running. 

## Install

- Install python elasticsearch low level lib:

`pip install elasticsearch`

- Install python elasticsearch high level lib to easy query:

`pip install elasticsearch-dsl`

- Install flask CORS to query the wrapper from anywhere:

`pip install flask-cors`

- Install flasgger for swagger apidocs:

`pip install flasgger`

- Clone and run it by flask:

```
git clone https://github.com/oxarbitrage/bitshares-es-wrapper.git
export FLASK_APP=wrapper.py
flask run --host=0.0.0.0
```

Or

```
uwsgi --ini wrapper.ini
```
 
 ## API Documentation
 
 Swagger api docs: http://185.208.208.184:5000/apidocs/#!/wrapper/
