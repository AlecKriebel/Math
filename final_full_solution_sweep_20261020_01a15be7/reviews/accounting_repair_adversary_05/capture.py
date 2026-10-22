from pathlib import Path
import datetime as dt,hashlib,json,os,shutil,subprocess,sys
sys.dont_write_bytecode=True
Q=Path(__file__).resolve().parent;B=Q.parent.parent;P=B/'reviews/accounting_repair_adversary_04'
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def capture(src,dst):
 assert src.is_file() and not src.is_symlink(),str(src)
 b=src.read_bytes();p=Q/dst;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);entries.append(dict(source=str(src),path=dst,bytes=len(b),sha256=sha(b),captured_at=now()))
save(Q/'RESEARCH_LOG.json',[dict(at=now(),completion_estimate_percent=5,event='Bounded independent local report review started; all writes confined to new05 review. No provider or Git mutations.')])
seals=[]
for name,expected in [('completed_publications_accounting_adversary',None),('accounting_repair_adversary_02',None),('accounting_repair_adversary_03',None),('accounting_repair_adversary_04','54f28f3872034f59f7c6612656f009b9662527e09b79c253690b7a71610f9f91')]:
 r=B/'reviews'/name;mb=(r/'OUTPUT_MANIFEST.json').read_bytes();m=json.loads(mb)
 if expected:assert sha(mb)==expected
 for e in m['files']:
  p=r/e['path'];assert not p.is_symlink(),str(p);b=p.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],str(p)
 for e in m.get('symlinks',[]):
  p=r/e['path'];assert p.is_symlink() and os.readlink(p)==e['target'] and str(p.resolve())==e['resolved_target']
 seals.append(dict(review=name,files=len(m['files']),symlinks=len(m.get('symlinks',[])),manifest_sha256=sha(mb),pass_=True))
save(Q/'PRIOR_SEAL_VALIDATION.json',seals)
entries=[];attempts=[]
for _ in range(30):
 a={n:(B/n).read_bytes() for n in ['STATE.json','rest_inventory.json','dispositions.jsonl']};s=json.loads(a['STATE.json']);j=[json.loads(l) for l in a['dispositions.jsonl'].splitlines() if l.strip()];stable=all((B/n).read_bytes()==v for n,v in a.items());coherent=[e['pr'] for e in j]==list(range(s['start_pr'],s['next_pr'])) and s['completed_pr_count']==len(j) and s['last_completely_processed_pr']==s['next_pr']-1;attempts.append(dict(at=now(),stable=stable,coherent=coherent,next_pr=s['next_pr']))
 if stable and coherent:break
else:raise RuntimeError('No coherent capture')
for n,b in a.items():
 p=Q/'inputs/current'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);entries.append(dict(source=str(B/n),path='inputs/current/'+n,bytes=len(b),sha256=sha(b),captured_at=now()))
for n in ['coverage_snapshot.py','ROOT_ACCOUNTING_REVIEW04_ACCEPTANCE.json','ACCOUNTING_REPAIR04_ROOT_REPLAY.json']:capture(B/n,'inputs/current/'+n)
assert sha((Q/'inputs/current/coverage_snapshot.py').read_bytes())=='b8bf6aea20822d53b82af962dd8462a82ff2f71f1f802fc5484ab6d723695fcf'
for e in j:capture(B/f"PR{e['pr']:04d}_DISPOSITION.json",f"inputs/current/PR{e['pr']:04d}_DISPOSITION.json")
for e in s['reopened_disposition_overrides']:capture(B/e['replacement_disposition'],'inputs/current/'+e['replacement_disposition'])
for e in s['completed_publications']:
 capture(B/e['verification'],'inputs/current/'+e['verification']);v=json.loads((B/e['verification']).read_text())
 for rel in v['evidence'].values():
  p=Path(rel)
  if not p.is_absolute() and (B/p).is_file():capture(B/p,'inputs/current/'+rel)
for rel in ['REPORT.md','CONTROL_ADJUDICATION.json','OUTPUT_MANIFEST.json','INPUT_MANIFEST.json','NEW_CONTROL_RESULTS.json','NEW_CONTROL_SUMMARY.json','new_controls.py']:capture(P/rel,'prior04/'+rel)
# Preserve each complete historical harness/input tree. Only mounted current code changes.
for name,src,scripts in [('prior',P/'replay/prior',['controls.py','supplementary.py']),('new03',P/'replay/new03',['new_controls.py']),('new04',P,['new_controls.py'])]:
 dst=Q/'replay'/name;dst.mkdir(parents=True)
 for p in (src/'inputs').rglob('*'):
  if p.is_file():capture(p,str((dst/'inputs'/p.relative_to(src/'inputs')).relative_to(Q)))
 for n in scripts:capture(src/n,str((dst/n).relative_to(Q)))
 shutil.copyfile(Q/'inputs/current/coverage_snapshot.py',dst/'inputs/current/coverage_snapshot.py')
assert all(json.loads((Q/'inputs/current'/f"PR{e['pr']:04d}_DISPOSITION.json").read_text())==e for e in j)
save(Q/'CAPTURE_COHERENCE.json',dict(at=now(),attempts=attempts,prefix_count=len(j),next_pr=s['next_pr'],note='Coherent byte capture; later canonical progress may change cursor/journal/inventory.'))
save(Q/'INPUT_MANIFEST.json',dict(at=now(),files=entries,note='Captured source bytes. Replay mounts deliberately replace only coverage_snapshot.py after capture; original sources and historical expectations remain untouched.'))
# independent accounting before invoking helper
raw=[e for e in j if e['disposition']=='published_verified_full_solution'];effective={e['pr']:e for e in j}
for o in s['reopened_disposition_overrides']:
 p=Q/'inputs/current'/f"PR{o['pr']:04d}_DISPOSITION.json";assert sha(p.read_bytes())==o['historical_disposition_sha256'];e=json.loads((Q/'inputs/current'/o['replacement_disposition']).read_text());assert e['historical_disposition_sha256']==sha(p.read_bytes());effective[o['pr']]=e
pub=[e for e in effective.values() if e['disposition']=='published_verified_full_solution'];assert len(raw)==3 and len(pub)==4 and {e['pr'] for e in pub}=={280,292,397,399}
save(Q/'INDEPENDENT_ACCOUNTING.json',dict(at=now(),raw_publications=len(raw),effective_publications=len(pub),preserved280_sha256=sha((Q/'inputs/current/PR0280_DISPOSITION.json').read_bytes()),own=s['completed_publications'],prefix_count=len(j),next_pr=s['next_pr'],highest=json.loads(a['rest_inventory.json'])['highest_pr'],scope='Local structural crossartifact evidence, no provider/proof/priority authority.'))
print(json.dumps(dict(captured_files=len(entries),seals=seals,prefix_count=len(j),next_pr=s['next_pr'])))
