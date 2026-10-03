#!/usr/bin/env python3
"""Private mutation negatives against exact manifest, program and queue scope."""
from pathlib import Path
import json,hashlib,subprocess,shutil,datetime
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3];CAND=HERE.parent/'snapshot/problems/30004320_laurent_descent';PYTHON=REPO/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python';RUN=HERE/'private_controls';RUN.mkdir(exist_ok=False)
HEAD='74617174ddfb3ea726cea343a4ba915613724bdc';BASE='efd29c05204703acca9a0860812f54b94fae54b1';Q='unsolved_math_prioritization/QUEUE.md'
results=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def reject(name,check):
 try:check()
 except (AssertionError,ValueError,KeyError) as e:results.append({'control':name,'rejected':True,'reason':str(e)});return
 raise AssertionError('Unexpected acceptance: '+name)
manifest=json.loads((CAND/'PUBLICATION_MANIFEST.json').read_bytes());expected={r['path']:r for r in manifest['files']}
def scope(files):
 assert set(files)==set(expected),'closed path scope'
 for p,r in expected.items():
  assert len(files[p])==r['bytes'] and sha(files[p])==r['sha256'],p
baseline={p:(CAND/p).read_bytes() for p in expected};scope(baseline)
d=dict(baseline);d.pop('TURN_3.md');reject('missing historical proof',lambda:scope(d))
d=dict(baseline);d['undisclosed.pdf']=b'foreign';reject('unexpected public path',lambda:scope(d))
d=dict(baseline);d['TURN_5.md']+=b'\n';reject('one-byte proof drift',lambda:scope(d))
d=dict(baseline);d['review/INDEPENDENT_CHECKS.json']=b'{"status":"PASS"}';reject('selected-output replacement',lambda:scope(d))
# Actual original verifier executions on tampered private copies.
for label,target in [('tampered_turn_proof','TURN_4.md'),('tampered_checker','check_turn_1.py'),('tampered_author_manifest','FINAL_AUTHOR_MANIFEST.json')]:
 p=RUN/label;shutil.copytree(CAND,p);original=(p/target).read_bytes();(p/target).write_bytes(original+b'\n')
 r=subprocess.run([str(PYTHON),str(p/'verify_publication.py')],cwd=p,capture_output=True)
 (HERE/(label+'.stdout')).write_bytes(r.stdout);(HERE/(label+'.stderr')).write_bytes(r.stderr)
 assert r.returncode!=0,label
 results.append({'control':label,'rejected':True,'exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'original_sha256':sha(original),'mutated_sha256':sha(original+b'\n')})
# Validate an entire proposed queue against the base file, not only its own row.
base=subprocess.check_output(['git','show',BASE+':'+Q],cwd=REPO);actual=(HERE.parent/'snapshot'/Q).read_bytes();bl=base.splitlines(keepends=True);al=actual.splitlines(keepends=True)
def queue_ok(proposed):
 pl=proposed.splitlines(keepends=True);assert len(pl)==len(bl),'queue line count'
 dif=[i for i,(a,b) in enumerate(zip(bl,pl)) if a!=b];assert dif==[398],'exact own physical line399 only'
 bc=bl[398].decode().split('|');pc=pl[398].decode().split('|');assert len(bc)==len(pc),'queue columns'
 assert [j for j,(a,b) in enumerate(zip(bc,pc)) if a!=b]==[8,9],'queue cells8/9 only'
 assert pc[8].strip()=='unsolved' and pc[9].strip()=='5/5','queue final status'
queue_ok(actual);pl=al[:];pl[0]+=b'foreign';reject('foreign queue byte drift',lambda:queue_ok(b''.join(pl)))
pl=al[:];cells=pl[398].decode().split('|');cells[4]=' 0.9999 ';pl[398]='|'.join(cells).encode();reject('foreign own-row column drift',lambda:queue_ok(b''.join(pl)))
pl=al[:];cells=pl[398].decode().split('|');cells[8]=' claimed_solved ';pl[398]='|'.join(cells).encode();reject('unearned solved promotion',lambda:queue_ok(b''.join(pl)))
# These predicates are prospective binding guards, not a claim of live acceptance.
def pins(head,base,draft,body_hash):
 assert head==HEAD and base==BASE and draft is True and body_hash=='frozen-body','frozen metadata pins'
pins(HEAD,BASE,True,'frozen-body')
for label,args in [('changed head',('0'*40,BASE,True,'frozen-body')),('changed base',(HEAD,'0'*40,True,'frozen-body')),('changed draft state',(HEAD,BASE,False,'frozen-body')),('changed body',(HEAD,BASE,True,'edited-body'))]:reject(label,lambda args=args:pins(*args))
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'negative_controls':len(results),'results':results,'scope':'Private manifest, original verifier and entire-queue drift negatives only. The metadata predicate tests prospective pin rejection; actual live accepted body/head/base/draft gates remain pending.','snapshot_untouched':True}
(HERE/'DRIFT_NEGATIVES.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
