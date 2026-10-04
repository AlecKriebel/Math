#!/usr/bin/env python3
"""Finish assessment of completed streams; do not rerun or relabel old runs."""
from pathlib import Path
import hashlib,json,re,stat,subprocess
N=Path(__file__).resolve().parent;R=N/'bound_replay_receipts';P=N/'archive_replay'
sha=lambda b:hashlib.sha256(b).hexdigest()
records=[]
assert (N/'replay_packet_bound.failed_v01.py').read_bytes()==(N/'replay_packet_bound.py').read_bytes()
for receipt in sorted(R.glob('*.json')):
    r=json.loads(receipt.read_bytes());label=r['label']
    assert r['state']=='completed' and r['actual_exit']==r['expected_exit'],label
    script=Path(r['executed_body']);assert sha(script.read_bytes())==r['executed_body_sha256_before']==r['executed_body_sha256_after']
    assert sha((N/'replay_packet_bound.failed_v01.py').read_bytes())==r['runner_body_sha256']
    out=(R/r['stdout_file']).read_bytes();err=(R/r['stderr_file']).read_bytes()
    assert len(out)==r['stdout_bytes'] and sha(out)==r['stdout_sha256']
    assert len(err)==r['stderr_bytes'] and sha(err)==r['stderr_sha256']
    if label.startswith('optimization_guard_'):
        assert not out and err==b'Verification refuses Python optimization (-O/-OO).\n'
    elif label.startswith(('positive_','mutant_')):
        assert not err
        name=label[len('positive_'):] if label.startswith('positive_') else label
        if name.startswith('geometry'):
            lines=[]
            for line in out.decode().splitlines():
                if re.fullmatch(r'native_utc(?:_start|_end)? \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00',line):continue
                line=re.sub(r' native_utc \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00$','',line)
                lines.append(line)
            assert ('\n'.join(lines)+'\n').encode()==(P/'expected'/(name+'.txt')).read_bytes()
        else:
            actual=json.loads(out)
            if name=='division_chord':del actual['interpreter']
            assert actual==json.loads((P/'expected'/(name+'.json')).read_bytes())
        assert r['complete_mathematical_output_equal'] is True
    else:
        assert not err;v=json.loads(out)
        if label=='public_priority_verify':assert v['result']=='PASS' and v['exact_comparisons']==25
        else:assert v['status']=='PASS' and v['all_bodies_modes_inventory_unchanged'] is True
    records.append(r)
assert len(records)==29,len(records)
manifest=json.loads((P/'MANIFEST.json').read_bytes());files={};dirs={}
for p in sorted(P.rglob('*')):
    assert not p.is_symlink()
    rel=str(p.relative_to(P));mode=format(stat.S_IMODE(p.stat().st_mode),'04o')
    if p.is_file():
        b=p.read_bytes();files[rel]={'bytes':len(b),'sha256':sha(b),'mode':mode}
    elif p.is_dir():dirs[rel]=mode
assert set(files)==set(manifest['files'])|{'MANIFEST.json'}
assert {k:v for k,v in files.items() if k!='MANIFEST.json'}==manifest['files']
assert dirs==manifest['directory_modes']
utc=subprocess.run(['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ'],capture_output=True,check=True).stdout.decode().strip()
summary={'status':'PASS','assessment_utc':utc,'positive_programs':11,'negative_mutants':4,'optimization_guards':11,
         'shipped_full_and_stdlib_arithmetic_replay':True,'public_priority_replay':True,
         'all_archive_bodies_modes_directories_unchanged':True,
         'failed_assessor_preserved':'replay_packet_bound.failed_v01.py',
         'failure_boundary':'All 29 child executions completed with their required exits; original assessor then failed on the public priority output field name (result, not status). This assessment validates the original complete streams at its own contemporary clock, not a backdated rerun.',
         'receipts':records}
(N/'BOUND_PACKET_REPLAY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='receipts'},indent=2))
