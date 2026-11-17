"""Own-lane finite initial inventory/seal only. No scientific computation."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

OWN = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23204176/reviews/scope-sol')
TERMINALS = {'INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'}


def need(condition, reason):
    if not condition:
        raise AssertionError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


before = json.loads((OWN / 'SOURCE_BEFORE.json').read_bytes())
after = json.loads((OWN / 'SOURCE_AFTER.json').read_bytes())
need(before['entries'] == after['entries'] and after['whole_source_before_after_exact'], 'whole source preservation')
need((before['files'], before['child_directories']) == (43, 7), 'source whole topology')
for name in ['CUSTODY_BEFORE.stderr.txt', 'CUSTODY_AFTER.stderr.txt', 'PDF_RENDER.stdout.txt', 'PDF_RENDER.stderr.txt', 'PDFINFO.stderr.txt']:
    need((OWN / name).read_bytes() == b'', 'empty successful literal stream ' + name)
for page in range(1, 5):
    need((OWN / ('native-page-' + str(page) + '.png')).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'), 'fresh page PNG')
    need(len((OWN / ('native-page-' + str(page) + '.txt')).read_bytes()) > 0, 'fresh complete page text')
for name in TERMINALS:
    need(not (OWN / name).exists(), 'terminal absent before single seal')
for name in sorted(TERMINALS):
    fd = os.open(str(OWN / name), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    os.close(fd)
rows = []


def visit(path):
    s = path.lstat()
    rel = path.relative_to(OWN).as_posix()
    row = {'path': rel, 'mode_octal': oct(stat.S_IMODE(s.st_mode)),
           'hidden_component': any(p.startswith('.') and p != '.' for p in Path(rel).parts)}
    if stat.S_ISDIR(s.st_mode):
        children = sorted(path.iterdir(), key=lambda p: os.fsencode(p.name))
        row.update(kind='directory', empty=not children)
        rows.append(row)
        for child in children:
            visit(child)
    else:
        need(stat.S_ISREG(s.st_mode), 'no symlink/special own-lane object')
        row['kind'] = 'file'
        if rel in TERMINALS:
            row['terminal_control'] = True
        else:
            data = path.read_bytes()
            row.update(bytes=len(data), sha256=sha(data))
        rows.append(row)


visit(OWN)
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest = {'schema': 'finite-row191-original-only-INITIAL-manifest-v1', 'UTC': now, 'root': str(OWN),
            'regular_files': sum(r['kind'] == 'file' for r in rows),
            'child_directories': sum(r['kind'] == 'directory' for r in rows) - 1,
            'entries': rows, 'exact_already_created_terminal_recursive_hash_exclusions': sorted(TERMINALS),
            'other_exclusions': [], 'all_actual_hidden_empty_modes_and_topology_included': True,
            'INITIAL_completion_percent': 100, 'overall_scientific_review_estimate_percent': 30}
manifest_path = OWN / 'INITIAL_MANIFEST.json'
manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
seal = {'schema': 'row191-original-only-INITIAL-seal-v1', 'UTC': now,
        'status': 'ORIGINAL_ONLY_INITIAL_FROZEN_NO_SCIENTIFIC_CLEARANCE',
        'root': str(OWN), 'regular_files': manifest['regular_files'], 'child_directories': manifest['child_directories'],
        'manifest': {'path': 'INITIAL_MANIFEST.json', 'bytes': manifest_path.stat().st_size, 'sha256': sha(manifest_path.read_bytes())},
        'source': {'files': 43, 'child_directories': 7, 'all_bytes_modes_hidden_empty_topology_preserved': True,
                   'before_snapshot_sha256': sha((OWN / 'SOURCE_BEFORE.json').read_bytes()),
                   'after_snapshot_sha256': sha((OWN / 'SOURCE_AFTER.json').read_bytes()),
                   'SOURCE_FINAL_sha256': 'f7bc05f4e7d56f0fbad45d77bdb4992d9fd92de8d976bdc5ff3b446f7dbfe9c8',
                   'SOURCE_MANIFEST_sha256': '53be96c6f47deccccc173286d10bdf46b50df4f237c985f42f2da8a69d8c8ffb',
                   'root_adoption_sha256': before['root_adoption_sha256']},
        'original_coverage': {'main_tex_lines': 247, 'main_tex_bytes': 12066,
                              'main_tex_sha256': 'f9566f03e925bc2cff721fc80d231276733a4540d27450589da98df6c229cfe8',
                              'outer_PDF_bytes': 67264, 'outer_PDF_pages': 4,
                              'outer_PDF_sha256': '483a6edff90202ef4d31560049a32ce946dcd1c6a999ab5b1f25b66a8f326612',
                              'all_fresh_page_texts_read': True, 'all_fresh_page_images_individually_personally_viewed': True,
                              'complete_native_API_HTML_Description_metadata_read': True},
        'native_asset_order': ['paper.pdf', 'source-and-verification.zip'], 'embedded_PDF_count': 0,
        'native_version_field_present': False, 'native_version': None,
        'HTML_host_version_label_only': 'v1', 'declared_publication_date': '2026-10-06',
        'created': '2026-10-07T05:32:38.758232+00:00', 'modified': '2026-10-10T21:25:06.224514+00:00',
        'license': 'cc-by-4.0', 'exposure_ledger': 'EXPOSURE_LEDGER.json',
        'own_pre_Description_derivation': {'path': 'OWN_DERIVATION_PRE_METADATA.md', 'sha256': sha((OWN / 'OWN_DERIVATION_PRE_METADATA.md').read_bytes())},
        'private_initial_scientific_notes': {'path': 'INITIAL_ANALYSIS.md', 'sha256': sha((OWN / 'INITIAL_ANALYSIS.md').read_bytes())},
        'packaged_README_support_audit_code_or_imported_primary_body_semantic_exposure': False,
        'native_author_assertions_exposed_as_declared': True,
        'scientific_execution_import_AST_compile_build_test_repair': 0,
        'network_Git_W_Sheet_deploy_AA_redirect_release_Zenodo_mutation_contact_outreach_children': 0,
        'INITIAL_completion_percent': 100, 'overall_scientific_review_estimate_percent': 30,
        'follow_up': None, 'action_authority': False,
        'quiescent': True, 'continuation_requires_root_checkpoint_explicit_RESUME_and_new_sibling': True}
(OWN / 'INITIAL_SEAL.json').write_text(json.dumps(seal, indent=2, sort_keys=True) + '\n')
