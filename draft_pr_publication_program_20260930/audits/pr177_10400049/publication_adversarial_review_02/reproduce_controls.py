#!/usr/bin/env python3
"""Own archive reproduction and deliberately scientific mutation controls.
Run only in this reviewer folder. No frozen-package writes; no external actions.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
ARCHIVE=ROOT/'archive_replay'
OUT=ROOT/'runs';OUT.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
variants={
 'verify.py':[
  ('wrong_half_parameter','half=F(1,2);chi_g=half**2','half=F(1,3);chi_g=half**2','half_twist_character'),
  ('odd_resolution_shift','expanded={2*n+r+e:a','expanded={2*n+r+e+1:a','braid_full_twist_resolution'),
  ('cubic_instead_of_square','def G(v):return sum(x*x for x in v)','def G(v):return sum(x*x*x for x in v)','actual_algebraically_split_zero_set_OR_orientation_and_order_independence')
 ],
 'review/independent_checks.py':[
  ('wrong_half_parameter','half=F(1,2);g=half*half','half=F(1,3);g=half*half','ideal_killed_by_character'),
  ('wrong_linking_normalization','lk=F(signed_intercomponent,2)','lk=F(signed_intercomponent,4)','full_twist_linking_normalization'),
  ('wrong_division_sign','p[shift+2]+=lead','p[shift+2]-=lead','full_algebra_restriction_radical_diagnostic')
 ]
}
for rel,mutations in variants.items():
 original=(ARCHIVE/rel).read_text()
 for label,old,new,gate in [('baseline','','','PASS')]+mutations:
  code=original
  if old:
   if code.count(old)!=1:raise RuntimeError('mutation anchor not unique: '+label)
   code=code.replace(old,new)
  # Keep the file's runtime layout; only altered script bytes differ.
  dest=OUT/(Path(rel).stem+'_'+label)
  dest.mkdir(exist_ok=True)
  for c in ['CANDIDATE.md','review/author_replay/CANDIDATE.md']:
   q=dest/c;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((ARCHIVE/c).read_bytes())
  script=dest/rel;script.parent.mkdir(parents=True,exist_ok=True);script.write_text(code)
  for optimized in [False,True]:
   cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(script)]
   start=datetime.now(timezone.utc).isoformat()
   run=subprocess.run(cmd,cwd=dest,capture_output=True,text=True,timeout=20)
   mode='optimized' if optimized else 'ordinary'
   stdout=dest/(mode+'.stdout.json');stderr=dest/(mode+'.stderr.txt')
   stdout.write_text(run.stdout);stderr.write_text(run.stderr)
   row={'script':rel,'variant':label,'mode':mode,'start_UTC':start,'end_UTC':datetime.now(timezone.utc).isoformat(),'exit_code':run.returncode,'script_SHA256':sha(script.read_bytes()),'stdout_SHA256':sha(stdout.read_bytes()),'stderr_SHA256':sha(stderr.read_bytes()),'expected_gate':gate}
   if label=='baseline':
    if run.returncode!=0:raise RuntimeError('baseline failed: '+run.stderr)
    data=json.loads(run.stdout);row['assertions']=data['assertions'];row['categories']=data['categories'];row['result']='PASS'
   else:
    if run.returncode==0 or 'scientific control failed:' not in run.stderr:raise RuntimeError('mutation not scientifically rejected: '+str(row))
    row['observed_gate']=run.stderr.strip().split('scientific control failed: ')[-1]
    row['result']='SCIENTIFIC_MUTATION_REJECTED'
   rows.append(row)
result={'UTC':datetime.now(timezone.utc).isoformat(),'Python':sys.version,'archive_SHA256':sha((ROOT.parent/'publication_package_v2/verification-package.zip').read_bytes()),'baseline_passes':sum(x['variant']=='baseline' for x in rows),'scientific_mutation_rejections':sum(x['variant']!='baseline' for x in rows),'rows':rows,'limits':'Finite supporting diagnostics only; universal proof assessed independently before reading scripts.'}
(ROOT/'INDEPENDENT_REPRODUCTION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
print('Baseline counts:',[(x['script'],x['mode'],x['assertions']) for x in rows if x['variant']=='baseline'])
print('Mutation gates:',[(x['variant'],x['mode'],x['observed_gate']) for x in rows if x['variant']!='baseline'])
