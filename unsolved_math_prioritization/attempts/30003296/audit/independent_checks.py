#!/usr/bin/env python3
"""Independent offline audit controls; not a formal geometric proof checker.

Run with --author-dir pointing at the unmodified 12-file author packet.
No source PDFs, external modules, network, or writes are required.
"""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import subprocess
import sys

EXPECTED_MANIFEST = "77864bb9f2bd0493b64b8bdd73c004e03a9e0125374929ff37a05d165c3bf70f"
EXPECTED_PARTIAL = "f5d33306717ca687719748155444b7f41ade41c87cee49e2a5ec79fcd089801d"
ALLOWLIST = {
    "CONTROL_RESULTS.json", "PARTIAL.md", "README.md", "RESEARCH_LOG.md",
    "SHA256SUMS.json", "SOURCE_GATE.md", "SOURCE_MANIFEST.json", "STATUS.json",
    "VALIDATION_LIMITS.md", "turns.jsonl", "verify.py", "verify_manifest.py",
}
checks = 0

def check(condition, message):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prime(n):
    return n >= 2 and all(n % d for d in range(2, __import__('math').isqrt(n) + 1))


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def partitions(n, minimum=1):
    if n == 0:
        yield ()
    else:
        for k in range(minimum, n + 1):
            for rest in partitions(n-k, k):
                yield (k,) + rest


def ag_dim(g):
    return g * (g + 1) // 2


