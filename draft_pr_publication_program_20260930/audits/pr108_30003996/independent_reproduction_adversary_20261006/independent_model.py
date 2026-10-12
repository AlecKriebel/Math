#!/usr/bin/env python3
"""Frozen before reading author/reviewer code. All checks survive python -O."""
from __future__ import annotations
import datetime, hashlib, itertools, json, random, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

def require(test, message):
    if not test:
        raise RuntimeError(message)

def edge(a, b):
    return tuple(sorted((a, b)))

def adjacency(vertices, edges):
    adj = {v: [] for v in vertices}
    for u, v in edges:
        require(u in adj and v in adj and u != v, 'invalid edge endpoint')
        adj[u].append(v)
        adj[v].append(u)
    return adj

def validate_tree(vertices, edges):
    if not vertices or len(edges) != len(vertices) - 1 or len(set(edges)) != len(edges):
        return False
    try:
        adj = adjacency(vertices, edges)
    except RuntimeError:
        return False
    seen, todo = set(), [vertices[0]]
    while todo:
        v = todo.pop()
        if v in seen:
            continue
        seen.add(v)
        todo.extend(adj[v])
    return len(seen) == len(vertices)

def all_subset_trees(vertices, graph_edges):
    """Actual N-1 graph-edge subsets; no gadget structure is assumed."""
    for candidate in itertools.combinations(graph_edges, len(vertices) - 1):
        if validate_tree(vertices, candidate):
            yield candidate

def prufer_tree(vertices, word):
    deg = Counter({v: 1 for v in vertices})
    deg.update(word)
    ans = []
    for w in word:
        leaf = min(v for v in vertices if deg[v] == 1)
        ans.append(edge(leaf, w))
        deg[leaf] -= 1
        deg[w] -= 1
    last = [v for v in vertices if deg[v] == 1]
    require(len(last) == 2, 'bad Prufer decoder')
    ans.append(edge(*last))
    return tuple(sorted(ans))

def rooted_total(vertices, tree, costs):
    require(validate_tree(vertices, tree), 'rooted evaluator requires a tree')
    adj = adjacency(vertices, tree)
    total = 0
    for root in vertices:  # Every root, even roots with all-zero cost vectors.
        seen = {root}
        todo = [root]
        while todo:
            u = todo.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
                    total += costs[root][(u, v)]
        require(len(seen) == len(vertices), 'disconnected rooted traversal')
    return total

def cut_total(vertices, tree, costs):
    """For u-v cut, r in component(u) sees u->v, all other r see v->u."""
    require(validate_tree(vertices, tree), 'cut evaluator requires a tree')
    adj = adjacency(vertices, tree)
    total = 0
    for u, v in tree:
        side, todo = {u}, [u]
        while todo:
            a = todo.pop()
            for b in adj[a]:
                if edge(a, b) != edge(u, v) and b not in side:
                    side.add(b)
                    todo.append(b)
        require(v not in side and len(side) < len(vertices), 'cut did not separate tree')
        total += sum(costs[r][(u, v)] if r in side else costs[r][(v, u)] for r in vertices)
    return total

def dense_zero(vertices, edges):
    arcs = [(u, v) for u, v in edges] + [(v, u) for u, v in edges]
    return {r: {a: 0 for a in arcs} for r in vertices}

