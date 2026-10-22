"""Check a finite UNSAT tree using only Python integer/set operations.

This checker does not trust solver pruning counters, the solver's search
heuristic, or its claim of completeness. It verifies every cover branch.
"""
from pathlib import Path
import gzip
import hashlib
import json
import sys


def verify_case(case):
    m, maximum = case["edges"], case["maximum_degree"]
    assert 6 <= m <= 10 and 4 <= maximum <= m - 2
    all_rows = (1 << m) - 1
    candidates = {s for s in range(1, all_rows + 1) if 4 <= s.bit_count() <= maximum}
    fixed = (1 << maximum) - 1
    nodes = case["nodes"]
    visited = set()
    leaves = 0

    def feasible(support, selected):
        if any((support | previous) == all_rows for previous in selected):
            return False
        trial = selected + (support,)
        signatures = [tuple(j for j, s in enumerate(trial) if s >> row & 1)
                      for row in range(m)]
        if any(len(row) > 3 for row in signatures):
            return False
        full_rows = [row for row in signatures if len(row) == 3]
        return len(full_rows) == len(set(full_rows))

    def visit(node_id, allowed, selected):
        nonlocal leaves
        assert isinstance(node_id, int) and 0 <= node_id < len(nodes)
        assert node_id not in visited
        visited.add(node_id)
        target, branches = nodes[node_id]
        assert 0 <= target <= all_rows and target.bit_count() == 5
        assert all((s & target).bit_count() <= 3 for s in selected)
        options = {s for s in allowed
                   if (s & target).bit_count() >= 4 and feasible(s, selected)}
        offered = [s for s, _ in branches]
        assert len(offered) == len(set(offered)) and set(offered) == options
        if not branches:
            assert not options
            leaves += 1
            return
        remaining = set(allowed)
        for support, child in branches:
            assert support in remaining and support in candidates
            assert child > node_id  # explicit well-founded finite tree
            remaining.remove(support)
            visit(child, remaining, selected + (support,))

    assert fixed in candidates and feasible(fixed, ())
    visit(case["root"], candidates - {fixed}, (fixed,))
    assert len(visited) == len(nodes)
    return dict(edges=m, maximum_degree=maximum, nodes=len(nodes), leaves=leaves, verified=True)


def verify(path):
    raw = Path(path).read_bytes()
    data = json.loads(gzip.decompress(raw) if str(path).endswith(".gz") else raw)
    cases = data["cases"]
    expected = {(m, d) for m in range(6, 11) for d in range(4, m - 1)}
    observed = [(c["edges"], c["maximum_degree"]) for c in cases]
    assert len(observed) == len(set(observed)) and set(observed) == expected
    results = [verify_case(c) for c in cases]
    return dict(certificate_sha256=hashlib.sha256(raw).hexdigest(), cases=results,
                total_nodes=sum(c["nodes"] for c in results),
                total_leaves=sum(c["leaves"] for c in results), verified=True)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name("turn3_tau3_certificate.json.gz")
    print(json.dumps(verify(path), indent=2))
