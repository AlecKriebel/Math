"""Authenticate actual scientific inputs; no scientific program is executed."""
from pathlib import Path
import hashlib, json, stat
from datetime import datetime, timezone

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
B=P/'papers/23204212'
sha=lambda x:hashlib.sha256(x).hexdigest()
packets=[
 ('sources','SOURCE_MANIFEST.json','SOURCE_FINAL.json','afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be','b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5',55,14),
 ('reviews/root-initial-20261117','INITIAL_MANIFEST.json','INITIAL_SEAL.json','6d7391ebdb60c59b7b622c6fbd5a60c320f2c22bf8fc49ee02908e05d187537e','3abdabfd35529755468a8f489afbee537b3b82d26b8743434f69a9878b5e5993',21,0),
 ('reviews/adversarial-continuation-20261117','FINAL_MANIFEST.json','FINAL_SEAL.json','7f98849c904df24dffdb92f021670d68fd54f110c8801e5b01a4cb8084efd7c2','34944d317839028bd74a10d292a0a9cda4570573475887ff120fdd8a496db355',224,3),
 ('reviews/scope-continuation-20261117','FINAL_MANIFEST.json','FINAL_SEAL.json','2f248eee505141f2e0d99c3a38a3bd613057b5de2741ba7581abbe534bcdb84e','d71455da2997c8af23ebdf92986b9a1891654e8d71d750b25dbde7d92910b807',191,16),
]
results=[]
for rel,mn,sn,mh,sh,nf,nd in packets:
    base=B/rel
    assert sha((base/mn).read_bytes())==mh
    assert sha((base/sn).read_bytes())==sh
    m=json.loads((base/mn).read_bytes())
    rows=m.get('entries',m.get('payload'))
    if rows is None:
        rows=[dict(x,kind='file') for x in m['payload_files']]
        rows += [dict(x,kind='directory') for x in m['directories']]
        if not any(x['path']=='.' for x in rows):
            rows.append({'path':'.','kind':'directory','mode':m['root_mode']})
        rows += [dict(x,kind='file') for x in m['terminal_control_files']]
    declared={x['path']:x for x in rows}
    actual={'.':base}
    actual.update({f.relative_to(base).as_posix():f for f in base.rglob('*')})
    assert not any(x.is_symlink() for x in actual.values())
    assert set(actual)==set(declared)|{mn,sn}, rel
    assert sum(f.is_file() for f in actual.values())==nf
    assert sum(f.is_dir() for f in actual.values())==nd+1
    for name,f in actual.items():
        if name not in declared:
            mode=m.get('terminal_modes',{}).get(name,'0o644')
            assert stat.S_IMODE(f.stat().st_mode)==int(mode,8)
            continue
        r=declared[name]
        assert f.is_dir()==(r['kind']=='directory'),f
        assert stat.S_IMODE(f.stat().st_mode)==int(r.get('mode',r.get('mode_octal')),8),f
        if f.is_file():
            b=f.read_bytes()
            if 'bytes' in r:assert len(b)==r['bytes'],f
            h=r.get('SHA256',r.get('sha256'))
            if h is not None:assert sha(b)==h,f
            elif name not in {mn,sn}:raise AssertionError(f)
        if 'empty' in r:
            assert (not any(f.iterdir()) if f.is_dir() else f.stat().st_size==0)==r['empty'],f
    results.append({'path':rel,'files':nf,'child_directories':nd,'manifest_SHA256':mh,'seal_SHA256':sh})
result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'EXACT_SCIENTIFIC_EVIDENCE_AUTHENTICATED',
        'packets':results,'files':491,'child_directories':33,
        'root_current_peer_reports_read_after_independent_primary_checkpoint88':True,
        'root_scientific_or_Lean_executions':0,'new_scientific_verdict_here':False}
out=B/'reviews/root-continuation-20261117/FINAL_EVIDENCE_AUTHENTICATION.json'
with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result))
