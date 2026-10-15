"""Audit runner: copies exact source to private fixtures; never edits snapshot."""
from pathlib import Path
import json,hashlib,subprocess,shutil,sys,datetime,ast
case=Path(__file__).resolve().parents[2]
source=case/'source_snapshot/unsolved_math_prioritization/attempts/6800014'
private=case/'private_sources/algebra_reproduction'
python=private/'venv/bin/python'
receipt=json.loads((case/'SOURCE_RECEIPT.json').read_text())
def hashes(p):
 d=p.read_bytes(); return len(d),hashlib.sha256(d).hexdigest(),hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()
inventory=[]
for e in receipt['files']:
 p=case/e['local_path']; size,sha,blob=hashes(p)
 inventory.append({'path':p.relative_to(source).as_posix(),'size':size,'sha256':sha,'blob_sha1':blob,'receipt_match':(size==e['size'] and sha==e['sha256'] and blob==e['blob_sha'])})
if len(inventory)!=19 or not all(e['receipt_match'] for e in inventory):raise RuntimeError('source inventory mismatch')
manifest=json.loads((source/'PUBLICATION_MANIFEST.json').read_text())
for e in manifest['files_except_this_manifest']:
 size,sha,blob=hashes(source/e['path'])
 if (size,sha,blob)!=(e['bytes'],e['sha256'],e['git_blob_sha1']):raise RuntimeError('publication manifest mismatch')
frozen=json.loads((source/'FROZEN_AUTHOR_HASHES.json').read_text())
for e in frozen['publication_allowed_files']:
 size,sha,blob=hashes(source/'frozen_author'/e['path'])
 if (size,sha)!=(e['bytes'],e['sha256']):raise RuntimeError('frozen manifest mismatch')
paths=['verify.py','check_hessian.py','audit/independent_checks.py','frozen_author/verify.py','frozen_author/check_hessian.py']
trust=[]
for rel in paths:
 tree=ast.parse((source/rel).read_text())
 trust.append({'path':rel,'assert_count':sum(isinstance(n,ast.Assert) for n in ast.walk(tree)),'uses_explicit_raise':any(isinstance(n,ast.Raise) for n in ast.walk(tree))})
fixtures=private/'fixtures'; fixtures.mkdir(exist_ok=True)
runs=[]
def fixture(name):
 root=fixtures/name
 if root.exists():shutil.rmtree(root)
 shutil.copytree(source,root)
 return root
def run(root,rel,opt=False,cwd_kind='publication',scenario='baseline'):
 cwd=root if cwd_kind=='publication' else private
 cmd=[str(python)]+(['-O'] if opt else [])+[str(root/rel)]
 p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,timeout=60)
 tag=f'{scenario}__{rel.replace("/","__")}__{"optimized" if opt else "normal"}__{cwd_kind}'
 log=private/(tag+'.txt')
 log.write_text(json.dumps({'command':cmd,'cwd':str(cwd),'returncode':p.returncode},indent=2)+'\nSTDOUT\n'+p.stdout+'\nSTDERR\n'+p.stderr)
 row={'scenario':scenario,'path':rel,'optimized':opt,'cwd':cwd_kind,'returncode':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest(),'printed_pass_or_verified':('PASS' in p.stdout or 'verified exactly' in p.stdout),'raw_output_private':log.relative_to(case).as_posix()}
 runs.append(row)
base=fixture('baseline')
for rel in paths:
 for opt in [False,True]:
  for cwd in ['publication','foreign']:run(base,rel,opt,cwd)
# False algebra assertions: exact scripts continue printing success under -O.
mutations={
 'verify.py':('assert norm2(S(A)) == u**2 / 2','assert norm2(S(A)) == u**2 / 2 + 1'),
 'check_hessian.py':('assert sp.factor(Rdd-expected)==0','assert sp.factor(Rdd-expected)==1'),
 'audit/independent_checks.py':('assert zero(Ric-expected)','assert zero(Ric-expected+sp.eye(5))'),
 'frozen_author/verify.py':('assert norm2(S(A)) == u**2 / 2','assert norm2(S(A)) == u**2 / 2 + 1'),
 'frozen_author/check_hessian.py':('assert sp.factor(Rdd-expected)==0','assert sp.factor(Rdd-expected)==1')}
for idx,(rel,(old,new)) in enumerate(mutations.items()):
 f=fixture('false_identity_'+str(idx)); text=(f/rel).read_text()
 if old not in text:raise RuntimeError('control anchor')
 (f/rel).write_text(text.replace(old,new,1))
 for opt in [False,True]:run(f,rel,opt,scenario='false_algebra_identity')
# All five scripts can pass a false current-proof range: current prose isn't bound by scripts.
f=fixture('false_current_prose')
p=f/'attempts/turn02_slice_proof.md';text=p.read_text()
old='Fix `u₀` with `0<u₀<1/2`.'
if old not in text:raise RuntimeError('prose control anchor')
p.write_text(text.replace(old,'Fix `u₀` with `0<u₀<2`.',1))
for rel in paths:run(f,rel,scenario='false_current_prose_range')
# Frozen bytes tampering is caught by audit only in normal execution.
f=fixture('false_frozen_bytes');p=f/'frozen_author/attempts/turn02_slice_proof.md';p.write_text(p.read_text()+'\nTampered fixture bytes.\n')
for opt in [False,True]:run(f,'audit/independent_checks.py',opt,scenario='frozen_bytes_tamper')
# Publication manifest is not read by any checker.
f=fixture('false_publication_manifest');p=f/'PUBLICATION_MANIFEST.json';m=json.loads(p.read_text());m['claim']='F is 2/3 for every u>0';m['files_except_this_manifest'][0]['sha256']='0'*64;p.write_text(json.dumps(m))
for rel in paths:run(f,rel,scenario='false_publication_manifest')
result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'inventory':inventory,'publication_entries_checked':len(manifest['files_except_this_manifest']),'frozen_entries_checked':len(frozen['publication_allowed_files']),'checker_assertions':trust,'runs':runs,'source_snapshot_unchanged':all(hashes(case/e['local_path'])==(e['size'],e['sha256'],e['blob_sha']) for e in receipt['files'])}
(case/'reviews/algebra_reproduction/REPRODUCTION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'runs':len(runs),'baseline_all_exit_zero':all(r['returncode']==0 for r in runs if r['scenario']=='baseline'),'false_identity_normal_all_fail':all(r['returncode']!=0 for r in runs if r['scenario']=='false_algebra_identity' and not r['optimized']),'false_identity_optimized_all_exit_zero':all(r['returncode']==0 for r in runs if r['scenario']=='false_algebra_identity' and r['optimized']),'false_prose_all_exit_zero':all(r['returncode']==0 for r in runs if r['scenario']=='false_current_prose_range'),'false_manifest_all_exit_zero':all(r['returncode']==0 for r in runs if r['scenario']=='false_publication_manifest'),'frozen_tamper':[(r['optimized'],r['returncode']) for r in runs if r['scenario']=='frozen_bytes_tamper'],'source_snapshot_unchanged':result['source_snapshot_unchanged']},indent=2))