def cnf_model(variable_ids, clauses):
    """Explicit dense table, with literal labels remapped before graph creation."""
    require(len(variable_ids) == len(set(variable_ids)), 'duplicate variable ID')
    require(all(isinstance(i, int) and i > 0 for i in variable_ids), 'invalid variable ID')
    mapping = {a: i for i, a in enumerate(variable_ids)}
    normalized = []
    for clause in clauses:
        require(all(abs(l) in mapping and l != 0 for l in clause), 'undeclared literal')
        s = set(clause)
        if any(-l in s for l in s):
            continue
        if not s:
            return fixed_model(False)
        normalized.append(tuple(sorted(s)))
    if not normalized:
        return fixed_model(True)
    n, m = len(variable_ids), len(normalized)
    require(n >= 1, 'nonempty formula needs variables')
    t, f = 'H:T', 'H:F'
    variables = [f'V:{i}' for i in range(n)]
    clause_nodes = [f'C:{j}' for j in range(m)]
    vertices = tuple([t, f] + variables + clause_nodes)
    edges = {edge(t, f)}
    for v in variables:
        edges.add(edge(t, v)); edges.add(edge(f, v))
    for q, cl in zip(clause_nodes, normalized):
        for l in cl:
            edges.add(edge(q, variables[mapping[abs(l)]]))
    edges = tuple(sorted(edges))
    costs = dense_zero(vertices, edges)
    B, K = n + 1, (n + 1) * m + n
    for u, v in edges:
        base = 0 if edge(u, v) == edge(t, f) else B if u.startswith('C:') or v.startswith('C:') else 1
        costs[t][(u, v)] = costs[t][(v, u)] = base
    for q, cl in zip(clause_nodes, normalized):
        for l in cl:
            v = variables[mapping[abs(l)]]
            costs[q][(v, t)] = int(l < 0)
            costs[q][(v, f)] = int(l > 0)
    return {'vertices': vertices, 'edges': edges, 'costs': costs, 'K': K, 'n': n, 'm': m,
            'normalized': normalized, 'variables': variables, 'clause_nodes': clause_nodes,
            'variable_ids': tuple(variable_ids), 'kind': 'reduction'}

def fixed_model(yes):
    vertices, edges = ('H:T', 'H:F'), (('H:F', 'H:T'),)
    costs = dense_zero(vertices, edges)
    if not yes:
        for c in costs.values():
            for a in c:
                c[a] = 1
    return {'vertices': vertices, 'edges': edges, 'costs': costs,
            'K': 0 if yes else 1, 'kind': 'fixed_yes' if yes else 'fixed_no'}

def sat(variable_ids, clauses):
    for vals in itertools.product((False, True), repeat=len(variable_ids)):
        a = dict(zip(variable_ids, vals))
        if all(any(a[abs(l)] == (l > 0) for l in cl) for cl in clauses):
            return True
    return False

def serialize(model):
    return json.dumps({'vertices': model['vertices'], 'edges': model['edges'], 'K': model['K'],
        'costs': [[r, u, v, model['costs'][r][(u, v)]] for r in model['vertices'] for u, v in
                  [(u, v) for u, v in model['edges']] + [(v, u) for u, v in model['edges']]]},
                  sort_keys=True, separators=(',', ':')).encode()

def deserialize(blob):
    d = json.loads(blob)
    vertices, edges = tuple(d['vertices']), tuple(tuple(e) for e in d['edges'])
    costs = dense_zero(vertices, edges)
    require(len(d['costs']) == len(vertices) * 2 * len(edges), 'incomplete dense encoding')
    keys = set()
    for r, u, v, c in d['costs']:
        require((r, u, v) not in keys and r in costs and (u, v) in costs[r], 'duplicate or foreign cost key')
        require(isinstance(c, int) and c >= 0, 'invalid encoded cost')
        keys.add((r, u, v)); costs[r][(u, v)] = c
    return {'vertices': vertices, 'edges': edges, 'costs': costs, 'K': d['K']}

