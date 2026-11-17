from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OUT = P / 'verification/root-mixed-k3-moduli-editorial-adoption-20261117.json'
assert not OUT.exists()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def authenticate(rel, manifest_name, pins, counts):
    root = P / rel
    for name, expected in pins.items():
        assert sha(root / name) == expected, (rel, name)
    manifest = json.loads((root / manifest_name).read_text())
    if 'entries' in manifest:
        entries = manifest['entries'][:]
        entries += manifest.get('terminal_control_topology', [])
    else:
        entries = [dict(e, kind='file') for e in manifest['payload_files']]
        entries += [dict(e, kind='directory') for e in manifest['directories']]
        entries += [dict(e, kind='file') for e in manifest.get('terminal_control_topology', manifest.get('terminal_controls', []))]
        entries += [{'path':'.', 'kind':'directory', 'mode':manifest['root_mode']}]
    expected = {e['path']:e for e in entries}
    assert len(expected) == len(entries), rel
    actual = {'.':root}
    actual.update({str(f.relative_to(root)):f for f in root.rglob('*')})
    assert set(actual) == set(expected), (rel, set(actual)^set(expected))
    files = dirs = 0
    authenticated = []
    for name, f in sorted(actual.items()):
        e = expected[name]
        assert not f.is_symlink(), (rel, name)
        mode = oct(stat.S_IMODE(f.stat().st_mode))
        assert mode == e.get('mode', e.get('mode_octal')), (rel, name, mode)
        assert f.is_dir() == (e['kind']=='directory'), (rel, name)
        if f.is_dir():
            dirs += name != '.'
            if 'empty' in e: assert (not any(f.iterdir())) == e['empty']
            authenticated.append({'path':name,'kind':'directory','mode':mode})
        else:
            files += 1
            data = f.read_bytes()
            if 'bytes' in e: assert len(data) == e['bytes'], (rel, name)
            digest = hashlib.sha256(data).hexdigest()
            expected_sha = e.get('SHA256', e.get('sha256'))
            if expected_sha is not None: assert digest == expected_sha, (rel, name)
            else: assert name in pins, (rel, name, 'unbound terminal control')
            expected_md5 = e.get('MD5', e.get('md5'))
            if expected_md5 is not None: assert hashlib.md5(data).hexdigest() == expected_md5
            if 'empty' in e: assert (len(data)==0) == e['empty']
            authenticated.append({'path':name,'kind':'file','mode':mode,'bytes':len(data),'SHA256':digest})
    assert [files, dirs] == counts, (rel, files, dirs)
    return {'root':rel,'files':files,'childdirs':dirs,'objects':authenticated}

specs = [
 ('papers/23204176/sources','SOURCE_MANIFEST.json', {
  'SOURCE_MANIFEST.json':'53be96c6f47deccccc173286d10bdf46b50df4f237c985f42f2da8a69d8c8ffb',
  'SOURCE_FINAL.json':'f7bc05f4e7d56f0fbad45d77bdb4992d9fd92de8d976bdc5ff3b446f7dbfe9c8'}, [43,7]),
 ('verification/mixed-k3-moduli-editorial-sol-20261117','MANIFEST.json', {
  'FINAL.json':'245fcc03a3105d4a3a093821bd79e995d13225246a5e0f96b7a6c3e322a814b8',
  'MANIFEST.json':'1aa3d7271c59f80db746b41005b605d2e68ec448cdf3125b3b282ae7e6acb171'}, [28,1]),
 ('verification/mixed-k3-moduli-fact-sol-20261117','MANIFEST.json', {
  'FINAL.json':'3f0ddf35c05aa9d59b1a915bda5fff1e9210572430952171681a435c08f57489',
  'MANIFEST.json':'923f7ade0128849fecfd818f6e8b40d3962e5ceccfa365e150d257e0dea595f8'}, [16,0]),
 ('verification/mixed-k3-moduli-legacy-sol-20261117','MANIFEST.json', {
  'FINAL.json':'05e61e679920219b18e8be177e92271f59ecfeae29ff012c13096381c1f7b6b7',
  'MANIFEST.json':'53115613a9b5ef742e691d65d402adafa5ba488a4c5f575cc5f935bffb529189'}, [80,2])
]
authenticated = [authenticate(*s) for s in specs]
writer = P / specs[1][0]
assert sha(writer/'article.html') == 'fa80a828093717d9648e8a806aed891f0e52e9c517c17f7200624e67915c37e5'
model = json.loads((writer/'page-model.json').read_text())
assert model['record_id']=='23204176' and model['follow_up'] is None
for name in ['canonical_url','base_url','production_url','actual_publication_date','AA']:
    assert model[name] is None
assert model['publication_authority'] is False
assert sha(P/'verification/root-clearance-23204176-20261117.json') == 'ea5472784dffe99ee849d40700541b9453466b2f3edf064a3a02fe091e7f55cd'
assert sha(P/'papers/23204176/reviews/root-continuation-20261117/ROOT_REVIEW.md') == '726d07488144fb2a7e4cbc0351c235a4a422a42346e71410000833596c2f6b94'
result = {
 'UTC':datetime.now(timezone.utc).isoformat(), 'record_id':'23204176','sheet_row':191,
 'status':'PRIVATE_EDITORIAL_ACCEPTED_FOR_SEPARATE_STAGING', 'completion_percent':100,
 'personally_read':['Entire actual article/head/body/main in previous turn','Entire page-model and BibTeX','Writer FINAL and REPORT','Fact FINAL, REPORT and ISSUES','Legacy FINAL and REPORT','Actual custody manifest schemas'],
 'scientific_disposition':'Inherited bounded substantive PASS, with SCOPE reservation preserved verbatim in scientific evidence; no unanimity or formal/human review certificate',
 'copy_disposition':'Faithful attributed corollary; rational mixed-product hypotheses, native absent API version, original date, rights, assets, AI disclosure and passive contribution-based collaboration retained',
 'legacy_disposition':'No genuine corresponding article identified in three bounded existing docs views; no global historical/live absence certificate or redirect authority',
 'authenticated':authenticated,'files':167,'childdirs':10,
 'follow_up':None,'canonical_url':None,'AA':None,'publication_authority':False,
 'scientific_or_producer_execution':False,'W_Git_network_Sheet_mutation':False,
 'next_action':'Create and independently inspect a fresh private staging candidate from current website state'
}
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'files':167,'childdirs':10,'receipt':str(OUT),'SHA256':sha(OUT)}))
