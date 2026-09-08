#!/usr/bin/env python3
"""Fresh nonmutating historical-route and portable-baseline controls."""
import hashlib,json,shutil
from audit_driver import HERE,SOURCE,SCRATCH,LOGS,ENV,run,verify_manifest

def tree(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
def fresh(name,source=SOURCE):
    dst=SCRATCH/name
    if dst.exists():shutil.rmtree(dst)
    shutil.copytree(source,dst)
    return dst
results=[]
d=fresh('negative_preflight');(d/'release/replay.log').write_text('ARCHIVED_SUCCESS_SENTINEL\n');before=tree(d)
e=ENV.copy();e['FROZEN_BASE']=str(SCRATCH/'absent_archives')
status=run('historical_lineage_unavailable',['bash','release/one_command_replay.sh'],d,expected=2,env=e)
assert status==2 and tree(d)==before
assert (LOGS/'historical_lineage_unavailable.log').read_text().count('MISSING ')==5
results.append(dict(name='historical_lineage_unavailable',status=status,missing_archives=5,entire_tree_unchanged=True,archived_success_log_sentinel_unchanged=True,full_historical_replay_completed=False))
e=ENV.copy();e['TOOLCHAIN_LOCK_FILE']=str(SCRATCH/'invalid_toolchain.lock')
(SCRATCH/'invalid_toolchain.lock').write_text((SOURCE/'environment/texlive-2022.04.lock.txt').read_text().replace('pdfTeX','INVALID-pdfTeX',1))
status=run('refresh_wrong_toolchain',['bash','release/refresh_packages.sh'],d,expected=2,env=e)
assert status==2 and tree(d)==before
results.append(dict(name='refresh_wrong_toolchain',status=status,entire_tree_unchanged=True))
for forged_self_manifest in [False,True]:
    name='portable_forged_self_manifest' if forged_self_manifest else 'portable_baseline_mutation'
    d=fresh('negative_'+name,SOURCE/'public/repository')
    f=d/'data/current_profile_exact.json';f.write_text(f.read_text()+'\n')
    if forged_self_manifest:
        (d/'verification_outputs/replay_self_consistency_manifest.txt').write_text(hashlib.sha256(f.read_bytes()).hexdigest()+'  ./data/current_profile_exact.json\n')
    before=tree(d)
    status=run(name,['bash','replay.sh'],d,expected=1)
    assert status==1 and tree(d)==before
    results.append(dict(name=name,status=status,entire_tree_unchanged=True))
portable=SCRATCH/'portable'
assert (portable/'sha256_manifest.txt').read_bytes()==(SOURCE/'public/repository/sha256_manifest.txt').read_bytes()
count=verify_manifest(portable,'verification_outputs/replay_self_consistency_manifest.txt')
results.append(dict(name='fresh_full_portable_replay',downloaded_baseline_unchanged=True,replay_self_manifest_verified_entries=count))
(HERE/'PREFLIGHT_CONTROLS.json').write_text(json.dumps(results,indent=2)+'\n')
print('PREFLIGHT_CONTROLS_PASS')
