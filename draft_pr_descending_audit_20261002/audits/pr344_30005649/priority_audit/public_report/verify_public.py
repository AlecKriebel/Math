"""Portable read-only payload and convention verification; standard library only.

Run: python3 -B verify_public.py [directory]
No network, installation, source PDFs, private receipts, or repository is needed.
No file is written. This is not a novelty/first-priority certificate.
"""
from pathlib import Path
import hashlib, json, runpy, stat, sys

def verify(root):
    root=root.resolve()
    manifest=json.loads((root/'PUBLIC_MANIFEST.json').read_text())
    assert manifest['sealed'] is False, 'Unexpected seal status'
    rows=manifest['payloads']
    paths=[x['path'] for x in rows]
    assert len(set(paths))==len(paths)
    assert all(Path(p).name==p and not Path(p).is_absolute() for p in paths)
    actual={p.name for p in root.iterdir() if p.is_file() and p.name!='PUBLIC_MANIFEST.json'}
    assert set(paths)==actual, 'Public payload inventory mismatch'
    for row in rows:
        p=root/row['path']
        assert not p.is_symlink(), 'Symlink payload rejected'
        data=p.read_bytes()
        assert len(data)==row['bytes'], 'Byte-length mismatch: '+row['path']
        assert hashlib.sha256(data).hexdigest()==row['sha256'], 'SHA mismatch: '+row['path']
        assert stat.S_IMODE(p.stat().st_mode)==int(row['mode'],8), 'Mode mismatch: '+row['path']
    result=runpy.run_path(str(root/'convention_compare.py'))['verify']()
    assert result['status']=='PASS' and result['known_module']=='M(vvfvff)'
    gaps=json.loads((root/'GAPS.json').read_text())
    assert gaps['closure_status'].startswith('not authorized')
    assert any(g['id']=='G07' and g['status']=='closed_mathematical' for g in gaps['gaps'])
    assert gaps['mathematical_mechanism']=='closed_PASS'
    assert all(g['status']=='open_historical_limit' for g in gaps['gaps'] if g['id']!='G07')
    decision=json.loads((root/'MATHEMATICAL_ADJUDICATION.json').read_text())
    assert decision['mathematical_mechanism']=='closed_PASS'
    assert decision['root_decision_sha256']==gaps['root_decision_sha256']
    assert decision['focused_report_sha256']=='590dd09fc252a0a1f0657033f0b1ef05a237b108ac8bff983209258c2658e878'
    assert not any(decision[k] for k in ['first_discovery_certified','first_application_certified','continuing_openness_2026_certified','priority_audit_seal_authorized'])
    return {'status':'PASS','sealed':False,'payload_count':len(rows),'convention':result,'mathematical_mechanism':'closed_PASS_adjudication_record','historical_priority':'not certified','historical_limit_count':sum(g['status']=='open_historical_limit' for g in gaps['gaps'])}

if __name__=='__main__':
    try:
        print(json.dumps(verify(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent),indent=2))
    except Exception as e:
        print(json.dumps({'status':'FAIL','error':str(e)}));sys.exit(1)
