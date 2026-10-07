#!/usr/bin/env python3
"""Reproducible static scope audit, isolated source copy, and Lean build probe.

This script does not assert that source-level token checks constitute kernel
verification. All writes are confined to this script's project-local directory.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, re, shutil, subprocess, os

PIN = 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'
DEFAULT_SOURCE = Path('/Users/alec/Desktop/math/lean')
HERE = Path(__file__).resolve().parent
ROOT = 'OAI.Combinatorics.MatchingCount.Main'
METADATA = ['README.md', 'docs/113.md', 'formalization.yaml', 'lakefile.lean',
            'lake-manifest.json', 'lean-toolchain', 'LICENSE',
            'ComparatorChallenges/README.md', 'ComparatorChallenges/MatchingFPRAS.json',
            'ComparatorChallenges/MatchingFPRAS.lean']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def imports(text):
    result = []
    for line in text.splitlines():
        if line.startswith('import '):
            result.extend(line[7:].split('--')[0].split())
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--lean', type=Path,
        default=Path('/Users/alec/.elan/toolchains/leanprover--lean4---v4.34.1/bin/lean'))
    args = parser.parse_args()
    source = args.source.resolve()
    seen, external, pending = set(), set(), [ROOT]
    while pending:
        module = pending.pop()
        if module in seen:
            continue
        path = source / (module.replace('.', '/') + '.lean')
        if not path.is_file():
            external.add(module)
            continue
        seen.add(module)
        pending.extend(imports(path.read_text()))
    paths = sorted(module.replace('.', '/') + '.lean' for module in seen)
    copy = HERE / 'pinned_lean'
    copy.mkdir(exist_ok=True)
    hashes = {}
    token_hits = []
    critical = re.compile(r'\b(sorry|admit|axiom|unsafe|native_decide|ofReduceBool|implemented_by|partial|opaque|run_tac|run_cmd)\b')
    for rel in paths + METADATA:
        raw = (source / rel).read_bytes()
        hashes[rel] = sha(raw)
        dest = copy / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
        if rel in paths:
            for number, line in enumerate(raw.decode().splitlines(), 1):
                if critical.search(line):
                    token_hits.append({'path': rel, 'line': number, 'text': line})
    model = (copy / 'OAI/Combinatorics/MatchingCount/Model.lean').read_text()
    challenge = (copy / 'ComparatorChallenges/MatchingFPRAS.lean').read_text()
    comparator_prefix = challenge.split('/-- A fully polynomial randomized')[0]
    model_prefix = model.rsplit('end MatchingFPRAS', 1)[0]
    whitespace_equal = ''.join(model_prefix.split()) == ''.join(comparator_prefix.split())
    configuration = json.loads((copy / 'ComparatorChallenges/MatchingFPRAS.json').read_text())
    # A kernel axiom audit must be run only AFTER the actual solution builds.
    # Never load the comparator module in this probe: its declaration is a stub.
    probe = '''import OAI.Combinatorics.MatchingCount.Main\n#print OAI.MatchingFPRAS.thm_main\n#print axioms OAI.MatchingFPRAS.thm_main\n'''
    (copy / 'AxiomAudit.lean').write_text(probe)
    requested = [(f'{PIN}:lean/{rel}') for rel in hashes]
    pinned = subprocess.run(['git', '-C', str(source.parent), 'cat-file', '--batch'],
        input=('\n'.join(requested) + '\n').encode(), capture_output=True)
    cursor = 0
    pin_mismatches = []
    for rel in hashes:
        line_end = pinned.stdout.find(b'\n', cursor)
        header = pinned.stdout[cursor:line_end].decode()
        fields = header.split()
        if len(fields) != 3 or fields[1] != 'blob':
            raise RuntimeError(f'Pinned source retrieval failed for {rel}: {header}')
        size = int(fields[2])
        start = line_end + 1
        raw = pinned.stdout[start:start + size]
        cursor = start + size + 1
        if sha(raw) != hashes[rel]:
            pin_mismatches.append(rel)
    report = {
        'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'upstream_pin': PIN,
        'pin_validation_basis': 'Every copied source byte compared by SHA256 against git cat-file of exact pinned commit.',
        'pin_mismatches': pin_mismatches,
        'source_root': str(source), 'root_module': ROOT,
        'local_module_count': len(seen), 'local_source_bytes': sum((source / p).stat().st_size for p in paths),
        'external_imports': sorted(external), 'local_modules': sorted(seen),
        'lexical_critical_token_hits': token_hits,
        'model_and_comparator_definitions_equal_mod_whitespace': whitespace_equal,
        'comparator_configuration': configuration,
        'main_listed_in_formalization_yaml': ROOT in (copy / 'formalization.yaml').read_text(),
        'original_source_has_lake_directory': (source / '.lake').exists(),
        'free_disk_bytes_at_probe': shutil.disk_usage(HERE).free,
        'tool_availability': {name: shutil.which(name) for name in ['comparator', 'landrun', 'lean4export']},
        'hashes': hashes,
    }
    if args.lean.is_file():
        version = subprocess.run([str(args.lean), '--version'], text=True, capture_output=True)
        report['lean_version'] = version.stdout.strip() or version.stderr.strip()
        env = os.environ.copy()
        env['LEAN_PATH'] = str(copy)
        command = [str(args.lean), ROOT.replace('.', '/') + '.lean']
        result = subprocess.run(command, cwd=copy, env=env, text=True, capture_output=True)
        report['build_probe'] = {'command': command, 'cwd': str(copy),
                                 'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
        report['kernel_build_reproduced'] = result.returncode == 0
    else:
        report['lean_version'] = 'unavailable'
        report['kernel_build_reproduced'] = False
        report['build_probe'] = {'limitation': 'Pinned Lean executable unavailable.'}
    (HERE / 'static_audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in [
        'local_module_count', 'local_source_bytes', 'external_imports',
        'model_and_comparator_definitions_equal_mod_whitespace',
        'lexical_critical_token_hits', 'main_listed_in_formalization_yaml',
        'free_disk_bytes_at_probe', 'pin_mismatches', 'tool_availability', 'lean_version',
        'build_probe', 'kernel_build_reproduced']}, indent=2))

if __name__ == '__main__':
    main()
