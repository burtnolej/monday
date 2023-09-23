import datetime
import sys
import requests
import json
import ast
from prettytable import PrettyTable, ALL


apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjExMTgyMDkwNiwidWlkIjoxNTE2MzEwNywiaWFkIjoiMjAyMS0wNS0zMFQxMTowMDo1OS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NjY5MDk4NSwicmduIjoidXNlMSJ9.zIeOeoqeaZ2Q8NuKBPPw2LQFh2JRPvPwIkhhn4e5Q08"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : apiKey}

def _get_status(item):
    for _item in item:
        if _item['id'] == 'status':
            _status = ast.literal_eval(str(_item['value']).replace("null","0"))
            if _status != None:
                return _status['index']
    return "NOTSET"

def _get_tags(item):
    for _item in item:
        if _item['id'] == 'tags':
            _tags = ast.literal_eval(str(_item['value']).replace("null","0"))
            if _tags != None:
                return "^".join(str(__tag) for __tag in _tags['tag_ids'])
    return "NOTSET"

def _get_person(item):
    for _item in item:
        if _item['id'] == 'person':
            _persons = ast.literal_eval(str(_item['value']).replace("null","0"))
            if _persons != None:
                _personlist = []
                for _person in _persons['personsAndTeams']:
                    _personlist.append(_person['id'])

                if _personlist != None:
                    return "^".join(str(_person) for _person in _personlist)
    return "NOTSET"

def _get_data(query):
	data = {'query' : query}
	return requests.post(url=apiUrl, json=data, headers=headers) # make request

def _unpack(items,__items,result,item_type):
        _item_results.append(item_type)
        _item_results.append(__items['name'])
        _item_results.append(items[i]['group']['title'])
        for _base_column in _base_columns:
            _item_results.append(items[i][_base_column])

        _item_results.append(_get_status(items[i]['columns']))
        _item_results.append(_get_tags(items[i]['columns']))
        _item_results.append(_get_person(items[i]['columns']))
        
_board_ids="[1140656959,2193345626,2193345626,2259144314,2763786972,4973959122,4974012540,4977328922,4977328522,4909340518,4973204278]"
_base_columns = ["id","name","created_at","updated_at"]
_columns = "(ids: [\"status\",\"person\",\"creation_log\",\"last_updated\",\"last_updated2\",\"last_updated3\",\"item_id\",\"tags\"])"
_column_values = " columns: column_values " + _columns + "{title id text value }"
_subitems = "subitems {" + " ".join(_base_columns) + " " + _column_values + "}"

r = _get_data('{boards(ids: ' + _board_ids + ') { id name items(newest_first: true, limit: 5, page: 1) {' + " ".join(_base_columns) + ' group { title } ' + _column_values + '  ' + _subitems + ' } } }') 

boards = r.json()['data']['boards']

t = PrettyTable(["Type","Board","Group","ID","Name","Created","Updated","Status","Tags","Person"])

results = {}
for __items in boards:
    items = __items['items']
    for i in range(0,len(items)):
        _item_results=[]
        _unpack(items,__items,_item_results,"item")
        
        results[items[i]["created_at"]]=_item_results[:10]

        if items[i]['subitems'] != None:
            _item_results=[]
            _unpack(items,__items,_item_results,"subitem")

            results[items[i]["created_at"]]=_item_results[:10]


sorted_items = list(set(results.keys()))
sorted_items.sort(reverse=True)

for _item in sorted_items:
    t.add_row(results[_item])
    #print ",".join(str(_field) for _field in results[_item])

t.align = "l"
t._max_width = {"Group" : 20}
t.hrules=ALL
print(t)
