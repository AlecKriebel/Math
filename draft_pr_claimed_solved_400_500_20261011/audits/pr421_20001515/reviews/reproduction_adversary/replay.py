#!/usr/bin/env python3
"""Clean finite-certificate replays. Private fixtures never modify frozen input.

Use the local Python interpreter; no network or package dependencies.
"""
import argparse
import ast
from datetime import datetime, timezone
import dis
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
import types


PROGRAMS = ('verify.py', 'audit/independent_audit.py', 'audit/independent_algebra.py')
GENERATED = ('checks.json', 'audit/independent_results.json',
             'audit/independent_algebra_results.json')
EXPECTED = dict(zip(PROGRAMS, GENERATED))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def assertions_in_bytecode(code):
    # Python 3.14 replaced LOAD_ASSERTION_ERROR by LOAD_COMMON_CONSTANT.
    total = sum(i.opname == 'LOAD_ASSERTION_ERROR' or
                (i.opname == 'LOAD_COMMON_CONSTANT' and i.argrepr == 'AssertionError')
                for i in dis.get_instructions(code))
    return total + sum(assertions_in_bytecode(c) for c in code.co_consts
                       if isinstance(c, types.CodeType))


def replace_once(path, old, new):
    src = path.read_text()
    if src.count(old) != 1:
        raise RuntimeError(f'Expected exactly one mutation anchor: {path}: {old!r}')
    path.write_text(src.replace(old, new, 1))


# Each control changes a finite certificate input, not an import or dependency.
CONTROLS = {
 'verify_fullness': ('verify.py', 'Q_LINKS = links("ABCD", Q_EDGES, Q_FACES)',
     'Q_LINKS = links("ABCD", Q_EDGES, Q_FACES)\nQ_LINKS["A"]["edges"].remove(frozenset((-1, 2)))',
     'Delete the A link corner x-/y+ before testing local fullness.'),
 'verify_cube_corner': ('verify.py',
     'assert (len(Z_VERTS), len(Z_EDGES), len(Z_TRIANGLES)) == (14, 32, 16)',
     'Z_TRIANGLES.remove(frozenset((1, 2, 5)))\nassert (len(Z_VERTS), len(Z_EDGES), len(Z_TRIANGLES)) == (14, 32, 16)',
     'Delete the z_B+ cube triangle x+/y+/z_B+ after incidence reconstruction.'),
 'verify_stable_sign': ('verify.py',
     'gens = {1: ((), 1), 2: ((-1,), 1), 3: ((2,), 0), 4: ((-3,), -1)}',
     'gens = {1: ((), 1), 2: ((-1,), 1), 3: ((2,), 0), 4: ((-3,), 1)}',
     'Change the t exponent in z=c^-1 t^-1 from -1 to +1.'),
 'independent_fullness': ('audit/independent_audit.py', 'qlinks={}',
     "qcorners['A'].pop()\nqlinks={}",
     'Delete one actual Q corner at A before checking its induced link image.'),
 'independent_cube_corner': ('audit/independent_audit.py', 'ztri=set(tri_counts)',
     "ztri=set(tri_counts)\nztri.remove(frozenset([('x',1),('y',1),('zB',1)]))",
     'Delete the x+/y+/z_B+ actual cube corner before comparing to cliques.'),
 'independent_cube_side': ('audit/independent_audit.py',
     'side=[l,vertical(v),inv(lamb(l)),vertical(u,-1)]',
     "side=[l,vertical(u if a[0]=='p' else v),inv(lamb(l)),vertical(u,-1)]",
     'Attach the p cube side to z_B in place of z_A; triangles remain separately derived.'),
 'algebra_stable_sign': ('audit/independent_algebra.py',
     'x=t;y=prod(inverse(a),t);z=prod(inverse(c),inverse(t))',
     'x=t;y=prod(inverse(a),t);z=prod(inverse(c),t)',
     'Change z=c^-1 t^-1 to z=c^-1 t in the independent algebra input.'),
 'proof_byte': ('audit/independent_audit.py', None, None,
     'Append a newline to the proof bytes without editing the verifier.'),
}


