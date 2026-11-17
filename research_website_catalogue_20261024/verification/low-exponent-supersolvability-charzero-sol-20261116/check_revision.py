#!/usr/bin/env python3
"""MIT licensed. Read-only static data checks for the bounded private COPY-1.

This program reads exact local packet files and the one pinned root clearance.
It does not import native/scientific code, write files, spawn processes, browse,
use a network, render, inspect other reviews, or certify scientific findings.
Stdout is its only output; the caller separately retains stdout and stderr.
"""
from pathlib import Path
import hashlib
import json
import re
import stat
from datetime import datetime, timezone
from html.parser import HTMLParser


BASE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification')
OWN = BASE / 'low-exponent-supersolvability-charzero-sol-20261116'
OLD = BASE / 'low-exponent-supersolvability-editorial-sol-20261116'
CLEARANCE = BASE / 'root-clearance-23331709-20261116.json'
BEFORE = b'A relation-incidence proof that free central arrangements with nonzero exponents 1 or 2 and at most one 3 are supersolvable, with matching-work credit.'
AFTER = b'Supersolvability in characteristic zero for finite central free arrangements of distinct hyperplanes with nonzero exponents 1 or 2 and at most one 3.'
CHANGES = {'index.html': 2, 'HEAD.html': 2, 'model.json': 1}
INPUTS = ['index.html', 'HEAD.html', 'MAIN.html', 'model.json', 'citation.bib',
          'EXPECTED_ABSTRACT.txt', 'low_exponent_supersolvability.pdf',
          'low_exponent_verification.zip']
OLD_NAMES = {
    'CHECK_READ.json', 'EXECUTION.json', 'EXPECTED_ABSTRACT.txt', 'FINAL.json',
    'HEAD.html', 'LICENSE_CODE.txt', 'LICENSES.md', 'MAIN.html',
    'OWNED_MANIFEST.json', 'REPORT.md', 'RESEARCH_LOG.md', 'SOURCES.json',
    'check.final.stderr.txt', 'check.final.stdout.json', 'check.stderr.txt',
    'check.stdout.json', 'check_copy.py', 'citation.bib', 'index.html',
    'low_exponent_supersolvability.pdf', 'low_exponent_verification.zip', 'model.json'
}
OWN_NAMES = set(INPUTS) | {
    'ORIGINAL_REFERENCE.json', 'REVISION_RECEIPT.json', 'RESEARCH_LOG.md',
    'REPORT.md', 'LICENSE_CODE.txt', 'LICENSES.md', 'check_revision.py',
    'CHECK_READ.json', 'check.stdout.json', 'check.stderr.txt', 'EXECUTION.json',
    'OWNED_MANIFEST.json', 'FINAL.json'
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin(path, name):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), ('nonregular', str(path))
    data = path.read_bytes()
    return {'path': name, 'type': 'regular',
            'mode': format(stat.S_IMODE(info.st_mode), '04o'),
            'bytes': len(data), 'sha256': digest(data)}


def flat_inventory(root, names):
    assert root.is_dir() and not root.is_symlink()
    assert format(stat.S_IMODE(root.lstat().st_mode), '04o') == '0755'
    actual = list(root.iterdir())
    assert {p.name for p in actual} == names, ('extent mismatch', str(root))
    rows = [pin(p, p.name) for p in sorted(actual, key=lambda p: p.name)]
    assert all(row['mode'] == '0644' for row in rows)
    return rows


