#!/usr/bin/env python3
"""Read-only authentication and exact diagnostics; finite checks are not proofs.

Prints JSON and never writes a receipt. Uses explicit exceptions under -O/-OO.
Only declared manifest members are interpreted as membership.
"""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    snapshot = json.loads((HERE / 'SUBMITTED_SNAPSHOT.json').read_text())
    submitted = HERE / 'submitted'
    names = []
    for row in snapshot['files']:
        path = HERE / row['local']
        need(path.name in [p.name for p in path.parent.iterdir()], 'lexical case')
        data = path.read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'submitted bytes')
        blob = subprocess.check_output(['git', 'show', snapshot['head'] + ':' + row['path']], cwd=REPO)
        need(data == blob, 'actual Git blob differs')
        oid = subprocess.check_output(['git', 'hash-object', '--stdin'], input=data, cwd=REPO).decode().strip()
        need(oid == row['blob'], 'Git object identity')
        names.append(path.name)
    need(len(names) == len(set(names)) == 10, 'ten original files required')
    public = json.loads((submitted / 'PUBLIC_MANIFEST.json').read_text())
    need(public['file_count'] == 10 and len(public['files']) == 9, 'manifest count')
    def members(rows, key):
        for row in rows:
            name = row[key]
            need(name in names and name == Path(name).name, 'member path')
            data = (submitted / name).read_bytes()
            need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'manifest identity')
    members(public['files'], 'path')
    need(set(r['path'] for r in public['files']) | {'PUBLIC_MANIFEST.json'} == set(names), 'membership closure')
    audit = json.loads((submitted / 'AUDIT_MANIFEST.json').read_text())
    members(audit['artifacts'], 'file')
    acceptance = json.loads((submitted / 'ACCEPTANCE.json').read_text())
    members(acceptance['required_joint_artifacts'], 'path')
    members(acceptance['source_metadata'], 'path')
    members([acceptance['editorial_export']['map']], 'path')

    editorial = json.loads((submitted / 'EDITORIAL_MAP.json').read_text())
    ranges = protected = 0
    for artifact in editorial['artifacts']:
        out = artifact['output']
        data = (submitted / out['path']).read_bytes()
        need(len(data) == out['bytes'] and sha(data) == out['sha256'], 'editorial output identity')
        partitions = []
        for row in artifact['operations']:
            start, end = row['output_start'], row['output_end']
            replacement = row['replacement_utf8'].encode()
            need(data[start:end] == replacement and sha(replacement) == row['replacement_sha256'], 'replacement bytes')
            need(row['removed_bytes'] == row['input_end'] - row['input_start'], 'removed length')
            partitions.append((start, end))
            ranges += 1
        for row in artifact['unchanged_ranges']:
            start, end = row['output_start'], row['output_end']
            need(end-start == row['input_end']-row['input_start'], 'unchanged range length')
            need(sha(data[start:end]) == row['sha256'], 'available unchanged output hash')
            partitions.append((start, end))
            ranges += 1
        cursor = 0
        for start, end in sorted(partitions):
            need(start == cursor and start <= end <= len(data), 'partition overlap/gap')
            cursor = end
        need(cursor == len(data), 'complete output partition')
        for row in artifact.get('protected_mathematical_regions', []):
            piece = data[row['output_start']:row['output_end']]
            need(len(piece) == row['bytes'] and sha(piece) == row['sha256'], 'protected output range')
            protected += 1

    squares5 = sorted({a*a % 5 for a in range(5)})
    need(squares5 == [0, 1, 4] and not ({2, 3} & set(squares5)), 'norm obstruction modulo five')
    basis_cases = [(m,n) for m in range(4) for n in range(4) if (m*m-10*n*n) % 4 == 0]
    need(all(m%2 == n%2 == 0 for m,n in basis_cases), 'integral basis parity')
    denominator_cases = [v for v in range(1,41) if 40 % (v*v) == 0]
    need(denominator_cases == [1,2], 'reduced denominator bound')
    def mul(x,y,d=10):
        a,b=x; c,e=y
        return a*c+d*b*e, a*e+b*c
    def norm(x,d=10):
        a,b=x
        return a*a-d*b*b
    hom_cases = 0
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    need(mul((a,b),(c,d))[0]%2 == (a*c)%2, 'residue multiplication')
                    hom_cases += 1
    lattice_cases = 0
    for a in range(-30,31):
        for b in range(-30,31):
            if a == b == 0:
                continue
            x=(a,b)
            need(norm(x) != 0 and abs(norm(x)) != 2, 'bounded norm diagnostic')
            need(mul(x,(a,-b)) == (norm(x),0), 'conjugate identity')
            lattice_cases += 1
    # Meaningful countercontrols: replacing prime by irreducible admits a triangle;
    # quotient by (2) has a nonzero nilpotent, so it cannot prove 2 prime.
    sqrt10=(0,1)
    need(any(c%2 for c in sqrt10) and all(c%2 == 0 for c in mul(sqrt10,sqrt10)), '(2) nilpotent witness')
    need(norm((2,0)) == 4 and norm((1,0)) == 1, 'irreducible-difference triangle 0,1,2')
    # Dropping nonprincipality breaks the exclusion: sqrt(2) generates a prime
    # ideal of norm two and lies in that ideal, connecting two equal residues.
    need(abs(norm((0,1),2)) == 2 and mul((0,1),(0,1),2) == (2,0), 'principal norm-two countercontrol')
    return {
        'result': 'PASS', 'original_files': len(names), 'public_nonself_members': len(public['files']),
        'editorial_output_partition_ranges': ranges, 'protected_output_regions': protected,
        'historical_input_bytes_reconstructed': False,
        'historical_input_limit': 'Unavailable removed input bytes cannot be recovered or authenticated from hashes alone.',
        'square_residues_mod5': squares5, 'basis_parity_residues': basis_cases,
        'reduced_denominator_candidates': denominator_cases, 'homomorphism_residue_products': hom_cases,
        'bounded_nonzero_lattice_cases': lattice_cases,
        'countercontrols': ['irreducible difference triangle', '(2) nonzero nilpotent', 'principal norm-two ideal exclusion fails'],
        'universal_proof_limit': 'Finite arithmetic diagnoses local identities only; the written ideal and coloring arguments prove the universal conclusion.'
    }

if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
