"""Authenticate a closed independent priority corpus without modifying it."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat
A=Path(__file__).resolve().parent
D=A/'priority_general_20261004'
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
    assert p.is_file() and not p.is_symlink(),p
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':sha(b),'mode':oct(stat.S_IMODE(p.stat().st_mode))}
seal=D/'SOURCE_SEAL.json'
assert pin(seal)['sha256']=='e9d4efbfa9ed162b24c67daad595cf2e7b2052c424d61057fc9ec706199a7c2c'
j=json.loads(seal.read_bytes())
assert j['criteria_sha256']=='1a24fc1a7e5729bb0750ae68f1ff7c5d4b30fc99c74462f1771cfaca361cafb6'
assert (D/'SOURCE_SEAL.sha256').read_text().split()[0]==pin(seal)['sha256']
expected={}
for e in j['files']:
    p=Path(e['path'])
    assert not p.is_absolute() and '..' not in p.parts and str(p) not in expected
    assert pin(D/p)=={k:e[k] for k in ['bytes','sha256','mode']},p
    expected[str(p)]=e
actual={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file()}
assert actual==set(expected)|set(j['excluded_self_reference'])
assert all(not p.is_symlink() for p in D.rglob('*'))
dirs={'.':oct(stat.S_IMODE(D.stat().st_mode))}
dirs.update({str(p.relative_to(D)):oct(stat.S_IMODE(p.stat().st_mode)) for p in D.rglob('*') if p.is_dir()})
assert dirs=={e['path']:e['mode'] for e in j['directories']}
records=[]
for q in sorted((D/'custody').glob('*.json')):
    o=json.loads(q.read_bytes())
    for v in o if isinstance(o,list) else [o]:
        if 'argv' not in v:continue
        assert v['cwd']==str(D) and v['exit_code']==0
        assert datetime.fromisoformat(v['start_utc'].replace('Z','+00:00'))<=datetime.fromisoformat(v['end_utc'].replace('Z','+00:00'))
        for k in ['stdout','stderr']:
            p=Path(v[k+'_file']);assert p.is_relative_to(D)
            assert pin(p)['sha256']==v[k+'_sha256']
        if 'artifact' in v:
            p=Path(v['artifact']);assert p.is_relative_to(D)
            assert {k:pin(p)[k] for k in ['bytes','sha256','mode']}=={k:v[k] for k in ['bytes','sha256','mode']}
        records.append(v)
assert len(records)==j['native_operation_records']==68
assert sum('requested_url' in v for v in records)==j['native_retrieval_records']==36
assert len({v['artifact'] for v in records if 'artifact' in v})==j['distinct_native_source_artifacts']==66
assert pin(D/'CRITERIA_FREEZE.md')['sha256']==j['criteria_sha256']
prior=json.loads((A/'ROOT_PRIORITY_CRITERIA_CUSTODY.json').read_bytes())
assert j['criteria_sha256'] in json.dumps(prior)
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_CLOSED_GENERAL_PRIORITY_CORPUS_CUSTODY',
     'closed_utc':j['closed_utc'],'seal':pin(seal),'checksum_envelope':pin(D/'SOURCE_SEAL.sha256'),
     'payload_files':len(expected),'directory_modes':dirs,'native_operation_records':len(records),
     'native_retrieval_records':36,'distinct_source_artifacts':66,
     'all_payload_bytes_modes_and_full_native_streams_read_and_authenticated':True,
     'read_permissions_qualification':'Measured files0600 and directories0700. Closure is an explicit no-more-writes commitment, not filesystem write protection.',
     'reports_root_read_in_full':['FULL_PRIORITY_REPORT.md','DERIVATIONS.md','SOURCE_READ_LEDGER.md','SELF_REVIEW.md','STOP_WRITING.md'],
     'decisive_root_primary_read_scope':['Querret printed283–284 facsimiles and whole extracted article; Fierobe v5 real setup and full Lemma4.1 proof',
     'Akopyan–Schwartz–Tabachnikov Theorem3 and full section7 proof','Bialy–Tabachnikov Theorem4.1, Lemma4.2 and beginning of Theorem4.3 proof',
     'Khare–Lakshminarayan–Sukhatme local master identities section4.1 equations39–42 and full type-I proof'],
     'fresh_check_bridges_reproduction_pending':True,'integrated_priority_acceptance':False,'publishing_clearance':False}
(A/'ROOT_PRIORITY_GENERAL_CUSTODY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
