from pathlib import Path
import urllib.request, urllib.error, hashlib, json, datetime
BASE=Path(__file__).resolve().parent
JOBS={'stubborn_v1_pdf': 'https://arxiv.org/pdf/2602.01191v1', 'stubborn_current_abs': 'https://arxiv.org/abs/2602.01191', 'stubborn_v1_html': 'https://arxiv.org/html/2602.01191v1', 'bkr_v1_pdf': 'https://arxiv.org/pdf/2407.21779v1', 'bkr_current_abs': 'https://arxiv.org/abs/2407.21779', 'bkr_current_publisher': 'https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/on-odd-powers-of-nonnegative-polynomials-that-are-not-sums-of-squares/7C4BAF1C7EBA17DE741C36DB40691412', 'owr_original_pdf': 'https://ems.press/content/serial-article-files/47007', 'scheiderer_author_pdf': 'https://www.math.uni-konstanz.de/~scheider/preprints/ppss.pdf', 'scheiderer_publisher': 'https://link.springer.com/article/10.1007/s00229-011-0484-3', 'blekherman_publications': 'https://sites.google.com/site/grrigg/', 'stacks_01XS': 'https://stacks.math.columbia.edu/tag/01XS', 'pinelis_mo': 'https://mathoverflow.net/questions/444079/are-truncated-even-degree-binomial-polynomials-psd', 'bkr_publisher_pdf': 'https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7C4BAF1C7EBA17DE741C36DB40691412/S2050509426102217a.pdf/on-odd-powers-of-nonnegative-polynomials-that-are-not-sums-of-squares.pdf', 'sinn_current_research': 'https://wwwuser.gwdguser.de/~sinn3/research.html', 'mo_53047': 'https://mathoverflow.net/questions/53047/when-is-a-power-of-a-nonnegative-polynomial-a-sum-of-squares', 'baldi_current_research': 'https://lorenzobaldi.github.io/', 'crossref_bkr_metadata': 'https://api.crossref.org/works/10.1017/fms.2026.10221', 'arxiv_stubborn_atom': 'https://export.arxiv.org/api/query?id_list=2602.01191', 'baldi_current_pub': 'https://lorenzobaldi.github.io/pub/', 'surfaces_2409_v1_html': 'https://arxiv.org/html/2409.08834v1'}
receipts=[]
for key,url in JOBS.items():
 row={'key':key,'requested_url':url,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent scholarly verification; Python urllib'})
  with urllib.request.urlopen(req,timeout=50) as r:
   body=r.read(); typ=r.headers.get('Content-Type',''); ext='.pdf' if body.startswith(b'%PDF') else '.html'
   path=BASE/'sources/private'/(key+ext);path.write_bytes(body)
   row.update(status=r.status,final_url=r.url,content_type=typ,bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),private_local_path=str(path.relative_to(BASE)))
 except Exception as e:row['error']=type(e).__name__+': '+str(e)
 row['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();receipts.append(row)
 (BASE/'FETCH_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
 print(key,row.get('status'),row.get('bytes'),row.get('error',''),flush=True)
