#!/usr/bin/env python3
"""Run exact frozen workers only from detached copies in family scratch."""
import os,sys
sys.dont_write_bytecode=True
from pathlib import Path
R=Path(__file__).resolve().parent;A=R.parents[1];S=R/'scratch/replays';S.mkdir(parents=True,exist_ok=True)
os.environ['TMPDIR']=str(S);os.environ['PYTHONDONTWRITEBYTECODE']='1'
import datetime,hashlib,json,shutil,subprocess
ENV=dict(os.environ);ENV.pop('PYTHONOPTIMIZE',None)
def need(v,m):
 if not v:raise RuntimeError(m)
def cp(src,dest):dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def invoke(p,flags,args=(),expected=0):
 x=subprocess.run([sys.executable,'-B',*flags,str(p),*args],cwd=S,env=ENV,text=True,capture_output=True,timeout=240)
 need(x.returncode==expected,'Unexpected replay '+str(p)+' '+str(flags)+' '+x.stderr[-2000:])
 try:out=json.loads(x.stdout)
 except json.JSONDecodeError:out=x.stdout
 return {'flags':flags,'returncode':x.returncode,'result':out,'stderr':x.stderr}
def main():
 # Current deployed8 and current coordinator, in exact operative relative layout.
 pub=S/'deployed/program/audits/pr1268_10900050/publication';pub.mkdir(parents=True,exist_ok=True)
 names=['prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py','zenodo-deposit.json']
 for n in names:cp(A/'publication'/n,pub/n)
 cp(A.parents[1]/'publication_coordinators/pr1268.py',pub.parents[2]/'publication_coordinators/pr1268.py')
 workflow=[invoke(pub/'workflow_regression.py',f,['--worker'])for f in [[],['-O'],['-OO']]]
 need(all(x['result']==workflow[0]['result']for x in workflow),'current workflow mode dependent')
 # Historical supplementary tooling is explicitly retained as old baseline.
 hist=S/'historical/program/audits/pr1268_10900050/reviews/workflow_tooling'
 for p in (A/'reviews/workflow_tooling').glob('*.py'):cp(p,hist/p.name)
 for p in (A/'submitted').iterdir():cp(p,hist.parents[1]/'submitted'/p.name)
 cp(A/'SUBMITTED_SNAPSHOT.json',hist.parents[1]/'SUBMITTED_SNAPSHOT.json')
 additional=[invoke(hist/'offline_fault_checks.py',f,['--worker'])for f in [[],['-O'],['-OO']]]
 edition=[invoke(hist/'edition_and_path_controls.py',f,['--worker'])for f in [[],['-O'],['-OO']]]
 # Mathematical diagnostics preserve actual original ten and Git authentication.
 math=S/'math';math.mkdir(exist_ok=True)
 for p in (A/'submitted').iterdir():cp(p,math/'submitted'/p.name)
 cp(A/'SUBMITTED_SNAPSHOT.json',math/'SUBMITTED_SNAPSHOT.json')
 candidate=math/'reviews/candidate_adversary/verify_candidate.py';cp(A/'reviews/candidate_adversary/verify_candidate.py',candidate)
 candidates=[]
 for f in [[],['-O'],['-OO']]:
  candidates.append({'positive':invoke(candidate,f),'negative':invoke(candidate,f,['--self-test-corruption'],1)})
 cp(A/'reconstruction_replay.py',math/'reconstruction_replay.py');cp(A/'reviews/reconstruction_adversary/audit_checks.py',math/'reviews/reconstruction_adversary/audit_checks.py')
 for p in (A/'reviews/source_question_family').iterdir():
  if p.is_file():cp(p,math/'reviews/source_question_family'/p.name)
 reconstruction=invoke(math/'reconstruction_replay.py',[],['--source',str(math/'reviews/source_question_family'),'--scratch',str(math/'reconstruction_work')])
 need(len(reconstruction['result']['negative_controls'])==18,'reconstruction mutant count')
 # Original exact checker needs actual repository prerequisites but writes nothing.
 cp(A/'root_exact_checks.py',math/'root_exact_checks.py')
 runner=math/'root_runner.py';runner.write_text("import sys\nsys.dont_write_bytecode=True\nimport importlib.util,json\nfrom pathlib import Path\np=Path(__file__).parent/'root_exact_checks.py'\ns=importlib.util.spec_from_file_location('r2_root_exact',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.REPO=Path('/Users/alec/Documents/Math');print(json.dumps(m.main()))\n")
 exact=[invoke(runner,f)for f in [[],['-O'],['-OO']]]
 need(all(x['result']==exact[0]['result']for x in exact),'exact checks mode dependent')
 save(R/'REPLAY_RECEIPT.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'current_deployed_workflow':workflow,'historical_supplementary_baseline':additional,'historical_edition_path_worker':edition,'candidate_actual_original_positive_negative':candidates,'reconstruction_corrected_entrypoint':reconstruction,'root_exact_current_outputs':exact,'scope':'Detached exact copies; synthetic compiler/service/Git fixture operations only for workflow tests. Original Git queries in mathematical authentication are read-only. No actual compiler/generator main targets actual input directories; historical supplementary postmerge checks are not substituted for current postmerge.'})
 print(json.dumps({'workflow_three_modes':'PASS','historical_workers_three_modes':'PASS','candidate_positive_negative_three_modes':'PASS','reconstruction_18_mutants':'PASS','root_exact_three_modes':'PASS'}))
if __name__=='__main__':main()
