"""Fresh actual reproduction of this closed source-first review; no closed-file writes."""
from pathlib import Path
import argparse,datetime,hashlib,json,shutil,subprocess
SOURCE=Path(__file__).resolve().parent
ROOT=Path('/Users/alec/Documents/Math')
REL=Path('draft_pr_publication_program_20260930/audits/pr34_7000004')
P=ROOT/REL;C=P/'reviewed_candidate_v2'
FROZEN='8afc9a17669c12559aea4287117069a20fbb39eea2af4ffe9bba81d7586a702a'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def closed():
 m=load(SOURCE/'MANIFEST.json');rows=[]
 actual=sorted(str(p.relative_to(SOURCE)) for p in SOURCE.rglob('*') if p.is_file() and p!=SOURCE/'MANIFEST.json' and not set(p.relative_to(SOURCE).parts)&{'tmp','__pycache__'})
 assert actual==sorted(z['path'] for z in m['files'])
 for z in m['files']:
  p=SOURCE/z['path'];assert not p.is_symlink();b=p.read_bytes()
  assert len(b)==z['bytes'] and sha(b)==z['sha256'],str(p)
  if '.jsonl' in p.name:
   for line in b.splitlines():json.loads(line)
  elif '.json' in p.name:json.loads(b)
  rows.append(z)
 return rows
def bindings():
 assert sha((C/'MANIFEST.json').read_bytes())==FROZEN
 rows=load(SOURCE/'BINDINGS_BEFORE.json')['bindings']
 for z in rows:
  b=(ROOT/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
 return rows
def equivalent(q):
 if isinstance(q,dict):return {k:equivalent(v) for k,v in q.items() if k not in {'utc','stdout_sha256'}}
 if isinstance(q,list):return [equivalent(v) for v in q]
 return q
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();dest=a.output.expanduser().resolve()
 assert dest.is_relative_to((SOURCE/'tmp').resolve()) or dest.is_relative_to((P/'tmp').resolve()),'private output only'
 assert not dest.exists(),'use a new output directory'
 before=closed();bound=bindings();dest.mkdir(parents=True)
 r=dest/'repository';h=r/REL/'source_first_whole_adversary';h.mkdir(parents=True)
 for z in before:
  d=h/z['path'];d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(SOURCE/z['path'],d)
 shutil.copyfile(SOURCE/'MANIFEST.json',h/'MANIFEST.json')
 for z in bound:
  d=r/z['path'];d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/z['path'],d)
 shutil.copyfile(C/'MANIFEST.json',r/REL/'reviewed_candidate_v2/MANIFEST.json')
 u=r/'unsolved_math_prioritization';u.mkdir(exist_ok=True)
 for name in ['manifest.json','policy.json','QUEUE.md','queue.py','README.md','review_v2/related_target_groups.json']:
  q=u/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/'unsolved_math_prioritization'/name,q)
 # Read-only actual cache and Git objects; only pure score and read-only SQL/Git reads execute.
 for name,src in [('.git',ROOT/'.git'),('unsolved_math_prioritization/cache',ROOT/'unsolved_math_prioritization/cache')]:
  q=r/name;q.symlink_to(src,target_is_directory=True)
 for name in ['inventory.json','RESEARCH_LOG.md']:
  q=r/'draft_pr_publication_program_20260930'/name;shutil.copyfile(ROOT/'draft_pr_publication_program_20260930'/name,q)
 # replay_all's builder sandbox is a separate repository-shaped replica.
 rep=h/'tmp/replica';rep.mkdir(parents=True)
 for z in bound:
  d=rep/z['path'];d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/z['path'],d)
 shutil.copyfile(C/'MANIFEST.json',rep/REL/'reviewed_candidate_v2/MANIFEST.json')
 for name in ['manifest.json','policy.json','QUEUE.md','queue.py','README.md','review_v2/related_target_groups.json']:
  q=rep/'unsolved_math_prioritization'/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/'unsolved_math_prioritization'/name,q)
 for name,src in [('.git',ROOT/'.git'),('unsolved_math_prioritization/cache',ROOT/'unsolved_math_prioritization/cache')]:
  q=rep/name;q.symlink_to(src,target_is_directory=True)
 for name in ['inventory.json','RESEARCH_LOG.md']:
  q=rep/'draft_pr_publication_program_20260930'/name;shutil.copyfile(ROOT/'draft_pr_publication_program_20260930'/name,q)
 # Saved receipts remain read-only at SOURCE; remove copied receipts to force fresh execution.
 shutil.rmtree(h/'actual_replays')
 runs=[]
 for name in ['replay_all.py','independent_controls.py','review_closed_v2.py']:
  proc=subprocess.run(['/usr/bin/python3',str(h/name)],capture_output=True,timeout=900)
  out=dest/'runs'/name;out.mkdir(parents=True);(out/'stdout.txt').write_bytes(proc.stdout);(out/'stderr.txt').write_bytes(proc.stderr)
  rec={'program':name,'implementation_sha256':sha((h/name).read_bytes()),'returncode':proc.returncode,'stdout_sha256':sha(proc.stdout),'stderr_sha256':sha(proc.stderr)}
  (out/'receipt.json').write_text(json.dumps(rec,indent=2)+'\n');runs.append(rec)
  assert proc.returncode==0 and not proc.stderr,(name,proc.returncode,proc.stderr.decode())
 comparisons={}
 for name in ['ACTUAL_REPLAYS.json','INDEPENDENT_RESULTS.json']:
  assert equivalent(load(h/name))==equivalent(load(SOURCE/name)),name
  comparisons[name]='whole JSON equal except actual UTC and stdout hashes containing actual UTC'
 second=load(h/'SECOND_CLOSED_REVIEW.json');old=load(SOURCE/'SECOND_CLOSED_REVIEW.json')
 assert second['reviewed_second_manifest_sha256']==old['reviewed_second_manifest_sha256']
 assert second['complete_read_binding_ledger']==old['complete_read_binding_ledger']
 assert equivalent(second['actual_final_closure_replay'])==equivalent(old['actual_final_closure_replay'])
 assert second['actual_HTTP_helper_replays']==old['actual_HTTP_helper_replays']
 comparisons['SECOND_CLOSED_REVIEW.json']='whole bindings and replay result equal except actual UTC; HTTP source hashes equal'
 assert closed()==before and bindings()==bound
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'closed_review_manifest_sha256':sha((SOURCE/'MANIFEST.json').read_bytes()),'frozen_current_v2_manifest_sha256':FROZEN,'actual_fresh_helpers':runs,'comparisons':comparisons,'all_closed_source_and_273_frozen_bindings_unchanged':True,'original_substantive_attempts_added':0,'scope':'Actual verification replay only. Source-first chronology is historical and proved by original two seals, not retrospectively generated by replay. No queue entrypoint, shared builder write, branch mutation or external-person contact.'}
 (dest/'ROOT_REPLAY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
