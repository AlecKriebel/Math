#!/usr/bin/env python3
"""Create a deterministic reviewer ZIP only from a fully verified companion.

Run after the clean verification receipt and its logs have been copied to
verification/recorded. This command never invokes Lean or updates a receipt.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

from check import ALLOWED_AXIOMS, COMPILER, SOURCE_BLOB, SOURCE_SHA256, parse_axioms, RESOURCE_DIAGNOSTIC, validate_negative_diagnostics
from static_audit import ROOT, validation_registry

AXIOM_COUNT = 1852
PDF_SHA256 = '9d0d23837aed20346f6e97234095ee146f7e7b852c7a4a4b5d646e5fa595c0f6'
PRIVATE_PATH = re.compile(rb'/(?:Users|home)/')
ROOT_FILES = ('README.md', 'REVIEWER_GUIDE.md', 'COVERAGE.md', 'AXIOMS.md', '.gitignore',
              'lean-toolchain', 'lakefile.toml', 'lake-manifest.json', 'CyclicBell.lean',
              'CyclicBell/AxiomAudit.lean')
SCRIPT_NAMES = ('check', 'static_audit', 'source_inventory', 'project_reference_audit',
                'test_runner', 'package', 'test_package')
REFERENCE_NAMES = ('expected_theorems', 'source_inventory', 'paper_claim_ledger', 'manuscript')
FIXED_FILES = (ROOT_FILES + tuple('scripts/'+s+'.py' for s in SCRIPT_NAMES) +
               tuple('reference/'+s+'.json' for s in REFERENCE_NAMES) +
               ('reference/manuscript/main.tex', 'reference/manuscript/paper.pdf',
                'verification/README.md', 'verification/STATEMENT_REVIEW.md',
                'verification/source_preservation.json', 'verification/recorded/run.json'))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_read(root: Path, relative: str) -> bytes:
    parts = PurePosixPath(relative).parts
    require(parts and not PurePosixPath(relative).is_absolute() and
            all(p not in ('.', '..') for p in parts) and '\\' not in relative and
            str(PurePosixPath(relative)) == relative and not any(ord(c) < 32 for c in relative),
            'Unsafe archive input path: '+relative)
    path = root
    require(not path.is_symlink(), 'Symlinked companion root')
    for part in parts:
        path = path/part
        require(not path.is_symlink(), 'Symlinked archive input: '+relative)
    require(path.is_file(), 'Missing required file: '+relative)
    return path.read_bytes()


def protected_fingerprints(root: Path) -> dict[str, str]:
    """The same protected input set as check.protected_fingerprints, root-parametrized."""
    paths = [root/n for n in ('lean-toolchain', 'lakefile.toml', 'lake-manifest.json',
                              '.gitignore', 'CyclicBell.lean')]
    paths.extend(root.glob('*.md'))
    paths.extend(root.glob('*.cff'))
    for sub in ('CyclicBell', 'validation', 'scripts', 'reference'):
        directory = root/sub
        require(not directory.is_symlink(), 'Symlinked protected directory: '+sub)
        for p in directory.rglob('*'):
            require(not p.is_symlink(), 'Symlink in protected tree: '+str(p.relative_to(root)))
            if p.is_file() and '__pycache__' not in p.parts:
                paths.append(p)
    return {str(p.relative_to(root)): digest(safe_read(root, str(p.relative_to(root))))
            for p in sorted(set(paths))}


def json_file(payload: dict[str, bytes], name: str):
    return json.loads(payload[name])


def validate_manuscript(payload, receipt):
    meta = json_file(payload, 'reference/manuscript.json')
    expected = {'reference/manuscript/main.tex': SOURCE_SHA256,
                'reference/manuscript/paper.pdf': PDF_SHA256}
    require(meta['files'] == expected, 'Manuscript metadata pins changed')
    require(meta['source_git_blob_sha1'] == SOURCE_BLOB, 'Manuscript Git blob pin changed')
    for name, sha in expected.items():
        require(digest(payload[name]) == sha, 'Manuscript digest mismatch: '+name)
    tex = payload['reference/manuscript/main.tex']
    blob = hashlib.sha1(b'blob '+str(len(tex)).encode()+b'\0'+tex).hexdigest()
    require(blob == SOURCE_BLOB, 'Manuscript Git blob mismatch')
    require(receipt['manuscript'] == {'path': 'reference/manuscript/main.tex',
            'git_blob_sha1': SOURCE_BLOB, 'sha256': SOURCE_SHA256, 'bytes': len(tex)},
            'Recorded manuscript differs from the packaged manuscript')


def expected_commands(receipt, lock, controls):
    """Reconstruct the runner's complete ordered command contract, including bootstrap."""
    actual = receipt['commands']
    sequence = []
    bootstrapped_dependency = False
    def add(command, cwd='.', fail=False):
        sequence.append((command, cwd, fail))
    def next_is(command):
        return len(actual) > len(sequence) and actual[len(sequence)]['command'] == command
    add(['lean', '--version'])
    add(['lean', '--githash'])
    for p in lock['packages']:
        cwd = '.lake/packages/'+p['name']
        if next_is(['git', 'init', '--quiet']):
            bootstrapped_dependency = True
            add(['git', 'init', '--quiet'], cwd)
            add(['git', 'remote', 'add', 'origin', p['url']], cwd)
            add(['git', 'fetch', '--depth=1', 'origin', p['rev']], cwd)
            add(['git', 'checkout', '--detach', p['rev']], cwd)
        add(['git', 'rev-parse', 'HEAD'], cwd)
        add(['git', 'status', '--porcelain', '--untracked-files=no'], cwd)
    add(['lake', 'env', 'lean', '--githash'])
    if next_is(['lake', 'build', 'Cache.Main']):
        add(['lake', 'build', 'Cache.Main'])
        add(['lake', 'env', 'lean', '--run', '.lake/packages/mathlib/Cache/Main.lean', 'get'])
    else:
        require(not bootstrapped_dependency, 'Bootstrap receipt omitted cache command')
    add(['lake', 'build'])
    # Python dictionaries preserve the runner's literal registration order only
    # before validation_registry sorts it. Read actual control order from check.py.
    import ast
    tree = ast.parse(receipt['_check_source'])
    registered = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'run' and node.args:
            try:
                command = ast.literal_eval(node.args[0])
            except (ValueError, TypeError):
                continue
            if isinstance(command, list) and len(command) == 4 and command[:3] == ['lake', 'env', 'lean'] and command[3] in controls:
                registered.append((node.lineno, command))
    for _, command in sorted(registered):
        add(command, fail=controls[command[3]]['expect_failure'])
    require(type(receipt['standalone_axiom_repeat']) is bool, 'Missing standalone audit mode')
    if receipt['standalone_axiom_repeat']:
        add(['lake', 'env', 'lean', 'CyclicBell/AxiomAudit.lean'])
    add(['lake', 'env', 'lean', 'CyclicBell/Statements.lean'])
    for p in lock['packages']:
        cwd = '.lake/packages/'+p['name']
        add(['git', 'rev-parse', 'HEAD'], cwd)
        add(['git', 'status', '--porcelain', '--untracked-files=no'], cwd)
    return sequence


