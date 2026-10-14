#!/usr/bin/env python3
"""Check sealed file membership, hashes, preserved acceptance pins and references.

Standard library only. All checks raise explicit errors and remain active under
normal Python, -O and -OO. This verifies packaging, not mathematical truth.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import sys
import stat

ROOT = Path(__file__).resolve().parent
ANCHORS = {
    'accepted/pass1_audit/ACCEPTANCE_INDEX_MANIFEST.json':
        '10ee2c58e2bfc0314531c768ca7daf19739a31a0869d4a7ddd037c26be8e9d96',
    'accepted/pass1_hardy/MANIFEST.json':
        '639004491380b086324f5cce2a378226e7080ec18cd8a134bf1147d94dc2d074',
}
ANCHORS.update({
    'scope_adjudication/SOURCE_RESOLUTION_SCOPE.md':
        '8ec01edaeb9817b83abf6fd3abfffaa738937bb549181ff122e3ab28d0074475',
    'ORIGINAL_ARTIFACTS.json':
        'e0bea685af27dda0eeaa5579fa24b34d9ec77b859b3099040aa9d8a8c5bde1d8',
})
ORIGINAL_COLLECTIONS = {'accepted', 'source_context', 'scope_adjudication'}
CHECKER_COUNT = 8


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    def invalid_constant(value):
        raise RuntimeError('Nonfinite JSON value: ' + value)
    return json.loads(path.read_text(), object_pairs_hook=unique, parse_constant=invalid_constant)


def checked_relative(root, name):
    require(isinstance(name, str) and name, 'Invalid relative path')
    path = Path(name)
    require(not path.is_absolute() and '..' not in path.parts, 'Unsafe manifest path')
    target = root / path
    require(root in target.resolve().parents, 'Reference escapes reader root')
    return target


def verify(root):
    root = root.resolve()
    require(root.is_dir(), 'Reader directory does not exist')
    manifest = read_json(root / 'MANIFEST.json')
    require(manifest.get('schema_version') == 1, 'Unexpected manifest schema')
    require(manifest.get('full_informal_source_question_resolved') is False,
            'Unqualified source resolution is outside the reader scope')
    require(manifest.get('source_operational_disposition') == 'deferred for formulation selection', 'Source disposition changed')
    require(manifest.get('mathematical_passes_used') == 1 and manifest.get('mathematical_pass_limit') == 5, 'Pass count changed')
    records = manifest['files']
    expected = {record['path'] for record in records}
    require(len(expected) == len(records), 'Duplicate manifest member')
    actual = set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symbolic links are not admitted')
        mode = path.lstat().st_mode
        require(stat.S_ISREG(mode) or stat.S_ISDIR(mode), 'Unexpected filesystem entry type')
        if stat.S_ISREG(mode):
            rel = path.relative_to(root).as_posix()
            require(path.suffix in {'.md', '.json', '.py', '.txt'}, 'Unexpected file type')
            actual.add(rel)
    require(actual == expected | {'MANIFEST.json'}, 'File membership differs from sealed manifest')
    for record in records:
        require(type(record['bytes']) is int and record['bytes'] >= 0, 'Invalid byte count')
        require(isinstance(record['sha256'], str) and re.fullmatch('[0-9a-f]{64}', record['sha256']), 'Invalid file digest')
        path = checked_relative(root, record['path'])
        data = path.read_bytes()
        require(not data.startswith(b'%PDF-'), 'Disguised PDF document is not admitted')
        require(len(data) == record['bytes'], 'Byte count mismatch: ' + record['path'])
        require(sha(data) == record['sha256'], 'SHA-256 mismatch: ' + record['path'])
    for name, expected_sha in ANCHORS.items():
        require(sha((root / name).read_bytes()) == expected_sha, 'Frozen acceptance anchor mismatch: ' + name)

    copy_map = read_json(root / 'ORIGINAL_ARTIFACTS.json')
    require(copy_map['editorial_transforms_to_originals'] == [], 'Unexpected original-file transformation')
    originals = copy_map['originals']
    names = {item['reader_path'] for item in originals}
    original_members = {name for name in actual if name.split('/')[0] in ORIGINAL_COLLECTIONS}
    require(names == original_members and len(names) == len(originals), 'Original copy-map coverage differs')
    for item in originals:
        data = checked_relative(root, item['reader_path']).read_bytes()
        require(item['transformation'] == 'none; exact byte copy', 'Unexpected copy transformation')
        require(len(data) == item['bytes'] and sha(data) == item['sha256'], 'Original pin mismatch')

    # Replay artifact identity is checked separately from the artifact's reported
    # results. Retained output is evidence of a past run, not a fresh execution.
    for evidence_name in ('REPLAY_EVIDENCE.json', 'review/INDEPENDENT_REPLAY_EVIDENCE.json'):
        replay = read_json(root / evidence_name)
        require(replay['status'] == 'PASS' and replay['checker_count'] == CHECKER_COUNT, 'Incomplete replay evidence')
        require(replay['successful_checker_runs'] == 24 and replay['successful_active_failure_controls'] == 24,
                'Replay mode/failure-control counts differ')
        checker_names = set()
        for item in replay['checkers']:
            checker_names.add(item['reader_path'])
            path = checked_relative(root, item['reader_path'])
            data = path.read_bytes()
            require(sha(data) == item['sha256'] and len(data) == item['bytes'], 'Replay checker pin differs')
            require(item['assert_nodes'] == 0 and item['normalized_results_identical_across_modes'] is True,
                    'Unsafe optimization or mode inconsistency')
            require([run['mode'] for run in item['runs']] == ['normal', 'O', 'OO'], 'Missing replay mode')
            for run in item['runs']:
                require(run['exit_code'] == 0 and run['stderr_empty'] is True, 'Checker did not pass')
                require(run['negative_control']['expected_failure_observed'] is True
                        and run['negative_control']['exit_code'] != 0, 'Inactive negative control')
        require(len(checker_names) == CHECKER_COUNT, 'Duplicate checker evidence')
        actual_checkers = {path.relative_to(root).as_posix() for path in (root / 'accepted').rglob('check_*.py')}
        require(checker_names == actual_checkers, 'Replay checker coverage differs')
    
    # Every digest in every original JSON is assigned an explicit JSON pointer.
    # Resolution uses this exact map; never a basename search or file-name exclusion.
    pin_map = read_json(root / 'review/EMBEDDED_PIN_MAP.json')['records']
    expected_pointers = {(entry['origin'], entry['pointer']) for entry in pin_map}
    require(len(expected_pointers) == len(pin_map), 'Duplicate embedded pin mapping')
    observed = {}
    def visit(value, origin, pointer=''):
        if isinstance(value, dict):
            for key, child in value.items():
                here = pointer + '/' + key.replace('~', '~0').replace('/', '~1')
                if 'sha256' in key:
                    require(isinstance(child, str) and re.fullmatch('[0-9a-f]{64}', child),
                            'Malformed or unclassified embedded digest')
                    observed[(origin, here)] = (child, value, key)
                visit(child, origin, here)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, origin, pointer + '/' + str(index))
    for name in sorted(original_members):
        if name.endswith('.json'):
            visit(read_json(root / name), name)
    require(set(observed) == expected_pointers, 'Embedded pin coverage differs')
    embedded_pins = 0
    citation_only_pins = 0
    public_sources = {}
    for entry in pin_map:
        digest, owner, key = observed[(entry['origin'], entry['pointer'])]
        require(digest == entry['sha256'], 'Embedded digest map differs')
        size = owner.get('pdf_bytes' if key == 'pdf_sha256' else 'bytes')
        require(size == entry.get('bytes'), 'Embedded size map differs')
        if size is not None:
            require(type(size) is int and size >= 0, 'Invalid embedded byte count')
        if entry['kind'] == 'local_artifact':
            require(entry['target'] in original_members, 'Embedded target is not an original')
            data = checked_relative(root, entry['target']).read_bytes()
            require(sha(data) == digest and (size is None or len(data) == size),
                    'Exact embedded artifact pin mismatch')
            label = next((owner[field] for field in ('path', 'name', 'file', 'filename')
                          if isinstance(owner.get(field), str)), None)
            require(label == entry.get('declared_label'), 'Embedded declared label differs')
            if label:
                require(Path(label).name == Path(entry['target']).name, 'Embedded target label mismatch')
            embedded_pins += 1
        else:
            require(entry['kind'] == 'external_source_metadata', 'Unknown embedded pin kind')
            url = owner.get('url') or owner.get('public_url')
            require(url == entry['url'] and url.startswith('https://'), 'Source URL mismatch')
            require(size is not None, 'External source size missing')
            require(url not in public_sources or public_sources[url] == (digest, size),
                    'Inconsistent repeated public-source pin')
            public_sources[url] = (digest, size)
            citation_only_pins += 1

    local_links = 0
    scripts = 0
    # Pattern construction avoids embedding real forbidden paths in this code.
    # Every byte of every text file, including this validator, is scanned.
    prohibited = ['/' + 'workspace' + '/', '/' + 'root' + '/', 'codex' + '://',
                  'https?://' + r'chatgpt\.com/c/',
                  r'(?i)(?:^|[/\\])(?:private|internal)[/\\]']
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        content = path.read_text()
        require(not any(re.search(pattern, content) for pattern in prohibited), 'Private-path/material marker found: ' + path.relative_to(root).as_posix())
        if path.suffix == '.py':
            scripts += 1
            require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(content))),
                    'A Python assert would disappear under optimization')
        if path.suffix == '.md':
            prose = re.sub(r'\\\[.*?\\\]|\\\(.*?\\\)|\$\$.*?\$\$|(?<!\\)\$[^$\n]*\$|`[^`]*`', '', content, flags=re.S)
            for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', prose):
                if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                    continue
                target = target.split('#', 1)[0]
                if not target:
                    continue
                destination = (path.parent / target).resolve()
                require(root in destination.parents and destination.is_file(), 'Broken local Markdown link: ' + target)
                local_links += 1
    return {'status': 'PASS', 'optimization_flag': sys.flags.optimize,
            'sealed_files': len(records), 'exact_original_copies': len(originals),
            'frozen_acceptance_and_scope_anchors': len(ANCHORS), 'embedded_artifact_pins_checked': embedded_pins,
            'citation_only_pdf_pins_not_bundled': citation_only_pins,
            'distinct_external_source_pin_sets': len(public_sources),
            'original_json_digest_fields_checked': len(observed),
            'text_files_exempted_from_private_marker_scan': 0,
            'python_files_without_assert_nodes': scripts, 'local_markdown_links_checked': local_links,
            'recorded_checker_runs_per_replay': 24, 'recorded_active_failure_controls_per_replay': 24,
            'checked_replay_records': 2,
            'scope': 'Packaging integrity only; this command does not rerun the diagnostic programs or prove the mathematics.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT, help='Reader directory to validate')
    args = parser.parse_args()
    print(json.dumps(verify(args.root), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
