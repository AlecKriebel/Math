#!/usr/bin/env python3
"""Bounded read-only primary/index source requests; no author contact."""
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,datetime
P=Path(__file__).resolve().parent;R=P/'private_reading'
qbase='https://api.archives-ouvertes.fr/search/?'
fields='halId_s,version_i,title_s,authFullName_s,publicationDate_s,submittedDate_s,modifiedDate_s,uri_s,doiId_s,arxivId_s,docType_s,fileMain_s'
qs=[('hal_static','halId_s:hal-04004998'),('hal_costabel_since2023','authLastName_s:Costabel AND producedDateY_i:[2023 TO 2026]'),('hal_dauge_since2023','authLastName_s:Dauge AND producedDateY_i:[2023 TO 2026]'),('hal_nedaiasl','authLastName_s:Nedaiasl'),('hal_dynamic_title','title_t:("discrete dipole" AND stability) AND (authLastName_s:Costabel OR authLastName_s:Dauge OR authLastName_s:Nedaiasl)')]
requests=[(key,qbase+urlencode({'q':q,'fl':fields,'wt':'json','rows':100,'sort':'producedDate_tdate desc'}),'json') for key,q in qs]
requests += [('costabel_list','https://costabel.perso.math.cnrs.fr/publis/listepublis.txt','txt'),('dauge_docs','https://dauge.pages.math.cnrs.fr/core/indexgen.html','html'),('dauge_cv2026','https://dauge.pages.math.cnrs.fr/CV/MDauge-CV%5B2026%5D.pdf','pdf'),('crossref_static','https://api.crossref.org/works/10.1007/s00020-023-02750-7','json'),('crossref_dynamic_title','https://api.crossref.org/works?'+urlencode({'query.bibliographic':'On the Stability of the Discrete Dipole Approximation in Time-Harmonic Dielectric Scattering Costabel Dauge Nedaiasl','rows':10}),'json'),('openalex_static_citations','https://api.openalex.org/works?filter=cites:W4388614641&per-page=100','json'),('semantic_static_citations','https://api.semanticscholar.org/graph/v1/paper/ARXIV:2302.13159/citations?fields=title,authors,year,externalIds,openAccessPdf&limit=100','json')]
for name,query in [('costabel','Costabel, Martin'),('dauge','Dauge, Monique'),('nedaiasl','Nedaiasl, Khadijeh')]:
 requests.append(('arxiv_'+name,'https://arxiv.org/search/?'+urlencode({'query':query,'searchtype':'author','abstracts':'show','order':'-announced_date_first','size':200}),'html'))
def fetch(item):
 key,url,ext=item;record={'key':key,'requested_url':url,'requested_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=Request(url,headers={'User-Agent':'Independent mathematical source audit (read only)'})
  with urlopen(req,timeout=20) as res:
   b=res.read(2500000);record.update(status=res.status,final_url=res.url,headers={k:v for k,v in res.headers.items() if k.lower() in ['content-type','last-modified','etag','content-length','date']})
  record.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),private_file=str(R/(key+'.'+ext)))
  (R/(key+'.'+ext)).write_bytes(b)
 except Exception as e:record['error']=str(e)
 return record
with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(fetch,requests))
(P/'CURRENT_FETCH_RECEIPT.json').write_text(json.dumps(results,indent=2)+'\n')
for r in results:print(r['key'],r.get('status',r.get('error')),r.get('bytes'),r.get('sha256'))