def validate_receipt(root: Path, payload, current):
    receipt = json_file(payload, 'verification/recorded/run.json')
    require(receipt.get('status') == 'passed' and receipt.get('kernel_checked') is True,
            'A passed kernel-checked recorded run is required')
    require(receipt.get('protected_source_hashes') == current, 'Stale recorded source fingerprints')
    require(receipt.get('compiler_commit') == COMPILER, 'Recorded compiler pin mismatch')
    require(re.search(r'\b4\.19\.0\b', receipt.get('lean_version', '')), 'Recorded Lean version mismatch')
    require(receipt.get('clean_project_build_directory') == '.lake/build', 'Missing clean build receipt')
    require(receipt.get('axiom_report_source') == 'fresh clean lake build of CyclicBell.AxiomAudit',
            'Missing fresh build axiom provenance')
    inventory = json_file(payload, 'reference/source_inventory.json')
    names = [d['name'] for d in inventory['declarations']]
    expected = json_file(payload, 'reference/expected_theorems.json')
    require(len(names) == len(set(names)) == AXIOM_COUNT and len(expected) == AXIOM_COUNT and
            set(names) == set(expected), 'Axiom inventory is not the exact required declaration set')
    production = {p for p in payload if p == 'CyclicBell.lean' or p.startswith('CyclicBell/')}
    require(set(inventory['files']) == production - {'CyclicBell/AxiomAudit.lean'}, 'Source inventory file omission')
    for name, record in inventory['files'].items():
        require(digest(payload[name]) == record['sha256'], 'Stale source inventory: '+name)
    axioms = receipt.get('axioms', {})
    require(set(axioms) == set(expected), 'Recorded axiom inventory mismatch')
    for name, deps in axioms.items():
        require(isinstance(deps, list) and all(isinstance(a, str) for a in deps) and
                set(deps) <= ALLOWED_AXIOMS, 'Unapproved recorded axiom: '+name)
    controls = validation_registry(root)
    require(controls, 'No validation controls registered')
    lock = json_file(payload, 'lake-manifest.json')
    receipt['_check_source'] = payload['scripts/check.py'].decode('utf-8')
    sequence = expected_commands(receipt, lock, controls)
    require(len(receipt['commands']) == len(sequence), 'Missing or extra recorded commands')
    build_axioms = None
    revisions = {'.lake/packages/'+p['name']: p['rev'] for p in lock['packages']}
    for i, (record, (command, cwd, fail)) in enumerate(zip(receipt['commands'], sequence), 1):
        require(record['command'] == command and record['cwd'] == cwd and
                record['expected_failure'] is fail and type(record['exit_code']) is int and
                record['exit_code'] == (1 if fail else 0), 'Unexpected command or exit code at '+str(i))
        require(record['log'] == f'{i:03d}.log', 'Unexpected recorded log path')
        name = 'verification/recorded/'+record['log']
        data = safe_read(root, name)
        require(digest(data) == record['log_sha256'], 'Corrupt command log: '+name)
        payload[name] = data
        text = data.decode('utf-8')
        require(not RESOURCE_DIAGNOSTIC.search(text), 'Resource failure in recorded log')
        require(not re.search(r'(?i)(sorryAx|declaration uses .?sorry|unknown (?:module|package|identifier|constant|namespace)|invalid field|failed to synthesize|unexpected token|failed to load|segmentation fault)', text),
                'Invalid compiler diagnostic in recorded log')
        if fail:
            validate_negative_diagnostics(text, root/command[-1])
        else:
            require(not re.search(r'(^|\n).*\berror:', text), 'Error in successful command log')
        if command in (['lean', '--githash'], ['lake', 'env', 'lean', '--githash']):
            require(text.strip() == COMPILER, 'Compiler log mismatch')
        elif command == ['lean', '--version']:
            require(text.strip() == receipt['lean_version'], 'Lean version log mismatch')
        elif command == ['git', 'rev-parse', 'HEAD']:
            require(text.strip() == revisions[cwd], 'Dependency revision log mismatch')
        elif command == ['git', 'status', '--porcelain', '--untracked-files=no']:
            require(not text.strip(), 'Recorded dependency modifications')
        elif command == ['lake', 'build']:
            build_axioms = parse_axioms(text, expected)
            require(build_axioms == axioms, 'Build axiom reports differ from receipt')
        elif command == ['lake', 'env', 'lean', 'CyclicBell/AxiomAudit.lean']:
            require(parse_axioms(text, expected) == axioms, 'Repeated axiom reports differ')
    require(build_axioms is not None, 'No actual build axiom log')
    validate_manuscript(payload, receipt)


