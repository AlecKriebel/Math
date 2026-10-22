#!/usr/bin/env python3
"""Read-only public-source retrieval; raw bodies stay in the scoped private directory."""
import concurrent.futures, datetime, hashlib, json, pathlib, urllib.request, urllib.error
BASE = pathlib.Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
OUT = BASE/'audits/pr0280_30000156/reviews/reconciliation_priority_20261021/manuscript_family'
RAW = BASE/'private/pr0280_priority_reconciliation/manuscript_family'
URLS = [
('nrv12_final','https://web.maths.unsw.edu.au/~jagr/NRV12.pdf'),
('roberts2011','https://www.dma.uvigo.es/~eliz/pdf/Roberts.pdf'),
('thesis_noah','https://noah.nrw/ubbihs/download/pdf/5124915'),
('vivaldi_old','https://webspace.maths.qmul.ac.uk/f.vivaldi/research/oldwork.html'),
('vivaldi_ari','https://webspace.maths.qmul.ac.uk/f.vivaldi/research/ari_dyn.html'),
('crossref_title','https://api.crossref.org/works?query.title=The%20dynamics%20of%20reversible%20rational%20maps%20over%20finite%20fields&rows=20'),
('arxiv_neumarker','https://export.arxiv.org/api/query?search_query=au%3ANeumarker&start=0&max_results=100'),
('bielefeld_oai','https://pub.uni-bielefeld.de/oai?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai%3Apub.uni-bielefeld.de%3A2508475'),
('openalex_name','https://api.openalex.org/authors?search=Natascha%20Neumaerker&per-page=20'),
('unsw_profile','https://research.unsw.edu.au/people/professor-john-alexander-gordon-roberts/publications'),
]
def fetch(item):
    key,url=item
    rec={'id':key,'url':url,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 independent mathematical bibliography audit'})
        with urllib.request.urlopen(req,timeout=28) as f:
            body=f.read(); rec.update(http_status=f.status,final_url=f.url,content_type=f.headers.get('Content-Type'))
        suffix='.pdf' if body.startswith(b'%PDF') else '.json' if body.lstrip().startswith((b'{',b'[')) else '.txt'
        dest=RAW/(key+suffix); dest.write_bytes(body)
        rec.update(bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),private_path=str(dest))
    except Exception as e:
        rec.update(error=type(e).__name__+': '+str(e))
    rec['finished_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    return rec
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        receipts=list(pool.map(fetch,URLS))
    (OUT/'ACCESS_RECEIPTS_01.json').write_text(json.dumps({'scope':'primary public bibliography/version retrieval; raw bodies private only','requests':receipts},indent=2)+'\n')
    for r in receipts: print(json.dumps({k:r.get(k) for k in ['id','http_status','content_type','bytes','error']}))
