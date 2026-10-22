from pathlib import Path
import datetime,hashlib,json,os,stat,shutil
R=Path(__file__).resolve().parent;P=R.parent/'operations06';O=R.parent/'operations'
D=R/'inputs';D.mkdir(exist_ok=False)
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
    s=p.stat();b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns}
inputs={}
def copy(p,n):
    q=D/n;q.parent.mkdir(parents=True,exist_ok=True);before=pin(p);q.write_bytes(p.read_bytes());need(sha(q.read_bytes())==before['sha256'],'Copy changed');need(q.stat().st_ino!=p.stat().st_ino,'Copied input shares inode');inputs[str(p)]={**before,'copy':str(q.relative_to(R))}
ms='4d491443d4be4d07ef9abb45c0ce6f9c56bf77c20dd7a2254ae43dce2638ab79';bs='e8c7f35bc6d60318146ae9794fe84c7c8a18e99e818a350bb78298fd85bd9852';whole='cde78679a06a8ec0954f9af1785cd339762a5cc57b3154661c3313706677852b'
need(sha((P/'MANIFEST.json').read_bytes())==whole,'Whole input manifest changed');manifest=json.loads((P/'MANIFEST.json').read_bytes());files={};dirs={}
for parent,ds,ns in os.walk(P,followlinks=False):
    for n in ds+ns:
        p=Path(parent)/n;s=p.lstat();rel=p.relative_to(P).as_posix();need(not p.is_symlink(),'Input symlink')
        if p.is_dir():dirs[rel]={'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns}
        elif p!=P/'MANIFEST.json':files[rel]=pin(p)
need(files==manifest['files'] and dirs==manifest['directories'],'Whole source/support recursive closure mismatch')
for p in P.iterdir():
    if p.is_file():copy(p,'operations06/'+p.name)
for p in (P/'source').iterdir():copy(p,'operations06/source/'+p.name)
need(sha((P/'source/SOURCE_MANIFEST.json').read_bytes())==ms and sha((P/'source/bootstrap06.py').read_bytes())==bs,'New source anchors changed')
freeze=json.loads((P/'source/SOURCE_FREEZE.json').read_bytes())
oldmanifest=(O/'OPERATIONS_MANIFEST.json').read_bytes();need(sha(oldmanifest)==freeze['prior_operations_manifest_sha256'],'Old source manifest changed')
old=json.loads(oldmanifest)
for name,wanted in old['files'].items():
    b=(O/name).read_bytes();need({'bytes':len(b),'sha256':sha(b)}==wanted,'Old pinned source changed '+name)
for p in O.iterdir():
    if p.is_file():copy(p,'operations/'+p.name)
for name,wanted in freeze['prior_runtime_files'].items():
    p=O/'runtime'/name;b=p.read_bytes();need({'bytes':len(b),'sha256':sha(b)}==wanted,'Runtime pin changed');copy(p,'preserved05_runtime/'+name)
need({p.name for p in (O/'runtime').iterdir()}==set(freeze['prior_runtime_files']),'Runtime closure changed')
for name,wanted in freeze['prior_wrapper_files'].items():
    p=R.parent/'stage_known_unattempted_resumption01'/name;b=p.read_bytes();need({'bytes':len(b),'sha256':sha(b)}==wanted,'Wrapper pin changed');copy(p,'wrapper01/'+name)
repo=O.parents[3]
for name,wanted in json.loads((O/'DEPENDENCY_PINS.json').read_bytes()).items():
    p=repo/name;b=p.read_bytes();need({'bytes':len(b),'sha256':sha(b)}==wanted,'Dependency changed');copy(p,name)
for name in ['PACKAGE_FREEZE_01.json','ROOT_SCIENTIFIC_CLEARANCE.json','ROOT_STAGE_RESUMPTION_REVIEW01_HOLD_ADOPTION.json','ROOT_OPERATIONS05_ACTION_HOLD_AFTER_NEW_COUNTEREXAMPLES.json','operations05_whole_review01/REPORT.md','operations05_whole_review01/ACTION_REVIEW.json','stage_resumption_review01/REPORT.md','stage_resumption_review01/ACTION_REVIEW.json']:
    copy(R.parent/name,'parent_context/'+name)
# Read/check only pinned current scientific closure; never replay historical custody archives.
ns={'__file__':str(O/'bootstrap.py'),'__name__':'verified_readonly'};b=(O/'bootstrap.py').read_bytes();need(sha(b)==freeze['prior_bootstrap_sha256'],'Old bootstrap changed');exec(compile(b,str(O/'bootstrap.py'),'exec'),ns)
load,_=ns['load_verified'](O,freeze['prior_operations_manifest_sha256'],freeze['prior_bootstrap_sha256'])
c=load('ops_common');pkg=c.package();proposal=c.proposal()
result={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','source_manifest_sha256':ms,'bootstrap_sha256':bs,'target_recursive_manifest_sha256':whole,'target_complete_file_count':len(files),'target_complete_directory_count':len(dirs),'old_public_payloads_rehashed':len(old['files']),'old_runtime_files_rehashed':len(freeze['prior_runtime_files']),'wrapper_files_rehashed':len(freeze['prior_wrapper_files']),'scientific_current_source_payloads_checked':len(pkg['source']),'flat_upload_kit_members_checked':len(pkg['flat']),'selected_original_files':len(c.ORIGINALS),'proposal_overlay_files_checked':len(proposal[1]),'historical49GB_custody_replayed':False,'new_live_service_queries':0,'production06_runtime_absent':not (P/'runtime').exists(),'old_clearance_original_absent':not (O/'runtime/ROOT_OPERATIONAL_CLEARANCE.json').exists(),'readiness':json.loads((P/'READINESS.json').read_bytes()),'copied_input_files':inputs,'overall_percent':80}
(R/'INPUT_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in {'copied_input_files','readiness'}},indent=2))
