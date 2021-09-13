import requests
import json

url = "https://api.notion.com/v1/databases/b7a15cb698a541ac897710f7c578dd56/query"

payload = json.dumps({
  "filter": {
    "property": "Tags",
    "select": {
      "equals": "In Progress"
    }
  }
})
headers = {
  'Authorization': 'Bearer secret_GsPbngjCFPw1TQdfOqw1w88t5VdMxFuL56r7U5o6stI',
  'Content-Type': 'application/json',
  'Notion-Version': '2021-05-13'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
