#!/usr/bin/env python3
"""Read-only input inventory audit; writes only a review-owned JSON receipt."""
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import runpy
import sys
import zipfile

ROOT = Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1001_6900004')
P = ROOT / 'publication'
O = ROOT / 'reviews' / 'package_02'


def need(value, message):
    if not value:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    manifest = json.loads((P/'PACKAGE_MANIFEST.json').read_text())
    rows = manifest['files']
    names = [row['path'] for row in rows]
    need(len(names) == len(set(names)), 'duplicate manifest path')
    for row in rows:
        path = PurePosixPath(row['path'])
        need(not path.is_absolute() and '..' not in path.parts, 'unsafe manifest path')
        data = (P/row['path']).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'manifest byte mismatch')
    archive = P/'full_stress_stratifications_source_verification_v1.zip'
    prefix = 'full_stress_stratifications_v1/'
    expected = set(names) | {'PACKAGE_MANIFEST.json'}
    with zipfile.ZipFile(archive) as z:
        need(z.testzip() is None, 'zip CRC failure')
        members = z.namelist()
        need(len(members) == len(set(members)), 'duplicate zip member')
        need(all(name.startswith(prefix) for name in members), 'unexpected archive root')
        archived = {name[len(prefix):] for name in members}
        need(archived == expected, 'archive inventory differs from manifest')
        for member in members:
            name = member[len(prefix):]
            need(z.read(member) == (P/name).read_bytes(), 'archive/local byte mismatch')
            need((z.getinfo(member).external_attr >> 16) & 0o170000 != 0o120000,
                 'archive symlink')
        need(all(not name.endswith('.pdf') or name == 'research_note.pdf' for name in archived),
             'unexpected external PDF redistributed')

    metadata = json.loads((P/'metadata.json').read_text())
    deposit = json.loads((P/'zenodo-deposit.json').read_text())
    need(metadata == deposit['metadata'], 'metadata differs between files')
    need(metadata['creators'] == [{'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher',
                                 'orcid': '0009-0001-9320-500X'}], 'creator metadata differs')
    need(metadata['publication_type'] == 'preprint' and metadata['upload_type'] == 'publication',
         'incorrect publication type')
    need(metadata['license'] == 'cc-by-4.0' and metadata['access_right'] == 'open',
         'license or access differs')

    links = []
    for relative in ('README.md', 'SUPPLEMENT.md', 'evidence/README.md'):
        source = P/relative
        for target in re.findall(r'\]\(([^)]+)\)', source.read_text()):
            if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', target):
                continue
            path = source.parent/target.split('#', 1)[0]
            need(path.exists(), 'broken portable link: '+relative+' -> '+target)
            need(path.resolve().is_relative_to(P), 'portable link escapes package')
            links.append({'source': relative, 'target': target})

    # Preserved originals must match the pinned PR snapshot, not freshly rewritten claims.
    submitted = json.loads((P/'evidence/SUBMITTED_PINS.json').read_text())
    srows = {row['relative']: row for row in submitted['files']}
    historic_matches = []
    for name in ('REPORT.md', 'ACCEPTANCE.md', 'STATUS.json'):
        data = (P/'evidence/submitted'/name).read_bytes()
        need(sha(data) == srows[name]['sha256'], 'submitted historical record rewritten')
        historic_matches.append(name)
    for name in ('check_collision_witness.py', 'independent_kernel_check.py'):
        data = (P/'checks'/name).read_bytes()
        need(sha(data) == srows[name]['sha256'], 'submitted checker changed')
        historic_matches.append('checks/'+name)
    # First round's own preserved output manifest checks original byte identities.
    first = P/'evidence/package_review_01'
    stage = json.loads((first/'REVIEW_OUTPUT_MANIFEST.json').read_text())
    included, omitted = [], []
    for row in stage['files']:
        path = first/row['name']
        if path.exists():
            data = path.read_bytes()
            need(len(data) == row['bytes'] and sha(data) == row['sha256'],
                 'first-stage report changed')
            included.append(row['name'])
        else:
            omitted.append(row['name'])

    sources = {name: sha((P/name).read_bytes()) for name in
               ('run_checks.py', 'checks/check_collision_witness.py',
                'checks/independent_kernel_check.py', 'checks/independent_exact_check.py')}
    for name in sources:
        tree = ast.parse((P/name).read_text())
        need(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
             'guard relies on assert: '+name)
    runner = runpy.run_path(str(P/'run_checks.py'), run_name='review_import')
    eq = runner['exact_json_equal']
    comparisons = (
        ({'n': True}, {'n': 1}, False), ({'n': 1.0}, {'n': 1}, False),
        ({'a': [1, False]}, {'a': [1, 0]}, False),
        ({'a': [1, {'v': False}]}, {'a': [1, {'v': 0}]}, False),
        ({'a': 1}, {'a': 1, 'b': 2}, False),
        ({'a': [1, 2]}, {'a': [2, 1]}, False),
        ({'a': None}, {'a': False}, False),
        ({'a': {'b': [1, True, None]}}, {'a': {'b': [1, True, None]}}, True),
        ({'x': 'PASS', 'y': 2}, {'y': 2, 'x': 'PASS'}, True),
    )
    for a, b, wanted in comparisons:
        need(eq(a, b) is wanted, 'strict JSON comparator accepted an unintended type')
    gate = json.loads((P/'evidence/CURRENT_REVIEW_STATE.json').read_text())
    need(gate['preprint_ready_for_immutable_publication'] is False,
         'premature completed review gate')
    result = {
        'status': 'PASS', 'manifest_file_count': len(rows),
        'archive_file_count': len(expected), 'archive_sha256': sha(archive.read_bytes()),
        'pdf_sha256': sha((P/'research_note.pdf').read_bytes()),
        'all_archive_members_match_package_bytes': True,
        'all_manifest_members_match_hash_and_size': True,
        'metadata_exactly_equal': True, 'portable_links_checked': links,
        'submitted_original_records_hash_match': historic_matches,
        'first_stage_included_records_preserved': included,
        'first_stage_omitted_extraction_record': omitted,
        'source_hashes': sources, 'strict_json_comparator_cases': len(comparisons),
        'all_guards_survive_optimization_by_explicit_exceptions': True,
        'pending_review_gate_honest': True,
        'limits': 'Archive and stage manifests have distinct documented roles; omitted historic source bodies and extraction artifacts are not claimed to be included.'
    }
    (O/'PACKAGE_INTEGRITY_CHECK.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ('portable_links_checked', 'first_stage_included_records_preserved', 'source_hashes')}, indent=2))


if __name__ == '__main__':
    main()
