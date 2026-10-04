from pathlib import Path
import datetime, hashlib, json, subprocess

P=Path(__file__).resolve().parent
D=P.parent/'snapshot/problems/11000151_artin_a5_quotient'
ROOT=Path('/Users/alec/Documents/Math')
TARGET='problems/11000151_artin_a5_quotient/'
HEAD='d977c9564f079cde975a7b4261776eb9061c5f5f'
BASE='efd29c05204703acca9a0860812f54b94fae54b1'
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_checks':[],
     'remote_receipt_blob_checks':[],'checkpoint_commit_checks':[],'head_file_checks':[]}
for name in ['TURN_1_MANIFEST.json','TURN_2_MANIFEST.json','TURN_3_MANIFEST.json','TURN_4_MANIFEST.json',
             'FINAL_AUTHOR_MANIFEST.json','review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
    mpath=D/name
    data=json.loads(mpath.read_text())
    folder=mpath.parent
    mismatches=[]
    for r in data['files']:
        b=(folder/r['path']).read_bytes()
        if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:
            mismatches.append(r['path'])
    out['manifest_checks'].append(dict(path=name,bound_files=len(data['files']),mismatches=mismatches))
for turn in range(1,4):
    m=json.loads((D/f'TURN_{turn}_REMOTE_RECEIPT.json').read_text())
    mismatches=[]
    commit_failures=[]
    for r in m['files']:
        b=(D/r['name']).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        if blob!=r['sha'] or len(b)!=r['size']:
            mismatches.append(r['name'])
        process=subprocess.run(['git','show',m['commit']+':'+TARGET+r['name']],cwd=ROOT,
                               stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if process.returncode or process.stdout!=b:
            commit_failures.append(dict(path=r['name'],returncode=process.returncode,
                                        stderr=process.stderr.decode(errors='replace')))
    out['remote_receipt_blob_checks'].append(dict(turn=turn,blob_files=len(m['files']),mismatches=mismatches))
    out['checkpoint_commit_checks'].append(dict(turn=turn,commit=m['commit'],failures=commit_failures))
for path in sorted(D.rglob('*')):
    if not path.is_file():continue
    name=path.relative_to(D).as_posix()
    process=subprocess.run(['git','show',HEAD+':'+TARGET+name],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out['head_file_checks'].append(dict(path=name,exact=process.returncode==0 and process.stdout==path.read_bytes(),
                                       returncode=process.returncode))
process=subprocess.run(['git','diff','--name-status',BASE,HEAD,'--'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(P/'frozen_diff_paths.stdout').write_bytes(process.stdout)
(P/'frozen_diff_paths.stderr').write_bytes(process.stderr)
out['diff_returncode']=process.returncode
process=subprocess.run(['git','show','--no-patch','--format=%H%n%P%n%aI%n%cI%n%s',HEAD],cwd=ROOT,
                       stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(P/'frozen_head_metadata.stdout').write_bytes(process.stdout)
(P/'frozen_head_metadata.stderr').write_bytes(process.stderr)
out['metadata_returncode']=process.returncode
out['all_pass']=not any(r['mismatches'] for r in out['manifest_checks']+out['remote_receipt_blob_checks']) and not any(r['failures'] for r in out['checkpoint_commit_checks']) and all(r['exact'] for r in out['head_file_checks']) and out['diff_returncode']==0 and out['metadata_returncode']==0
(P/'artifact_bindings.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
