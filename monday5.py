from datetime import datetime, timedelta
import sys
import requests
import json
import pprint

s = " ".join(sys.argv[1:])

inputargs={}
for token in s.split("^"):
	_name,_value = token.split(":")
	inputargs[_name] = _value.split(",")

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjExMTgyMDkwNiwidWlkIjoxNTE2MzEwNywiaWFkIjoiMjAyMS0wNS0zMFQxMTowMDo1OS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NjY5MDk4NSwicmduIjoidXNlMSJ9.zIeOeoqeaZ2Q8NuKBPPw2LQFh2JRPvPwIkhhn4e5Q08"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : apiKey}

def _get_returned_columns(columns,_id):

    d = {} 
    for j in range(0,len(columns)):
        d[columns[j]['id']] = (columns[j]['text'])

    if d.has_key('item_id') == False:
        if d.has_key('item_id3') == True:
            d['item_id2'] = "a" + d['item_id3']
            d['item_id'] = d['item_id3']
            d.pop('item_id3')
        else:
            #d['item_id'] = 
            pprint.pprint(columns)
    else:
        d['item_id2'] = "a" + d['item_id']
    return d
	
def _get_item_values(output,columns,_id):
    _columns = _get_returned_columns(columns,_id)
    _sorted_columns = _columns.keys()
    _sorted_columns.sort()

    num_valid_dates=0
    for _id in _sorted_columns:
        try:
            text = _columns[_id].strip()
        except:
            text = ""
        try:
            if text[-3:] == "UTC":
                dt = datetime.strptime(text,"%Y-%m-%d %H:%M:%S %Z")

                if dt > cutoffdt:
                    num_valid_dates=num_valid_dates+1

                output.append(dt.strftime("%Y-%m-%d %H:%M"))
            else:
				output.append(text) 
        except:
			output.append("")

    if num_valid_dates==0:
        return -1
	return output

def _process_item(output,columns,_id):
    if _get_item_values(output,_columns,_id) != -1:
	    print u"^".join(output).encode('utf-8').strip()

def _print_column_titles(_titles):
	titles=["Type","Board","Group","Item","Sub Item"]
	for _value in _titles:
		titles.append(_value)
	print "^".join(str(_t) for _t in titles)

def _get_data(query):
	data = {'query' : query}
	return requests.post(url=apiUrl, json=data, headers=headers) # make request


cutoffdt=datetime.now() - timedelta(days=int(inputargs['timewindow'][0]))

_board_ids="[1140656959]"
#,2193345626,2193345626,2259144314,2763786972,4973959122,4974012540,4909340518,4973204278]"
_base_columns = ["id","name","created_at","updated_at"]
_columns = "(ids: [\"status\",\"person\",\"creation_log\",\"last_updated\",\"last_updated2\",\"last_updated3\",\"item_id3\",\"item_id\",\"tags\",\"people\",\"people5\"])"
_column_values = " columns: column_values " + _columns + "{title id text value }"
_subitems = "subitems {" + " ".join(_base_columns) + " " + _column_values + "}"

newest_first="true"
limit=5

for _board_id in inputargs['board_id']:

    r = _get_data('{boards(ids: ' + _board_id + ') { id name items (newest_first : true, limit : 200) {' + " ".join(_base_columns) + ' group { title } ' + _column_values + '  ' + _subitems + ' } } }')
    response = r.json()
    if response.has_key('status_code') == True:
        if response['status_code']==429:
            print response['error_message'] 
            exit()

#u'{"error_code":"ComplexityException","status_code":429,"error_message":"Complexity budget exhausted, query cost 3607822 budget remaining 2784356 out of 10000000 reset in 13 seconds","error_data":{},"errors":["Complexity budget exhausted, query cost 3607822 budget remaining 2784356 out of 10000000 reset in 13 seconds"],"account_id":6690985}'

    #print r.text

    boards = r.json()['data']['boards']

    for __items in boards:
        tasks = __items['items']
        _boardname = __items['id']

        for i in range(0,len(tasks)):

            _itemname = tasks[i]['name']
            _groupname = tasks[i]['group']['title']
            _id = tasks[i]['id']
            _output = ["item",_boardname,_groupname,_itemname,""]
            _columns = tasks[i]['columns']
            _process_item(_output,_columns,_id)
	
            _subitems = tasks[i]['subitems']
            if _subitems is not None:
                for j in range(0,len(_subitems)):
                    _id = _subitems[j]['id']
                    _subitemname = _subitems[j]['name']
                    _output = ["subitem",_boardname,_groupname,_itemname,_subitemname]
                    _columns = _subitems[j]['columns']
                    _process_item(_output,_columns,_id)

