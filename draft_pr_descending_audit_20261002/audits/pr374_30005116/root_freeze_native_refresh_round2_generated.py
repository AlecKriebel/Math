"""Freeze the actual normal branch refresh without rewriting the first certificate."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];I=A/'live_acceptance_inputs_round2';assert not I.exists();I.mkdir()
OLD='4afe89d1439e0d0d2a28a55f27709192cd56738e';MAIN='eb3c6dbe6a1d978e39c30518137264bdc69ec30b';HEAD='2bb07868e8fb5ac48cae8ec0b7f69aed02b36807';TREE='1464f6e71c9db2ab696db9e75373413267030156';Q='unsolved_math_prioritization/QUEUE.md'
sha=lambda b:hashlib.sha256(b).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=R)
assert git('branch','--show-current').strip()==b'main'
assert git('show','-s','--format=%P',HEAD).decode().strip().split()==[OLD,MAIN]
assert git('rev-parse',HEAD+'^{tree}').decode().strip()==TREE
original=json.loads((A/'snapshot_manifest.json').read_bytes());rows=original['files'];paths={r['path'] for r in rows};assert len(paths)==46
def treemap(commit):
    out={}
    for item in git('ls-tree','-r','-z',commit).split(b'\0'):
        if item:
            metadata,path=item.split(b'\t',1);out[path]=metadata
    return out
before=treemap(MAIN);after=treemap(HEAD);expected=dict(before)
for path in paths:expected[path.encode()]=after[path.encode()]
assert expected==after,'unrelated current-main path changed'
assert set(git('diff','--name-only',MAIN,HEAD).decode().splitlines())==paths
newrows=[]
for row in rows:
    path=row['path'];b=git('show',HEAD+':'+path)
    if path!=Q:assert b==(A/'snapshot'/path).read_bytes()==git('show',OLD+':'+path)
    p=I/'repaired_snapshot'/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    newrows.append({'path':path,'bytes':len(b),'sha256':sha(b),'git_blob_sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()})
oldqueue=git('show',MAIN+':'+Q);newqueue=git('show',HEAD+':'+Q);lines=oldqueue.splitlines(keepends=True);old=lines[410];cells=old.split(b'|')
assert cells[1].strip()==b'400' and b'| 30005116 / OWR-10252930-028 |' in old and cells[8]==b' queued ' and cells[9]==b' 0/5 '
cells[8]=b' unsolved ';cells[9]=b' 5/5 ';lines[410]=b'|'.join(cells);assert newqueue==b''.join(lines)
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest={'pr':374,'head':HEAD,'base':MAIN,'original_frozen_head':original['head'],'previous_reviewed_head':OLD,'frozen_utc':stamp,'files':newrows}
(A/'live_snapshot_manifest_round2.json').write_text(json.dumps(manifest,indent=2)+'\n');shutil.copyfile(A/'live_snapshot_manifest_round2.json',I/'repaired_snapshot_manifest.json')
shutil.copyfile(A/'snapshot_manifest.json',I/'snapshot_manifest.json');shutil.copytree(A/'snapshot',I/'snapshot')
receipt={'utc':stamp,'pr':374,'original_head':original['head'],'previous_reviewed_head':OLD,'repaired_head':HEAD,'current_main_parent':MAIN,'parents':[OLD,MAIN],'tree':TREE,'all_original_target_files_unchanged':45,'changed_queue_line':411,'changed_queue_pipe_cells':[8,9],'old_row':old.decode(),'new_row':lines[410].decode(),'all_other_queue_bytes_preserved':True,'every_other_current_main_path_and_mode_preserved':True,'normal_expected_head_update_branch_succeeded':True,'force_push':False,'raw_source_count':0,'initial_whole_manifest_preserved_sha256':sha((A/'clean_final_adversary/public/PUBLIC_MANIFEST.json').read_bytes())}
(A/'native_refresh_verification_round2.json').write_text(json.dumps(receipt,indent=2)+'\n');(I/'queue_repair_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
oldbody=(A/'accepted_pr_body.txt').read_text();start=oldbody.index('Original head:');end=oldbody.index('\n\nAI tools',start)
newbody=oldbody[:start]+f'''Original head: {original['head']}. Author checkpoint: e27668a5dd99e38705ec6a97d15710b7eb1b0f41. First queue-only refreshed head: 26df33899c95d860403ab311c568e0328bc87eeb, with parent ceada39994b1cd2c4935709143b53e2f7a581a45. After a persistent stale GitHub test-merge cache, the first normal expected-head update produced intermediate head {OLD}, with parents [26df33899c95d860403ab311c568e0328bc87eeb, 8e04757bff6e5c6c25d2dbf23ce10f736da8c5c8] and tree9b4c96e230fc3aecca24760e6804ea671d559ca4. Concurrent acceptance advanced main and its other queue rows. A second normal expected-head update merged current main {MAIN} into that reviewed head, producing final reviewed head {HEAD}, exact parents [{OLD}, {MAIN}] and full tree {TREE}. All 45 original mathematical/review/publication files remain byte-identical throughout. Against the current-main parent only this problem's queue status and turn count change; every other current-main path and queue byte is preserved. Historical pending-review statements and initial certificates remain frozen history, with the accepted disposition and additive final-head verification recorded in the descending audit.'''+oldbody[end:]
(A/'live_accepted_pr_body_round2.txt').write_text(newbody);(I/'accepted_pr_body.txt').write_text(newbody)
shutil.copyfile(A/'merge_body.txt',A/'live_merge_body_round2.txt');shutil.copyfile(A/'merge_body.txt',I/'merge_body.txt')
bindings={'utc':stamp,'head':HEAD,'previous_reviewed_head':OLD,'main_parent':MAIN,'tree':TREE,'body_sha256':sha(newbody.encode()),'merge_body_sha256':sha((I/'merge_body.txt').read_bytes()),'input_files_sha256':{name:sha((I/name).read_bytes()) for name in ['snapshot_manifest.json','repaired_snapshot_manifest.json','queue_repair_receipt.json','accepted_pr_body.txt','merge_body.txt']},'source_inputs_unchanged':True,'new_exact_body_not_yet_live':True,'new_additive_adversarial_gate_pending':True}
(A/'native_refresh_input_bindings_round2.json').write_text(json.dumps(bindings,indent=2)+'\n')
print(json.dumps(bindings,indent=2))
