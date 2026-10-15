"""Whole immutable package validation and isolated unchanged replays.
Every executable copy writes only below this family's ignored tmp.
No generator, Git mutation, canonical update, installation or outside contact.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib,json,shutil,subprocess,os,datetime
OWN=Path(__file__).resolve().parent
AUDIT=OWN.parent
REPO=OWN.parents[3]
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads((AUDIT/'reviewed_candidate/MANIFEST.json').read_text())
assert sha((AUDIT/'reviewed_candidate/MANIFEST.json').read_bytes())=='2bb662fe662ac51380e57ecb03a8b404591ba7761d7e57cd6f6dab7520ec2a69'
for row in manifest['files']:
 data=(AUDIT/'reviewed_candidate'/row['path']).read_bytes();assert len(data)==row['bytes'] and sha(data)==row['sha256']
deps=json.loads((AUDIT/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json').read_text())
for row in deps['supporting_first_party_files']:
 data=(REPO/row['path']).read_bytes();assert len(data)==row['bytes'] and sha(data)==row['sha256']

# Reproduce the original path topology in an isolated workspace. Read-only Git
# commands see the real object database via explicit environment references.
WORK=OWN/'tmp'/'replay_repo';workaudit=WORK/'draft_pr_publication_program_20260930/audits/pr27_30003713'
workaudit.mkdir(parents=True,exist_ok=True)
for name in ['snapshot_manifest.json','pr_input.json']:
 shutil.copyfile(AUDIT/name,workaudit/name)
for name in ['source_snapshot','reviewed_candidate']:
 shutil.copytree(AUDIT/name,workaudit/name,dirs_exist_ok=True)
for name,mname in [('character_family','artifact_manifest.json'),('homological_family','FIRST_PARTY_SHA256_MANIFEST.json'),('primary_scope_family','FIRST_PARTY_SHA256_MANIFEST.json')]:
 destination=workaudit/name;destination.mkdir(exist_ok=True)
 fm=json.loads((AUDIT/name/mname).read_text());rows=[{'path':p,**v} for p,v in fm['artifacts'].items()] if 'artifacts' in fm else fm['files']
 for row in rows+[{'path':mname}]:
  f=destination/row['path'];f.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(AUDIT/name/row['path'],f)
for name in ['root_powell_base_controls.py','root_powell_base_controls_failed_v1.py']:
 shutil.copyfile(AUDIT/name,workaudit/name)
q=WORK/'unsolved_math_prioritization';q.mkdir(exist_ok=True)
shutil.copyfile(REPO/'unsolved_math_prioritization/manifest.json',q/'manifest.json')
if not (q/'cache').exists():(q/'cache').symlink_to(REPO/'unsolved_math_prioritization/cache',target_is_directory=True)
ENV=os.environ.copy();ENV.update({'GIT_DIR':str(REPO/'.git'),'GIT_WORK_TREE':str(WORK)})
PY='/usr/bin/python3'
# Manifest checks precede expected receipt rewrites in the copied tree.
pre=[]
for family,program,args in [('character_family','verify_artifact_manifest.py',[]),('homological_family','make_manifest.py',['--check'])]:
 r=subprocess.run([PY,str(workaudit/family/program)]+args,cwd=WORK,env=ENV,capture_output=True,text=True)
 assert r.returncode==0;rout=r.stdout;pre.append({'family':family,'exit':r.returncode,'stdout':rout})

jobs=[('original_author',workaudit/'source_snapshot/verify.py',workaudit/'source_snapshot/verification.json',AUDIT/'source_snapshot/verification.json',[]),('original_reviewer',workaudit/'source_snapshot/review/independent_checks.py',workaudit/'source_snapshot/review/independent_results.json',AUDIT/'source_snapshot/review/independent_results.json',[]),('current_author',workaudit/'reviewed_candidate/verify.py',workaudit/'reviewed_candidate/verification.json',AUDIT/'reviewed_candidate/verification.json',[]),('current_reviewer',workaudit/'reviewed_candidate/review/independent_checks.py',workaudit/'reviewed_candidate/review/independent_results.json',AUDIT/'reviewed_candidate/review/independent_results.json',[]),('character_family',workaudit/'character_family/character_controls.py',workaudit/'character_family/character_results.json',AUDIT/'character_family/character_results.json',['timestamp_utc','python']),('homological_family',workaudit/'homological_family/exact_ce_controls.py',workaudit/'homological_family/NEW_EXACT_CE_RECEIPT.json',AUDIT/'homological_family/NEW_EXACT_CE_RECEIPT.json',['utc']),('primary_scope_family',workaudit/'primary_scope_family/independent_source_type_controls.py',workaudit/'primary_scope_family/independent_source_type_results.json',AUDIT/'primary_scope_family/independent_source_type_results.json',[]),('root_powell_base',workaudit/'root_powell_base_controls.py',workaudit/'root_powell_base_results.json',AUDIT/'root_powell_base_results.json',[])]

def run(job):
 name,script,receipt,expected,volatile=job
 result=subprocess.run([PY,str(script)],cwd=script.parent,env=ENV,capture_output=True,text=True,timeout=600)
 log=OWN/'tmp'/(name+'.log');log.write_text(result.stdout+'\n'+result.stderr)
 assert result.returncode==0,(name,result.stderr)
 assert script.read_bytes()==(AUDIT/script.relative_to(workaudit)).read_bytes()
 fresh=receipt.read_bytes();old=expected.read_bytes();f=json.loads(fresh);o=json.loads(old)
 for key in volatile:f.pop(key,None);o.pop(key,None)
 assert f==o,(name,'receipt semantic mismatch')
 return {'name':name,'exit_code':result.returncode,'script_sha256':sha(script.read_bytes()),'fresh_receipt_sha256':sha(fresh),'historical_receipt_sha256':sha(old),'byte_equal':fresh==old,'mathematical_fields_equal':f==o,'excluded_volatile_fields':volatile,'log_sha256':sha(log.read_bytes()),'fresh_receipt_ignored_path':str(receipt.relative_to(OWN))}
rows=[]
with ThreadPoolExecutor(max_workers=4) as pool:
 futures=[pool.submit(run,j) for j in jobs]
 for f in as_completed(futures):
  row=f.result();rows.append(row);print('reproduced',row['name'],flush=True)
# Re-run utility provenance code unchanged under matching isolated topology.
for name,script in [('primary_provenance',workaudit/'primary_scope_family/reproduce_provenance_checks.py'),('homological_packet_provenance',workaudit/'homological_family/audit_packet.py')]:
 result=subprocess.run([PY,str(script)],cwd=WORK,env=ENV,capture_output=True,text=True,timeout=600)
 assert result.returncode==0,(name,result.stderr)
 (OWN/'tmp'/(name+'.log')).write_text(result.stdout+'\n'+result.stderr)
 rows.append({'name':name,'exit_code':0,'script_sha256':sha(script.read_bytes()),'stdout_sha256':sha(result.stdout.encode()),'isolated_topology':True,'only_readonly_git_and_SQLite_operations':True})
 if name=='primary_provenance':(OWN/'FRESH_PROVENANCE_RECEIPT.json').write_text(result.stdout)
# Expected historical failure must remain a failed harness and produce no receipt.
failed=OWN/'tmp'/'failed_root_replay';failed.mkdir(exist_ok=True)
shutil.copyfile(AUDIT/'root_powell_base_controls_failed_v1.py',failed/'root_powell_base_controls_failed_v1.py')
r=subprocess.run([PY,str(failed/'root_powell_base_controls_failed_v1.py')],cwd=failed,capture_output=True,text=True)
assert r.returncode!=0 and 'AttributeError' in r.stderr and not (failed/'root_powell_base_results.json').exists()
(OWN/'tmp/root_failed_v1.log').write_text(r.stdout+'\n'+r.stderr)
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_REPRODUCTION','runtime':PY,'sympy_version':'1.14.0','pre_replay_manifest_checks':pre,'runs':rows,'preserved_failed_root_v1':{'exit_code':r.returncode,'expected_Expr_rem_AttributeError':True,'no_mathematical_receipt':True},'all_original_and_current_receipts_byte_exact':all(r['byte_equal'] for r in rows if r['name'].startswith(('original_','current_'))),'new_substantive_attempts':0,'scope':'Exact existing computations and provenance only; prior PASS labels are not evidence. Future merge/canonical/publication bytes not blessed.'}
(OWN/'REPRODUCTION_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'runs':len(rows),'old_current_exact':out['all_original_and_current_receipts_byte_exact']},indent=2))
