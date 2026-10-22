from pathlib import Path
import json,gzip,urllib.request,urllib.parse,hashlib,datetime,concurrent.futures,subprocess
P=Path(__file__).resolve().parent;D=P/'private';OUT=D/'sources';OUT.mkdir(exist_ok=True)
PIN='0804de278fdf1d355aea7b584ac5b67e0955f27b'
queries={
'dpt_paper':f'https://raw.githubusercontent.com/Pengbinghui/pipeline-math/{PIN}/papers/erdos1038/Erdos_1038.pdf',
'dpt_readme':f'https://raw.githubusercontent.com/Pengbinghui/pipeline-math/{PIN}/README.md',
'dpt_tree':f'https://api.github.com/repos/Pengbinghui/pipeline-math/git/trees/{PIN}?recursive=1',
'dpt_path_history':'https://api.github.com/repos/Pengbinghui/pipeline-math/commits?path=papers/erdos1038/Erdos_1038.pdf&per_page=100',
'dpt_releases':'https://api.github.com/repos/Pengbinghui/pipeline-math/releases?per_page=100',
'dpt_tags':'https://api.github.com/repos/Pengbinghui/pipeline-math/tags?per_page=100',
'wang_paper':'https://multiscalar.ai/results/erdos-1038/paper.pdf',
'wang_page':'https://multiscalar.ai/results/erdos-1038/',
'wang_head':'https://api.github.com/repos/ShouqiaoW/erdos/commits?per_page=1',
'wang_path_history':'https://api.github.com/repos/ShouqiaoW/erdos/commits?path=1038/paper.pdf&per_page=100',
'wang_releases':'https://api.github.com/repos/ShouqiaoW/erdos/releases?per_page=100',
'wang_tags':'https://api.github.com/repos/ShouqiaoW/erdos/tags?per_page=100',
'wrong_zenodo_record':'https://zenodo.org/api/records/19549033',
'zenodo_erdos':'https://zenodo.org/api/records?'+urllib.parse.urlencode({'q':'"Erdos" "1038"','size':100}),
'zenodo_piranian':'https://zenodo.org/api/records?'+urllib.parse.urlencode({'q':'Piranian','size':100}),
'datacite_1038':'https://api.datacite.org/dois?'+urllib.parse.urlencode({'query':'titles.title:(Erdos 1038)','page[size]':100}),
'datacite_piranian':'https://api.datacite.org/dois?'+urllib.parse.urlencode({'query':'Piranian','page[size]':100}),
'datacite_dpt_title':'https://api.datacite.org/dois?'+urllib.parse.urlencode({'query':'"A Solution to a Problem of Erdős-Herzog-Piranian"','page[size]':100}),
'datacite_wang_title':'https://api.datacite.org/dois?'+urllib.parse.urlencode({'query':'"A Proposed Complete Solution to Erdős Problem 1038"','page[size]':100}),
'crossref_piranian':'https://api.crossref.org/works?'+urllib.parse.urlencode({'query.bibliographic':'A Solution to a Problem of Erdos Herzog Piranian Darvas Peng Tao','rows':20}),
'crossref_wang':'https://api.crossref.org/works?'+urllib.parse.urlencode({'query.bibliographic':'A Proposed Complete Solution to Erdos Problem 1038 Shouqiao Wang','rows':20}),
'arxiv_dpt':'https://export.arxiv.org/api/query?'+urllib.parse.urlencode({'search_query':'all:"Erdos-Herzog-Piranian"','max_results':100}),
'arxiv_1038':'https://export.arxiv.org/api/query?'+urllib.parse.urlencode({'search_query':'all:"Erdos" AND all:"1038"','max_results':100}),
}
def fetch(k,u):
 at=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  req=urllib.request.Request(u,headers={'User-Agent':'IndependentMathematicsAudit/1.0','Accept':'application/json' if 'api.' in u else '*/*'})
  with urllib.request.urlopen(req,timeout=35) as r:
   b=r.read(3500001);status=r.status;final=r.url;headers={x:r.headers.get(x) for x in ['Content-Type','ETag','Last-Modified','Date'] if r.headers.get(x)}
  if len(b)>3500000:raise RuntimeError('bounded-source limit')
  (OUT/(k+'.gz')).write_bytes(gzip.compress(b,mtime=0))
  return dict(key=k,url=u,at_utc=at,status=status,final_url=final,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),headers=headers,capture='private/sources/'+k+'.gz',private=True)
 except Exception as e:return dict(key=k,url=u,at_utc=at,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:results=list(ex.map(lambda x:fetch(*x),queries.items()))
(P/'SOURCE_INDEX.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
for r in results:print(json.dumps({k:r[k] for k in ['key','status','bytes','sha256','error'] if k in r}))
for key in ['dpt_paper','wang_paper']:
 b=gzip.decompress((OUT/(key+'.gz')).read_bytes());(D/(key+'.pdf')).write_bytes(b)
 r=subprocess.run(['pdftotext','-layout','-','-'],input=b,capture_output=True)
 if r.returncode:raise RuntimeError('pdftotext failed')
 (OUT/(key+'_text.gz')).write_bytes(gzip.compress(r.stdout,mtime=0));print(key,'text bytes',len(r.stdout))
print('TOTAL_BYTES',sum(f.stat().st_size for f in P.rglob('*') if f.is_file()))
