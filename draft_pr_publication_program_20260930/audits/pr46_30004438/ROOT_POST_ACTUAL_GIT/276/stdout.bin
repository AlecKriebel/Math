from pathlib import Path
import datetime
import hashlib
import json
import os
import stat

root=Path(__file__).resolve().parent
audit=root.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
prep=audit/'ORIGINAL_PREPARATION_MANIFEST.json'
assert sha(prep)=='da37655e9b3bab420862a0c17c761e67fa9a4bc2028a328d033547249c54ad2e'
preparation=json.loads(prep.read_text())
assert len(preparation['files'])==318
for item in preparation['files']:
    p=audit/item['path']
    assert sha(p)==item['sha256'],item['path']
    assert p.stat().st_size==item['bytes'],item['path']
    assert stat.S_IMODE(p.stat().st_mode)==item['full_mode'],item['path']
snapshot=json.loads((audit/'snapshot_manifest.json').read_text())
assert snapshot['head']=='a39d178b10f75fb127058b08e0d0002b3ae97f8a'
assert len(snapshot['files'])==13
for item in snapshot['files']:
    p=audit/'source_snapshot'/item['relative_path']
    assert sha(p)==item['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
assert json.loads((root/'run_completion.json').read_text())['returncode']==0
assert len(json.loads((root/'run_stdout.json').read_text())['checks'])==15
for selection,receipt in [('author','verification.json'),('prior_review','independent_results.json')]:
    capture=root/('original_'+selection+'_capture')
    completion=json.loads((capture/'COMPLETION.json').read_text())
    assert completion['returncode']==0
    pre=json.loads((capture/'PRELAUNCH.json').read_text())
    assert pre['operator_source_sha256']==sha(root/'replay_original_controls.py')
    assert completion['frozen_control_source_sha256_after']==pre['frozen_control_source_sha256']
    assert completion['stdout_sha256']==sha(capture/'stdout.txt')
    assert completion['stderr_sha256']==sha(capture/'stderr.txt')
    result=json.loads((root/('replay_'+selection)/receipt).read_text())
    assert result['passed']==(51 if selection=='author' else 848) and result['failed']==0
    original=(audit/'source_snapshot'/('' if selection=='author' else 'independent_review')/receipt)
    assert (root/('replay_'+selection)/receipt).read_bytes()==original.read_bytes()
assert json.loads((root/'failed01_run_completion.json').read_text())['returncode']==1
assert sha(root/'independent_checks_failed01.py')==json.loads((root/'failed01_run_prelaunch.json').read_text())['source_sha256']
verdict=json.loads((root/'verdict.json').read_text())
assert verdict['acceptance_approval'] is None
assert verdict['mathematical_gap_remaining'] is None
assert verdict['new_substantive_turns']==0
log=root/'research_log.md'
with log.open('a') as stream:
    stream.write(f'\n{utc} — Exact closure validated original 13 scientific hashes/modes, all 318 preparation bindings, successful 15-case independent controls, both exact source replays, and the preserved failed run. No mathematical gap for the scoped target; no acceptance approval. Completion toward this family’s audit: 100%. Owned files are sealed 0444; the closing actual capture is completed and sealed by its operator afterward.\n')
exclude={'FAMILY_MANIFEST.json','closure_actual_capture/PRELAUNCH.json',
         'closure_actual_capture/LAUNCHED.json','closure_actual_capture/stdout.txt',
         'closure_actual_capture/stderr.txt','closure_actual_capture/COMPLETION.json'}
files=[]
for p in sorted(root.rglob('*')):
    if not p.is_file() or p.relative_to(root).as_posix() in exclude:continue
    assert not p.is_symlink()
    p.chmod(0o444)
    files.append({'path':p.relative_to(root).as_posix(),'sha256':sha(p),
                  'bytes':p.stat().st_size,'full_mode':stat.S_IMODE(p.stat().st_mode)})
manifest={'schema':'pr46-projective-algebra-family-self-only-manifest/v1',
          'created_utc':utc,'actual_pid':os.getpid(),'head':snapshot['head'],
          'preparation_manifest_sha256':sha(prep),'preparation_files_bound':318,
          'scientific_files_bound':13,'files_count':len(files),'files':files,
          'authorship_root':str(root),'foreign_source_bodies_in_authorship':False,
          'acceptance_approval':None,'new_substantive_turns':0,
          'self_excluded':sorted(exclude),
          'separately_completed_actual_capture':'closure_actual_capture',
          'completion_estimate_percent':100}
target=root/'FAMILY_MANIFEST.json'
target.write_text(json.dumps(manifest,indent=2)+'\n')
target.chmod(0o444)
print(json.dumps({'closed_utc':utc,'pid':os.getpid(),'owned_files_bound':len(files),
                  'manifest_sha256':sha(target),'original_preparation_bindings_passed':318,
                  'original_scientific_files_passed':13,'math_verdict':verdict['verdict'],
                  'acceptance_approval':None},indent=2))
