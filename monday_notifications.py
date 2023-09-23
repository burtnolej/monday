from datetime import datetime, timedelta
import sys
import requests
import json

s = " ".join(sys.argv[1:])

inputargs={}
if s != "":
    for token in s.split("^"):
        _name,_value = token.split(":")
        inputargs[_name] = _value.split(",")

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjExMTgyMDkwNiwidWlkIjoxNTE2MzEwNywiaWFkIjoiMjAyMS0wNS0zMFQxMTowMDo1OS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NjY5MDk4NSwicmduIjoidXNlMSJ9.zIeOeoqeaZ2Q8NuKBPPw2LQFh2JRPvPwIkhhn4e5Q08"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : apiKey}

def _get_data(query):
        data = {'query' : query}
	print data
        return requests.post(url=apiUrl, json=data, headers=headers) # make request

if inputargs.has_key("timewindow") == False:
    inputargs['timewindow'] = [3000]

cutoffdt=datetime.now() - timedelta(days=int(inputargs['timewindow'][0]))

query = "{updates (limit: 3000) { text_body id item_id created_at creator { name id } } }"
r = _get_data(query)
updates = r.json()['data']['updates']

for i in range(0,len(updates)):

    dt = datetime.strptime(updates[i]['created_at'][:-1],"%Y-%m-%dT%H:%M:%S")
    if dt > cutoffdt:
	    output = []
	    output.append(updates[i]['created_at'])	
	    output.append(updates[i]['item_id'])	
	    output.append(updates[i]['id'])	
	    output.append(updates[i]['creator']['name'])	
	    topline = updates[i]['text_body'].split("\n")[0] 
	    output.append(topline)
	    print u"^".join(output).encode('utf-8').strip()