def run_one(source, private, label, program, optimized, mutation=None,
            explicit_checks=False):
    mode = 'optimized' if optimized else 'normal'
    fixture = private / f'{label}__{mode}'
    if fixture.exists():
        shutil.rmtree(fixture)
    shutil.copytree(source, fixture)
    removed = {}
    for name in GENERATED:
        p = fixture / name
        if p.exists():
            removed[name] = {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
            p.unlink()
    before = {str(p.relative_to(fixture)): sha(p.read_bytes())
              for p in sorted(fixture.rglob('*')) if p.is_file()}
    mutation_record = None
    if mutation is not None:
        target, old, new, reason = CONTROLS[mutation]
        if mutation == 'proof_byte':
            p = fixture / 'ATTEMPT_1.md'
            p.write_bytes(p.read_bytes() + b'\n')
        else:
            p = fixture / target
            replace_once(p, old, new)
        mutation_record = {'control': mutation, 'reason': reason,
                           'path': str(p.relative_to(fixture)),
                           'before_sha256': before[str(p.relative_to(fixture))],
                           'after_sha256': sha(p.read_bytes()), 'old': old, 'new': new}
    overlay_records = []
    if explicit_checks:
        from explicit_checks import transform
        for name in PROGRAMS:
            p = fixture / name
            original_bytes = p.read_bytes()
            transformed, certificate = transform(p.read_text())
            p.write_text(transformed)
            overlay_records.append({'program': name,
                                    'input_sha256': sha(original_bytes),
                                    'output_sha256': sha(p.read_bytes()),
                                    **certificate})
    argv = [sys.executable] + (['-O'] if optimized else []) + [program]
    start_utc = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()
    proc = subprocess.run(argv, cwd=fixture, capture_output=True, timeout=60)
    elapsed = time.perf_counter() - start
    (fixture / 'REPLAY.stdout').write_bytes(proc.stdout)
    (fixture / 'REPLAY.stderr').write_bytes(proc.stderr)
    outputs = {}
    for name in GENERATED:
        p = fixture / name
        if p.exists():
            outputs[name] = {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes()),
                             'matches_frozen_expected_bytes': p.read_bytes() == (source / name).read_bytes()}
    try:
        stdout_json = json.loads(proc.stdout)
    except (json.JSONDecodeError, UnicodeDecodeError):
        stdout_json = None
    code = compile((fixture / program).read_text(), str(fixture / program), 'exec',
                   optimize=int(optimized))
    return {'label': label, 'program': program, 'optimized': optimized,
            'fixture': str(fixture.resolve()), 'cwd': str(fixture.resolve()),
            'argv': argv, 'started_at_utc': start_utc, 'duration_seconds': elapsed,
            'exit_code': proc.returncode, 'stdout': proc.stdout.decode(),
            'stderr': proc.stderr.decode(), 'stdout_sha256': sha(proc.stdout),
            'stderr_sha256': sha(proc.stderr), 'outputs': outputs,
            'removed_stale_outputs': removed, 'mutation': mutation_record,
            'explicit_check_transforms': overlay_records,
            'source_program_sha256': sha((fixture / program).read_bytes()),
            'compiled_assertion_error_instructions': assertions_in_bytecode(code),
            'stdout_matches_frozen_expected_bytes':
                proc.stdout == (source / EXPECTED[program]).read_bytes(),
            'generated_output_matches_frozen_expected_bytes':
                (fixture / EXPECTED[program]).read_bytes() == (source / EXPECTED[program]).read_bytes()
                if (fixture / EXPECTED[program]).exists() else None,
            'reported_status': stdout_json.get('status') if isinstance(stdout_json, dict) else None,
            'stdout_json': stdout_json}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--tag', default='frozen')
    parser.add_argument('--explicit-checks', action='store_true')
    args = parser.parse_args()
    case = args.case.resolve()
    public = case / 'reviews' / 'reproduction_adversary'
    private = case / 'private_sources' / 'reproduction_adversary' / args.tag
    source = args.source.resolve() if args.source else (
        case / 'source_snapshot' / 'unsolved_math_prioritization' / 'attempts' / '20001515')
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    runs = []
    for program in PROGRAMS:
        for optimized in (False, True):
            runs.append(run_one(source, private, 'baseline_' + Path(program).stem,
                                program, optimized, explicit_checks=args.explicit_checks))
    for control, (program, _, _, _) in CONTROLS.items():
        for optimized in (False, True):
            runs.append(run_one(source, private, control, program, optimized, control,
                                explicit_checks=args.explicit_checks))
    result = {'schema': 'pr421-finite-replay-v1', 'tag': args.tag,
              'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
              'runner_argv': sys.argv, 'interpreter': sys.executable,
              'python_version': sys.version, 'platform': platform.platform(),
              'programs': list(PROGRAMS), 'runs': runs}
    path = public / (args.tag.upper() + '_REPLAYS.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'record': str(path), 'runs': len(runs),
       'baseline_exits': [(r['program'], r['optimized'], r['exit_code'])
                          for r in runs if r['mutation'] is None],
       'controls': [(r['label'], r['optimized'], r['exit_code'], r['reported_status'])
                    for r in runs if r['mutation'] is not None]}, indent=2))


if __name__ == '__main__':
    main()