def formula_census():
    suite = []
    for n in (1, 2):
        clauses = []
        for signs in itertools.product((-1, 0, 1), repeat=n):
            c = tuple(sign * i for i, sign in enumerate(signs, 1) if sign)
            if c:
                clauses.append(c)
        for m in range(1, 4):
            for cs in itertools.combinations_with_replacement(clauses, m):
                suite.append((f'full_n{n}_m{m}', tuple(range(1, n+1)), cs))
    # Exhaustive all normalized one/two-clause formulas with 3 variables.
    clauses3 = [tuple(s * i for i, s in enumerate(signs, 1) if s)
                for signs in itertools.product((-1, 0, 1), repeat=3) if any(signs)]
    for m in (1, 2):
        for cs in itertools.combinations_with_replacement(clauses3, m):
            suite.append((f'full_n3_m{m}', (1, 2, 3), cs))
    # Fixed boundary/unsatisfiable cases, then seeded sample; not claimed full families.
    suite.extend([
        ('boundary_empty_formula', (), ()),
        ('boundary_empty_clause', (), ((),)),
        ('boundary_tautology', (1,), ((1, -1),)),
        ('boundary_duplicate_literals', (1,), ((1, 1, 1),)),
        ('boundary_units_unsat', (1,), ((1,), (-1,))),
        ('boundary_2var_unsat', (1, 2), ((1, 2), (1, -2), (-1, 2), (-1, -2))),
        ('boundary_unused_variables', (1, 2, 3, 4), ((1,), (-1,))),
        ('sparse_ids_unsat', (7, 1000000009), ((7, 1000000009), (7, -1000000009), (-7, 1000000009), (-7, -1000000009))),
        ('sparse_ids_sat', (7, 1000000009, 2**100+39), ((7, -1000000009), (1000000009, 2**100+39), (-7, -2**100-39))),
    ])
    rng = random.Random(10803996)
    for k in range(20):
        suite.append((f'sample_n3_m3_{k}', (1,2,3), tuple(rng.choices(clauses3, k=3))))
    return suite