class Metadata(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.meta = []
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta':
            self.meta.append(attrs)
        if tag == 'link':
            self.links.append(attrs)

    def value(self, key, name):
        rows = [row['content'] for row in self.meta if row.get(key) == name]
        assert len(rows) == 1, (key, name, rows)
        return rows[0]


def main():
    original = flat_inventory(OLD, OLD_NAMES)
    reference = json.loads((OWN / 'ORIGINAL_REFERENCE.json').read_text())
    assert reference['original_root'] == str(OLD)
    assert reference['files'] == original
    assert reference['regular_files'] == 22 and reference['child_directories'] == 0
    old_map = {row['path']: row for row in original}
    assert old_map['FINAL.json']['bytes'] == 10446
    assert old_map['FINAL.json']['sha256'] == '6d2d89ace44b565c9a523c4beaaa375e5f66131f79c8c94b5ddf7715d746fe1b'
    assert old_map['OWNED_MANIFEST.json']['bytes'] == 5521
    assert old_map['OWNED_MANIFEST.json']['sha256'] == '03f5e41139040d259036ae5646aad5248e622612aa6f79ec3aed9e2104835f85'
    manifest = json.loads((OLD / 'OWNED_MANIFEST.json').read_text())
    assert {row['path'] for row in manifest['files']} == OLD_NAMES
    for row in manifest['files']:
        if row['path'] not in {'FINAL.json', 'OWNED_MANIFEST.json'}:
            assert row == old_map[row['path']]
    clearance = pin(CLEARANCE, str(CLEARANCE))
    assert clearance['bytes'] == 2388
    assert clearance['sha256'] == '94df1cd5e29413a1db22e5e25ccc290e5a649c22b1d3aa21b2be0ef88b887144'
    assert reference['root_clearance'] == clearance
    receipt = json.loads((OWN / 'REVISION_RECEIPT.json').read_text())
    assert receipt['root_clearance'] == clearance
    assert receipt['description_before'] == BEFORE.decode()
    assert receipt['description_after'] == AFTER.decode()
    assert receipt['total_deliverable_text_replacements'] == 5
    assert receipt['old_fact_packet_certifies_revision'] is False
    assert receipt['new_scientific_review_or_native_execution'] is False
    output_pins = []
    for name in INPUTS:
        old_data = (OLD / name).read_bytes()
        new_data = (OWN / name).read_bytes()
        if name in CHANGES:
            assert old_data.count(BEFORE) == CHANGES[name]
            assert old_data.count(AFTER) == 0
            assert new_data == old_data.replace(BEFORE, AFTER)
            assert new_data.count(AFTER) == CHANGES[name]
            assert new_data.count(BEFORE) == 0
        else:
            assert new_data == old_data
        output_pins.append(pin(OWN / name, name))
    index = (OWN / 'index.html').read_text()
    head = (OWN / 'HEAD.html').read_text()
    old_index = (OLD / 'index.html').read_text()
    assert re.findall(r'<body\b[^>]*>.*?</body>', index, re.S) == re.findall(r'<body\b[^>]*>.*?</body>', old_index, re.S)
    assert index[index.index('<head>'):index.index('</head>') + 7] == head.rstrip('\n')
    abstract = (OWN / 'EXPECTED_ABSTRACT.txt').read_text().rstrip('\n')
    model = json.loads((OWN / 'model.json').read_text())
    old_model = json.loads((OLD / 'model.json').read_text())
    old_model['description'] = AFTER.decode()
    assert model == old_model
    assert model['abstract'] == model['schema']['abstract'] == abstract
    for text in (index, head):
        meta = Metadata(text)
        assert meta.value('name', 'description') == AFTER.decode()
        assert meta.value('property', 'og:description') == AFTER.decode()
        assert meta.value('name', 'DC.description') == abstract
        assert meta.value('name', 'robots') == 'noindex, nofollow'
        assert not any(link.get('rel') == 'canonical' for link in meta.links)
    assert f'<p id="original-abstract">{abstract}</p>' in index
    for key in ['canonical', 'base_url', 'production_url', 'AA']:
        assert model[key] is None
    assert model['publication_authority'] is False and model['private_noindex'] is True
    assert model['deployment_metadata']['status'] == 'PROPOSED_ONLY_ROOT_ADOPTION_REQUIRED'
    assert model['native_order'] == INPUTS[-2:]
    owned = flat_inventory(OWN, OWN_NAMES)
    read_receipt = json.loads((OWN / 'CHECK_READ.json').read_text())
    helper = pin(OWN / 'check_revision.py', 'check_revision.py')
    assert read_receipt['helper'] == helper
    assert read_receipt['entire_current_body_personally_read_before_execution'] is True
    assert read_receipt['authorized_ordinary_invocations'] == 1
    print(json.dumps({
        'schema': 'charzero-revision-static-check-result-v1',
        'UTC': datetime.now(timezone.utc).isoformat(),
        'status': 'PASS', 'ordinary_invocation': 1,
        'original_all22_files_exact_pins_extent_modes_unchanged': True,
        'pinned_root_clearance_unchanged': True,
        'approved_replacements': CHANGES, 'total_replacements': 5,
        'eight_deliverable_pins': output_pins,
        'all_other_deliverable_bytes_body_full_abstract_native_unchanged': True,
        'private_null_noindex_full_proposed_url_plan_preserved': True,
        'owned_extent_at_check': {'regular_files': len(owned), 'child_directories': 0,
                                  'all_hidden_ignored_empty_streams_included': True},
        'helper': helper, 'read_receipt': pin(OWN / 'CHECK_READ.json', 'CHECK_READ.json'),
        'scope': 'Static metadata-only data check; no scientific, live-render, native-reader or independent fact certification.',
        'finalization_after_check': 'Execution receipt, log/report and terminal finite closure are written afterward by the caller; this result does not hash their final contents.'
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
