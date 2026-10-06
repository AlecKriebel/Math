#!/usr/bin/env python3
"""Verify exact package inventory; --full explicitly reproduces finite controls."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, sys

ROOT = Path(__file__).resolve().parent
def require(c, m):
    if not c: raise RuntimeError(m)
def files():
    found = {}
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(), 'Symlink: '+str(p))
        if p.is_file():
            b = p.read_bytes()
            found[p.relative_to(ROOT).as_posix()] = {'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}
    return found

def main():
    require(__debug__, 'Run without Python optimization; checks use assertions in preserved controls.')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--full', action='store_true')
    args = ap.parse_args()
    before = files()
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    require(set(before) == set(manifest['files'])|{'MANIFEST.json'}, 'Actual package inventory mismatch')
    for name, record in manifest['files'].items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe manifest path')
        require(before[name] == record, 'Payload mismatch: '+name)
    candidate = ROOT/'submitted_problem'
    expected_candidate = json.loads((ROOT/'SOURCE_IDENTITY.json').read_text())['submitted_files']
    actual_candidate = {k.removeprefix('submitted_problem/'):v for k,v in before.items() if k.startswith('submitted_problem/')}
    require(actual_candidate == expected_candidate, 'Original submitted16 files mismatch')
    commands = [
      ('signed_public', 'audits/signed_graph/public/verify_namespace.py', ['--mode','public'], 'expected/signed_public.stdout'),
      ('word_public', 'audits/word_overlap/public/verify_namespace.py', ['--mode','public-only'], 'expected/word_public.stdout'),
      ('definitions_public', 'audits/definitions/public/verify_namespace.py', ['--mode','public'], 'expected/definitions_public.stdout'),
      ('priority_public', 'audits/priority/verify_priority.py', ['--public-only'], 'expected/priority_public.stdout')]
    if args.full:
        commands += [
          ('submitted_author', 'submitted_problem/check_turn1.py', [], 'submitted_problem/TURN_1_CHECKS.json'),
          ('submitted_portable', 'submitted_problem/review/run_portable.py', [], 'submitted_problem/review/PORTABLE_CHECKS.json'),
          ('signed_graph', 'audits/signed_graph/public/check_signed_graph.py', [], 'audits/signed_graph/public/SIGNED_GRAPH_CHECKS.json'),
          ('word_overlap', 'audits/word_overlap/public/check_word_overlap.py', [], 'audits/word_overlap/public/WORD_OVERLAP_CHECKS.json'),
          ('definition_constraints', 'audits/definitions/public/verify_constraints.py', [], 'audits/definitions/public/EXPECTED_CHECKS.json'),
          ('priority_comparisons', 'audits/priority/comparison_check.py', [], 'audits/priority/comparison.stdout')]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    runs = []
    for name, code, flags, expected in commands:
        p = subprocess.run([sys.executable,'-B',str(ROOT/code),*flags],cwd=ROOT,env=env,capture_output=True)
        require(p.returncode == 0, name+' failed: '+p.stderr.decode(errors='replace'))
        require(p.stderr == b'', name+' emitted stderr')
        require(p.stdout == (ROOT/expected).read_bytes(), 'Whole stdout mismatch: '+name)
        require(files() == before, name+' changed package files')
        runs.append({'name':name,'exit_code':p.returncode,'stdout_bytes':len(p.stdout),
                     'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'whole_expected_stdout_equal':True})
    print(json.dumps({'status':'PASS','mode':'full' if args.full else 'integrity',
      'payload_files_checked':len(manifest['files']),'submitted_files_checked':16,
      'runs':runs,'package_bytes_unchanged':True,'network_or_installations':False,
      'limitations':['Finite controls do not replace the universal proof or certify priority.',
        'Only curated public audit bytes and their seals are included; private source downloads, native execution histories and full provenance are omitted.',
        'The historical optional five-source 68413 mode is not reproduced; public portable output is68408.',
        'Checksums establish integrity relative to the manifest, not independent authenticity or human peer review.']},indent=2))

if __name__ == '__main__': main()
