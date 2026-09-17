#!/usr/bin/env python3
"""Independent finite-relaxation and UNSAT check. Standard library only.

Does not import package code. Reconstructs every clause from coordinates,
exhaustively checks each kind of Boolean gadget against its mathematical
meaning, checks the supplied proof using residual clauses, and derives a
fresh contradiction by unit propagation on both values of K(-1,1).
"""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / 'certificates'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_cnf():
    raw = (CERT / 'local_relaxation.cnf').read_bytes()
    header = None
    clauses, pending = [], []
    for line in raw.decode('ascii').splitlines():
        fields = line.split()
        if not fields or fields[0] == 'c':
            continue
        if fields[0] == 'p':
            require(header is None and len(fields) == 4 and fields[1] == 'cnf', 'header')
            header = tuple(map(int, fields[2:]))
            continue
        require(header is not None, 'missing header')
        for value in map(int, fields):
            if value == 0:
                clauses.append(tuple(pending))
                pending = []
            else:
                require(0 < abs(value) <= header[0], 'literal out of range')
                pending.append(value)
    require(header is not None and not pending and len(clauses) == header[1], 'clause count')
    return raw, header[0], clauses


def exhaustive_gadgets():
    checked = 0
    def check(n, clauses, predicate):
        nonlocal checked
        for bits in product((False, True), repeat=n):
            got = all(any(bits[abs(v)-1] == (v > 0) for v in c) for c in clauses)
            require(got == predicate(bits), 'Boolean gadget mismatch')
            checked += 1
    check(3, [(-1, -2), (-1, 3), (-2, 3), (-3, 1, 2)],
          lambda b: not (b[0] and b[1]) and b[2] == (b[0] or b[1]))
    for n in range(1, 7):
        check(n+1, [(-i, n+1) for i in range(1, n+1)] +
              [(-(n+1), *range(1, n+1))], lambda b: b[-1] == any(b[:-1]))
    for n in (2, 3, 4):
        check(n+1, [(-1, *(-j for j in triple))
                    for triple in combinations(range(2, n+2), 3)],
              lambda b: not b[0] or sum(b[1:]) <= 2)
    for n in (4, 6):
        check(n+1, [(-1, *subset) for subset in combinations(range(2, n+2), n-3)],
              lambda b: not b[0] or sum(b[1:]) >= 4)
    for n in range(6):
        check(n+2, [(-1, -2, *range(3, n+3))],
              lambda b: not (b[0] and b[1]) or any(b[2:]))
    return checked


def reconstruct(names):
    points = set(product(range(-3, 1), range(-3, 4)))
    directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
    jumps = tuple((sx*a, sy*b) for a, b in ((1, 2), (2, 1))
                  for sx, sy in product((-1, 1), repeat=2))
    distinguished = ((0, 0), (-1, -1), (-1, 0), (-1, 1))
    expected_names, groups = set(), {}
    def piece(kind, p):
        name = f'{kind}({p[0]},{p[1]})'
        expected_names.add(name)
        return names[name]
    def add(group, clause):
        groups.setdefault(group, []).append(tuple(clause))
    for p in sorted(points):
        k, r, o = (piece(kind, p) for kind in 'KRO')
        for clause in ((-k, -r), (-k, o), (-r, o), (-o, k, r)):
            add('occupancy', clause)
        rays = []
        for dx, dy in directions:
            q = (p[0]+dx, p[1]+dy)
            ray = []
            while q in points:
                ray.append(piece('O', q))
                q = (q[0]+dx, q[1]+dy)
            if ray:
                name = f'V({p[0]},{p[1]};{dx},{dy})'
                expected_names.add(name)
                v = names[name]
                rays.append(v)
                add('ray_equivalence', (-v, *ray))
                for o_q in ray:
                    add('ray_equivalence', (-o_q, v))
        for triple in combinations(rays, 3):
            add('ray_cap', (-r, *(-v for v in triple)))
    # Build aligned pairs from ordered row/column lists, without testing
    # collinearity or sharing the generator's between-square expression.
    lines = [[(x, y) for x in range(-3, 1)] for y in range(-3, 4)]
    lines += [[(x, y) for y in range(-3, 4)] for x in range(-3, 1)]
    for line in lines:
        for i, j in combinations(range(len(line)), 2):
            add('rook_separation', (-piece('R', line[i]), -piece('R', line[j]),
                                   *(piece('K', s) for s in line[i+1:j])))
    neighbor_counts = {}
    for p in distinguished:
        neighbors = [(p[0]+dx, p[1]+dy) for dx, dy in jumps]
        require(all(q in points or q[0] > 0 for q in neighbors), 'truncated knight neighborhood')
        rook_variables = [piece('R', q) for q in neighbors if q in points]
        neighbor_counts[str(p)] = len(rook_variables)
        for subset in combinations(rook_variables, len(rook_variables)-3):
            add('knight_lower_bound', (-piece('K', p), *subset))
    add('anchor', (piece('K', (0, 0)),))
    require(expected_names == set(names), 'unexpected or missing variable names')
    return groups, neighbor_counts


