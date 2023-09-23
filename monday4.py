import datetime
import sys
import requests
import json


s = " ".join(sys.argv[1:])

inputargs={}
for token in s.split("^"):
	_name,_value = token.split(":")
	inputargs[_name] = _value.split(",")

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjExMTgyMDkwNiwidWlkIjoxNTE2MzEwNywiaWFkIjoiMjAyMS0wNS0zMFQxMTowMDo1OS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NjY5MDk4NSwicmduIjoidXNlMSJ9.zIeOeoqeaZ2Q8NuKBPPw2LQFh2JRPvPwIkhhn4e5Q08"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : apiKey}

def _get_returned_columns(columns):

	d = {} 
	for j in range(0,len(columns)):
		d[columns[j]['id']] = (columns[j]['text'])

	d['item_id2'] = "a" + d['item_id']
	return d
	
def _get_item_values(output,columns):
	_columns = _get_returned_columns(columns)
 
	_sorted_columns = _columns.keys()
	_sorted_columns.sort()

	for _id in _sorted_columns:
		try:
			text = _columns[_id].strip()
		except:
			text = ""
		try:
			if text[-3:] == "UTC":
				dt = datetime.datetime.strptime(text,"%Y-%m-%d %H:%M:%S %Z")
				output.append(dt.strftime("%Y-%m-%d %H:%M"))
			else:
				output.append(text) 
		except:
			output.append("")
	return output

def _process_item(output,columns):
	_get_item_values(output,_columns)
	print u"^".join(output).encode('utf-8').strip()

def _print_column_titles(_titles):
	titles=["Type","Board","Group","Item","Sub Item"]
	for _value in _titles:
		titles.append(_value)
	print "^".join(str(_t) for _t in titles)

def _get_data(query):
	data = {'query' : query}
	return requests.post(url=apiUrl, json=data, headers=headers) # make request

#========================================================================

if inputargs["columntype"][0] == "select":
	_columns = "(ids: [\"status\",\"person\",\"creation_log\",\"last_updated\",\"last_updated2\",\"last_updated3\",\"item_id\",\"tags\"])"
	#_columns = "(ids: [\"status\",\"person\",\"creation_log\",\"last_updated\",\"last_updated2\",\"last_updated3\",\"item_id\",\"people\",\"people5\",\"watchers\",\"tags\",\"dropdown\",\"dropdown2\"])"
else:
	_columns = ""


if inputargs.has_key("item_id"):
    for _item_id in inputargs["item_id"]:
        r = _get_data('{ items (ids:[' + _item_id + ']) { column_values ' + _columns + ' { title id text value } subitems { id name column_values ' + _columns + '{ title id text value } } } }')
        print r.json()['data']['items']

        #r = _get_data('{ items_by_multiple_column_values (item_id:' + _item_id + ', board_id:' + _board_id + ', column_id: "status", column_values: ["Working","Not Started","Completed","Ongoing","ARCHIVED","PUBLISHED"]) { id name board { id description } group { id title } column_values ' + _columns + ' { title id text value } subitems { id name column_values ' + _columns + '{ title id text value } } } }')
        #print r.json()['data']['items_by_multiple_column_values']

#exit()


newest_first="true"
limit=5

for _board_id in inputargs['board_id']:
    r = _get_data('{ items_by_multiple_column_values (board_id:' + _board_id + ', column_id: "status", column_values: ["Working","Not Started","Completed","Not Needed","Unknown","Duplicate"]) { id name board { id description } group { id title } column_values ' + _columns + ' { title id text value } subitems { id name column_values ' + _columns + '{ title id text value } } } }')

    tasks = r.json()['data']['items_by_multiple_column_values']

    if "json" in inputargs['output']:
	    print json.dumps(r.json(),sort_keys=True, indent=4)

    if "csv" in inputargs['output']:
	    boardname = _board_id

		#_print_column_titles(tasks[0])
	
	    for i in range(0,len(tasks)):

			#item
			_itemname = tasks[i]['name']
			_groupname = tasks[i]['group']['title']
			_output = ["item",boardname,_groupname,_itemname,""]
			_columns = tasks[i]['column_values']
			_process_item(_output,_columns)
	
			#subitem
			_subitems = tasks[i]['subitems']
			if _subitems is not None:
				for j in range(0,len(_subitems)):
                       			_subitemname = _subitems[j]['name']
                       			_output = ["subitem",boardname,_groupname,_itemname,_subitemname]
					_columns = _subitems[j]['column_values']
					_process_item(_output,_columns)

