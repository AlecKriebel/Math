#!/usr/bin/env python3
"""Explicit fresh ordinary primary-source GETs; no source scientific imports."""
from pathlib import Path
from urllib.parse import urlsplit,urljoin
import datetime,hashlib,http.client,json,sys
R=Path(__file__).resolve().parent/'primary_raw'
HOSTS={'doi.org','ems.press','publications.mfo.de','openaccess.city.ac.uk','arxiv.org','export.arxiv.org'}
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main(url,role):
 receipts=[];current=url
 for hop in range(8):
  p=urlsplit(current)
  if p.scheme!='https' or p.hostname not in HOSTS:raise RuntimeError('Unexpected primary redirect host: '+str(p.hostname))
  bodypath=R/(role+'.hop%02d.response.body'%hop)
  if bodypath.exists():raise RuntimeError('Preserve earlier attempt')
  headers=[['Host',p.netloc],['User-Agent','Python-http.client (independent primary verification)'],['Accept','*/*']]
  c=http.client.HTTPSConnection(p.hostname,p.port or 443,timeout=30);start=utc();partial=b'';status=None;received=[]
  try:
   c.putrequest('GET',p.path+('?' +p.query if p.query else ''),skip_host=True,skip_accept_encoding=True)
   for k,v in headers:c.putheader(k,v)
   c.endheaders();response=c.getresponse();status=response.status;reason=response.reason;received=response.getheaders()
   try:body=response.read()
   except http.client.IncompleteRead as e:body=e.partial;raise
   bodypath.write_bytes(body)
   receipt={'started_UTC':start,'completed_UTC':utc(),'method':'GET','actual_URL':current,'request_headers_ordered':headers,'HTTP_status':status,'HTTP_reason':reason,'response_headers_ordered':received,'whole_body_path':str(bodypath),'bytes':len(body),'SHA256':hashlib.sha256(body).hexdigest(),'transport_error':None}
  except Exception as e:
   if isinstance(e,http.client.IncompleteRead):body=e.partial;bodypath.write_bytes(body)
   receipt={'started_UTC':start,'completed_UTC':utc(),'method':'GET','actual_URL':current,'request_headers_ordered':headers,'HTTP_status':status,'response_headers_ordered':received,'whole_body_path':str(bodypath) if bodypath.exists() else None,'bytes':bodypath.stat().st_size if bodypath.exists() else None,'SHA256':hashlib.sha256(bodypath.read_bytes()).hexdigest() if bodypath.exists() else None,'transport_error':type(e).__name__,'message':str(e),'partial_body_if_incomplete':isinstance(e,http.client.IncompleteRead)}
   receipts.append(receipt);(R/(role+'.transports.json')).write_text(json.dumps(receipts,indent=2)+'\n');raise
  finally:c.close()
  receipts.append(receipt);(R/(role+'.transports.json')).write_text(json.dumps(receipts,indent=2)+'\n')
  if status in [301,302,303,307,308]:
   location=[v for k,v in received if k.lower()=='location']
   if len(location)!=1:raise RuntimeError('Ambiguous redirect')
   current=urljoin(current,location[0]);continue
  print(json.dumps({'role':role,'HTTP_status':status,'bytes':len(body),'SHA256':receipt['SHA256'],'whole_body_path':str(bodypath),'hops':len(receipts)}));return
 raise RuntimeError('Bounded redirects exceeded')
if __name__=='__main__':
 if len(sys.argv)!=3:raise SystemExit('Usage: primary_get.py URL role')
 main(sys.argv[1],sys.argv[2])
