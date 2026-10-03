import json,urllib.request
url='https://api.crossref.org/works/10.1142%2FS0218216503002561'
try:
 response=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source validation'}),timeout=30)
 payload=json.loads(response.read())['message']
 print(json.dumps({'url':url,'http_status':response.status,'selected_primary_metadata':{k:payload.get(k) for k in ('DOI','title','author','container-title','volume','issue','page','published','abstract')}},indent=2))
except Exception as e:
 print(json.dumps({'url':url,'source_access_failed':True,'error_type':type(e).__name__,'error':str(e)},indent=2))
 raise SystemExit(2)
