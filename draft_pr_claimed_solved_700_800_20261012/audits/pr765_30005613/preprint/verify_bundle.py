"""Offline verification of closed bytes and finite diagnostics, not a PDE proof."""
from pathlib import Path
import argparse
import json
import math
import os
import subprocess
import sys
from build_package import (METADATA, PREFIX, PIN, REVIEW_PINS, identity, safe_name,
                           require, regular, inventory, review_entries, priority_scope)

ROOT = Path(__file__).resolve().parent


def read_closed(root):
    actual = inventory(root)
    listed = {}
    for row in json.loads(actual['MANIFEST.json'])['files']:
        name = safe_name(row['path'])
        require(name not in listed and name != 'MANIFEST.json', 'Duplicate/self bundle path')
        listed[name] = {k: row[k] for k in ('bytes', 'sha256')}
    require(set(actual) == set(listed) | {'MANIFEST.json'}, 'Bundle inventory mismatch')
    for name, expected in listed.items():
        require(identity(actual[name]) == expected, 'Bundle content mismatch: ' + name)
    return actual


def compare_diagnostics(a, b):
    """Exact structure and nonfloats; floats allow documented cross-libm rounding."""
    require(type(a) is type(b), 'Diagnostic type mismatch')
    if isinstance(a, float):
        require(math.isfinite(a) and math.isfinite(b) and
                math.isclose(a, b, rel_tol=1e-12, abs_tol=0), 'Float diagnostic mismatch')
    elif isinstance(a, dict):
        require(a.keys() == b.keys(), 'Diagnostic keys mismatch')
        for k in a:
            compare_diagnostics(a[k], b[k])
    elif isinstance(a, list):
        require(len(a) == len(b), 'Diagnostic length mismatch')
        for x, y in zip(a, b):
            compare_diagnostics(x, y)
    else:
        require(a == b, 'Exact diagnostic mismatch')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--integrity-only', action='store_true')
    ap.add_argument('--pdf', type=Path, help='Optional published PDF for exact external binding')
    args = ap.parse_args()
    before = read_closed(ROOT)
    require(json.loads(before['zenodo-metadata.json']) == {'metadata': METADATA},
            'Metadata differs')
    priority_scope(json.loads(before['audit/PRIORITY_GATE.json']))
    bindings = json.loads(before['PREPRINT_BINDINGS.json'])
    require(identity(before['paper.tex']) == bindings['paper.tex'], 'Paper binding differs')
    if args.pdf:
        require(identity(regular(args.pdf)) == bindings['paper.pdf'], 'PDF binding differs')
    prefix = 'historical_candidate/'
    require(identity(before[prefix + 'PUBLICATION_MANIFEST.json'])['sha256']
            == PIN, 'Historical manifest pin differs')
    original = {}
    snapshot = json.loads(before['audit/SNAPSHOT.json'])
    require(len(snapshot['files']) == 39, 'Original count differs')
    for row in snapshot['files']:
        require(row['path'].startswith(PREFIX), 'Wrong original problem')
        name = safe_name(row['path'][len(PREFIX):])
        require(name not in original, 'Duplicate original path')
        original[name] = {k: row[k] for k in ('bytes', 'sha256')}
        require(identity(before[prefix + name]) == original[name], 'Original bytes differ')
    require({n[len(prefix):] for n in before if n.startswith(prefix)}
            == set(original), 'Original closure differs')
    require(identity(before[prefix + 'author/PROOF.md'])['sha256']
            == bindings['original_proof_sha256'], 'Original proof binding differs')
    for family, pin in REVIEW_PINS.items():
        prefix = 'audit/' + family + '/'
        raw = before[prefix + 'MANIFEST.json']
        require(identity(raw)['sha256'] == pin, 'Review manifest pin differs')
        names = set()
        for row in review_entries(json.loads(raw)):
            name = safe_name(row['path'])
            require(name not in names and name != 'MANIFEST.json', 'Review duplicate/self')
            names.add(name)
            require(identity(before[prefix + name]) == {k: row[k] for k in ('bytes', 'sha256')},
                    'Review bytes differ')
        require({n[len(prefix):] for n in before if n.startswith(prefix)}
                == names | {'MANIFEST.json'}, 'Review closure differs')
    result = {'status': 'PASS', 'inventory_files': len(before), 'original_files': 39,
              'outer_optimization': sys.flags.optimize, 'pdf_binding_checked': bool(args.pdf),
              'scope': 'Integrity and finite diagnostics; no formal PDE or priority certificate.'}
    if not args.integrity_only:
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE', None)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        def run(script, *arguments):
            child = subprocess.run([sys.executable, '-I', '-B', str(script), *arguments],
                env=env, cwd='/', capture_output=True, text=True, timeout=300)
            require(child.returncode == 0, 'Child failed: ' + child.stderr)
            return child.stdout
        require(run('-c', 'print(__debug__)').strip() == 'True', 'Child assertions disabled')
        h = json.loads(run(ROOT / 'historical_candidate/verify_publication.py'))
        require(h['status'] == 'PASS' and h['author_assertions'] == 4187
                and h['first_portable_assertions'] == 2911
                and h['first_with_author_archive_assertions'] == 2923
                and h['second_exact_tail_checks'] == 2304, 'Historical replay changed')
        result['historical_replay'] = h
        # Intercept the immutable spectral control's adjacent-file write.
        code = """
import contextlib,io,json,pathlib,runpy,sys
from unittest.mock import patch
writes={}
def capture(p,data,*a,**kw):
    if p != pathlib.Path(sys.argv[1]).with_name('CONTROLS_RESULTS.json'):
        raise RuntimeError('Unexpected control write')
    writes[str(p)]=data
    return len(data)
out=io.StringIO()
with patch.object(pathlib.Path,'write_text',capture),contextlib.redirect_stdout(out):
    runpy.run_path(sys.argv[1],run_name='__main__')
if len(writes)!=1 or json.loads(next(iter(writes.values())))!=json.loads(out.getvalue()):
    raise RuntimeError('Missing or inconsistent intercepted control output')
print(out.getvalue(),end='')
"""
        spectral = ROOT / 'audit/review_spectral_family/controls.py'
        s = json.loads(run('-c', code, str(spectral)))
        require(s == json.loads(before['audit/review_spectral_family/CONTROLS_RESULTS.json']),
                'Spectral controls differ')
        g = json.loads(run(ROOT / 'audit/review_geometry_family/controls.py'))
        compare_diagnostics(g, json.loads(before['audit/review_geometry_family/CONTROLS.json']))
        guard = json.loads(run(ROOT / 'guard_controls.py'))
        require(guard['status'] == 'PASS' and guard['negative_controls'] == 9,
                'Guard controls differ')
        result['spectral_controls'] = s
        result['geometry_controls'] = g
        result['geometry_float_tolerance'] = {'relative': 1e-12, 'absolute': 0}
        result['historical_guard_controls'] = guard
        require(read_closed(ROOT) == before, 'Replay changed closed inputs')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
