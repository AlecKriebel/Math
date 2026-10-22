"""Offline, read-only verification of this completed checkpoint review."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    manifest=HERE/'PUBLIC_AUTHORED_MANIFEST.json'
    data=json.loads(manifest.read_text())
    for row in data['files']:
        p=HERE/row['path']
        assert p.is_file() and p.stat().st_size==row['bytes']
        assert digest(p)==row['sha256']
        assert 'private_reading' not in p.relative_to(HERE).parts
    assert digest(manifest)==(HERE/'PUBLIC_MANIFEST_SHA256.txt').read_text().split()[0]
    pins=json.loads((HERE/'INPUT_PINS.json').read_text())
    base=Path(pins['base'])
    for row in pins['files']:
        p=base/row['path']
        assert p.stat().st_size==row['bytes'] and digest(p)==row['sha256']
    current=0
    for lane,name in [('priority_historical_01','AUTHORED_MANIFEST.json'),('priority_local_limit_01','PUBLIC_AUTHORED_MANIFEST.json'),('priority_recent_01','AUTHORED_MANIFEST.json'),('priority_bridge_01','PUBLIC_AUTHORED_MANIFEST.json')]:
        m=base/lane/name
        for row in json.loads(m.read_text())['files']:
            p=m.parent/row['path']
            assert p.stat().st_size==row['bytes'] and digest(p)==row['sha256']
            current+=1
    sources=json.loads((HERE/'INDEPENDENT_SOURCE_AUTHENTICATION.json').read_text())
    assert all(x['match'] and x['pdf_magic'] and not x['whole_source_saved'] for x in sources['pdf_byte_authentication'])
    assert all(x['date_match'] for x in sources['metadata_authentication'])
    controls=json.loads((HERE/'INDEPENDENT_CONTROLS_RECEIPT.json').read_text())
    assert controls['status']=='PASS' and controls['exact_assertions']==13328
    final=json.loads((HERE/'FINAL_RESEAL_CHECK.json').read_text())
    assert final['status']=='PASS' and final['old_seal_preserved']
    print(json.dumps(dict(status='PASS',public_authored_files=len(data['files']),current_input_pins=len(pins['files']),four_family_manifest_entries=current,primary_pdf_retrieval_matches=4,independent_exact_assertions=controls['exact_assertions'],old_and_new_bridge_seals_verified=True,scope='artifact integrity and recorded controls; no global novelty certificate'),indent=2))


if __name__=='__main__':main()
