#!/usr/bin/env python3
"""Portable, offline verifier for the exact frozen QCI partial-results release."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile
ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def safe(name):
    require(isinstance(name, str), 'Non-string path')
    p = PurePosixPath(name)
    require(str(p) == name and not p.is_absolute() and name not in ('', '.')
            and '..' not in p.parts and '\\' not in name, 'Unsafe path: ' + name)
    return name

def read_manifest(base, name):
    names = set()
    for rec in json.loads((base / name).read_text())['files']:
        rel = safe(rec['path'])
        require(rel not in names, 'Duplicate manifest path')
        names.add(rel)
        p = base / rel
        require(p.is_file() and not p.is_symlink(), 'Missing or linked file: ' + rel)
        data = p.read_bytes()
        require(len(data) == rec['bytes'] and digest(data) == rec['sha256'], 'Manifest mismatch: ' + rel)
    return names

def verify(integrity_only=False):
    for path in ROOT.rglob('*'):
        require(not path.is_symlink(), 'Symlink present')
        require(path.is_file() or path.is_dir(), 'Nonregular object')
    names = read_manifest(ROOT, 'PUBLICATION_MANIFEST.json')
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    require(actual == names | {'PUBLICATION_MANIFEST.json'}, 'Unexpected or missing file')
    for archive, prefix, expected, size in (
        ('rank668-30001222-authored-packet.zip', 'packet/', '4fc5af73089e545434dbb7020c197edb070066208122ad03237879da58bb01fa', 23282),
        ('rank668-30001222-independent-audit.zip', 'audit/', '2fff6f35083905fbbbaa50f8f599cd61bc91b63e7acef1bfbf28114c6b45cc64', 17826),
    ):
        data = (ROOT / archive).read_bytes()
        require(digest(data) == expected and len(data) == size, 'Archive mismatch')
        with zipfile.ZipFile(ROOT / archive) as z:
            members = z.namelist()
            require(len(members) == len(set(members)) == 10, 'Archive member count')
            for member in members:
                safe(member)
                require(member.startswith(prefix), 'Unexpected archive root')
                require(z.read(member) == (ROOT / member).read_bytes(), 'Archive extraction mismatch')
            require(set(members) == {n for n in names if n.startswith(prefix)}, 'Archive file-set mismatch')
    author = ROOT / 'packet'
    audit = ROOT / 'audit'
    require(len(read_manifest(author, 'MANIFEST.json')) == 9, 'Author manifest count')
    require(len(read_manifest(audit, 'MANIFEST.json')) == 9, 'Audit manifest count')
    gate = json.loads((ROOT / 'PUBLICATION_GATE.json').read_text())
    binding = json.loads((audit / 'AUDIT_BINDING.json').read_text())
    require(gate['status'] == 'unsolved' and gate['turns'] == '5/5' and binding['approaches_completed'] == 5,
            'Disposition mismatch')
    require(not gate['general_resolution_established'] and not binding['general_resolution_established']
            and not gate['counterexample_established'] and not binding['counterexample_established'], 'Unsupported resolution')
    require(gate['F11_pair_stable_Morita_equivalence'] == 'UNDETERMINED'
            and gate['characteristic_three_deformation_stable_Morita_equivalence'] == 'EXCLUDED_BY_HH1_DIMENSIONS_8_VERSUS_7'
            and gate['derived_equivalences_are_k_linear']
            and gate['Benson_Kessar_Linckelmann_parameter_order_minimum'] == 2
            and gate['ordinary_center_isomorphism_is_independent_hypothesis'], 'Scope mismatch')
    commands = [
        [sys.executable, '-B', str(author / 'verify_manifest.py')],
        [sys.executable, '-B', str(audit / 'verify_audit.py'), '--input-zip', str(ROOT / 'rank668-30001222-authored-packet.zip')],
    ]
    for command in commands:
        subprocess.run(command, check=True, capture_output=True)
    result = {'status': 'PASS_INTEGRITY' if integrity_only else 'PASS', 'target': '30001222 / OWR-3400-006',
              'publication_files': len(actual), 'frozen_author_files': 10, 'frozen_audit_files': 10,
              'original_problem_status': 'UNSOLVED', 'approaches_completed': 5,
              'F11_pair_stable_Morita_equivalence': 'UNDETERMINED',
              'characteristic_three_deformation_stable_Morita_equivalence': 'EXCLUDED'}
    if not integrity_only:
        author_run = subprocess.run([sys.executable, '-B', str(author / 'verify.py')], check=True, capture_output=True).stdout
        require(author_run == (author / 'verification_results.json').read_bytes() == (audit / 'replay_results.json').read_bytes(),
                'Author replay bytes mismatch')
        ar = json.loads(author_run)
        require(ar['assertions_total'] == 204097 and ar['status'] == 'PASS_EXACT_PARTIAL_CHECKS'
                and not ar['general_problem_resolved'] and not ar['stable_equivalence_constructed'], 'Author replay assertions')
        independent_run = subprocess.run([sys.executable, '-B', str(audit / 'independent_checks.py')], check=True, capture_output=True).stdout
        require(independent_run == (audit / 'independent_results.json').read_bytes(), 'Independent replay bytes mismatch')
        ir = json.loads(independent_run)
        require(ir['status'] == 'PASS_INDEPENDENT_WORD_AND_FULL_COCYCLE_CHECKS', 'Independent replay status')
        require([r['HH1_dimension'] for r in ir['results']] == [12,12,8,7], 'Independent HH1 dimensions')
        result.update(author_assertions=204097, independent_full_cocycle_equations=sum(r['all_basis_leibniz_equations'] for r in ir['results']),
                      independent_associativity_triples=sum(r['associativity_triples'] for r in ir['results']),
                      independent_word_checks=sum(r['left_right_reduction_word_checks'] for r in ir['results']),
                      replays_byte_identical=True)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.integrity_only), indent=2, sort_keys=True))
