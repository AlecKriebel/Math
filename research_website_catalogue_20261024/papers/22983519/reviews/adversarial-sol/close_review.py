"""One row184 finite data closure; no scientific code execution/import/retry."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = P / 'papers/22983519/sources'
O = P / 'papers/22983519/reviews/adversarial-sol'
C = Path('/Users/alec/Documents/Math/radial_statistical_counterexample')
F = Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001')

def need(ok, message):
    if not ok: raise RuntimeError(message)

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonordinary file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': stat.S_IMODE(info.st_mode)}

def inventory(root):
    files, dirs = {}, {}
    need(stat.S_ISDIR(root.lstat().st_mode), 'Nonordinary root')
    for path in sorted(root.rglob('*')):
        info = path.lstat()
        rel = path.relative_to(root).as_posix()
        if stat.S_ISREG(info.st_mode): files[rel] = pin(path)
        else:
            need(stat.S_ISDIR(info.st_mode), 'Symlink/special node')
            dirs[rel] = stat.S_IMODE(info.st_mode)
    return files, dirs

def save(name, value):
    path = O / name
    need(not path.exists(), 'Refusing repeated closure: ' + name)
    path.write_text(json.dumps(value, indent=2) + '\n')

need(pin(O / 'INITIAL_SEAL.json')['SHA256'] == '9d27680a6e74295410a4d2d39a319ed06f2de651904f2d463079692d0ddd391d', 'INITIAL seal differs')
need(pin(O / 'INITIAL_MANIFEST.json')['SHA256'] == '0e3a6e3f6dfb49aaeb5004e60390cab68fc16ca26f4235189855b8209a3dff68', 'INITIAL manifest differs')
im = json.loads((O / 'INITIAL_MANIFEST.json').read_bytes())
need(len(im['files']) == 20 and im['directories'] == [{'path': 'rasters', 'mode': 493}], 'INITIAL extent differs')
for row in im['files']:
    need(pin(O / row['path']) == {k: row[k] for k in ('bytes', 'SHA256', 'mode')}, 'INITIAL payload changed: ' + row['path'])
need(stat.S_IMODE((O / 'rasters').stat().st_mode) == 493, 'INITIAL raster directory mode differs')
need(sorted(x.name for x in (O / 'rasters').iterdir()) == ['page-' + str(i) + '.png' for i in range(1, 5)], 'INITIAL raster extent differs')
mp, fp = pin(S / 'SOURCE_MANIFEST.json'), pin(S / 'SOURCE_FINAL.json')
need(mp == {'bytes': 17481, 'SHA256': 'e05b1df4559bac1a55fac1cfbda2a6aa6428d675e0ce7fbf708766037d425ace', 'mode': 420}, 'Source manifest differs')
need(fp == {'bytes': 826, 'SHA256': '7449712c5c396fde640b7497b20f97fb174593071fce71ca80ff763a23df4954', 'mode': 420}, 'Source FINAL differs')
sm = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
expected = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in sm['files']}
need(len(expected) == len(sm['files']) == 69, 'Source duplicate/extent differs')
expected.update({'SOURCE_MANIFEST.json': mp, 'SOURCE_FINAL.json': fp})
sf, sd = inventory(S)
need(sf == expected and len(sf) == 71, 'Source bytes/modes/extent changed')
need(sd == {x['path']: x['mode'] for x in sm['directories']} and len(sd) == 14, 'Source topology changed')
need(stat.S_IMODE(S.stat().st_mode) == sm['root_mode'] == 493, 'Source root changed')
ready = json.loads((S / 'SOURCE_READY.json').read_bytes())
need([x['key'] for x in ready['native_assets']] == ['SHA256SUMS.txt', 'source-and-verification.zip', 'paper.pdf'], 'Native order changed')
for asset in ready['native_assets']:
    path = Path(asset['path'])
    need(path.parent == S / 'assets', 'Asset outside source')
    need(pin(path)['bytes'] == asset['bytes'] and pin(path)['SHA256'] == asset['SHA256'], 'Native asset changed')
    need(hashlib.md5(path.read_bytes()).hexdigest() == asset['MD5'], 'Native MD5 differs')
fmu = F / 'private/root_primary/fmu.pdf'
kurose = C / 'tmp/kurose_1994.pdf'
matsu = C / 'tmp/priority_supplied_pdfs/matsuzoe1999-p178.png'
need(pin(fmu)['SHA256'] == 'fa552d73c0f1e1017608102a7a80eff048cd3d95ed413ae04c2fdf710da3b8f5', 'FMU raw primary differs')
need(pin(kurose)['SHA256'] == 'adfe06cd01217b31e82d3371dd7cd50803c3ff24380a168b2db215883875d138', 'Kurose raw primary differs')
need(pin(matsu)['SHA256'] == 'af6cad1cc1999c8f623562f545f507e967192572c0bd5aa5ccbf03f48f258f05', 'Matsuzoe actual page differs')
need((F / 'private/root_primary/fmu.txt').read_bytes() == b'\x0c\x0c\x0c', 'FMU cached-text limit differs')
native = json.loads((O / 'NATIVE_RUN.json').read_bytes())
need(native['actual_exit'] == 1 and native['scientific_checks_executed'] == 0 and native['new_native_invocations'] == 1, 'Native failure receipt differs')
need((O / 'native.stdout.txt').read_bytes() == b'', 'Native stdout unexpectedly nonempty')
need((O / 'native.stderr.txt').read_text().endswith("ModuleNotFoundError: No module named 'sympy'\n"), 'Literal native failure differs')
base = 'published-source/container-001/tree/radial_statistical_counterexample/'
need((S / (base + 'verification/requirements.txt')).read_text().strip() == 'sympy==1.14.0', 'Declared requirements differ')
access = json.loads((O / 'PRIMARY_ACCESS.json').read_bytes())
body = (O / 'matsuzoe.response.body').read_bytes()
headers = (O / 'matsuzoe.response.headers').read_text()
need(access['actual_curl_exit'] == 0 and access['literal_HTTP_chain'] == [302, 200], 'Access receipt differs')
need(len(body) == 1159 and b'Request unsuccessful.' in body and not body.startswith(b'%PDF'), 'Actual access failure body differs')
need('HTTP/2 302' in headers and 'HTTP/2 200' in headers and 'text/html' in headers, 'Literal access headers differ')
need((O / 'matsuzoe.curl.stdout.txt').read_text().startswith('200 https://projecteuclid.org/'), 'Literal transport status differs')
need(all((O / x).read_bytes() == b'' for x in ('closure.stdout.txt', 'closure.stderr.txt')), 'Nonempty closure stream; inspect before sealing')
raw_paths = [fmu, F / 'private/root_primary/fmu.txt', kurose, C / 'tmp/kurose_1994.txt', matsu,
    F / 'reviews/classical_priority/private/matsuzoe1998.pdf', F / 'reviews/classical_priority/private/matsuzoe1998.txt']
utc = datetime.now(timezone.utc).isoformat()
save('CLOSURE_CUSTODY.json', {'schema': 'row184-finite-independent-review-custody-v1', 'UTC': utc,
    'source_files': 71, 'source_child_directories': 14, 'source_all_buffers_modes_topology_unchanged': True,
    'original_INITIAL_files': 22, 'original_INITIAL_all_buffers_modes_topology_unchanged': True,
    'raw_primary_and_rejected_candidate_inputs': [{'path': str(x), **pin(x)} for x in raw_paths],
    'selected_native_code': {'path': base + 'verification/verify_symbolic.py', **pin(S / (base + 'verification/verify_symbolic.py'))},
    'requirements': {'path': base + 'verification/requirements.txt', **pin(S / (base + 'verification/requirements.txt'))},
    'native_attempt': {'actual_exit': 1, 'invocations': 1, 'checks_executed': 0, 'stdout': pin(O / 'native.stdout.txt'), 'stderr': pin(O / 'native.stderr.txt')},
    'ordinary_DOI_GET': {'transport_exit': 0, 'scholarly_body_acquired': False, 'headers': pin(O / 'matsuzoe.response.headers'), 'body': pin(O / 'matsuzoe.response.body'), 'stdout': pin(O / 'matsuzoe.curl.stdout.txt'), 'stderr': pin(O / 'matsuzoe.curl.stderr.txt')},
    'full_Matsuzoe1999_PDF_hash_verified_or_retained': False,
    'cached_critical_page_personally_inspected': 178,
    'peer_root_or_archived_review_opinion_bodies_opened': False,
    'retry_environment_repair_bypass_browser_W_Git_Sheet_deploy_contact_actions': False,
    'publication_authority': False})
files, dirs = inventory(O)
need(len(files) == 45 and dirs == {'primary-pages': 493, 'rasters': 493}, 'Unexpected final owned extent')
need(all(x['mode'] == 420 for x in files.values()) and stat.S_IMODE(O.stat().st_mode) == 493, 'Owned modes differ')
save('OWNED_MANIFEST.json', {'schema': 'finite-whole-scientific-review-manifest-v1', 'UTC': utc,
    'root': str(O), 'root_mode': 493, 'files': [{'path': k, **v} for k, v in files.items()],
    'directories': [{'path': k, 'mode': v} for k, v in dirs.items()],
    'exact_terminal_exclusions': ['OWNED_MANIFEST.json', 'FINAL.json'],
    'ignored_and_empty_files_included': True, 'no_future_or_subtree_exclusions': True})
save('FINAL.json', {'schema': 'independent-full-original-scientific-final-v1', 'UTC': utc,
    'row': 184, 'record': 22983519, 'family': 'adversarial-sol',
    'status': 'COMPLETE_FROZEN_QUIESCENT', 'scientific_disposition': 'PASS_FULL_ORIGINAL_WITH_LITERAL_REPRODUCTION_ACCESS_LIMITS',
    'substantive_unresolved_proof_gap': None, 'follow_up': None, 'completion_percent': 100,
    'report': {'path': 'REPORT.md', **pin(O / 'REPORT.md')},
    'manifest': {'path': 'OWNED_MANIFEST.json', **pin(O / 'OWNED_MANIFEST.json')},
    'INITIAL_seal': {'path': 'INITIAL_SEAL.json', **pin(O / 'INITIAL_SEAL.json')},
    'payload_files': 45, 'actual_files': 47, 'child_directories': 2,
    'all_source_and_INITIAL_unchanged': True, 'native_scientific_attempts': 1, 'native_exit': 1,
    'new_native_scientific_checks_executed': 0, 'fresh_Matsuzoe1999_scholarly_body_acquired': False,
    'scientific_findings_withheld_until_root_gate': True,
    'publication_authority': False, 'AA': None, 'canonical_url': None,
    'postseal_owned_writes_executions_allowed': False})
