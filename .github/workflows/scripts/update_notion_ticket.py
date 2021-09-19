import requests
import json
import os

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
  'Authorization': f'Bearer {os.getenv('your_token')}', #store your token in this environment variable name
  'Content-Type': 'application/json',
  'Notion-Version': '2021-05-13'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
