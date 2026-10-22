#!/usr/bin/env python3
"""Read-only independent audit replay. Bounded diagnostics are not topology proofs."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    out = {}
    for p in sorted(root.rglob('*')):
        need(not p.is_symlink(), 'symlink in audit input tree')
        if p.is_file():
            out[p.relative_to(root).as_posix()] = {'bytes': p.stat().st_size, 'sha256': digest(p)}
        else:
            need(p.is_dir(), 'nonregular input entry')
    return out


def graph_oracle(n, edges, retained):
    """Independent adjacency/flood-fill implementation (no disjoint-set forest)."""
    degree = [0] * n
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        degree[u] += 1
        degree[v] += 1
        if i not in retained:
            adj[u].append(v)
            adj[v].append(u)
    unseen = set(range(n))
    blocks = []
    while unseen:
        stack = [min(unseen)]
        component = set()
        while stack:
            v = stack.pop()
            if v in component:
                continue
            component.add(v)
            stack.extend(adj[v])
        unseen -= component
        caps = sum(degree[v] == 1 for v in component)
        # Every vertex initially has degree[v] horizontal boundary sides;
        # each deleted internal edge removes exactly two sides.
        deleted = sum(i not in retained and u in component for i, (u, v) in enumerate(edges))
        boundary = sum(degree[v] for v in component) - 2 * deleted
        blocks.append((len(component), caps, boundary))
    return sorted(blocks)


def pairings(stubs):
    if not stubs:
        yield ()
        return
    u = stubs[0]
    for i in range(1, len(stubs)):
        v = stubs[i]
        for rest in pairings(stubs[1:i] + stubs[i + 1:]):
            yield tuple(sorted(((min(u, v), max(u, v)),) + rest))


def connected(n, edges):
    reached = {0}
    for _ in range(n):
        for u, v in edges:
            if u in reached or v in reached:
                reached.update((u, v))
    return len(reached) == n


def mathematical_controls(module):
    cases = graphs = 0
    for n in range(1, 6):
        unique = set()
        for degrees in itertools.product((1, 2), repeat=n):
            stubs = tuple(v for v, deg in enumerate(degrees) for _ in range(deg))
            if len(stubs) % 2:
                continue
            for edges in pairings(stubs):
                if connected(n, edges):
                    unique.add(edges)
        for edges in sorted(unique):
            graphs += 1
            for mask in range(1, 1 << len(edges)):
                retained = [i for i in range(len(edges)) if mask & (1 << i)]
                expected = graph_oracle(n, edges, set(retained))
                actual = module.graph_blocks(n, [list(e) for e in edges], retained)
                need(actual == expected, 'graph implementation disagrees with independent oracle')
                need(all(caps <= 1 and boundary == 2 - caps for _, caps, boundary in expected), 'graph topological bookkeeping condition failed')
                cases += 1
    bad = [
        (0, [[0, 0]], [0]), (True, [[0, 0]], [0]), (1.0, [[0, 0]], [0]),
        (1, [], [0]), (1, [[0, 0]], []), (1, [[0, 0]], [True]),
        (1, [[0, 0]], [0, 0]), (1, [[0, 0]], [1]), (1, [[0, 0]], [-1]),
        (1, [[0, False]], [0]), (1, [[0, 0.0]], [0]), (1, [[0, 1]], [0]),
        (1, [[0, 0, 0]], [0]), (1, [(0, 0)], [0]), (1, ((0, 0),), [0]),
        (2, [[0, 0]], [0]), (2, [[0, 0], [1, 1]], [0]),
        (4, [[0, 1], [0, 2], [0, 3]], [0]),
        (2, [[0, 1], [0, 1], [0, 1]], [0]),
    ]
    for args in bad:
        try:
            module.graph_blocks(*args)
        except ValueError:
            pass
        else:
            raise ValueError('malformed graph accepted')
    # Independent exact Euler characteristic + Kunneth bookkeeping.
    for genus in range(2, 101):
        cut_surface_chi = (2 - 2 * genus)  # cutting an annular collar preserves chi
        surface_b1 = 1 - cut_surface_chi  # connected with nonempty boundary, H2=0
        product_b1 = surface_b1 + 1       # H1(surface x circle; Q)
        need(product_b1 == 2 * genus and product_b1 > 2, 'Betti obstruction failed')
    return {'labelled_path_cycle_multigraphs': graphs, 'retained_subsets': cases,
            'malformed_graphs_rejected': len(bad), 'surface_genera_checked': 99}


def run(command):
    return subprocess.run(command, capture_output=True, text=True, timeout=180)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--subject', required=True, type=Path)
    parser.add_argument('--sources-dir', type=Path)
    parser.add_argument('--corpora-dir', type=Path)
    args = parser.parse_args()
    root = args.subject.resolve()
    authority = json.loads((Path(__file__).resolve().parent / 'REVIEWED_SUBJECT.json').read_text())
    before = inventory(root)
    need(before == authority['inventory'], 'subject bytes/inventory differ from reviewed freeze')
    verify = root / authority['verify_relative_path']
    spec = importlib.util.spec_from_file_location('reviewed_subject_verifier', verify)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    math_result = mathematical_controls(module)
    claims = verify.parent / 'CLAIMS.json'
    original = json.loads(claims.read_text())
    tests = []
    for key, value in [('problem_id', True), ('rank', 1004.0), ('turns_used', 5.0), ('general_solution', 0), ('novelty_claim', 0), ('status', 'solved'), ('claim_ids', []), ('verification_scope', 'formal proof')]:
        item = dict(original)
        item[key] = value
        tests.append(json.dumps(item))
    tests.extend(['', '{}', 'null', '[1]', '{"x":Infinity}', '{"x":-Infinity}', '{"x":NaN}', json.dumps(original)[:-1] + ',"rank":1004}', json.dumps(original) + '\n{}'])
    positive = negative = 0
    baseline = None
    source_before = inventory(args.sources_dir) if args.sources_dir else None
    corpus_before = None
    if args.corpora_dir:
        corpus_before = {n: digest(args.corpora_dir/n) for n in ('problems.json', 'research_results.json')}
    with tempfile.TemporaryDirectory(prefix='independent-sublamination-') as temp:
        t = Path(temp)
        for flags in ([], ['-O'], ['-OO']):
            command = [sys.executable, '-I', '-S', '-B', *flags, str(verify)]
            good = run(command)
            need(good.returncode == 0 and not good.stderr, 'positive verifier failed')
            baseline = baseline or good.stdout
            need(good.stdout == baseline, 'optimization altered result')
            positive += 1
            for i, text in enumerate(tests):
                path = t / ('bad-%d.json' % i)
                path.write_text(text)
                result = run(command + ['--input', str(path)])
                need(result.returncode != 0 and not result.stdout and result.stderr, 'malformed claims accepted')
                negative += 1
            explicit = run(command + ['--input', str(claims)])
            need(explicit.returncode == 0 and explicit.stdout == baseline and not explicit.stderr, 'exact input rejected')
            positive += 1
            if args.sources_dir or args.corpora_dir:
                extended = command[:]
                if args.sources_dir:
                    extended += ['--sources-dir', str(args.sources_dir)]
                if args.corpora_dir:
                    extended += ['--corpora-dir', str(args.corpora_dir)]
                result = run(extended)
                need(result.returncode == 0 and not result.stderr, 'full source/corpus replay failed')
                positive += 1
            bad_source = t / 'bad_sources'
            bad_source.mkdir(exist_ok=True)
            result = run(command + ['--sources-dir', str(bad_source)])
            need(result.returncode != 0 and not result.stdout and result.stderr, 'empty source directory accepted')
            negative += 1
            # Existing, regular caller files with wrong bytes must fail the hash
            # gate, not merely the missing-file gate.
            pins = json.loads((verify.parent/'SOURCE_PINS.json').read_text())
            for item in pins['sources']:
                (bad_source/item['filename']).write_bytes(b'invalid PDF control')
            result = run(command + ['--sources-dir', str(bad_source)])
            need(result.returncode != 0 and not result.stdout and 'source bytes mismatch' in result.stderr, 'wrong source bytes not rejected by hash gate')
            negative += 1
            bad_corpora = t/'bad_corpora'
            bad_corpora.mkdir(exist_ok=True)
            for name in ('problems.json', 'research_results.json'):
                (bad_corpora/name).write_text('{}')
            result = run(command + ['--corpora-dir', str(bad_corpora)])
            need(result.returncode != 0 and not result.stdout and 'corpus bytes mismatch' in result.stderr, 'wrong corpus bytes not rejected by hash gate')
            negative += 1
    need(inventory(root) == before, 'audit changed subject files')
    if args.sources_dir:
        need(inventory(args.sources_dir) == source_before, 'audit changed source files')
    if args.corpora_dir:
        need({n: digest(args.corpora_dir/n) for n in corpus_before} == corpus_before, 'audit changed corpus bytes')
    print(json.dumps({'status': 'PASS_INDEPENDENT_SCOPED_AUDIT', 'problem_id': 10300011,
                     'normal_O_OO_agree': True, 'read_only_verified': True,
                     'positive_subprocesses': positive, 'malformed_subprocesses_rejected': negative,
                     'sources_checked': bool(args.sources_dir), 'corpora_checked': bool(args.corpora_dir),
                     'mathematical_diagnostics': math_result, 'machine_proved_topology': False,
                     'general_solution': False}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(2)
