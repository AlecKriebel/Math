#!/usr/bin/env python3
"""Ordinary unauthenticated primary GETs with literal ordered header receipts.
No project/native/science imports, cookies, retries, bypasses or programme replay.
"""
from pathlib import Path
import datetime
import hashlib
import http.client
import json
import ssl
import sys
from urllib.parse import urlsplit,urljoin
E=Path(__file__).resolve().parent;D=E/'primary'
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
 if len(sys.argv)!=3:raise ValueError('explicit label and URL required')
 label,url=sys.argv[1:]
 if not label.replace('-','').replace('_','').isalnum():raise ValueError('safe fresh label required')
 D.mkdir(exist_ok=True);receipts=[]
 for hop in range(6):
  prefix=D/(label+'-hop'+str(hop));body=prefix.with_suffix('.body');receipt=prefix.with_suffix('.transport.json')
  if body.exists() or receipt.exists():raise ValueError('refuse primary overwrite')
  u=urlsplit(url)
  if u.scheme!='https' or not u.hostname or u.username or u.password:raise ValueError('ordinary HTTPS only')
  target=u.path or '/'
  if u.query:target+='?'+u.query
  headers=[['Host',u.netloc],['User-Agent','Independent mathematical primary-source audit'],['Accept','application/pdf, application/json, text/html, text/plain, */*']]
  r={'started_UTC':stamp(),'method':'GET','URL':url,'actual_request_headers_in_sent_order':headers,'redirect_hop':hop,'authentication_cookies_proxy_retry_or_bypass':False};conn=None
  try:
   conn=http.client.HTTPSConnection(u.hostname,u.port or 443,timeout=30,context=ssl.create_default_context());conn.putrequest('GET',target,skip_host=True,skip_accept_encoding=True)
   for k,v in headers:conn.putheader(k,v)
   conn.endheaders();response=conn.getresponse();b=response.read();r.update({'HTTP_status':response.status,'HTTP_reason':response.reason,'response_headers_in_received_order':[list(x) for x in response.getheaders()],'body':str(body.relative_to(E)),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest(),'error':None});body.write_bytes(b)
   location=response.getheader('Location')
  except Exception as error:
   r.update({'HTTP_status':None,'error_type':type(error).__name__,'error':str(error)});location=None
  finally:
   if conn:conn.close()
  r['completed_UTC']=stamp();receipt.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');receipts.append({'receipt':str(receipt.relative_to(E)),**r})
  if r.get('HTTP_status') in [301,302,303,307,308] and location:
   url=urljoin(url,location);continue
  break
 print(json.dumps({'label':label,'hops':receipts,'no_scientific_programme_execution':True},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