def main():
    if '--known-false' in sys.argv:
        require(False, 'known-false sentinel')
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    totals, coverage, families, records = Counter(), Counter(), Counter(), []
    for index, (family, ids, clauses) in enumerate(formula_census()):
        model = cnf_model(ids, clauses)
        vertices, edges, costs, K = (model[k] for k in ('vertices','edges','costs','K'))
        decoded = deserialize(serialize(model))
        require(decoded['vertices'] == vertices and decoded['edges'] == edges and decoded['costs'] == costs and decoded['K'] == K, 'dense encoding mismatch')
        shifted = {r: {a: c+1 for a,c in vec.items()} for r,vec in costs.items()}
        count, low_count, minimum, classes = 0, 0, None, Counter()
        for tree in all_subset_trees(vertices, edges):
            count += 1
            F = rooted_total(vertices, tree, costs)
            require(F == cut_total(vertices, tree, costs), 'root/cut aggregate mismatch')
            require(rooted_total(vertices, tree, shifted) == F + len(vertices)*(len(vertices)-1), 'positive shift mismatch')
            if F <= K:
                low_count += 1
            minimum = F if minimum is None else min(minimum, F)
            if model['kind'] == 'reduction':
                n, m = model['n'], model['m']
                h = int(edge('H:T', 'H:F') in tree)
                q = sum(u.startswith('C:') or v.startswith('C:') for u,v in tree)
                p = len(tree)-q-h
                base = sum(costs['H:T'][e] for e in tree)
                require(base == K+(1-h)+n*(q-m), 'structural identity mismatch')
                require(q >= m, 'clause-edge count below m')
                structured = h == 1 and q == m
                adj = adjacency(vertices, tree)
                cl = 'structured' if structured else ('missing_tf_and_nonleaves' if not h and q>m else 'missing_tf' if not h else 'clause_nonleaves')
                classes[cl] += 1
                if structured:
                    require(all(len(adj[v]) == 1 for v in model['clause_nodes']), 'structured clause not leaf')
                    assign = {}
                    for identifier, v in zip(ids, model['variables']):
                        hubs = [w for w in adj[v] if w in ('H:T', 'H:F')]
                        require(len(hubs) == 1, 'structured variable has wrong hub degree')
                        assign[identifier] = hubs[0] == 'H:T'
                    false_count = 0
                    for node, clause in zip(model['clause_nodes'], model['normalized']):
                        selected_var = adj[node][0]
                        selected_id = ids[model['variables'].index(selected_var)]
                        literal = next(l for l in clause if abs(l) == selected_id)
                        false_count += int(assign[selected_id] != (literal > 0))
                    require(F == K+false_count, 'literal-cost identity mismatch')
                if F <= K:
                    require(structured and F == K, 'nonstructured low-cost tree or F<K')
        expect = sat(ids, clauses)
        require(count > 0 and (low_count > 0) == expect, 'SAT/tree threshold mismatch')
        totals.update(formulas=1, actual_spanning_trees=count, low_cost_trees=low_count,
                      sat_formulas=int(expect), unsat_formulas=int(not expect), dense_roundtrips=1,
                      all_root_cut_checks=count, positive_shift_checks=count)
        coverage.update(classes)
        families[family] += 1
        records.append({'index': index, 'family': family, 'ids': list(ids), 'clauses': clauses,
                        'normalized_kind': model['kind'], 'N': len(vertices), 'E': len(edges), 'K': K,
                        'sat': expect, 'tree_count': count, 'low_cost_tree_count': low_count,
                        'minimum': minimum, 'classes': dict(classes), 'model_sha256': hashlib.sha256(serialize(model)).hexdigest()})
    dense_count = 0
    dense_rejected = 0
    dense_records = []
    rng = random.Random(10816633013)
    for n in range(2, 7):
        vertices = tuple(f'sparse:{2**80+i*1000003}' for i in range(n))
        graph = tuple(itertools.combinations(vertices, 2))
        trees = [prufer_tree(vertices, word) for word in itertools.product(vertices, repeat=n-2)]
        require(len(set(trees)) == n**(n-2), 'Prufer cardinality mismatch')
        if n <= 5:
            require(set(trees) == set(tuple(sorted(t)) for t in all_subset_trees(vertices, graph)), 'Prufer/subset disagreement')
        costs = {r: {(u,v): rng.randrange(0, 2**70) for u,v in graph} | {(v,u): rng.randrange(0,2**70) for u,v in graph} for r in vertices}
        dense_zero_values = sum(c == 0 for vec in costs.values() for c in vec.values())
        require(dense_zero_values == 0, 'dense arbitrary-cost sample accidentally sparse')
        shifted = {r: {a:c+1 for a,c in vec.items()} for r,vec in costs.items()}
        digest = hashlib.sha256()
        for tree in trees:
            F = rooted_total(vertices, tree, costs)
            require(F == cut_total(vertices, tree, costs), 'dense root/cut mismatch')
            require(rooted_total(vertices, tree, shifted) == F+n*(n-1), 'dense shift mismatch')
            digest.update(f'{tree!r}:{F}\n'.encode())
            dense_count += 1
        # A corrupted model must fail against an unchanged independent cost oracle.
        bad = {r:dict(vec) for r,vec in costs.items()}
        for r in bad:
            for arc in bad[r]:
                bad[r][arc] += 1
        require(rooted_total(vertices, trees[0], bad) != cut_total(vertices, trees[0], costs), 'corrupted dense costs escaped control')
        dense_rejected += 1
        dense_records.append({'N':n,'actual_complete_graph_trees':len(trees),'objective_digest':digest.hexdigest(), 'max_cost_bit_length':max(c.bit_length() for vec in costs.values() for c in vec.values())})
    invalid_controls = 0
    for vertices, tree in [ (('a','b','c','d'), (('a','b'),('b','c'),('a','c'))),
                           (('a','b','c'), (('a','b'),('b','c'),('a','c'))),
                           (('a','b','c'), (('a','b'),('a','b'))) ]:
        require(not validate_tree(vertices, tree), 'cycle/disconnected/duplicate accepted')
        try:
            rooted_total(vertices, tree, {})
        except RuntimeError:
            invalid_controls += 1
        else:
            raise RuntimeError('bad tree did not fail evaluator')
    result={'schema':1,'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'python_optimized':sys.flags.optimize,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'counts':dict(totals),'unstructured_tree_coverage':dict(coverage),'formula_families':dict(families),
            'generic_dense_complete_graph_records':dense_records,'generic_dense_all_root_cut_checks':dense_count,
            'corrupted_dense_cost_controls_rejected':dense_rejected,'invalid_tree_controls_rejected':invalid_controls,
            'formula_records':records,
            'scope':'Finite actual-tree census and controls support but do not replace the universal proof; n3m3 is sampled.'}
    target = HERE/('independent_results_optimized.json' if sys.flags.optimize else 'independent_results.json')
    target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('formula_records','formula_families')},sort_keys=True))

if __name__ == '__main__':
    main()