def run(author):
    check(author.is_dir(), "Author directory missing")
    check({p.name for p in author.iterdir()} == ALLOWLIST, "Author allowlist mismatch")
    check(all(p.is_file() and not p.is_symlink() for p in author.iterdir()), "Nonregular author entry")
    before = {p.name: sha(p) for p in author.iterdir()}
    check(before['SHA256SUMS.json'] == EXPECTED_MANIFEST, "Manifest differs from reviewed bytes")
    check(before['PARTIAL.md'] == EXPECTED_PARTIAL, "Canonical note differs from reviewed bytes")
    manifest = json.loads((author/'SHA256SUMS.json').read_text())
    check(manifest['id'] == '30003296', "Wrong manifest target")
    check(set(manifest['files']) == ALLOWLIST - {'SHA256SUMS.json'}, "Wrong manifest file set")
    for name, digest in manifest['files'].items():
        check(before[name] == digest, "Frozen digest mismatch: " + name)

    outputs = {}
    for name in ('verify.py', 'verify_manifest.py'):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        proc = subprocess.run([sys.executable, str(author/name)], capture_output=True,
                              text=True, cwd=author, env=env, check=False)
        check(proc.returncode == 0, name + " failed")
        check(proc.stderr == '', name + " emitted stderr")
        outputs[name] = json.loads(proc.stdout)
    check(outputs['verify.py'] == json.loads((author/'CONTROL_RESULTS.json').read_text()),
          "Replayed arithmetic differs from frozen output")
    check(outputs['verify_manifest.py']['manifest_passed'] is True, "Author manifest replay failed")
    check(outputs['verify_manifest.py']['files'] == 11, "Author manifest counts 11 hashed payloads plus itself")

    status = json.loads((author/'STATUS.json').read_text())
    turns = [json.loads(row) for row in (author/'turns.jsonl').read_text().splitlines()]
    check(status['id'] == '30003296' and status['rank'] == 630, "Wrong status identity")
    check(status['status'] == 'unsolved' and status['target_solved'] is False, "Invalid resolution status")
    check(status['turn_limit'] == status['turns_used'] == len(turns) == 5, "Five-route ledger mismatch")
    check([x['turn'] for x in turns] == list(range(1,6)), "Turn numbering mismatch")
    check(len({x['approach_family'] for x in turns}) == 5, "Duplicate route families")
    check(all(x['outcome'] == 'unsolved' for x in turns), "Ledger contains solved claim")
    check(status['known_compact_dimension_lower_bound'] == 1 and
          status['known_compact_dimension_upper_bound'] == 2, "Wrong recorded smooth-curve bounds")

    # Independent finite derivation, with no Hurwitz-order cutoff:
    # h>=3 would give p(2h-2)>=8>6. For h=0, p-1 divides 8;
    # for h=1, p-1 divides 6; for h=2, 2p<=6.
    triples = []
    for d in divisors(8):
        p = d + 1
        if prime(p):
            triples.append((p, 0, 2+8//d))
    for d in divisors(6):
        p = d + 1
        if prime(p):
            triples.append((p, 1, 6//d))
    for p in (2,3):
        remainder = 6-2*p
        if remainder % (p-1) == 0:
            triples.append((p, 2, remainder//(p-1)))
    triples.sort()
    expected = [(2,0,10),(2,1,6),(2,2,2),(3,0,6),(3,1,3),(3,2,0),(5,0,4),(7,1,1)]
    check(triples == expected, "Cutoff-free RH derivation failed")
    check([list(t) for t in triples] == outputs['verify.py']['rh_arithmetic_possibilities'], "RH disagreement")
    branch_data = []
    for p,h,r in triples:
        check(p*(2*h-2)+r*(p-1) == 6, "RH identity failed")
        if r:
            # Ordered local monodromies; this is not a count of covers or components.
            count = sum(sum(v) % p == 0 for v in itertools.product(range(1,p), repeat=r))
            closed_form = ((p-1)**r+(p-1)*((-1)**r))//p
            check(count == closed_form, "Local-monodromy count mismatch")
            branch_data.append({'p':p,'h':h,'r':r,'ordered_zero_sum_nonzero_vectors':count})
            check((count == 0) == (p == 7 and h == 1 and r == 1), "Wrong branch obstruction")
        else:
            check((p,h) == (3,2), "Unexpected unramified case")
            # Hom(pi_1(C_2), Z/3) has 3^4 elements, 80 of them nonzero/surjective.
            check(p**(2*h)-1 == 80, "Unramified monodromy witness count failed")
            branch_data.append({'p':p,'h':h,'r':0,'nonzero_h1_characters':80})

    decomposition_dimensions = [
        {'partition':list(parts),'dimension':sum(ag_dim(g) for g in parts)}
        for parts in partitions(4) if len(parts)>1
    ]
    check({tuple(row['partition']):row['dimension'] for row in decomposition_dimensions} ==
          {(1,1,1,1):4,(1,1,2):5,(1,3):7,(2,2):6}, "Product strata dimension mismatch")
    satake_dimensions = [ag_dim(g) for g in range(4)]
    check(satake_dimensions == [0,1,3,6], "Satake strata dimension mismatch")
    bad_dimension = max(satake_dimensions+[x['dimension'] for x in decomposition_dimensions])
    check(bad_dimension == 7, "Wrong largest forbidden dimension")
    section_dimensions = []
    for cuts in (7,8):
        row = {'cuts':cuts,'jacobian_closure_dimension':9-cuts,
               'ambient_abelian_dimension':10-cuts,'bad_expected_dimension':bad_dimension-cuts}
        section_dimensions.append(row)
    check(section_dimensions[0]['jacobian_closure_dimension'] == 2 and
          section_dimensions[0]['bad_expected_dimension'] == 0, "Surface boundary control failed")
    check(section_dimensions[1]['jacobian_closure_dimension'] == 1 and
          section_dimensions[1]['ambient_abelian_dimension'] == 2 and
          section_dimensions[1]['bad_expected_dimension'] == -1, "Curve/abelian-surface distinction failed")

    # Logical countermodels, with their geometric justifications in AUDIT.md.
    # P^2 > P^1 > point has affine successive strata A^2, A^1, A^0.
    # Point counts are only an arithmetic check of this familiar model.
    for q in (2,3,5,7,11):
        check((q**3-1)//(q-1) == q*q+q+1, "Projective affine-cell countermodel failed")
    # Q[H]/(H^3) retains H^2 although H^3 is zero.
    def power_of_h(k):
        return tuple(int(i==k) for i in range(3))
    check(power_of_h(2) == (0,0,1) and power_of_h(3) == (0,0,0), "Truncated Chow-ring control failed")
    # A reducible divisor x0*x1=0 in P^3 meets b=(0:1:0:0),
    # while its component x1=0 misses b. This tests a quantifier, not M_4.
    b = (0,1,0,0)
    check(b[0]*b[1] == 0 and b[0] == 0 and b[1] != 0, "Reducible-component countermodel failed")

    cover_genus = lambda h,r: 2*h-1+r//2
    check(cover_genus(2,2)==4 and cover_genus(4,2)==8, "Double-cover genus mismatch")
    check(cover_genus(4,2)-4 == 4, "Prym dimension mismatch")
    check(2-2*2 == -2, "Tangent normal degree sign mismatch")
    check(2+2 == 4 and 0 == 2-2, "Compact-type gluing control failed")

    # Source-free publication safety checks on the entire frozen allowlist.
    forbidden = [r'/workspace/', r'/tmp/', r'/root/', r'-----BEGIN .*PRIVATE KEY',
                 r'gh[pousr]_[A-Za-z0-9]{20,}', r'(?i)authorization\s*:\s*bearer',
                 r'collaboration\.send_message', r'\ue200', r'\ue202']
    for name in sorted(ALLOWLIST):
        text = (author/name).read_text()
        check(not any(re.search(pattern,text) for pattern in forbidden), "Publication-safety hit: "+name)
    source_manifest = json.loads((author/'SOURCE_MANIFEST.json').read_text())
    check(source_manifest['redistributed_source_files'] == [], "Source redistribution flagged")
    check({p.name:sha(p) for p in author.iterdir()} == before, "Author bytes changed during replay")

    return {
        'problem_id':'30003296', 'rank':630, 'verdict':'pass_as_unsolved_limited_scope',
        'target_solved':False, 'author_file_count':12, 'author_payload_hashes_checked':11,
        'reviewed_manifest_sha256':EXPECTED_MANIFEST, 'reviewed_partial_sha256':EXPECTED_PARTIAL,
        'author_verifiers_passed':list(outputs), 'assertions_passed':checks,
        'cutoff_free_rh_triples':[list(t) for t in triples],
        'monodromy_checks':branch_data, 'decomposable_strata':decomposition_dimensions,
        'satake_boundary_stratum_dimensions':satake_dimensions,
        'section_dimensions':section_dimensions,
        'logical_countermodels':['P2 affine three-stratum filtration',
                                  'H^2 nonzero but H^3 zero on P2',
                                  'one bad component does not make every component bad'],
        'normal_degree_on_each_ruling':-2, 'original_files_changed':False,
        'negative_inferences_rejected':[
            'three affine strata imply no complete surface',
            'lambda cubed vanishing forces lambda squared to vanish',
            'a seven-hyperplane surface avoids a seven-dimensional projective boundary',
            'a reducible Schottky section meeting decomposables makes every component bad',
            'every arithmetic RH solution has consistent local monodromy',
            'a genus-eight covering curve itself answers the genus-four question',
            'a nodal compact-type family or constant Torelli image solves the smooth target'],
        'scope':'Exact arithmetic, bytes, status, and logical countermodels only; source hypotheses and geometry are reviewed in AUDIT.md, not formalized by this program.'
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-dir', type=Path,
                        default=Path(__file__).resolve().parent.parent/'submission')
    args = parser.parse_args()
    print(json.dumps(run(args.author_dir.resolve()), sort_keys=True, indent=2))
