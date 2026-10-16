#!/usr/bin/env python3
import urllib.request,hashlib,json,datetime
sources=[('Etingof MIT 18.755 2024 lecture notes','https://ocw.mit.edu/courses/18-755-lie-groups-and-lie-algebras-ii-spring-2024/mit18_755_s24_lec_full.pdf'),('Hatcher Algebraic Topology author PDF','https://pi.math.cornell.edu/~hatcher/AT/AT.pdf')]
records=[]
for title,url in sources:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with urllib.request.urlopen(url,timeout=40) as response:
  b=response.read(); kind=response.headers.get('Content-Type'); final_url=response.geturl()
 end=datetime.datetime.now(datetime.timezone.utc).isoformat()
 records.append({'title':title,'url':url,'final_url':final_url,'start_utc':start,'end_utc':end,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'content_type':kind,'raw_content_saved':False})
print(json.dumps({'sources':records},indent=2))
