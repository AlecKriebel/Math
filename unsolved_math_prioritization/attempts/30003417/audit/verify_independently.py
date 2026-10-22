#!/usr/bin/env python3
"""Independent integrity/scope/provenance verifier. Not a transfinite proof assistant.
No imports from, and no mutation of, the author packet. Python standard library only.
"""
import argparse
import copy
import hashlib
import io
import itertools
import json
from pathlib import Path
import stat
import zipfile
import warnings

ZIP_BYTES = 23352
ZIP_SHA = '69a2cea3fb5fcc1568d0bd538f5738d53ff7208b3b1c021d25f6b642cbdfbd4e'
NAMES = {'EXACT_CONTROLS.json', 'MANIFEST.json', 'README.md', 'REPORT.md',
         'RESEARCH_LOG.md', 'RETAINED_PROOFS.md', 'SOURCE_VERIFICATION.json',
         'VERIFICATION.json', 'verify_packet.py'}
DATASETS = {
 'problems.json': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
 'research_results.json': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')}
CATALOG = (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566')
CATALOG_GIT = 'bd5c23e4e6c7e1901717a7e596477a7f6dc72425'
STATEMENT_SHA = '95510472b00f597ee20b5d3b689d5638f605d14ea868458f0e114d9cfbf98296'
REVIEW_SHA = 'c4b6b81057cb7365d95fc908415f318373e18be6d655021fe9eeca8b14a1eb9e'
PDF_NAMES = ['owr2017.pdf', 'bbfm2018.pdf', 'degenerate2022.pdf', 'higherbaire.pdf',
             'horizontal2025.pdf', 'compactness2025v2.pdf', 'compactness.pdf', 'singular2026v2.pdf']


def require(condition, label):
    if not condition:
        raise ValueError(label)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check_bytes(data, expected, label):
    require((len(data), digest(data)) == expected, 'byte/hash mismatch: ' + label)


def archive_map(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        items = z.infolist()
        require(len(items) == len(NAMES), 'ZIP entry count')
        require(len({i.filename for i in items}) == len(items), 'ZIP duplicate member')
        require({i.filename for i in items} == NAMES, 'ZIP allowlist')
        for i in items:
            require('/' not in i.filename and '\\' not in i.filename, 'ZIP path')
            require(not i.is_dir(), 'ZIP directory')
            require(not stat.S_ISLNK(i.external_attr >> 16), 'ZIP symlink')
            require(not (i.flag_bits & 1), 'ZIP encryption')
        require(z.testzip() is None, 'ZIP CRC')
        return {i.filename: z.read(i) for i in items}


def controls_check(c):
    require(c['problem_id'] == 30003417 and c['problem_number'] == 'OWR-15216-023' and c['rank'] == 735, 'identity')
    h = c['hypotheses']
    require(h == {
        'kappa_uncountable': True, 'kappa_regular': True,
        'two_to_less_than_kappa_equals_kappa': True,
        'kappa_strongly_inaccessible_required': False, 'kappa_successor_required': False,
        'kappa_weakly_compact_required': False, 'kappa_supercompact_required': False,
        'two_to_kappa_equals_successor_required': False}, 'hypotheses')
    require(c['space'] == '2^kappa', 'space')
    require(c['topology'] == 'bounded topology, cylinders from initial segments of ordinal length below kappa', 'topology')
    require(c['meager'] == 'union of at most kappa nowhere dense sets', 'meager union convention')
    require(c['cofinality_order'] == 'ordinary subset inclusion in the meager ideal', 'cofinality order')
    require(c['domination'] == 'eventual coordinatewise domination modulo a bounded subset of kappa', 'domination order')
    require(c['target_parts'] == ['add(M_kappa)=b_kappa', 'cof(M_kappa)=d_kappa'], 'target parts')
    require(c['equivalent_missing_inequalities'] == ['b_kappa<=cov(M_kappa)', 'non(M_kappa)<=d_kappa'], 'remaining gap')
    require(c['retained_known_formulas'] == ['add(M_kappa)=min(b_kappa,cov(M_kappa))', 'cof(M_kappa)=max(d_kappa,non(M_kappa))'], 'known formulas')
    require(c['neither_part_resolved'] is True, 'no resolution')
    for k in ['countermodel_constructed', 'independence_proved', 'novelty_claimed',
              'full_resolution_claimed', 'combinatorial_ideal_identified_with_topological_ideal_at_successors',
              'degenerate_arithmetic_used_as_counterexample', 'singular_results_used_as_regular_results',
              'compactness_models_used_as_universal_theorem']:
        require(c[k] is False, k)
    require(c['approach_count'] == 5, 'five approach count')
    require(c['completion_estimate_new_full_resolution_percent'] == 0, 'completion estimate')
    require(c['recommended_disposition_after_audit'] == 'exhausted_no_resolution', 'disposition')
    require(c['independent_audit_status'] == 'pending', 'historical freeze status')


def verify_author(root):
    raw = (root / 'MEAGER_30003417_SAFE_PACKET.zip').read_bytes()
    check_bytes(raw, (ZIP_BYTES, ZIP_SHA), 'frozen ZIP')
    payload = archive_map(raw)
    safe = root / 'safe_output'
    require({p.name for p in safe.iterdir()} == NAMES, 'adjacent safe directory allowlist')
    for p in safe.iterdir():
        require(p.is_file() and not p.is_symlink(), 'safe member type')
        require(p.read_bytes() == payload[p.name], 'ZIP/directory divergence: ' + p.name)
    m = json.loads(payload['MANIFEST.json'])
    require(set(m['files']) == NAMES - {'MANIFEST.json'}, 'author manifest coverage')
    for name, entry in m['files'].items():
        check_bytes(payload[name], (entry['bytes'], entry['sha256']), name)
    receipt = json.loads((root / 'FREEZE_RECEIPT.json').read_text())
    require(receipt['bytes'] == ZIP_BYTES and receipt['sha256'] == ZIP_SHA, 'freeze receipt')
    require(receipt['manifest_sha256'] == digest(payload['MANIFEST.json']), 'manifest anchor')
    c = json.loads(payload['EXACT_CONTROLS.json'])
    controls_check(c)
    source = json.loads(payload['SOURCE_VERIFICATION.json'])
    require(source['remote_writes_performed'] is False, 'author remote-write flag')
    return payload, c, source


def order_tests():
    counts = {'admissible_assignments': 0, 'first_strict': 0, 'second_strict': 0, 'both_strict': 0}
    for b, d, cov, non in itertools.product(range(1, 9), repeat=4):
        if d < b or non < b or d < cov:
            continue
        counts['admissible_assignments'] += 1
        add, cof = sorted((b, cov))[0], sorted((d, non))[-1]
        require((add == b) == (b <= cov), 'add equivalence')
        require((cof == d) == (non <= d), 'cof equivalence')
        require((add < b) == (cov < b), 'add strict equivalence')
        require((d < cof) == (d < non), 'cof strict equivalence')
        require(b != 1 or add == b, 'smallest b special case')
        require(d != 8 or cof == d, 'largest d special case')
        counts['first_strict'] += add < b
        counts['second_strict'] += d < cof
        counts['both_strict'] += add < b and d < cof
    require(counts['both_strict'] > 0, 'strict logical witnesses exist')
    # Ordered labels only. These are not models of set theory.
    witnesses = {
      'cov_below_d_but_equal_b': {'b': 1, 'd': 2, 'cov': 1, 'non': 1},
      'minmax_not_first_target': {'b': 2, 'd': 2, 'cov': 1, 'non': 2},
      'minmax_not_second_target': {'b': 1, 'd': 1, 'cov': 1, 'non': 2},
      'both_targets_can_fail_in_order_logic': {'b': 2, 'd': 2, 'cov': 1, 'non': 3}}
    return {**counts, 'witnesses': witnesses, 'realizability_claimed': False,
            'transfinite_proofs_verified_by_computation': False}


def check_identity(records, reports):
    ids = [i for i, r in enumerate(records) if r.get('id') == 30003417]
    codes = [i for i, r in enumerate(records) if r.get('problem_number') == 'OWR-15216-023']
    require(ids == codes == [12201], 'unique target join')
    require('OWR-15216-023' not in reports, 'no separate target report')
    p = records[12201]
    require(digest(p['statement'].encode()) == STATEMENT_SHA, 'statement digest')
    review = json.dumps([p, {}], sort_keys=True).encode()
    require(digest(review) == REVIEW_SHA, 'review digest')
    return p


def source_checks(source_dir, catalog, source_metadata):
    out = {'scope': 'Full supplied local bytes independently hashed against the pinned public repository metadata; no fresh corpus download claimed.'}
    for filename, expected in DATASETS.items():
        b = (source_dir / filename).read_bytes()
        check_bytes(b, expected, filename)
        out[filename] = {'bytes': len(b), 'sha256': digest(b), 'match': True}
    records = json.loads((source_dir / 'problems.json').read_text())
    reports = json.loads((source_dir / 'research_results.json').read_text())
    require(len(records) == 15458 and len(reports) == 6701, 'corpus cardinalities')
    check_identity(records, reports)
    require(b'30003417' not in (source_dir / 'research_results.json').read_bytes(), 'numeric ID absent from reports bytes')
    out['target'] = {'unique_index': 12201, 'statement_sha256': STATEMENT_SHA, 'review_sha256': REVIEW_SHA,
                     'separate_report_present': False, 'numeric_id_in_report_bytes': False}
    pdfs = []
    require(len(source_metadata['sources']) == len(PDF_NAMES), 'scholarly source count')
    for filename, meta in zip(PDF_NAMES, source_metadata['sources']):
        b = (source_dir / filename).read_bytes()
        check_bytes(b, (meta['bytes'], meta['sha256']), filename)
        require(b.startswith(b'%PDF-'), 'PDF signature')
        pdfs.append({'title': meta['title'], 'url': meta['url'], 'bytes': len(b), 'sha256': digest(b), 'match': True})
    out['scholarly_pdf_byte_checks'] = pdfs
    if catalog:
        b = catalog.read_bytes()
        check_bytes(b, CATALOG, 'full catalog')
        blob = hashlib.sha1(('blob ' + str(len(b)) + '\0').encode() + b).hexdigest()
        require(blob == CATALOG_GIT, 'catalog Git blob')
        matches = [r for r in json.loads(b) if r['id'] == '30003417']
        require(len(matches) == 1, 'unique catalog record')
        r = matches[0]
        require(r['rank'] == 735 and r['statement_hash'] == STATEMENT_SHA and r['review_hash'] == REVIEW_SHA, 'catalog identity')
        require(r == json.loads((source_dir / 'catalog-record.json').read_text()), 'selected catalog record')
        out['catalog'] = {'bytes': len(b), 'sha256': digest(b), 'git_blob_sha1': blob, 'target_count': 1, 'descriptor_matches': True}
    return out


def make_zip(payload, change=None):
    buf = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        with zipfile.ZipFile(buf, 'w') as z:
            for name, data in payload.items():
                info = zipfile.ZipInfo(name)
                if change == 'symlink' and name == 'README.md':
                    info.create_system = 3
                    info.external_attr = (stat.S_IFLNK | 0o777) << 16
                z.writestr(info, data)
            if change == 'duplicate':
                z.writestr('README.md', b'duplicate')
    return buf.getvalue()


def negative_tests(payload, controls):
    accepted = []
    def rejected(label, fn):
        try:
            fn()
        except (ValueError, KeyError, zipfile.BadZipFile):
            accepted.append(label)
        else:
            raise ValueError('negative control was accepted: ' + label)
    for key, value in [('kappa_regular', False), ('kappa_uncountable', False),
                       ('two_to_less_than_kappa_equals_kappa', False), ('kappa_strongly_inaccessible_required', True)]:
        c = copy.deepcopy(controls); c['hypotheses'][key] = value
        rejected('changed_' + key, lambda c=c: controls_check(c))
    for key, value in [('meager', 'countable union of nowhere dense sets'),
                       ('cofinality_order', 'inclusion modulo meager sets'),
                       ('full_resolution_claimed', True), ('countermodel_constructed', True),
                       ('target_parts', ['add(M_kappa)=min(b_kappa,cov(M_kappa))']),
                       ('equivalent_missing_inequalities', ['cov(M_kappa)<=b_kappa', 'non(M_kappa)<=d_kappa'])]:
        c = copy.deepcopy(controls); c[key] = value
        rejected('changed_' + key, lambda c=c: controls_check(c))
    for label, name in [('source_pdf_in_payload', 'paper.pdf'), ('zip_traversal', '../README.md')]:
        p = dict(payload); p.pop('README.md'); p[name] = b'x'
        rejected(label, lambda p=p: archive_map(make_zip(p)))
    rejected('zip_duplicate', lambda: archive_map(make_zip(payload, 'duplicate')))
    rejected('zip_symlink', lambda: archive_map(make_zip(payload, 'symlink')))
    rejected('corrupted_archive', lambda: archive_map(b'not a ZIP'))
    rejected('wrong_byte_hash', lambda: check_bytes(b'tampered', (8, '0' * 64), 'synthetic mutation'))
    require(len(accepted) == 16, 'negative control count')
    return {'rejected_mutations': accepted, 'count': len(accepted), 'all_rejected': True,
            'scope': 'Integrity and semantic-control mutations, not counterexamples to transfinite mathematics.'}


def freeze_check(root, audit_dir):
    baseline = json.loads((audit_dir / 'AUTHOR_FREEZE_BASELINE.json').read_text())
    for name, meta in baseline['files'].items():
        check_bytes((root / name).read_bytes(), (meta['bytes'], meta['sha256']), 'unchanged author freeze ' + name)
    return {'files_checked': len(baseline['files']), 'unchanged': True}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--author-root', type=Path, required=True)
    p.add_argument('--source-dir', type=Path)
    p.add_argument('--catalog', type=Path)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    payload, controls, source = verify_author(a.author_root)
    result = {'status': 'PASS', 'scope': 'Independent executable integrity, exact controls, order logic and optional local-source byte checks only.',
              'problem_id': 30003417, 'frozen_zip': {'bytes': ZIP_BYTES, 'sha256': ZIP_SHA},
              'author_payload_files': len(payload), 'order_logic': order_tests(),
              'negative_controls': negative_tests(payload, controls),
              'freeze': freeze_check(a.author_root, Path(__file__).resolve().parent),
              'infinite_cardinal_proofs_formally_verified': False}
    if a.source_dir:
        result['source_checks'] = source_checks(a.source_dir, a.catalog, source)
    else:
        result['source_checks'] = {'status': 'NOT_RUN', 'reason': 'No source directory supplied.'}
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if a.output:
        a.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
