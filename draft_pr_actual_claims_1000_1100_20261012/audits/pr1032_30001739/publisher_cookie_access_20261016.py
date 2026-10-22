"""Ordinary public publisher requests with an in-memory cookie jar only."""
from pathlib import Path
import http.cookiejar,urllib.request,urllib.parse,hashlib,json,datetime
O=Path(__file__).resolve().parent/'publisher_cookie_access_20261016';O.mkdir(exist_ok=True)
jar=http.cookiejar.CookieJar();client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar));rows=[]
for tag,url in [('article','https://link.springer.com/article/10.1007/s11464-025-0256-0'),('pdf','https://link.springer.com/content/pdf/10.1007/s11464-025-0256-0.pdf')]:
 r={'label':tag,'requested_url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with client.open(url,timeout=25) as response:
   body=response.read(12*1024*1024+1);r.update(status=response.status,content_type=response.headers.get('Content-Type'),bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),final_url_without_query=urllib.parse.urlunsplit(urllib.parse.urlsplit(response.url)._replace(query='',fragment='')),is_PDF=body.startswith(b'%PDF-'))
   if len(body)>12*1024*1024:raise RuntimeError('body exceeds bounded capture')
   name=tag+('.pdf' if r['is_PDF'] else '.html');(O/name).write_bytes(body);r['retained_body']=name
 except Exception as e:r['error']=type(e).__name__+': '+str(e)
 rows.append(r)
 (O/'ACCESS_RECEIPT.json').write_text(json.dumps({'requests':rows,'cookie_values_persisted_or_printed':False,'access':'Ordinary unauthenticated public requests; no login, access request, header spoofing or access-control bypass. No body availability inferred from HTTP status alone.'},indent=2)+'\n')
print(json.dumps({'requests':rows,'cookie_values_printed':False}))
