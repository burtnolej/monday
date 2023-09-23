#!/bin/bash

access_code="eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjExMTgyMDkwNiwidWlkIjoxNTE2MzEwNywiaWFkIjoiMjAyMS0wNS0zMFQxMTowMDo1OS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NjY5MDk4NSwicmduIjoidXNlMSJ9.zIeOeoqeaZ2Q8NuKBPPw2LQFh2JRPvPwIkhhn4e5Q08"

curl -X POST \
       	-H "Content-Type:application/json" \
	-H "Authorization:$access_code" \
       	-H "API-Version:2023-07" \
 	-d "{\"query\":\"query{ boards(ids: 1140656959) { id name items(newest_first: true, limit: 25, page: 1) { id name created_at updated_at group { title } columns: column_values { title text } } } } \"}" \
       	"https://api.monday.com/v2/"

#-d "{\"query\":\"query{items (ids:5013296680) {name}}\"}" \
#-d "{\"query\":\"query{items (ids:5013296680){name}}\"}" \
