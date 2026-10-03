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
 head=git('rev-parse','HEAD').decode().strip();inv=load(P/'inventory.json');assert inv['completed_count']==35 and inv['current_pr']==46
 a44=P/'audits/pr44_2912';a45=P/'audits/pr45_9900007';a46=P/'audits/pr46_30004438'
 rootpost=load(a45/'ROOT_ACTUAL_POST_INSPECTION.json');assert rootpost['status']=='PASS'and rootpost['completed_primary_prs']==35 and rootpost['entire_native_proposal_and_saved_plan_reconstructed']is True
 for z in load(P/'checkpoints/CHECKPOINT_20261003_0410.json')['owned_files']:add(R/z['path'])
 for a in [a44,a45]:
  for p in a.iterdir():
   if p.is_file():add(p)
  for p in a.glob('root_*'):
   if p.is_dir()and p.name!='root_checkpoint_0441_actual_capture':tree(p)
 for d,n in [(a44/'acceptance_preparation_family','PREPARATION_MANIFEST.json'),(a44/'acceptance_source_adversary_family','SELF_MANIFEST.json'),(a45/'whole_current_source_first_family','MANIFEST.json'),(a46,'ORIGINAL_PREPARATION_MANIFEST.json'),(a46/'projective_algebra_family','FAMILY_MANIFEST.json'),(a46/'complex_dynamics_family','COMPLEX_DYNAMICS_MANIFEST.json'),(R/'unsolved_math_prioritization/attempts/2912','MANIFEST.json')]:closure(d,n)
 for p in [a44/'final_acceptance',a44/'integration_log_preimages',a45/'whole_current_source_first_closure_actual_capture',a46/'original_preparation_closure_actual_capture']:tree(p)
 for d,n in [(a45/'acceptance_source_adversary_family','SELF_MANIFEST.json'),(a46/'current_preparation_family','PREPARATION_MANIFEST.json'),(a46/'current_source_adversary_family','SELF_MANIFEST.json'),(P/'audits/pr47_2849','ORIGINAL_PREPARATION_MANIFEST.json'),(R/'unsolved_math_prioritization/attempts/9900007','MANIFEST.json')]:closure(d,n)
 for d in [a45/'final_review',a45/'integration_log_preimages',a45/'ROOT_POST_ACTUAL_GIT',a45/'acceptance_source_adversary_outer_closure_capture',P/'audits/pr47_2849/original_preparation_closure_actual_capture']:tree(d)
 for p in a46.glob('*closure*actual_capture'):
  if p.is_dir():tree(p)
 for n in ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl']:add(R/n)
 for n in ['RESEARCH_LOG.md','inventory.json']:add(P/n)
 add(Path(__file__))
 utc=dt.datetime.now(dt.timezone.utc).isoformat()
 note='\n'+utc+' — Completed-evidence checkpoint: program35/180=19.444444444444446%, next46. PR45 actual MERGED8a9f14c1a99d543331ae77990ddd3f154bb15dd7/tree15c43cadd94afa1c969be350e301a645d511a511 accepted UNSOLVED illustrative synchronous obstruction only; general characterization/priority gap preserved; original1/5 new0audit0 no paperDOItracker. SOURCE204/fresh SOURCE426+self and ROOT87305 full2469 bodies/109complete captures approved exact scope; two honest ROOT source-inspection failures preserved and corrected. Realfinal88023 PASS then newfresh13/head0b627 protects exactlyfive specific other-project trackedfiles. Initial89981 preflight rejected newdirtyotheraudit files; retained and91234 rebasepreflight PASS. Actual original-head conflict/whole382783bytequeue read,93001overlay505/exact506staged,95584prepush,96847push,96999finalize,98167mirror,253post PASS. ROOT3188 fullyinspects521capturedGitqueries/exact505mergefiles+queue/507+self full444canonical/all35priorstates/fullhistory/entire180inventory/fullproposal/savedplan/no-op/native13modes; exact20-key ROOTpost82e7d4abe822ca2df37fdfb1a3c165f1c3125a0436017acee9d7e5b1e5dfb7a6 PASS. Now36native targets/44substantive turns/35primary+oneolddduplicate. PR46 exactknownKozhasovKummer2020preprint math/rootreproduction100%; SOURCE60closed81543/freshSOURCE315+self96861 finds mandatoryfalseinnerGitlogpostexit claim, retained adverseREQUIRES_SOURCE_CORRECTION. Distinct operativeV2/sourcefreshreview pending, no acceptance. PR47 original301+self +separate5 frozen16science/17pathdiff, nullprior vsABSENT{} and original1/5 vsnative0/5 gap documented; two independent mathfamilies active, both find universalnormal-H1vanishing route false in genuine SU2abelian Seifertfamily, repair required. No foreignprimary/cache/SQL/PDF/OCR/access bodies published; activefamilies excluded, no evidence deleted.\n'
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
 out=P/'checkpoints/CHECKPOINT_20261003_0441.json'
 with out.open('x')as f:json.dump({'schema':'ROOT_exact_completed_owned_checkpoint/v1','utc':utc,'actual_pid':os.getpid(),'main_before':head,'owned_files':rows,'foreign_dirty_before':before,'foreign_bodies_included':False,'active_families_included':False,'completed_count':35,'total':180,'completion_estimate_percent':35/180*100},f,indent=2);f.write('\n')
 add(out);assert git('rev-parse','HEAD').decode().strip()==head
 subprocess.run(['git','add','-f','--',*sorted(names)],cwd=R,check=True)
 staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0')if n};assert staged<=names
 for n in staged:assert git('show',':'+n)==(R/n).read_bytes()
 assert not staged&{z['path']for z in before}
 print(json.dumps({'status':'PASS_EXACT_COMPLETED_OWNED_CHECKPOINT_STAGED','pid':os.getpid(),'main_before':head,'owned':len(names),'staged':len(staged),'completed':35,'foreign_before':before,'foreign_after':foreign(),'foreign_staged':0,'completion_percent':35/180*100}))
if __name__=='__main__':main()
