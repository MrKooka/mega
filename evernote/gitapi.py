import requests
import json


GITHUB_API="https://api.github.com"
API_TOKEN='b0e3f155491a054b9a237fa172a2277917f52189'

url=GITHUB_API+"/gists"
print("Request URL: %s"%url)
headers={'Authorization':'token %s'%API_TOKEN}
params={'scope':'gist'}
payload={"description":"GIST created by python code",
		 "public":True,
		 "files":{"python request module.py":{"content":"Python requests has 3 parameters:\
		 												 1)Request URL\n \
		 												 2)Header Fields\n \
		 												 3)Parameter \n\
		 												 4)Request body"}
		 										}}
res=requests.post(url,headers=headers,params=params,data=json.dumps(payload))

print(res.status_code)
print()
print(res.url)
print()
print(res.text)
j=json.loads(res.text)