def collect_payload(root: Path) -> dict[str, bytes]:
    names = set(FIXED_FILES)
    if (root/'CITATION.cff').exists() or (root/'CITATION.cff').is_symlink():
        names.add('CITATION.cff')
    for directory in ('CyclicBell', 'validation'):
        require(not (root/directory).is_symlink(), 'Symlinked source directory')
        files = list((root/directory).glob('*.lean'))
        require(files, 'Missing required source directory: '+directory)
        names.update(str(p.relative_to(root)) for p in files)
    payload = {name: safe_read(root, name) for name in sorted(names)}
    current = protected_fingerprints(root)
    require(set(current) <= set(payload), 'Protected inputs outside the share allowlist: '+
            ', '.join(sorted(set(current)-set(payload))))
    require(all(digest(payload[n]) == h for n, h in current.items()), 'Inputs changed during packaging')
    validate_receipt(root, payload, current)
    for name, data in payload.items():
        if name != 'reference/manuscript/paper.pdf':
            data.decode('utf-8')
            require(not PRIVATE_PATH.search(data), 'Private machine path in shareable text: '+name)
    require(protected_fingerprints(root) == current, 'Inputs changed during packaging')
    return payload


def write_archive(payload: dict[str, bytes], output: Path):
    require(not output.is_symlink(), 'Refusing symlinked archive output')
    sidecar = output.with_name(output.name+'.sha256')
    require(not sidecar.is_symlink(), 'Refusing symlinked checksum output')
    manifest = ''.join(digest(data)+'  '+name+'\n' for name, data in sorted(payload.items())).encode()
    entries = dict(payload)
    entries['SHA256SUMS'] = manifest
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_STORED) as archive:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo('lean_formalization/'+name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, data)
    sha = digest(output.read_bytes())
    sidecar.write_text(sha+'  '+output.name+'\n', encoding='utf-8')
    return sha


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT.parent/'cyclic-bell-lean-review.zip')
    args = parser.parse_args(argv)
    output = args.output.expanduser().absolute()
    require(not output.resolve().is_relative_to(ROOT.resolve()), 'Archive output must be outside the companion')
    require(not any(ord(c) < 32 for c in output.name), 'Invalid archive output filename')
    payload = collect_payload(ROOT)
    sha = write_archive(payload, output)
    print(f'Packaged {len(payload)} verified files; SHA-256 {sha}')
    print(output)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, TypeError, RuntimeError) as exc:
        print('Packaging refused: '+str(exc), file=sys.stderr)
        sys.exit(2)
