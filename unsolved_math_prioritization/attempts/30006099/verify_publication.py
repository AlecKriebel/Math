#!/usr/bin/env python3
"""Externally anchored source-free publication verification; not a proof assistant."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
ANCHORS = {
    'original/MANIFEST.json': 'a59fb26e06f8fc99027a248a1feaf80a196a2aa490d62c1ad0c4b7c3b5f9daa5',
    'accepted/MANIFEST.json': '4bb9b7ddf87bc047bbd3a46c198f47a65b1526fe2d9ed7b93ec54347a3682b39',
    'accepted/packet/MANIFEST.json': '19010cb1135f53d157d62882decb37cf9b8ca488a58b637406a5f6a53664f9c2',
}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def safe(name):
    require(isinstance(name, str), 'Non-string path')
    p = PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and str(p) == name
            and name != '.' and '\\' not in name, 'Unsafe path: ' + name)

def inventory(root):
    files, dirs = set(), set()
    require(root.is_dir() and not root.is_symlink(), 'Invalid root')
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISREG(mode):
            files.add(name)
        elif stat.S_ISDIR(mode):
            dirs.add(name)
        else:
            raise RuntimeError('Nonregular or linked member: ' + name)
    return files, dirs

def verify_manifest(root, manifest, is_outer=False):
    entries = manifest['files']
    if isinstance(entries, list):
        entries_map = {e['path']: {'bytes': e['bytes'], 'sha256': e['sha256']} for e in entries}
        require(len(entries_map) == len(entries), 'Duplicate path')
        entries = entries_map
    self_name = 'PUBLIC_MANIFEST.json' if is_outer else 'MANIFEST.json'
    require(self_name not in entries, 'Self-manifest entry')
    wanted = set(entries) | {self_name}
    wanted_dirs = set()
    for name in wanted:
        safe(name)
        wanted_dirs.update(str(p) for p in PurePosixPath(name).parents if str(p) != '.')
    files, dirs = inventory(root)
    require(files == wanted and dirs == wanted_dirs, 'Inventory mismatch: ' + root.name)
    for name, metadata in entries.items():
        require(digest((root / name).read_bytes()) == metadata, 'Payload mismatch: ' + name)
    return len(wanted)

def verify(anchor):
    require(ROOT.is_dir() and not ROOT.is_symlink(), 'Invalid publication root')
    mp = ROOT / 'PUBLIC_MANIFEST.json'
    require(stat.S_ISREG(mp.lstat().st_mode), 'Manifest is not regular')
    raw = mp.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == anchor, 'External manifest anchor mismatch')
    m = json.loads(raw)
    require(m['problem_id'] == 30006099 and m['status'] == 'unsolved' and m['turns'] == '5/5'
            and m['mathematical_changes'] == 0 and m['metadata_correction_required'] is True,
            'Disposition mismatch')
    count = verify_manifest(ROOT, m, True)
    for name, sha in ANCHORS.items():
        require(digest((ROOT / name).read_bytes())['sha256'] == sha, 'Frozen manifest anchor mismatch')
    for name in ('original', 'accepted', 'accepted/packet', 'accepted/audit'):
        verify_manifest(ROOT / name, json.loads((ROOT / name / 'MANIFEST.json').read_bytes()))
    original, corrected = ROOT / 'original', ROOT / 'accepted/packet'
    names = sorted(p.name for p in original.iterdir())
    changed = [n for n in names if (original / n).read_bytes() != (corrected / n).read_bytes()]
    require(changed == ['MANIFEST.json', 'SOURCE_METADATA.json'], 'Correction exceeded metadata scope')
    patch = ''.join(''.join(difflib.unified_diff(
        (original / n).read_text().splitlines(keepends=True),
        (corrected / n).read_text().splitlines(keepends=True),
        fromfile='a/' + n, tofile='b/' + n)) for n in ('SOURCE_METADATA.json', 'MANIFEST.json'))
    require(patch.encode() == (ROOT / 'accepted/audit/CORRECTION.patch').read_bytes(), 'Correction patch mismatch')
    old_meta = json.loads((original / 'SOURCE_METADATA.json').read_bytes())
    new_meta = json.loads((corrected / 'SOURCE_METADATA.json').read_bytes())
    corpus = new_meta['corpus_verification']
    require([e['name'] for e in corpus] == ['problems.json', 'research_results.json'], 'Corpus identity mismatch')
    require(corpus[0]['match_result'] == 'Exact target problem record present once (id 30006099; problem number OWR-14298803-003).', 'Problem match correction mismatch')
    require(corpus[1]['match_result'] == 'No target record or review entry under numeric ID 30006099 or problem-number key OWR-14298803-003; neither identifier occurs anywhere in this file.', 'Absent research record correction mismatch')
    for old, new in zip(old_meta['corpus_verification'], corpus):
        old['match_result'] = new['match_result']
    require(old_meta == new_meta, 'Unexpected source metadata change')
    a = json.loads((ROOT / 'accepted/audit/ACCEPTANCE.json').read_bytes())
    require(a['decision'] == 'accept_partial_progress_after_explicit_metadata_correction'
            and not a['broad_source_program_solved'] and not a['mathematical_changes_required'], 'Acceptance mismatch')
    runs = []
    with tempfile.TemporaryDirectory(prefix='maximal-average-replay-') as td:
        for optimized in (False, True):
            cmd = [sys.executable, '-I', '-B'] + (['-O'] if optimized else [])
            run = subprocess.run(cmd + [str(corrected / 'verify.py')], cwd=td, capture_output=True, timeout=300)
            require(run.returncode == 0, 'Author replay failed: ' + run.stderr.decode())
            require(run.stdout == (corrected / 'CHECKS.json').read_bytes(), 'Author receipt bytes differ; check package versions')
            author = json.loads(run.stdout)
            require(author['total_positive_checks'] == 367 and author['exact_symbolic_checks'] == 98
                    and len(author['negative_controls_rejected']) == 6, 'Author count mismatch')
            run = subprocess.run(cmd + [str(ROOT / 'accepted/audit/audit_independent.py'), str(corrected)], cwd=td, capture_output=True, timeout=300)
            require(run.returncode == 0, 'Independent replay failed: ' + run.stderr.decode())
            expected = ROOT / ('accepted/audit/independent.optimized.json' if optimized else 'accepted/audit/independent.normal.json')
            require(run.stdout == expected.read_bytes(), 'Independent receipt bytes differ')
            independent = json.loads(run.stdout)
            require(independent['positive_requirements'] == 690 and independent['exact_rational_lp_cases'] == 210
                    and independent['integrity_fault_rejections'] == 20, 'Independent count mismatch')
            runs.append({'optimized': optimized, 'author_positive_checks': 367, 'author_symbolic_checks': 98,
                         'author_rational_sensitivity_checks': 200, 'author_floating_diagnostics': 69,
                         'author_false_controls_rejected': 6, 'independent_requirements': 690,
                         'independent_rational_lp_pairs': 210, 'independent_integrity_rejections': 20,
                         'receipt_bytes_match': True, 'different_cwd': True})
    return {'result': 'PASS_SOURCE_FREE_PUBLICATION', 'problem_id': 30006099, 'status': 'unsolved',
            'turns': '5/5', 'packet_files': count, 'manifest_sha256': anchor, 'mathematical_changes': 0,
            'correction_patch_exact': True, 'original_and_accepted_bytes_preserved': True, 'runs': runs,
            'limits': 'Finite symbolic, rational, floating and integrity controls support the analytic proofs; the broad source program remains unresolved. Routes 4 and 5 are distinct proofs for the same LP.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.manifest_sha256), indent=2, sort_keys=True))
