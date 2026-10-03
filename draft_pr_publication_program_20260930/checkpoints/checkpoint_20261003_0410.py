"""Exact publication checkpoint: completed owned evidence; concurrent files stay outside index."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat,subprocess
P=Path(__file__).resolve().parents[1];R=P.parent;names=set()
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def add(p):
 assert p.is_file()and not p.is_symlink()and all(not q.is_symlink()for q in p.parents)
 assert p.stat().st_size<100*1024*1024
 names.add(p.relative_to(R).as_posix())
def tree(p):
 assert p.is_dir()and not p.is_symlink()
 for q in p.rglob('*'):
  assert not q.is_symlink()
  if q.is_file():add(q)
def closure(d,n):
 m=load(d/n)
 for z in m['files']:
  q=d/z['path'];b=q.read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']and stat.S_IMODE(q.stat().st_mode)==0o444
  if z.get('publication_allowed',True)is True:add(q)
 add(d/n)
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def foreign():
 out=[]
 for n in git('diff','--name-only','-z').decode().split('\0'):
  if n and n not in names:
   p=R/n;b=p.read_bytes();out.append({'path':n,'bytes':len(b),'sha256':sha(b)})
 return out
def main():
 assert __debug__ and git('branch','--show-current').strip()==b'main'and git('diff','--cached','--name-only')==b''
 head=git('rev-parse','HEAD').decode().strip();inv=load(P/'inventory.json');assert inv['completed_count']==34 and inv['current_pr']==45
 a44=P/'audits/pr44_2912';a45=P/'audits/pr45_9900007';a46=P/'audits/pr46_30004438'
 rootpost=load(a44/'ROOT_ACTUAL_POST_INSPECTION.json');assert rootpost['status']=='PASS'and rootpost['completed_primary_prs']==34 and rootpost['entire_native_proposal_and_saved_plan_reconstructed']is True
 for z in load(P/'checkpoints/CHECKPOINT_20261003_0337_v2.json')['owned_files']:add(R/z['path'])
 for a in [a44,a45]:
  for p in a.iterdir():
   if p.is_file():add(p)
  for p in a.glob('root_*'):
   if p.is_dir()and p.name!='root_checkpoint_0410_actual_capture':tree(p)
 for d,n in [(a44/'acceptance_preparation_family','PREPARATION_MANIFEST.json'),(a44/'acceptance_source_adversary_family','SELF_MANIFEST.json'),(a45/'whole_current_source_first_family','MANIFEST.json'),(a46,'ORIGINAL_PREPARATION_MANIFEST.json'),(a46/'projective_algebra_family','FAMILY_MANIFEST.json'),(a46/'complex_dynamics_family','COMPLEX_DYNAMICS_MANIFEST.json'),(R/'unsolved_math_prioritization/attempts/2912','MANIFEST.json')]:closure(d,n)
 for p in [a44/'final_acceptance',a44/'integration_log_preimages',a45/'whole_current_source_first_closure_actual_capture',a46/'original_preparation_closure_actual_capture']:tree(p)
 for p in a46.glob('*closure*actual_capture'):
  if p.is_dir():tree(p)
 for n in ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl']:add(R/n)
 for n in ['RESEARCH_LOG.md','inventory.json']:add(P/n)
 add(Path(__file__))
 utc=dt.datetime.now(dt.timezone.utc).isoformat()
 note='\n'+utc+' — Completed-evidence checkpoint: program34/180=18.88888888888889%, next45. PR44 actual acceptance and own5db508 checkpoint are on shared remote main; descending task reconciled429e3 remote PR383 via4342abee with exactly49 incoming paths, no ascending44/45whole/46 changes. PR45 ROOT actual59667 closed-whole inspection passes1068+self/1109 outside inputs/58 complete captures+8 newly captured frozen4 Git queries; initial59202 directory-row assumption failure preserved. SOURCE204+self867faf closed, fresh SOURCE adversary pending. PR46 ROOT mathematical review100% exact fullambient/allperiod construction creditedKozhasovKummer2020preprint; unchanged own62514 reproductions51/848 whole byte/typeequal, raw65174 checks149266659bytes/15458SQL/plain original source with ABSENT prior{}fallback. Original substantive0/5/sourceverification1, new0audit0. ROOT evidence37+self closed66642. Initial62101 empty failed-run-output JSON parse preserved; distinct correction succeeds. Current SOURCE preparation pending, no acceptance yet. No newpaperDOItracker. Foreign primary/cache/PDF/OCR/access data never copied; no evidence deleted.\n'
 for q in [P/'RESEARCH_LOG.md',a45/'ROOT_RESEARCH_LOG.md',a46/'ROOT_RESEARCH_LOG.md']:
  with q.open('a') as f:f.write(note)
  add(q)
 closure(a45/'acceptance_preparation_family','PREPARATION_MANIFEST.json')
 closure(a46/'root_original_actual_reproduction_v2','MANIFEST.json')
 for q in a46.iterdir():
  if q.is_file() and (q.name.startswith('ROOT_') or q.name in {'reproduce_original_ROOT.py','reproduce_original_ROOT_v2.py','audit_raw_provenance_ROOT.py','close_ROOT_reproduction.py'}):add(q)
 for q in a46.glob('root_*actual_capture'):
  if q.is_dir():tree(q)
 before=foreign();rows=[]
 for n in sorted(names):b=(R/n).read_bytes();rows.append({'path':n,'bytes':len(b),'sha256':sha(b),'observed_full_mode':stat.S_IMODE((R/n).stat().st_mode)})
 out=P/'checkpoints/CHECKPOINT_20261003_0410.json'
 with out.open('x')as f:json.dump({'schema':'ROOT_exact_completed_owned_checkpoint/v1','utc':utc,'actual_pid':os.getpid(),'main_before':head,'owned_files':rows,'foreign_dirty_before':before,'foreign_bodies_included':False,'active_families_included':False,'completed_count':34,'total':180,'completion_estimate_percent':34/180*100},f,indent=2);f.write('\n')
 add(out);assert git('rev-parse','HEAD').decode().strip()==head
 subprocess.run(['git','add','-f','--',*sorted(names)],cwd=R,check=True)
 staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0')if n};assert staged<=names
 for n in staged:assert git('show',':'+n)==(R/n).read_bytes()
 assert not staged&{z['path']for z in before}
 print(json.dumps({'status':'PASS_EXACT_COMPLETED_OWNED_CHECKPOINT_STAGED','pid':os.getpid(),'main_before':head,'owned':len(names),'staged':len(staged),'completed':34,'foreign_before':before,'foreign_after':foreign(),'foreign_staged':0,'completion_percent':34/180*100}))
if __name__=='__main__':main()
