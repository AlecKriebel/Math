"""Complete acquired source custody using provider commit metadata, not missing local objects."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'root_priority_recent_private'
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
pin=lambda p:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'mode':format(p.stat().st_mode&0o777,'04o')}
remote=(D/'repo_remote.stdout.bin').read_text().strip()
repo=remote.removesuffix('.git').split('github.com')[-1].lstrip('/:')
assert repo.count('/')==1 and repo.split('/')[1].lower()=='math'
def run(label,args):
 j={'argv':args,'cwd':str(R),'started_utc':utc()};(D/(label+'.spec.json')).write_text(json.dumps(j,indent=2)+'\n')
 r=subprocess.run(args,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 for k,b in [('stdout',r.stdout),('stderr',r.stderr)]:
  (D/(label+'.'+k+'.bin')).write_bytes(b);j[k]={'bytes':len(b),'sha256':sha(b)}
 j.update(ended_utc=utc(),exit_code=r.returncode);(D/(label+'.execution.json')).write_text(json.dumps(j,indent=2)+'\n')
 assert r.returncode==0,(label,r.returncode,r.stderr.decode(errors='replace'))
 return json.loads(r.stdout)
commit=run('candidate_commit_api',['/opt/homebrew/bin/gh','api','repos/'+repo+'/commits/cc083024dbd00de06ad444cd4070f51f60d209eb'])
pr=run('candidate_pr',['/opt/homebrew/bin/gh','api','repos/'+repo+'/pulls/305'])
assert commit['sha']=='cc083024dbd00de06ad444cd4070f51f60d209eb' and pr['head']['sha']==commit['sha'] and pr['state']=='open' and pr['draft'] is True
sources={}
for name,suffix in [('catalog','.html'),('recent0021','.pdf'),('recent0027','.pdf'),('recent0014','.pdf')]:
 p=D/(name+suffix);j=json.loads((D/(name+'_fetch.execution.json')).read_text());assert j['exit_code']==0
 sources[name]={'url':j['argv'][-1],'file':p.name,**pin(p),'fetch_execution':pin(D/(name+'_fetch.execution.json'))}
 if suffix=='.pdf':
  assert p.read_bytes().startswith(b'%PDF-');t=D/(name+'.txt');e=json.loads((D/(name+'_extract.execution.json')).read_text());assert e['exit_code']==0;sources[name]['text']=pin(t)
j={'utc':utc(),'status':'PASS_PRIMARY_ACQUISITION_ONLY_NO_PRIORITY_VERDICT','sources':sources,'candidate':{'commit':commit['sha'],'author_date':commit['commit']['author']['date'],'committer_date':commit['commit']['committer']['date'],'pr_created':pr['created_at'],'pr_state':pr['state'],'pr_draft':pr['draft']},'retained_failed_capture':'candidate_commit: local object absent, exit128; provider exact-commit response used instead. No failed history was overwritten.','custody_scope':'Whole PDFs and native streams retained privately; independent root comparison still required.','completion_estimates':{'mathematics':100,'priority':10,'workflow':31}}
(A/'ROOT_PRIORITY_RECENT_ACQUISITION.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
