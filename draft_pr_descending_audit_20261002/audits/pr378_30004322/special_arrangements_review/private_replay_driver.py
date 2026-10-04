from pathlib import Path
import shutil, subprocess, json, hashlib, datetime, sys
HERE=Path(__file__).resolve().parent
SNAP=HERE.parent/'snapshot'
manifest=json.loads((HERE.parent/'snapshot_manifest.json').read_text())
assert manifest['head']=='5da73632ab7a621de7b62edb5f70dfb8017e4a50'
verified=[]
for e in manifest['files']:
    p=SNAP/e['path']; b=p.read_bytes()
    assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
    verified.append(e['path'])
src=SNAP/'problems/30004322_arrangement_seshadri'
dst=HERE/'private_packet'
if dst.exists():shutil.rmtree(dst)
shutil.copytree(src,dst)
outdir=HERE/'private_replay_outputs';outdir.mkdir(exist_ok=True)
runs=[]
jobs=[(f'author_turn_{i}',[sys.executable,str(dst/f'check_turn_{i}.py')],dst,f'TURN_{i}_CHECKS.json') for i in range(1,6)]
jobs += [('author_wrapper',[sys.executable,str(dst/'REPLAY_ALL.py')],dst,None),('old_independent_93918',[sys.executable,str(dst/'review/independent_checks.py')],dst,'review/INDEPENDENT_CHECKS.json'),('old_review_wrapper',[sys.executable,str(dst/'review/verify_review.py'),'--author-dir',str(dst)],dst,None)]
for name,args,cwd,receipt in jobs:
    r=subprocess.run(args,cwd=cwd,capture_output=True)
    (outdir/f'{name}.stdout').write_bytes(r.stdout)
    (outdir/f'{name}.stderr').write_bytes(r.stderr)
    row={'name':name,'returncode':r.returncode,'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest()}
    if receipt:
        row['receipt_byte_exact']=r.stdout==(dst/receipt).read_bytes()
    runs.append(row);print(json.dumps(row),flush=True)
    assert r.returncode==0,name
    if receipt:assert row['receipt_byte_exact'],name
data={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'snapshot_head':manifest['head'],'snapshot_manifest_files_verified':len(verified),'private_packet':str(dst),'runs':runs,'sources_absent_from_private_public_copy':not(dst/'sources').exists(),'fresh_source_bytes_scope':'Separate own EMS/Pokora/HH-v1 fetches; does not silently change public source_files_checked=0.'}
(HERE/'private_replay_receipt.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2),flush=True)
