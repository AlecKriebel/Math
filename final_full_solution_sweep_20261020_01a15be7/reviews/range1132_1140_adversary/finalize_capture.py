#!/usr/bin/env python3
"""Final read-only service and local custody recheck."""
from pathlib import Path
import subprocess,json,hashlib,datetime as dt,concurrent.futures,urllib.request,time
H=Path(__file__).resolve().parent;P=H/'private';C='39e8a7e1f675baa98d4907e7831edcbf2bf53767'
def sha(b):return hashlib.sha256(b).hexdigest()
def run(a):return subprocess.run(a,capture_output=True,check=True).stdout
def save(p,b):p.write_bytes(b)
def load(p):return json.loads(p.read_text())
def need(v,m):
 if not v:raise RuntimeError(m)
def pr(n):
 b=run(['gh','api',f'repos/AlecKriebel/Math/pulls/{n}']);save(P/f'pr{n}/live_end.json',b);a=load(P/f'pr{n}/live_start.json');v=json.loads(b)
 keys=lambda x:(x['head']['sha'],x['base']['sha'],x.get('body'),x['state'],x['merged'],x['draft'])
 need(keys(a)==keys(v),f'PR{n}drift');return {'pr':n,'head':v['head']['sha'],'base':v['base']['sha'],'body_sha256':sha((v.get('body')or'').encode()),'state':v['state'],'merged':v['merged'],'draft':v['draft'],'start_end_equal':True}
def provider(n):
 req=urllib.request.Request(f'https://zenodo.org/api/records/{n}',headers={'User-Agent':'bounded-independent-audit/1.0'})
 with urllib.request.urlopen(req,timeout=45) as r:b=r.read()
 save(P/f'record{n}/record_end.json',b);a=load(P/f'record{n}/record_start.json');v=json.loads(b)
 key=lambda x:(x['metadata'],x['state'],x['submitted'],x['doi'],{f['key']:(f['size'],f['checksum']) for f in x['files']})
 need(key(a)==key(v),f'provider{n}drift');return {'record':n,'metadata_state_doi_filemap_unchanged':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:prs=list(ex.map(pr,range(1132,1141)))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:records=list(ex.map(provider,[23063072,23372668,23442649,23443039]))
params={'spreadsheetId':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','range':"'Math Puzzles'!A:AQ",'valueRenderOption':'FORMATTED_VALUE'}
b=run(['gws','sheets','spreadsheets','values','get','--params',json.dumps(params)]);save(P/'ledger_end.json',b);need(json.loads(b)==load(P/'ledger_start.json'),'ledger drift')
commit=run(['gh','api',f'repos/AlecKriebel/Math/git/commits/{C}']);save(P/'checkpoint_commit.json',commit);need(json.loads(commit)['sha']==C,'checkpoint identity')
start=load(P/'START_CUSTODY.json');end={'at':dt.datetime.now(dt.timezone.utc).isoformat(),'checkpoint':C,'branch':run(['git','branch','--show-current']).decode().strip(),'git_head':run(['git','rev-parse','HEAD']).decode().strip(),'index_sha256':sha(Path('.git/index').read_bytes()),'prs':prs,'providers':records,'ledger_rows':len(json.loads(b)['values']),'whole_ledger_start_end_equal':True,'shared_branch_head_index_unchanged':None}
end['shared_branch_head_index_unchanged']=all(start[k]==end[k] for k in ['branch','git_head','index_sha256']);need(end['shared_branch_head_index_unchanged'],'shared Git custody drift')
(H/'FINAL_RECHECK.json').write_text(json.dumps(end,indent=2)+'\n');print(json.dumps({'status':'PASS','at':end['at'],'prs':len(prs),'providers':len(records),'rows':end['ledger_rows'],'shared_git_preserved':True}))
