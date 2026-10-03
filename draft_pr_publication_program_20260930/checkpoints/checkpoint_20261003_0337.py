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
 assert __debug__and git('branch','--show-current').strip()==b'main'and git('diff','--cached','--name-only')==b''
 head=git('rev-parse','HEAD').decode().strip();inv=load(P/'inventory.json');assert inv['completed_count']==34 and inv['current_pr']==45
 a44=P/'audits/pr44_2912';a45=P/'audits/pr45_9900007';a46=P/'audits/pr46_30004438'
 rootpost=load(a44/'ROOT_ACTUAL_POST_INSPECTION.json');assert rootpost['status']=='PASS'and rootpost['completed_primary_prs']==34 and rootpost['entire_native_proposal_and_saved_plan_reconstructed']is True
 for z in load(P/'checkpoints/CHECKPOINT_20261003_0304.json')['owned_files']:add(R/z['path'])
 for a in [a44,a45]:
  for p in a.iterdir():
   if p.is_file():add(p)
  for p in a.glob('root_*'):
   if p.is_dir()and p.name!='root_checkpoint_0337_actual_capture':tree(p)
 for d,n in [(a44/'acceptance_preparation_family','PREPARATION_MANIFEST.json'),(a44/'acceptance_source_adversary_family','SELF_MANIFEST.json'),(a45/'whole_current_source_first_family','MANIFEST.json'),(a46,'ORIGINAL_PREPARATION_MANIFEST.json'),(a46/'projective_algebra_family','FAMILY_MANIFEST.json'),(a46/'complex_dynamics_family','COMPLEX_DYNAMICS_MANIFEST.json'),(R/'unsolved_math_prioritization/attempts/2912','MANIFEST.json')]:closure(d,n)
 for p in [a44/'final_acceptance',a44/'integration_log_preimages',a45/'whole_current_source_first_closure_actual_capture',a46/'original_preparation_closure_actual_capture']:tree(p)
 for p in a46.glob('*closure*actual_capture'):
  if p.is_dir():tree(p)
 for n in ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl']:add(R/n)
 for n in ['RESEARCH_LOG.md','inventory.json']:add(P/n)
 add(Path(__file__))
 utc=dt.datetime.now(dt.timezone.utc).isoformat()
 note='\n'+utc+' — PR44 completion checkpoint: workflow100%, discovery0%, program34/180=18.88888888888889%. Actual original-head merge f369d1e8f74b6462a0866f4b57a888233420a149 / tree6fa2de74e3b7d658cde5b04b94bc699ad6648d88; sealer29359, successful preflight33183, overlay34249, prepush34829, finalize35635, mirror36340, post38024; independent ROOT complete42112 verifies all34 old states/full history prefix/entire inventory/438 merge bodies/440+self canonical/full13 modes/complete proposal and exact saved plan/fresh no-op. Initial source-inspection epoch substitution27896 and capture-schema28485 failures preserved, corrected28945 checks99 source/113 adversary/1267 inputs/39 captures. Initial preflight30405 stopped on concurrent dirty files; actual refreshed main3edc then successful retry preserved. Ready wrapper33581 failed own stale numeric43 assertion before any mutation, corrected33973 succeeds. Initial final inspector40221 completed substantive checks then failed an invented history_after_bytes key; corrected42112 uses actual append bytes, complete hash and unchanged raw history. Both mathematical realization gaps, UNSOLVED2/5,new0,audit0 and no novelty/paper/new DOI/tracker remain. Disk pressure briefly prevented a here-document; storage recovered without deleting any project evidence.\n'
 for p in [a44/'ROOT_RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
  with p.open('a')as f:f.write(note)
  add(p)
 for p,t in [(a45/'ROOT_RESEARCH_LOG.md','PR45 new whole1068+self b372d0fd clean complete report/verdict personally read; own source-first fixed-coupling and provenance falsifiers clean; whole Root reconciliation and actual44 predecessor acceptance source preparation pending. UNSOLVED1/5,new0,audit0; workflow85%, discovery0%.'),(a46/'ROOT_RESEARCH_LOG.md','PR46 original318 closed; distinct algebra34+self and complex33+self families independently prove full ambient/all-period known result; 51+848 checks independently reproduced by algebra family, new15+101 controls; ROOT source extracts and original proof read, ROOT reproduction/current package pending. already_solved0/5 known Kozhasov–Kummer2020 preprint, no newpaperDOItracker; workflow40%, projectdiscovery0%.')]:
  with p.open('a')as f:f.write('\n'+utc+' — '+t+'\n')
  add(p)
 before=foreign();rows=[]
 for n in sorted(names):b=(R/n).read_bytes();rows.append({'path':n,'bytes':len(b),'sha256':sha(b),'observed_full_mode':stat.S_IMODE((R/n).stat().st_mode)})
 out=P/'checkpoints/CHECKPOINT_20261003_0337.json'
 with out.open('x')as f:json.dump({'schema':'ROOT_exact_completed_owned_checkpoint/v1','utc':utc,'actual_pid':os.getpid(),'main_before':head,'owned_files':rows,'foreign_dirty_before':before,'foreign_bodies_included':False,'active_families_included':False,'completed_count':34,'total':180,'completion_estimate_percent':34/180*100},f,indent=2);f.write('\n')
 add(out);assert git('rev-parse','HEAD').decode().strip()==head
 subprocess.run(['git','add','-f','--',*sorted(names)],cwd=R,check=True)
 staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0')if n};assert staged<=names
 for n in staged:assert git('show',':'+n)==(R/n).read_bytes()
 assert not staged&{z['path']for z in before}
 print(json.dumps({'status':'PASS_EXACT_COMPLETED_OWNED_CHECKPOINT_STAGED','pid':os.getpid(),'main_before':head,'owned':len(names),'staged':len(staged),'completed':34,'foreign_before':before,'foreign_after':foreign(),'foreign_staged':0,'completion_percent':34/180*100}))
if __name__=='__main__':main()
