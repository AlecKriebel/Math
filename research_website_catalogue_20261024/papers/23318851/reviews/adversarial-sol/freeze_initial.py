"""Passive original-only INITIAL closure; no source execution or project imports."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = P / 'papers/23318851/sources'
A = P / 'papers/23318851/reviews/adversarial-sol'
TERMINALS = {'INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def enc(v):
    return (json.dumps(v, indent=2, ensure_ascii=False) + '\n').encode()

def snap(root, md5=False):
    rows = []
    for p in [root, *sorted(root.rglob('*'))]:
        st = p.lstat()
        r = {'path': '.' if p == root else str(p.relative_to(root)),
             'mode_octal': oct(stat.S_IMODE(st.st_mode)),
             'hidden': any(x.startswith('.') for x in p.relative_to(root).parts)}
        if stat.S_ISDIR(st.st_mode):
            r.update(kind='directory', empty=not any(p.iterdir()))
        elif stat.S_ISREG(st.st_mode):
            b = p.read_bytes()
            r.update(kind='file', bytes=len(b), sha256=sha(b))
            if md5:
                r['md5'] = hashlib.md5(b).hexdigest()
        else:
            r.update(kind='other', target=os.readlink(p) if p.is_symlink() else None)
        rows.append(r)
    return rows

def counts(rows):
    return {'files': sum(r['kind'] == 'file' for r in rows),
            'child_directories': sum(r['kind'] == 'directory' for r in rows) - 1,
            'hidden_paths': sum(r['hidden'] for r in rows),
            'empty_directories': [r['path'] for r in rows if r['kind'] == 'directory' and r['empty']],
            'empty_files': [r['path'] for r in rows if r['kind'] == 'file' and r['bytes'] == 0]}

assert not (A / 'INITIAL.json').exists()
assert not any((A / n).exists() for n in TERMINALS)
before = json.loads((A / 'CUSTODY_BEFORE.json').read_text())
after = json.loads((A / 'CUSTODY_AFTER.json').read_text())
assert before['entries'] == after['entries'] == snap(S, md5=True)
assert before['files'] == 95 and before['child_directories'] == 16
assert after['before_after_exact'] is True
assert sha((S / 'SOURCE_FINAL.json').read_bytes()) == 'c61fb0473f0954877ab5af49e7b6139732eb4afab7cfab3377864a91dd98b317'
assert sha((S / 'SOURCE_MANIFEST.json').read_bytes()) == 'ed5c217040b7a0d72df7de7ef1d5cbce9bc516ab32c1f20ed6466ef153a6bac8'
assert sha((S / 'zenodo-files/gram_locus_note.pdf').read_bytes()) == 'ac0839eae1d0e83e0c47d3c840968363ce9271c83cc9ee88156197601b4d0018'
assert sha((S / 'archives/02-gram_locus_support.zip.extracted/gram_locus_note.tex').read_bytes()) == 'f6ddf7f510df8e7000a627a79be32413c53476104f87336b49dd0ded1983701a'
api = json.loads((S / 'native-metadata/record-api.json').read_text())
assert api['metadata']['version'] == '1.0.0' and api['metadata']['publication_date'] == '2026-10-12'
assert len(api['files']) == 2 and api['files'][0]['key'] == 'gram_locus_note.pdf'
assert (A / 'ORIGINAL_PDF_TEXT.txt').read_text().count('\f') == 5
assert sha((A / 'ORIGINAL_PDF_TEXT.txt').read_bytes()) == 'f63b9bb2844c2fa53bf5aec45487d7670bb726e16feeab77eac939a6a976f023'
page_paths = ['pages/native-' + str(i) + '.png' for i in range(1, 6)]
assert set(p.name for p in (A / 'pages').iterdir()) == set(Path(n).name for n in page_paths)
page_receipts = [{'path': n, 'bytes': (A / n).stat().st_size, 'sha256': sha((A / n).read_bytes()),
                  'fresh_native_page': i, 'personally_viewed_individually': True}
                 for i, n in enumerate(page_paths, 1)]
now = datetime.now(timezone.utc).isoformat()
with (A / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n' + now + ': Source-after guard exits0 and matches the complete95/16 source-before namespace exactly. Original-only reconstruction and exposure limits complete. INITIAL phase100%; full scientific/provenance review best guess40%. Finite terminal INITIAL manifest/seal closes this namespace. No support, code, primary or current-review content exposure and no scientific execution. Stop pending root source gate, checkpoint and explicit RESUME into a separate sibling.\n')
initial = {'UTC': now, 'row': 194, 'record': '23318851', 'phase': 'INITIAL_ORIGINALS_ONLY',
    'INITIAL_completion_percent': 100, 'full_scientific_provenance_review_completion_estimate_percent': 40,
    'final_scientific_or_priority_verdict': None, 'promotion_authorized': False, 'follow_up': None,
    'source_files': 95, 'source_child_directories': 16,
    'source_whole_byte_mode_hidden_empty_topology_before_after_exact': True,
    'SOURCE_FINAL_SHA256': 'c61fb0473f0954877ab5af49e7b6139732eb4afab7cfab3377864a91dd98b317',
    'SOURCE_MANIFEST_SHA256': 'ed5c217040b7a0d72df7de7ef1d5cbce9bc516ab32c1f20ed6466ef153a6bac8',
    'native_version': '1.0.0', 'native_version_field_present': True,
    'printed_declared_publication_date': '2026-10-12', 'PDF_container_format_version': '1.5',
    'controlling_TeX_read_completely': True, 'native_API_read_completely': True,
    'complete_native_Description_and_HTML_metadata_read': True,
    'fresh_native_PDF_text_all_pages_read': 5, 'fresh_page_images': page_receipts,
    'pre_TeX_author_Description_cover_exposure_recorded': True,
    'packaged_opinions_support_results_code_primary_or_current_reports_read': False,
    'scientific_native_routes_or_source_execution': 0, 'scientific_code_reading': 0,
    'project_import_AST_compiler_tests_installs': 0, 'children': 0, 'external_contact_outreach': 0,
    'website_access_or_guard': False, 'network_or_Git_operations': 0,
    'reports': ['PRE_TEX_ATTACK.md', 'INITIAL_RECONSTRUCTION.md', 'EXPOSURE_LEDGER.md', 'RESEARCH_LOG.md'],
    'mathematical_mechanisms_and_findings_withheld_from_coordination': True,
    'stop_requires_root_checkpoint_source_gate_and_explicit_RESUME': True,
    'continuation_must_be_separate_sibling': True}
(A / 'INITIAL.json').write_bytes(enc(initial))
for n in TERMINALS:
    (A / n).write_bytes(b'')
rows = snap(A)
assert not any(r['kind'] == 'other' for r in rows)
for r in rows:
    if r['path'] in TERMINALS:
        r['sha256'] = 'EXCLUDED_TERMINAL_RECURSIVE_HASH'
scope = counts(rows)
scope['empty_files'] = [n for n in scope['empty_files'] if n not in TERMINALS]
assert scope['files'] == 18 and scope['child_directories'] == 1
manifest = {'UTC': now, 'root': str(A), **scope, 'all_actual_paths_bytes_modes_hidden_empty_topology': True,
    'only_recursive_hash_exclusions': sorted(TERMINALS), 'entries': rows}
seal = {'UTC': now, 'frozen': True, 'phase': 'INITIAL_ORIGINALS_ONLY', 'root': str(A), **scope,
    'manifest_bytes': 0, 'manifest_sha256': '0' * 64,
    'INITIAL_sha256': sha((A / 'INITIAL.json').read_bytes()),
    'CUSTODY_BEFORE_sha256': sha((A / 'CUSTODY_BEFORE.json').read_bytes()),
    'CUSTODY_AFTER_sha256': sha((A / 'CUSTODY_AFTER.json').read_bytes()),
    'source95_16_exact': True, 'original_PDF_pages_individually_viewed': 5,
    'scientific_code_exposure_or_execution': 0,
    'only_recursive_hash_exclusions': sorted(TERMINALS), 'seal_sha256': 'EXCLUDED_TERMINAL_RECURSIVE_HASH',
    'INITIAL_completion_percent': 100, 'full_review_estimate_percent': 40,
    'final_verdict': None, 'follow_up': None, 'stop': True}
for _ in range(20):
    mb = enc(manifest)
    seal['manifest_bytes'] = len(mb)
    seal['manifest_sha256'] = sha(mb)
    sb = enc(seal)
    sizes = {'INITIAL_MANIFEST.json': len(mb), 'INITIAL_SEAL.json': len(sb)}
    if all(r['bytes'] == sizes[r['path']] for r in rows if r['path'] in TERMINALS):
        break
    for r in rows:
        if r['path'] in TERMINALS:
            r['bytes'] = sizes[r['path']]
else:
    raise AssertionError('Terminal byte-size fixed point did not converge')
(A / 'INITIAL_MANIFEST.json').write_bytes(mb)
(A / 'INITIAL_SEAL.json').write_bytes(sb)
actual = snap(A)
for r in actual:
    if r['path'] in TERMINALS:
        r['sha256'] = 'EXCLUDED_TERMINAL_RECURSIVE_HASH'
assert actual == rows and counts(actual) == scope
assert snap(S, md5=True) == before['entries']
print(json.dumps({'UTC': now, 'frozen': True, **scope,
    'INITIAL_sha256': seal['INITIAL_sha256'], 'manifest_bytes': len(mb), 'manifest_sha256': sha(mb),
    'seal_bytes': len(sb), 'seal_sha256': sha(sb), 'source95_16_exact': True,
    'pages_individually_viewed': 5, 'scientific_code_exposure_or_execution': 0,
    'INITIAL_completion_percent': 100, 'full_review_estimate_percent': 40}))
