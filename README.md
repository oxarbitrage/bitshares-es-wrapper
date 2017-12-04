# Bitshares ElasticSearch Wrapper

Wrapper for final user applications to interact with account data from the bitshares blockchain stored by  `bitshares-core` with `elasticsearch-plugin` running. 

## Install

- Install python elasticsearch low level lib:

`pip install elasticsearch`

- Install python elasticsearch high level lib to easy query:

`pip install elasticsearch-dsl`

- Clone and run it by flask:

```
git clone https://github.com/oxarbitrage/bitshares-es-wrapper.git
export FLASK_APP=wrapper.py
flask run --host=0.0.0.0
```
 
 ## Available Calls
 
 ### get_account history
 
Get all operations in history with pager, similar to bitshares node call but with fullter features like search by date, filter by operation and others. Check the samples on how versatile the call can be.
 
 #### Samples:
 
 get history of account sort by date:

[View Online Sample](http://209.188.21.157:5000/get_account_history?account_id=1.2.282&from=100&size=10&sort_by=block_data.block_time)

sort by operation_time

[View Online Sample](http://209.188.21.157:5000/get_account_history?account_id=1.2.282&from=100&size=10&sort_by=operation_type)

reverse order:

[View Online Sample](http://209.188.21.157:5000/get_account_history?account_id=1.2.282&from=100&size=10&sort_by=-operation_type)

get orders from an account and filter by date range from 2017-09-09 to current day and time. sort by time desc:

[View Online Sample](http://209.188.21.157:5000/get_account_history?account_id=1.2.282&from=0&size=10&sort_by=-block_data.block_time&from_date=2017-09-01&to_date=now)

same as before but get only transfer operations:

[View Online Sample](http://209.188.21.157:5000/get_account_history?account_id=1.2.282&from=0&size=10&sort_by=-block_data.block_time&from_date=2017-09-01&to_date=now&operation_type=0)

it is even possible to make queries to all the accounts in a period of time, getting the network activity in that range:

[View Online Sample](http://209.188.21.157:5000/get_account_history?from=0&size=10&sort_by=-block_data.block_time&from_date=2017-09-01&to_date=now)

get the fill orders from a trading bot during a selected deep period of time:

[View Online Sample](http://209.188.21.157:5000/get_account_history?account_id=1.2.36449&from=0&size=10&sort_by=-block_data.block_time&from_date=2016-10-01&to_date=2016-12-01&operation_type=4)