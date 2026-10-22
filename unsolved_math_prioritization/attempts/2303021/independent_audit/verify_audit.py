#!/usr/bin/env python3
"""Static audit consistency checks and independent finite diagnostics.
Authenticate this script with the external pinned bootstrap before execution.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

EXPECTED = {'ACCEPTANCE.json', 'ACCEPTANCE.md', 'AUTHOR_REPLAY_OPTIMIZED_RESULTS.json',
            'AUTHOR_REPLAY_RESULTS.json', 'CORPUS_REPLAY_OPTIMIZED_RESULTS.json',
            'CORPUS_REPLAY_RESULTS.json', 'CORPUS_VERIFICATION.json',
            'INDEPENDENT_DIAGNOSTICS.json', 'INDEPENDENT_DIAGNOSTICS_OPTIMIZED.json',
            'MANIFEST.json', 'MATHEMATICAL_AUDIT.md', 'PATCH_METADATA.json', 'README.md',
            'SOURCE_VERIFICATION.json', 'independent_math.py', 'replay_author.py',
            'verify_audit.py', 'verify_corpus.py'}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def main():
    need(sys.flags.isolated and sys.flags.no_site, 'run with -I -S')
    need(len(sys.argv) == 1, 'no extra arguments')
    root = pathlib.Path(__file__).absolute().parent
    need(not any(p.is_symlink() for p in (root, *root.parents)), 'symlink root')
    entries = list(root.iterdir())
    need({p.name for p in entries} == EXPECTED, 'closed audit inventory')
    need(all(p.is_file() and not p.is_symlink() for p in entries), 'nonregular member')
    def read(name):
        return json.loads((root / name).read_bytes(), object_pairs_hook=unique)
    manifest = read('MANIFEST.json')
    need(set(manifest) == {'schema', 'files'} and manifest['schema'] == 1, 'manifest shape')
    need(set(manifest['files']) == EXPECTED - {'MANIFEST.json'}, 'manifest inventory')
    for name, record in manifest['files'].items():
        raw = (root / name).read_bytes()
        need(set(record) == {'bytes', 'sha256'} and type(record['bytes']) is int, 'manifest metadata')
        need(len(raw) == record['bytes'] and hashlib.sha256(raw).hexdigest() == record['sha256'], 'member pin')
    acceptance = read('ACCEPTANCE.json')
    need(acceptance['problem_id'] == 2303021 and acceptance['rank'] == 853, 'target')
    need(acceptance['verdict'] == 'ACCEPT_UNCHANGED', 'verdict')
    need(acceptance['recommended_status'] == 'already_solved' and acceptance['authored_effort'] == '1/5', 'recommendation')
    for key in ['new_solution', 'formal_mathematical_verification', 'human_peer_review',
                'publication_performed', 'source_contents_included', 'mathematical_correction_required']:
        need(acceptance[key] is False, 'scope: ' + key)
    need(acceptance['source_theorem_external_input'] is True, 'external theorem')
    for name in ['AUTHOR_REPLAY_RESULTS.json', 'AUTHOR_REPLAY_OPTIMIZED_RESULTS.json']:
        replay = read(name)
        need(replay['result'] == 'PASS', 'replay pass')
        need(replay['positive_controls'] == 8 and replay['negative_controls'] == 38, 'control counts')
        need(len(replay['controls']) == 46, 'matrix size')
        need(all(x['attack_marker_absent'] for x in replay['controls']), 'attack marker')
        need(replay['original_preserved'] is True and replay['formal_mathematical_proof'] is False, 'replay scope')
    for name in ['CORPUS_REPLAY_RESULTS.json', 'CORPUS_REPLAY_OPTIMIZED_RESULTS.json']:
        corpus = read(name)
        need(corpus['result'] == 'PASS' and corpus['problem_id'] == 2303021, 'corpus result')
        need(corpus['review_sha256'] == 'ec496d5459f876cb044108dbd678ddf6e34cd1498bd2b9230519bb4b90f21a65', 'complete pair')
        need(corpus['contents_disclosed'] is False, 'corpus contents')
    source = read('SOURCE_VERIFICATION.json')
    need(source['source_contents_included'] is False, 'source content')
    need(source['sources'][1]['pdf_bytes_retrieved'] is False and source['sources'][1]['page_images_inspected'] is False, 'source access inflation')
    patch = read('PATCH_METADATA.json')
    need(patch['patch_required'] is False and patch['original_edited'] is False, 'patch scope')
    flags = ['-I', '-S', '-B'] + (['-O'] if sys.flags.optimize else [])
    proc = subprocess.run([sys.executable, *flags, str(root / 'independent_math.py')], text=True, capture_output=True, timeout=30)
    need(proc.returncode == 0 and not proc.stderr, 'diagnostics failed')
    diagnostic = json.loads(proc.stdout, object_pairs_hook=unique)
    need(diagnostic == read('INDEPENDENT_DIAGNOSTICS.json') == read('INDEPENDENT_DIAGNOSTICS_OPTIMIZED.json'), 'diagnostics changed')
    print(json.dumps({'problem_id': 2303021, 'result': 'PASS', 'verdict': 'ACCEPT_UNCHANGED',
        'inventory_files': len(EXPECTED), 'mathematical_theorem_proved_by_code': False,
        'general_published_theorem_is_external_input': True}, sort_keys=True))


if __name__ == '__main__':
    main()
