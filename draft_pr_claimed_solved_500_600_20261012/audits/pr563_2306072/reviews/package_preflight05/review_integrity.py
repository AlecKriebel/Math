#!/usr/bin/env python3
"""Independent read-only archive/integrity and historical-input checks."""
from pathlib import Path
import zipfile, json, stat, hashlib, datetime, platform
OUT=Path(__file__).resolve().parent
BASE=OUT.parents[1]
sha=lambda data:hashlib.sha256(data).hexdigest()
with zipfile.ZipFile(BASE/'publication/verification_package.zip') as z:
    infos=z.infolist();names=[p.filename for p in infos]
    assert len(set(names))==len(names)==255
    assert all(n.startswith('support_slit_verification/') and not n.endswith('/') for n in names)
    files={n.split('/',1)[1]:z.read(n) for n in names}
    assert all(not ('..' in n.split('/') or n.startswith('/') or '\\' in n or ':' in n) for n in files)
    assert all(stat.S_ISREG(p.external_attr>>16) for p in infos)
    assert all(p.date_time==(2026,10,13,12,0,0) for p in infos)
    m=json.loads(files['MANIFEST.json']);payload={k:v for k,v in files.items() if k!='MANIFEST.json'}
    assert set(payload)==set(m['files'])
    for n,d in payload.items():assert len(d)==m['files'][n]['bytes'] and sha(d)==m['files'][n]['sha256']
    registry=json.loads(files['SEALS.json']);assert registry==m['nested_seals'];nested=0;records=[]
    for n in registry:
        j=json.loads(files[n]);entries=j.get('files',j.get('authored_files',j.get('authored_outputs')))
        if isinstance(entries,dict):entries=[dict(path=k,**({'sha256':v} if isinstance(v,str) else v)) for k,v in entries.items()]
        seen=set()
        for entry in entries:
            p=str(Path(n).parent/entry['path']);assert p not in seen;seen.add(p)
            d=files[p];assert sha(d)==entry['sha256']
            size=entry.get('bytes',entry.get('size_bytes',entry.get('size')))
            assert size is None or size==len(d)
            nested+=1
        records.append({'seal':n,'entries_verified':len(entries)})
    assert nested==164
    j=json.loads(files['reviews/priority07_zemyan_bounds/SEAL.json'])
    for name,h in j['binds'].items():assert sha(files['reviews/priority07_zemyan_bounds/'+name])==h
    j=json.loads(files['reviews/priority12_goh1992_adversary/SOURCE_FIRST_SEAL.json'])
    assert sha(files['reviews/priority12_goh1992_adversary/SOURCE_FIRST_CHECKPOINT.md'])==j['source_first_sha256']
    baseline=files['root_reproduction/PRIMARY_AUDIT_BASELINE.tex'];pre=files['root_reproduction/PRE_GOH_MANUSCRIPT.tex']
    assert sha(baseline)=='eaf22e2617d2dbbe240b4adc7661801cff2cfa3751ba834379002789c4e7eb83'
    assert sha(pre)=='c46d521e893a46466cf26b50c54294d1923e93dad4076e4b5dfa16c52d42830a'
    for f in ('support_slit.tex','root_reproduction/PRIMARY_AUDIT_BASELINE.tex','root_reproduction/PRE_GOH_MANUSCRIPT.tex'):
        text=files[f];start=text.index(b'\\section{The question and precise statement}');end=text.index(b'\\section{Attribution, scope and verification}');body=text[start:end]
        assert len(body)==10407 and sha(body)=='8bdabc193370a4c11c42ce6d0b6dfe4fbc673d296daa9cefedfbe4663d97c852'
    assert not any(n.endswith(('.pdf','.png','.jpg','.html')) or (n.endswith('.txt') and n!='requirements.txt') or '.cache' in n.split('/') or '.private' in n for n in files)
    metadata=json.loads(files['metadata.json']);assert metadata==json.loads((BASE/'publication/zenodo-deposit.json').read_text())
    assert {i['path'] for i in metadata['files']}=={'support_slit.pdf','verification_package.zip'}
    checks={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive_members':len(infos),'outer_payloads':len(payload),'nested_entries':nested,'nested_seals':records,'additional_authored_seals_checked':['priority07 SEAL binds','priority12 source-first checkpoint SHA256'],'safe_regular_unique_paths':True,'outer_inventory_exact':True,'fixed_zip_timestamps':True,'no_third_party_fulltext_or_binary_raw_payload':True,'three_historical_proof_bodies_exact_match':True,'proof_body_sha256':'8bdabc193370a4c11c42ce6d0b6dfe4fbc673d296daa9cefedfbe4663d97c852','proof_body_bytes':10407,'metadata_copy_exact':True,'fresh_runtime':platform.python_version(),'pinned_mpmath':'1.4.1'}
print(json.dumps(checks,indent=2))
