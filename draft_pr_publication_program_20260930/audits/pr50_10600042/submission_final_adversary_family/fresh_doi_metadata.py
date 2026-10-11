#!/usr/bin/env python3
"""Read DOI-registration primary metadata only; no contact with people."""
import hashlib, json, urllib.request
from pathlib import Path
base=Path(__file__).absolute().parent
records=[]
for label,doi in [('survey','10.4064/bc103-0-1'),('GKS','10.1112/blms.12761'),('Fiedler','10.1142/S0218216503002561')]:
    url='https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='')
    req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical preprint source review','Accept':'application/json'})
    with urllib.request.urlopen(req,timeout=35) as response:
        body=response.read(); status=response.status; final=response.url
    data=json.loads(body)
    assert data['status']=='ok' and data['message']['DOI'].lower()==doi.lower()
    (base/('PRIMARY_'+label+'_crossref.json')).write_bytes(body)
    records.append({'label':label,'url':url,'final_url':final,'http_status':status,'bytes':len(body),
                    'sha256':hashlib.sha256(body).hexdigest(),'message':data['message']})
print(json.dumps({'status':'PASS_THREE_PRIMARY_DOI_REGISTRATION_RECORDS','records':records},indent=2))
