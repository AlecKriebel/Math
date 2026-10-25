"""Reconcile independent article, root article, PDF and actual-download evidence."""
from pathlib import Path
from datetime import datetime, timezone
import concurrent.futures, hashlib, json, urllib.request

P = Path(__file__).resolve().parents[1]
V = P / 'verification'
SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()
def load(p): return json.loads(Path(p).read_text())
def binding(p): return {'path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p)}
def save(p, d): p.write_text(json.dumps(d, indent=2, ensure_ascii=False)+'\n')

components = []
for folder, expected, count in [
    ('browser-approved-three-sol-20261025', 'd7bddc1caa3c45aba521257b789f577df95a0a0efd346c31bc05407d6e3e7899', 78),
    ('three-pdf-download-finish-sol-20261025', '6c9169da48a7f59e9aa84af9374347adcea5732a183c28acd2ff792c384eeb85', 46),
]:
    base = V/folder
    manifest = base/'evidence-manifest.json'
    assert sha(manifest) == expected
    entries = load(manifest)['files']
    assert len(entries) == count
    for e in entries:
        f = base/e['path']
        assert f.stat().st_size == e['bytes'] and sha(f) == e['sha256'], str(f)
    components.append({'manifest': str(manifest.relative_to(P)), 'sha256': expected, 'bindings_rechecked': count})

preserved = load(V/'three-pdf-download-finish-sol-20261025/preservation-before.json')['files']
assert len(preserved) == 591
for e in preserved:
    f=Path(e['path'])
    assert f.stat().st_size == e['bytes'] and sha(f) == e['sha256'], str(f)
downloads=load(V/'three-pdf-download-finish-sol-20261025/actual-download-verification.json')['files']
assert len(downloads)==6
for e in downloads:
    for path in [e['path'], e['site_path'], *e['matching_primary_sources']]:
        f=Path(path)
        assert f.stat().st_size == e['expected_bytes'] and sha(f)==e['expected_sha256'], path

root=V/'root-three-browser-finish-20261025'
assert load(root/'events.json')
rootfiles=[binding(f) for f in sorted(root.rglob('*')) if f.is_file() and f.name != 'evidence-manifest.json']
save(root/'evidence-manifest.json', {'utc':datetime.now(timezone.utc).isoformat(),'files':rootfiles,
    'excluded_positive_visuals':['attempts/failed-pointer-index-click.jpg','attempts/viewport-resize-before-anchor.jpg','index-narrow-footer.jpg'],
    'notes':['Native AX reset the emulation on three captures; filenames were corrected before sealing. Separate confirmed390 images are positive narrow evidence.',
    'The initial ordered-list count was inapplicable; actual main unordered-list title links were independently counted50.',
    'This root component completes remaining bosonic narrow and amplifier desktop/narrow article and actual Research-link return checks.']})

earlier=load(V/'live-approved-three-root-20261025.json')
def probe(e):
    with urllib.request.urlopen(e['url'],timeout=35) as r:
        body=r.read(); result={'url':e['url'],'status':r.status,'final_url':r.url,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),
            'cache_control':r.headers.get('Cache-Control')}
    assert result['status']==200 and result['final_url']==e['url'] and result['sha256']==e['expected_sha256'], result
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    live=list(pool.map(probe,earlier['checks']))
assert len(live)==16
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'ROOT_ACCEPTED_ALL_THREE_LIVE_ARTICLE_PDF_DOWNLOAD_GATES',
    'site_commit':'16b7b547c7cf7f54e586f2a753fc861763807f33','hosting_version':'f3d003e1e8f50e45',
    'records':[23306332,23203100,22089807], 'full_reports_read':True,'root_actual_raw_screenshots_inspected':True,
    'article_checks':'All three desktop and390px top, plain explanation, scope, embedded PDF, collaboration and citation; ordinary actual Research-link returns show50titles.',
    'pdf_checks':'All three actual full-window PDF links render first pages; desktop counts6/7/21 and narrow390px fit with visible properties counts6/7/21.',
    'limitations':'Desktop-browser viewport emulation only; fixed-page PDF text is small. No physical-phone or PDF reflow claim.',
    'components':components,'root_component_manifest':binding(root/'evidence-manifest.json'),
    'current_preservation_bindings_rehashed':591,'actual_downloads_rehashed_against_site_and_primary':6,'fresh_live_checks':live,
    'native_tracker_transition_authorized':True,'native_tracker_transition_completed':False,
    'cleanup':{'root_tab725_closed':True,'six_download_agent_tabs_closed':True,'protected_user_tabs_preserved':True,
        'inherited_tab718_close_unconfirmed':'Old session ownership prevents supported access. Owning-session attempt returned Tab not found; root supported claim refused ownership. No bypass or further attempts. Independent of publication readiness.'},
    'scientific_acceptance':'Existing root clearances and full public-copy/local integration acceptance remain prerequisites; this receipt does not replace scientific review.',
    'overall_goal_complete':False}
save(V/'root-approved-three-browser-20261025.json',receipt)
print(json.dumps({'status':receipt['status'],'owned_bindings':124,'preserved_bindings':591,'actual_downloads':6,'live_checks':16,'root_manifest_bindings':len(rootfiles)}))
