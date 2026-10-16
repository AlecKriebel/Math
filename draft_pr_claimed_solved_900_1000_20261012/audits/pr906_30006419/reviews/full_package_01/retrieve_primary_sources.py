#!/usr/bin/env python3
"""Fetch primary technical/source identities; raw bytes stay ignored."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,urllib.request
r=Path(__file__).resolve().parent
urls={'mvw_v1.pdf':'https://arxiv.org/pdf/2503.08553v1','mvw_current.pdf':'https://arxiv.org/pdf/2503.08553','owr.pdf':'https://ems.press/content/serial-article-files/52249','lw.pdf':'https://www.mi.uni-koeln.de/~alytchak/preprints/enarea.pdf','ks.pdf':'https://intlpress.com/site/pub/files/_fulltext/journals/cag/1993/0001/0004/CAG-1993-0001-0004-a004.pdf','crossref_final.json':'https://api.crossref.org/works/10.1515/crelle-2026-0042','publisher_final.html':'https://www.degruyterbrill.com/document/doi/10.1515/crelle-2026-0042/html','mcshane.pdf':'https://www.ams.org/bull/1934-40-12/S0002-9904-1934-05978-0/S0002-9904-1934-05978-0.pdf','hl.pdf':'https://projecteuclid.org/journals/acta-mathematica/volume-148/issue-none/Calibrated-geometries/10.1007/BF02392726.pdf'}
def get(item):
 n,u=item;d={'name':n,'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(u,timeout=40) as q:
   b=q.read();d.update({'status':q.status,'resolved':q.url,'mime':q.headers.get('Content-Type'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'authenticated_pdf':b.startswith(b'%PDF')})
  (r/'private_sources'/n).write_bytes(b)
 except Exception as e:d['error']=str(e)
 return d
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:out=list(ex.map(get,urls.items()))
(r/'PRIMARY_SOURCE_RECEIPTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