def residual(clause, assignment):
    if any(assignment.get(abs(l)) == (l > 0) for l in clause):
        return None  # Already satisfied.
    return set(l for l in clause if abs(l) not in assignment)


def check_certificate(clauses, nvars, cert):
    counts = dict(nodes=0, unit_steps=0, splits=0, conflicts=0)
    def walk(node, assignment):
        assignment = assignment.copy()
        counts['nodes'] += 1
        for literal, index in node.get('units', []):
            require(type(literal) is int and 1 <= abs(literal) <= nvars, 'invalid unit')
            require(type(index) is int and 0 <= index < len(clauses), 'invalid clause index')
            require(abs(literal) not in assignment, 'unit reassignment')
            require(residual(clauses[index], assignment) == {literal}, 'non-unit inference')
            assignment[abs(literal)] = literal > 0
            counts['unit_steps'] += 1
        if 'conflict' in node:
            require('split' not in node, 'ambiguous node')
            index = node['conflict']
            require(type(index) is int and 0 <= index < len(clauses), 'invalid conflict index')
            require(residual(clauses[index], assignment) == set(), 'no contradiction')
            counts['conflicts'] += 1
            return
        v = node['split']
        require(type(v) is int and 1 <= v <= nvars and v not in assignment, 'invalid split')
        counts['splits'] += 1
        for value, label in ((False, 'false'), (True, 'true')):
            walk(node[label], assignment | {v: value})
    walk(cert['tree'], {})
    return counts


def fresh_contradiction(clauses, assumption):
    assignment = {abs(assumption): assumption > 0}
    trace = []
    while True:
        progress = False
        # Reverse clause order deliberately differs from the original prover.
        for i in reversed(range(len(clauses))):
            reduced = residual(clauses[i], assignment)
            if reduced == set():
                return dict(assumption=assumption, units=trace, conflict=i)
            if reduced is not None and len(reduced) == 1:
                literal = next(iter(reduced))
                assignment[abs(literal)] = literal > 0
                trace.append([literal, i])
                progress = True
        require(progress, 'unit propagation stalled; this is not a contradiction')


def mutation_checks(clauses, nvars, cert):
    rejected = 0
    def must_reject(candidate):
        nonlocal rejected
        try:
            check_certificate(clauses, nvars, candidate)
        except (ValueError, KeyError):
            rejected += 1
            return
        raise ValueError('invalid mutated proof accepted')
    def mutate_units(path):
        node = cert['tree']
        for part in path:
            node = node[part]
        for i in range(len(node.get('units', []))):
            candidate = deepcopy(cert)
            target = candidate['tree']
            for part in path:
                target = target[part]
            target['units'][i][0] *= -1
            must_reject(candidate)
        if 'split' in node:
            for label in ('false', 'true'):
                candidate = deepcopy(cert)
                target = candidate['tree']
                for part in path:
                    target = target[part]
                del target[label]
                must_reject(candidate)
                mutate_units(path + [label])
    mutate_units([])
    return rejected


def main():
    raw, nvars, clauses = read_cnf()
    names = json.loads((CERT / 'local_variables.json').read_text())
    require(set(names.values()) == set(range(1, nvars+1)) and len(names) == nvars,
            'variable mapping not bijective')
    groups, neighbor_counts = reconstruct(names)
    canonical = lambda cs: Counter(tuple(sorted(c)) for c in cs)
    expected = [c for group in groups.values() for c in group]
    require(canonical(expected) == canonical(clauses), 'CNF differs from independently reconstructed model')
    cert = json.loads((CERT / 'local_unsat_tree.json').read_text())
    require(cert['cnf_sha256'] == sha256(raw).hexdigest(), 'CNF hash mismatch')
    certificate_counts = check_certificate(clauses, nvars, cert)
    split = names['K(-1,1)']
    branches = {label: fresh_contradiction(clauses, literal)
                for label, literal in (('false', -split), ('true', split))}
    fresh_cert = {'cnf_sha256': sha256(raw).hexdigest(), 'tree': {'split': split, **{
        label: {k: v for k, v in branch.items() if k != 'assumption'}
        for label, branch in branches.items()}}}
    fresh_counts = check_certificate(clauses, nvars, fresh_cert)
    result = dict(status='PASS', cnf_sha256=sha256(raw).hexdigest(), variables=nvars,
                  clauses=len(clauses), clause_groups={k: len(v) for k, v in groups.items()},
                  neighborhood_counts=neighbor_counts, exhaustive_gadget_assignments=exhaustive_gadgets(),
                  supplied_certificate=certificate_counts, fresh_derivation=fresh_counts,
                  invalid_certificate_mutations_rejected=mutation_checks(clauses, nvars, cert))
    (ROOT / 'review/encoding_results.json').write_text(json.dumps(result, indent=2)+'\n')
    (ROOT / 'review/encoding_fresh_proof.json').write_text(json.dumps(fresh_cert, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
