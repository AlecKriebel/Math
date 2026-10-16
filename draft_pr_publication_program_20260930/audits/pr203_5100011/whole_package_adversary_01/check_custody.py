from pathlib import Path
import json,hashlib,urllib.request,concurrent.futures
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;M=HERE.parent/'publication_package_v1/materials';A=M/'audit';C=json.loads((A/'ORIGINAL_SUBMISSION_CUSTODY.json').read_bytes())
def need(c,x):
 if not c:raise RuntimeError(x)
def get(u):return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Independent-mathematical-audit'}),timeout=30).read()
def one(z):
 rel,pin=z;b=(A/'original_submitted_head'/rel).read_bytes()
 need(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'sha256 '+rel)
 native=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();need(native==pin['git_blob'],'blob '+rel)
 u='https://raw.githubusercontent.com/AlecKriebel/Math/'+C['original_head']+'/unsolved_math_prioritization/attempts/5100011/'+rel
 remote=get(u);need(remote==b,'remote original '+rel)
 return {'path':rel,'bytes':len(b),'sha256':pin['sha256'],'git_blob':native,'immutable_remote_equal':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(one,C['files'].items()))
pr=json.loads(get('https://api.github.com/repos/AlecKriebel/Math/pulls/203'))
co=json.loads(get('https://api.github.com/repos/AlecKriebel/Math/git/commits/'+C['original_head']))
need(pr['created_at']=='2026-10-01T05:24:27Z','PR creation')
need(co['tree']['sha']==C['original_tree'],'original tree')
need([p['sha'] for p in co['parents']]==[C['original_sole_parent']],'parent')
r={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','original_files':rows,'count':len(rows),'bytes':sum(x['bytes'] for x in rows),'PR_public_API_created_at':pr['created_at'],'original_commit':co['sha'],'original_tree':co['tree']['sha'],'original_parent':co['parents'][0]['sha'],'scope':'Immutable raw original files authenticated directly plus current public PR object creation date. No claim about historical visibility, discovery time, or independent discovery.'}
(HERE/'CUSTODY_DIRECT_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='original_files'}))
