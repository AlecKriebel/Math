"""Capture recent primary texts and priority criteria; never infer a verdict."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, subprocess
A=Path(__file__).resolve().parent
R=A.parents[2]
D=A/'root_priority_recent_private';D.mkdir(exist_ok=False)
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
pin=lambda p:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'mode':format(p.stat().st_mode&0o777,'04o')}
criteria={'utc':utc(),'scope':'ROOT current/concurrent primary-publication and exact-target repository provenance route; candidate mathematics already read and accepted, no assertion of blind root review.','claims':['E displayed original-versus-outer signed focal ratio equality for all primitive elliptical-caustic periods and coprime winding','M same positive phase-independent multiplier at both foci','C phase constancy disproved by exact same-family controls'],'prior_equivalence':'Require complete authenticated theorem and explicit hypothesis/specialization map for E/M or documented counterexample/nonconstancy theorem for C. Restricted period, alternate pedal object or known method is not a full target theorem.','coverage_limit':'No-index-hit is a dated bounded observation only. Compare publication/version date with candidate commit and document later/concurrent work separately. No absolute historical-firstness certification.'}
(A/'ROOT_PRIORITY_RECENT_ROUTE_CRITERIA.json').write_text(json.dumps(criteria,indent=2)+'\n')
family={}
for rel in ['priority_focal_20261004/FROZEN_ACCEPTANCE_CRITERIA.md','priority_focal_20261004/CRITERIA_FREEZE.json','priority_general_20261004/CRITERIA_FREEZE.md']:
 p=A/rel;family[rel]=pin(p)
(A/'ROOT_PRIORITY_CRITERIA_CUSTODY.json').write_text(json.dumps({'utc':utc(),'independent_families':family,'body_read_by_root':True,'reports_not_consulted':True,'root_route_criteria':pin(A/'ROOT_PRIORITY_RECENT_ROUTE_CRITERIA.json')},indent=2)+'\n')
def run(label,args,cwd):
 j={'argv':args,'cwd':str(cwd),'started_utc':utc()}
 (D/(label+'.spec.json')).write_text(json.dumps(j,indent=2)+'\n')
 r=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 for k,b in [('stdout',r.stdout),('stderr',r.stderr)]:
  (D/(label+'.'+k+'.bin')).write_bytes(b);j[k]={'bytes':len(b),'sha256':sha(b)}
 j.update(ended_utc=utc(),exit_code=r.returncode)
 (D/(label+'.execution.json')).write_text(json.dumps(j,indent=2)+'\n')
 if r.returncode:raise RuntimeError((label,r.returncode,r.stderr.decode(errors='replace')))
 return r.stdout
sources={}
for name,url in [('catalog','https://eulersolve.org/papers/'),('recent0021','https://eulersolve.org/papers/amr-050-0021/paper.pdf?v=34ff068237a7'),('recent0027','https://eulersolve.org/papers/amr-050-0027/paper.pdf?v=2d6e66f9bba1'),('recent0014','https://eulersolve.org/papers/amr-050-0014/paper.pdf?v=5ff816c279e3')]:
 suffix='.html' if name=='catalog' else '.pdf';p=D/(name+suffix)
 run(name+'_fetch',['/usr/bin/curl','-q','--fail','--location','--max-time','60','--dump-header',str(D/(name+'.headers')),'--output',str(p),url],D)
 sources[name]={'url':url,'file':p.name,**pin(p)}
 if suffix=='.pdf':
  assert p.read_bytes().startswith(b'%PDF-')
  t=D/(name+'.txt');run(name+'_extract',['/opt/homebrew/bin/pdftotext','-layout',str(p),str(t)],D);sources[name]['text']=pin(t)
remote=run('repo_remote',['/usr/bin/git','remote','get-url','origin'],R)
commit=run('candidate_commit',['/usr/bin/git','show','-s','--format=fuller','cc083024dbd00de06ad444cd4070f51f60d209eb'],R)
pr=run('candidate_pr',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/305'],R)
j={'utc':utc(),'status':'PASS_PRIMARY_ACQUISITION_ONLY_NO_PRIORITY_VERDICT','sources':sources,'custody_scope':'Full primary PDF bytes and full native streams retained privately. Text must be read and compared before any priority conclusion.'}
(A/'ROOT_PRIORITY_RECENT_ACQUISITION.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(j,indent=2));print(remote.decode());print(commit.decode())
