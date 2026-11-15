#!/usr/bin/env python3
"""Ordinary native public GET custody only. No scientific programme imports/execution."""
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlsplit,urljoin
import hashlib,http.client,json,ssl,sys
A=Path(__file__).resolve().parent
if not (A/'INITIAL_SEAL.json').exists():raise RuntimeError('paper-first seal required')
if len(sys.argv)!=3:raise RuntimeError('explicit new role and exact observed URL required')
role,url=sys.argv[1:]
if not role or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_' for c in role):raise ValueError('role')
folder=A/'primary'/role
if folder.exists():raise RuntimeError('preserve existing transport; no silent retry/overwrite')
folder.mkdir()
def now():return datetime.now(timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
class HTTPS(http.client.HTTPSConnection):
 def send(self,data):
  if isinstance(data,(bytes,bytearray,memoryview)):self.sent.extend(bytes(data))
  return super().send(data)
class HTTP(http.client.HTTPConnection):
 def send(self,data):
  if isinstance(data,(bytes,bytearray,memoryview)):self.sent.extend(bytes(data))
  return super().send(data)
rows=[];initial=url
try:
 for hop in range(6):
  u=urlsplit(url)
  if u.scheme not in ['http','https'] or u.username or u.password:raise ValueError('ordinary public HTTP(S) only')
  cls=HTTPS if u.scheme=='https' else HTTP
  c=cls(u.hostname,port=u.port,timeout=60);c.sent=bytearray();target=u.path or '/'
  if u.query:target+='?'+u.query
  start=now();c.request('GET',target,headers={'User-Agent':'Python-http.client/'+str(sys.version_info.major)+'.'+str(sys.version_info.minor)})
  response=c.getresponse();headers=list(response.headers.raw_items());status=response.status;reason=response.reason;parts=[]
  try:
   while True:
    chunk=response.read1(65536)
    if not chunk:break
    parts.append(chunk)
  except Exception:
   bodypath=folder/('hop-%02d.partial-received.body'%hop);bodypath.write_bytes(b''.join(parts));sentpath=folder/('hop-%02d.actual-request.bin'%hop);sentpath.write_bytes(c.sent)
   rows.append({'hop':hop,'requested_URL':url,'UTC_started':start,'UTC_completed':now(),'HTTP_status':status,'reason':reason,'ordered_response_headers':headers,'whole_received_partial_body':pin(bodypath),'native_body_complete':False,'actual_sent_request_bytes':pin(sentpath),'partial_received_bytes_preserved_before_followup':True});c.close();raise
  body=b''.join(parts);c.close()
  bodypath=folder/('hop-%02d.body'%hop);bodypath.write_bytes(body);sentpath=folder/('hop-%02d.actual-request.bin'%hop);sentpath.write_bytes(c.sent)
  row={'hop':hop,'requested_URL':url,'UTC_started':start,'UTC_completed':now(),'method':'GET','HTTP_status':status,'reason':reason,'ordered_response_headers':headers,'whole_body':pin(bodypath),'actual_sent_request_bytes':pin(sentpath),'body_preserved_before_any_followup':True,'custom_auth_proxy_or_bypass':False};rows.append(row)
  (folder/'TRANSPORT.json').write_text(json.dumps({'role':role,'initial_URL':initial,'actual_requests':rows,'complete':False},ensure_ascii=False,indent=2)+'\n')
  if status in [301,302,303,307,308]:
   locations=[v for k,v in headers if k.lower()=='location']
   if len(locations)!=1:raise ValueError('no unique actual redirect Location')
   url=urljoin(url,locations[0]);continue
  receipt={'role':role,'initial_URL':initial,'actual_requests':rows,'complete':True,'final_HTTP_status':status,'final_URL':url,'final_body':pin(bodypath),'ordinary_native_GETs':len(rows),'native_body_reused':False}
  (folder/'TRANSPORT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'role':role,'status':status,'URL':url,'final_body':pin(bodypath),'transport':pin(folder/'TRANSPORT.json')}));break
 else:raise ValueError('bounded redirect limit')
except Exception as e:
 (folder/'FAILURE.json').write_text(json.dumps({'UTC':now(),'role':role,'initial_URL':initial,'actual_completed_requests':rows,'exception_type':type(e).__name__,'exception':str(e),'all_received_whole_bodies_preserved':True},indent=2)+'\n');raise
