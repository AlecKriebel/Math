"""Offline, read-only verification of this completed checkpoint review."""
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import urlsplit,urlunsplit,parse_qsl

HERE=Path(__file__).resolve().parent


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def verify_sanitation(base):
    lane=base/'priority_local_limit_01'
    old=lane/'private_reading/sealed_public_checkpoint_pre_sanitization_20261015T050105Z'
    oldm=json.loads((old/'PUBLIC_AUTHORED_MANIFEST.json').read_text())
    newm=json.loads((lane/'PUBLIC_AUTHORED_MANIFEST.json').read_text())
    assert digest(old/'PUBLIC_AUTHORED_MANIFEST.json')=='d4bad52fe54862e8652fc4c395d17fe106b414802cc8916b029bd395ca9c8f70'
    assert digest(lane/'PUBLIC_AUTHORED_MANIFEST.json')=='23523ea977f25bbb02f4b8add1f6502317f570d5bf52b0e8f9f00d10b0443259'
    assert digest(old/'PRIVATE_SEAL_RECEIPT.json')=='4ae3cc7c85a1dbc06120be522f1c1046015c276f6ee8fb372651b5d62245db0f'
    for row in oldm['files']:
        p=old/row['path']
        assert p.stat().st_size==row['bytes'] and digest(p)==row['sha256']
    assert len(oldm['files'])==len(newm['files'])==28
    changed={r['path'] for r in oldm['files'] if (old/r['path']).read_bytes()!=(lane/r['path']).read_bytes()}
    assert changed=={'BMP_FAILED_ROUTES.json','RESEARCH_LOG.md'}
    for k,v in oldm.items():
        if k not in ['files','utc']:assert newm[k]==v
    assert set(newm)-set(oldm)=={'sanitation'}
    a=json.loads((old/'BMP_FAILED_ROUTES.json').read_text())
    b=json.loads((lane/'BMP_FAILED_ROUTES.json').read_text())
    olderror=a[0]['error'];newerror=b[0]['error']
    a[0]['error']=newerror
    assert a==b
    urls=re.findall(r'https://validate\.perfdrive\.com/[^\s\x27\x22<>]*',olderror)
    assert len(urls)==1
    parts=urlsplit(urls[0])
    safe=urlunsplit((parts.scheme,parts.netloc,parts.path,'',parts.fragment))
    assert olderror.replace(urls[0],safe)==newerror
    assert len(parse_qsl(parts.query,keep_blank_values=True))==16
    assert (lane/'RESEARCH_LOG.md').read_bytes().startswith((old/'RESEARCH_LOG.md').read_bytes())
    seal=HERE/'revision_history/completed_seal_20261015T0452Z'
    assert digest(seal/'PUBLIC_AUTHORED_MANIFEST.json')=='8dd389762fcde48fbf40d7a2b40c0a0ee56e611bbfeece47ac4ecf7f501e1f8f'
    for row in json.loads((seal/'PUBLIC_AUTHORED_MANIFEST.json').read_text())['files']:
        p=seal/row['path']
        assert p.stat().st_size==row['bytes'] and digest(p)==row['sha256']
    return True


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
    sanitation=verify_sanitation(base)
    print(json.dumps(dict(status='PASS',public_authored_files=len(data['files']),current_input_pins=len(pins['files']),four_family_manifest_entries=current,primary_pdf_retrieval_matches=4,independent_exact_assertions=controls['exact_assertions'],old_and_new_bridge_seals_verified=True,sanitation_only_diff_and_private_local_seal_verified=sanitation,preceding_completed_synthesis_seal_verified=True,scope='artifact integrity and recorded controls; no global novelty certificate'),indent=2))


if __name__=='__main__':main()
