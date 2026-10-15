from pathlib import Path
import subprocess,json,hashlib,datetime,os
C=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'); A=Path(__file__).resolve().parent
EXPECTED='cb8091dcfa69ed41defad72963836f5f8920648f';D=A/'checkpoint_package_20261005';D.mkdir(exist_ok=False);records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(c,m):
 if not c:raise RuntimeError(m)
def run(args):
 start=now();p=subprocess.Popen(args,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();i=len(records)
 (D/(str(i)+'.stdout.bin')).write_bytes(out);(D/(str(i)+'.stderr.bin')).write_bytes(err)
 records.append({'argv':args,'PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'stdout':{'file':str(i)+'.stdout.bin','bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},'stderr':{'file':str(i)+'.stderr.bin','bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}})
 (D/'PROCESS_JOURNAL.json').write_text(json.dumps({'actual_operator_PID':os.getpid(),'records':records},indent=2)+'\n');require(p.returncode==0,str(args)+': '+err.decode()[:500]);return out
def git(*a):return run(['git',*a])
require(git('symbolic-ref','--short','HEAD').strip()==b'main','not main');require(git('rev-parse','HEAD').strip().decode()==EXPECTED,'head changed');require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==EXPECTED,'remote changed');require(not git('diff','--cached','--name-only','-z'),'foreign staged')
files=[A/x for x in ['ROOT_AUTHENTICATE_MATH_FAMILIES_20261005.py','ROOT_MATHEMATICAL_GATE_20261005.json','ROOT_ADJUDICATE_PRIORITY_20261005.py','ROOT_PRIORITY_ADJUDICATION_20261005.json','RESEARCH_LOG.md','assemble_package.py','record_cli.py','checkpoint_package_20261005.py']]
for d,names in {'author_followup_priority_20261005':['AUTHOR_FOLLOWUP_PRIORITY_AUDIT.md','BOUNDED_VERDICT.json','READ_SCOPE_AND_CUSTODY_MANIFEST.json','FINAL_READBACK_ACTUAL.json','RESEARCH_LOG.md'], 'general_operator_priority_20261005':['REPORT.md','READ_SCOPE.md','FINAL_EVIDENCE_MANIFEST.json','EXACT_QUERY_INPUTS.json','SEARCH_LOG.md','RESEARCH_LOG.md'], 'exact_reproduction_adversary_20261005':['REPORT.md','ARTIFACT_MANIFEST.json','CHECKER_REPAIR_MANIFEST.json','CHECKER_REPAIR_RESULTS.json','minimal_public_verifier_repair.patch'], 'verification_package_preparation_20261005':['REPORT.md','PUBLIC_SUPPORT_FILE_MANIFEST.json','ADAPTATION_AUDIT.json','PREPARATION_RESULTS.json']}.items():
 files += [A/d/x for x in names]
Dpub=A/'publication_package_v1';files += list((Dpub/'publicfiles').rglob('*'));files=[x for x in files if x.is_file()]
files += [Dpub/'zenodo-deposit.json']
files += [Dpub/'private_notes'/x for x in ['RESEARCH_LOG.md','SOURCE_PREPARATION_CHECKPOINT.json','BUILTIN_COMPILER_DIAGNOSTIC.json','ROOT_VISUAL_QA.json','PUBLIC_PACKAGE_MANIFEST.json']]
files += list((Dpub/'private_notes/final_verification_run').rglob('*'));files=[x for x in files if x.is_file()]
files += [A.parent.parent/'CURRENT_PROGRESS.json']
for label in ['compile_pdf_final','verify_final','render_final','zenodo_local_check']:
 files += list((A/'actual_operations'/label).glob('*'))
files=sorted(set(files));require(all(x.is_file() and not x.is_symlink() for x in files),'nonregularselected')
paths=[str(x.relative_to(C)) for x in files];pins=[{'file':str(x.relative_to(C)),'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in files]
git('add','-f','--',*paths);staged=sorted(x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x);require(set(staged)<=set(paths) and staged,'staged scope')
git('commit','-m','Prepare PR91 mixed Koopman spectrum research note and verification package')
commit=git('rev-parse','HEAD').strip().decode();require(git('rev-parse',commit+'^').strip().decode()==EXPECTED,'parent');changed=sorted(x.decode() for x in git('diff-tree','--no-commit-id','--name-only','-r','-z',commit).split(b'\0') if x);require(changed==staged,'commitscope')
for row in pins:
 b=git('show',commit+':'+row['file']);require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'committedbody')
git('push','--force-with-lease=refs/heads/main:'+EXPECTED,'https://github.com/AlecKriebel/Math.git','HEAD:refs/heads/main');require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==commit,'remote readback');require(not git('diff','--cached','--name-only','-z'),'stagedremainder')
r={'schema':'pr91-pre-review-package-main-checkpoint/v1','UTC':now(),'actual_operator_PID':os.getpid(),'commit':commit,'parent':EXPECTED,'branch':'main','remote_verified':True,'selected_files':len(pins),'changed_files':len(changed),'pins':pins,'publication_clearance':False,'whole_package_rounds':0,'primary_checkout_mutated':False,'primary_synchronization_pending':True,'PR_workflow_percent':65,'completed_program':11,'dated_total':99}
(D/'RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='pins'}))
