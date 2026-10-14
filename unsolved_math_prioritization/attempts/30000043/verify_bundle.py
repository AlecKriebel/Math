#!/usr/bin/env python3
"""Strict integrity validation of the canonical-tight wavelet reader.

This checks file membership, pins, claim flags, and recorded replay evidence.
It does not certify mathematical truth. All checks remain active with -O/-OO.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parent
ANCHORS = {
    'accepted/core/COUNTEREXAMPLE.md': '8c943a270c9b35d0cf3ddef2b94de5ec8bbbcb4ec45deca81d28fd2228e522a1',
    'accepted/core/CONSTRUCTION_CONTRACT.md': '3fb43063cba5f31579efbc0f4272f39db3caab7d9bcf297874d536c76a017d90',
    'accepted/audit_a/ACCEPTED_AUDIT.md': '1fc355da72d93121de4db00658e4a2c130c94eb03831a24925d3752bf52cc964',
    'accepted/audit_b/INDEPENDENT_HAAR_CHECK.md': '58ed145c605d3568b6592474a9566fe5c05d31cbac535db59395feb38f214c1f',
    'optional_bridge/BRIDGE_LEMMA.md': 'aeedf3442b91df6d1f9316fccb8f60d99f422cd3a94f457086cef14867728c35',
    'optional_bridge/BRIDGE_ACCEPTANCE_AUDIT.md': '60f2cb9cf0b0f7fa5ca649f00df10250e1b8e35fa710648c8c38126ffaad23ba',
    'scope_adjudication/SOURCE_SCOPE_ADJUDICATION.md': 'df9083443c2149658f738085844d796341c75d3fa0ba769454b802bd8c530edd',
    'scope_adjudication/SOURCE_METADATA.json': 'e344116bbc7802356e35facf283bc628d199bfd369cb6fc953f995d25d425f09',
    'scope_adjudication/PROOF_PINS.json': 'ed9fad3adefa37d58a7789055de26b3a085c63ee08b13b8bc914b2dd3a3bf903',
    'scope_adjudication/PUBLIC_MANIFEST.json': '5b9eb1747b9dea70f593cef0f6c20bb1083d985051c4cb35381b3e7beca7cb49',
}
SCOPE = {'fixed_dilation': True, 'fixed_translation_lattice': True,
         'fixed_natural_indexing': True, 'single_generator': True,
         'all_of_L2_R': True, 'direct_inverse_square_root_proof': True,
         'arbitrary_reindexing_claim': False, 'novelty_claim': False,
         'literature_wide_current_open_status_claim': False,
         'optional_bridge_required_for_counterexample': False}
COLLECTIONS = {'accepted', 'optional_bridge', 'scope_adjudication'}

INPUT_MANIFEST_SHA256 = '84665ba08d69150f7a0e21e5ee3959a080aff6680e2a93ef9e9897f2ef84bc18'
EDITORIAL_CHANGES = {'README.md', 'VALIDATION.md', 'SOURCE_METADATA.json',
                     'verify_bundle.py', 'test_negative_controls.py'}
REQUIRED_FILES = {'LINK_REVIEW.json', 'accepted/core/COUNTEREXAMPLE.md', 'scope_adjudication/SOURCE_METADATA.json', 'MANIFEST.json', 'INTEGRATION_EVIDENCE.json', 'PUBLICATION_BOUNDARY.md', 'INPUT_MANIFEST.json', 'SOURCE_METADATA.json', 'accepted/audit_b/INDEPENDENT_HAAR_CHECK.md', 'verify_bundle.py', 'test_negative_controls.py', 'optional_bridge/BRIDGE_ACCEPTANCE_AUDIT.md', 'scope_adjudication/SOURCE_SCOPE_ADJUDICATION.md', 'optional_bridge/BRIDGE_LEMMA.md', 'diagnostics/check_stated_constants.py', 'scope_adjudication/PROOF_PINS.json', 'scope_adjudication/PUBLIC_MANIFEST.json', 'SCHOLARLY_NOTES.md', 'README.md', 'ORIGINAL_ARTIFACTS.json', 'VALIDATION.md', 'replay_diagnostics.py', 'accepted/core/CONSTRUCTION_CONTRACT.md', 'INTEGRATION_ACCEPTANCE.md', 'REPLAY_EVIDENCE.json', 'accepted/audit_a/ACCEPTED_AUDIT.md'}
EXPECTED_VALUES = {'epsilon': '1/100', 'q': '201/10000',
                   'lower_frame_bound': '9801/10000', 'upper_frame_bound': '10201/10000',
                   'stated_error_factor': '3937/200', 'stated_defect_threshold': '1/1000'}
EXPECTED_CHECKS = {'epsilon_is_one_hundredth', 'lower_frame_bound', 'upper_frame_bound',
                   'q', 'q_less_than_three_epsilon', 'q_less_than_one_half',
                   'remainder_bound', 'adjusted_remainder_bound', 'stated_error_factor',
                   'error_factor_less_than_twenty', 'error_bound', 'displayed_defect_threshold'}
MANIFEST_KEYS = {'scope_flags', 'mathematical_passes_added_by_packaging', 'title', 'problem_id', 'files', 'schema_version', 'disposition', 'publication_performed', 'queue_row'}



def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON object key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(RuntimeError('Non-finite JSON number')))


def relative(root, name):
    require(isinstance(name, str) and name and '\\' not in name, 'Invalid relative path')
    path = PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts and path.as_posix() == name,
            'Unsafe or noncanonical relative path')
    target = root / name
    require(root in target.resolve().parents, 'Reference escapes reader root')
    return target


def check_pin(root, name, count, sha):
    require(type(count) is int and count >= 0, 'Invalid byte count')
    require(isinstance(sha, str) and re.fullmatch('[0-9a-f]{64}', sha), 'Invalid SHA-256')
    data = relative(root, name).read_bytes()
    require(len(data) == count, 'Byte count mismatch: ' + name)
    require(digest(data) == sha, 'SHA-256 mismatch: ' + name)


def verify(root):
    root = root.resolve()
    require(root.is_dir(), 'Reader root does not exist')
    manifest = read_json(root / 'MANIFEST.json')
    require(set(manifest) == MANIFEST_KEYS, 'Manifest fields differ from reviewed schema')
    require(manifest['publication_performed'] is False, 'Publication state differs from local preparation')
    require(manifest['disposition'] == 'Negative answer under the usual indexed single-generator interpretation',
            'Disposition differs from accepted scope')
    require(manifest['title'] == 'Direct canonical-tight analysis of a classical wavelet perturbation family',
            'Reader title differs from reviewed identity')
    require(type(manifest.get('schema_version')) is int and manifest.get('schema_version') == 1, 'Manifest schema mismatch')
    require(type(manifest.get('problem_id')) is int and type(manifest.get('queue_row')) is int
            and manifest.get('problem_id') == 30000043 and manifest.get('queue_row') == 1781,
            'Target identity mismatch')
    require(type(manifest.get('scope_flags')) is dict
            and all(type(value) is bool for value in manifest['scope_flags'].values()), 'Scope flags must be booleans')
    require(manifest.get('scope_flags') == SCOPE, 'Scope flags exceed accepted claim')
    require(type(manifest.get('mathematical_passes_added_by_packaging')) is int
            and manifest.get('mathematical_passes_added_by_packaging') == 0, 'Unexpected mathematical-pass claim')
    records = manifest['files']
    require(type(records) is list, 'Invalid manifest file list')
    expected = set()
    for record in records:
        require(type(record) is dict and set(record) == {'path', 'bytes', 'sha256'}, 'Invalid file record')
        relative(root, record['path'])
        require(record['path'] != 'MANIFEST.json', 'Self-referential manifest record')
        require(record['path'] not in expected, 'Duplicate manifest member')
        expected.add(record['path'])
    actual = set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symbolic links are not admitted')
        require(path.is_file() or path.is_dir(), 'Special filesystem node is not admitted')
        if path.is_file():
            require(path.suffix in {'.md', '.json', '.py'}, 'Unexpected file type')
            actual.add(path.relative_to(root).as_posix())
    require(actual == expected | {'MANIFEST.json'}, 'File membership differs from sealed manifest')
    require(actual == REQUIRED_FILES, 'Required reader membership differs')
    for record in records:
        check_pin(root, record['path'], record['bytes'], record['sha256'])
    for name, expected_sha in ANCHORS.items():
        require(digest(relative(root, name).read_bytes()) == expected_sha,
                'Frozen original anchor mismatch: ' + name)

    originals = read_json(root / 'ORIGINAL_ARTIFACTS.json')
    require(originals['editorial_transforms_to_originals'] == [], 'Unexpected transformation of original text')
    names = set()
    for item in originals['originals']:
        require(item['reader_path'] not in names, 'Duplicate original-copy record')
        names.add(item['reader_path'])
        require(item['transformation'] == 'none; exact byte copy', 'Original copy was transformed')
        check_pin(root, item['reader_path'], item['bytes'], item['sha256'])
    original_members = {name for name in actual if name.split('/')[0] in COLLECTIONS}
    require(names == original_members, 'Original pin-map coverage mismatch')
    require(set(ANCHORS).issubset(names), 'Frozen originals missing from copy map')

    require(names == set(ANCHORS), 'Original-copy map differs from frozen original membership')

    embedded_pins = 0
    for filename in ['scope_adjudication/PROOF_PINS.json', 'scope_adjudication/PUBLIC_MANIFEST.json']:
        embedded = read_json(root / filename)['artifacts']
        require(type(embedded) is list and len(embedded) == 3, 'Embedded pin coverage differs')
        labels = set()
        for record in embedded:
            require(type(record) is dict and set(record) == {'artifact', 'bytes', 'sha256'},
                    'Invalid embedded pin record')
            label = record['artifact']
            require(label not in labels, 'Duplicate embedded artifact pin')
            labels.add(label)
            require(type(record['bytes']) is int and record['bytes'] > 0
                    and isinstance(record['sha256'], str)
                    and re.fullmatch('[0-9a-f]{64}', record['sha256']), 'Invalid embedded pin types')
            require(PurePosixPath(label).name == label, 'Unexpected embedded artifact path')
            candidates = [root / name for name in names if PurePosixPath(name).name == label]
            matching = [candidate for candidate in candidates
                        if len(candidate.read_bytes()) == record['bytes']
                        and digest(candidate.read_bytes()) == record['sha256']]
            require(len(matching) == 1, 'Embedded artifact pin does not resolve uniquely: ' + label)
            embedded_pins += 1

    replay = read_json(root / 'REPLAY_EVIDENCE.json')
    require(type(replay['successful_runs']) is int and type(replay['active_runtime_failure_controls']) is int,
            'Replay run counts must be integers')
    require(replay['status'] == 'PASS' and replay['successful_runs'] == 3
            and replay['active_runtime_failure_controls'] == 3, 'Incomplete replay evidence')
    require(replay['diagnostic'] == 'diagnostics/check_stated_constants.py', 'Unexpected diagnostic')
    check_pin(root, replay['diagnostic'], replay['bytes'], replay['sha256'])
    require(replay['assert_nodes'] == 0 and replay['source_originals_modified'] is False
            and replay['normalized_results_identical_across_modes'] is True, 'Unsafe replay state')
    require([run['mode'] for run in replay['runs']] == ['normal', 'O', 'OO'], 'Replay modes incomplete')
    normalized = []
    for mode_index, run in enumerate(replay['runs']):
        require(run['exit_code'] == 0 and run['stderr_empty'] is True, 'Failed recorded diagnostic')
        report = run['report']
        require(report['status'] == 'PASS' and len(report['checks']) == 12
                and all(value is True for value in report['checks'].values()), 'Failed recorded arithmetic')
        require(set(report['checks']) == EXPECTED_CHECKS, 'Recorded check labels differ')
        require(report['values'] == EXPECTED_VALUES, 'Recorded scalar values differ')
        require(type(report['optimization_flag']) is int and report['optimization_flag'] == mode_index,
                'Recorded optimization flag differs')
        require(type(run['exit_code']) is int, 'Recorded exit code must be an integer')
        serialized = (json.dumps(report, indent=2, sort_keys=True) + '\n').encode()
        require(run['stdout_sha256'] == digest(serialized), 'Recorded stdout digest differs')
        normalized.append({key: value for key, value in report.items() if key != 'optimization_flag'})
        control = run['negative_control']
        require(control['expected_rejection_observed'] is True and control['exit_code'] != 0,
                'Inactive runtime-failure control')

    require(normalized[0] == normalized[1] == normalized[2], 'Recorded results differ across modes')

    metadata = read_json(root / 'SOURCE_METADATA.json')
    require(metadata['metadata_only'] is True and metadata['source_files_bundled'] is False,
            'Source-publication boundary differs')
    for source in metadata['sources']:
        require(source['url'].startswith('https://'), 'Non-public source URL')
        require(type(source['bytes']) is int and source['bytes'] > 0, 'Invalid source byte count')
        require(re.fullmatch('[0-9a-f]{64}', source['sha256']), 'Invalid external source digest')

    dh = [source for source in metadata['sources']
          if source['url'] == 'https://sites.math.duke.edu/~ingrid/publications/ACHA_12_2002.pdf']
    require(len(dh) == 1 and dh[0]['authors'] == ['Ingrid Daubechies', 'Bin Han'],
            'Daubechies-Han authorship metadata differs')

    input_bytes = (root / 'INPUT_MANIFEST.json').read_bytes()
    require(len(input_bytes) == 4200 and digest(input_bytes) == INPUT_MANIFEST_SHA256,
            'Preserved input manifest differs')
    input_manifest = read_json(root / 'INPUT_MANIFEST.json')
    preserved_count = 0
    for record in input_manifest['files']:
        if record['path'] not in EDITORIAL_CHANGES:
            check_pin(root, record['path'], record['bytes'], record['sha256'])
            preserved_count += 1

    prohibited = [r'/workspace/', r'/root/', r'codex://', r'https?://chatgpt\.com/c/',
                  r'(?i)(?:^|[/\\])(?:private|internal)[/\\]']
    python_files = local_links = 0
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        content = path.read_text(encoding='utf-8')
        require('\x00' not in content, 'Unexpected binary content')
        if path.name != 'verify_bundle.py':
            require(not any(re.search(pattern, content) for pattern in prohibited),
                    'Private-path/material marker found: ' + path.name)
        if path.suffix == '.json':
            read_json(path)
        if path.suffix == '.py':
            python_files += 1
            require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(content))),
                    'Optimization-removable Python assertion found')
        if path.suffix == '.md':
            prose = re.sub(r'`[^`]*`', '', content, flags=re.S)
            for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', prose):
                if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                    continue
                target = target.split('#', 1)[0]
                if target:
                    destination = (path.parent / target).resolve()
                    require(root in destination.parents and destination.is_file(), 'Broken local link: ' + target)
                    local_links += 1
    return {'status': 'PASS', 'optimization_flag': sys.flags.optimize,
            'sealed_files': len(records), 'exact_original_copies': len(names),
            'frozen_original_anchors': len(ANCHORS), 'python_files_without_assert_nodes': python_files,
            'embedded_artifact_pins_checked': embedded_pins,
            'local_markdown_links_checked': local_links, 'external_source_metadata_records': len(metadata['sources']),
            'recorded_scalar_runs': 3, 'recorded_runtime_failure_controls': 3,
            'preserved_input_manifest_entries': preserved_count, 'required_members': len(REQUIRED_FILES),
            'scope': 'Packaging integrity only; no fresh scalar replay or mathematical proof certification.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    print(json.dumps(verify(args.root), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
