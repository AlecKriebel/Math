"""Fresh paper-first finite falsification controls; no source imports or file writes."""
import itertools
import json
import random


def membership(h, word):
    b = h * h
    if len(word) % b:
        return False
    reachable = set(range(h))
    for start in range(0, len(word), b):
        reachable = {q for p in reachable for q in range(h)
                     if word[start + p * h + q] == 1}
    return bool(reachable)


def source(h, word):
    b = h * h
    active = {('U', p, 0) for p in range(h)}
    for c in word:
        nxt = set()
        for kind, p, t in active:
            if kind == 'U':
                if t + 1 < (p + 1) * h:
                    nxt.add(('U', p, t + 1))
                if c and t // h == p:
                    q = t % h
                    nxt.add(('U', q, 0) if t == b - 1 else ('V', q, t + 1))
            else:
                nxt.add(('U', p, 0) if t == b - 1 else ('V', p, t + 1))
        active = nxt
    return any(kind == 'U' and t == 0 for kind, _, t in active)


def compiled_count(h):
    return 2 + sum((p + 1) * h for p in range(h)) + sum(h * h - q - 1 for q in range(h))


def word_from_relation(h, rel):
    return tuple((rel >> (h * p + q)) & 1 for p in range(h) for q in range(h))


def compressed_step(h, k, j, phase, direction, mutant=False):
    b = h * h
    if j == 0:
        if direction < 0:
            return None
        return (j, phase) if direction == 0 else (1, 0)
    if j == k + 1:
        if direction > 0:
            return None
        return (j, phase) if direction == 0 else (k, b - 1)
    if direction == 0:
        return j, phase
    if direction == 1:
        if phase == b - 1:
            return j + 1, (b - 1 if mutant else 0)
        return j, phase + 1
    if phase == 0:
        return j - 1, b - 1
    return j, phase - 1


def project(h, k, j, phase):
    if j == 0:
        return 0
    if j == k + 1:
        return k * h * h + 1
    return (j - 1) * h * h + phase + 1


def binary_accept(table, finals, word, positive):
    tape = ('L',) + tuple(word) + ('R',)
    pending = [(0, 0, False)]
    seen = set()
    while pending:
        q, pos, stepped = pending.pop()
        key = (q, pos, stepped if positive else False)
        if key in seen:
            continue
        seen.add(key)
        if q in finals and (stepped or not positive):
            return True
        for nxt, direction in table.get((q, tape[pos]), ()):
            dest = pos + direction
            if 0 <= dest < len(tape):
                pending.append((nxt, dest, True))
    return False


def pullback_accept(h, table, finals, relations, positive):
    k = len(relations)
    pending = [(0, 0, 0, False)]
    seen = set()
    while pending:
        q, pos, phase, stepped = pending.pop()
        key = q, pos, phase, stepped if positive else False
        if key in seen:
            continue
        seen.add(key)
        if q in finals and (stepped or not positive):
            return True
        symbol = 'L' if pos == 0 else 'R' if pos == k + 1 else ((relations[pos - 1] >> phase) & 1)
        for nxt, direction in table.get((q, symbol), ()):
            dest = compressed_step(h, k, pos, phase, direction)
            if dest is not None:
                pending.append((nxt, dest[0], dest[1], True))
    return False


def main():
    rng = random.Random(23202966)
    source_cases = 0
    for h, max_length in [(2, 12), (3, 10)]:
        for length in range(max_length + 1):
            for word in itertools.product((0, 1), repeat=length):
                assert membership(h, word) == source(h, word), (h, word)
                source_cases += 1
        for _ in range(500):
            word = tuple(rng.randrange(2) for _ in range(rng.randrange(6 * h * h + 1)))
            assert membership(h, word) == source(h, word), (h, word)
            source_cases += 1
    fooling_cases = 0
    for h in range(2, 6):
        b = h * h
        assert compiled_count(h) == (3 * h ** 3 - h) // 2 + 2
        identity = word_from_relation(h, sum(1 << (p * h + p) for p in range(h)))
        pairs = []
        for p in range(h):
            diagonal = word_from_relation(h, 1 << (p * h + p))
            for t in range(b):
                pairs.append((diagonal + identity[:t], identity[t:] + diagonal))
        for i, (x, _) in enumerate(pairs):
            for j, (_, y) in enumerate(pairs):
                assert membership(h, x + y) == (i == j), (h, i, j)
                fooling_cases += 1
    local_edges = 0
    mutant_witness = None
    for h in (2, 3):
        b = h * h
        for k in range(3):
            for j in range(k + 2):
                for phase in range(b):
                    for direction in (-1, 0, 1):
                        before = project(h, k, j, phase)
                        expected = before + direction
                        expected = expected if 0 <= expected <= k * b + 1 else None
                        after = compressed_step(h, k, j, phase, direction)
                        actual = None if after is None else project(h, k, after[0], after[1])
                        assert actual == expected, (h, k, j, phase, direction, actual, expected)
                        local_edges += 1
                        bad = compressed_step(h, k, j, phase, direction, mutant=True)
                        bad_project = None if bad is None else project(h, k, bad[0], bad[1])
                        if bad_project != expected and mutant_witness is None:
                            mutant_witness = {'h': h, 'relation_word_length': k, 'cell': j,
                                             'phase': phase, 'direction': direction,
                                             'wrong_projection': bad_project, 'required': expected}
    assert mutant_witness is not None
    target_cases = 0
    target_profiles = 0
    for deterministic in (True, False):
        for _ in range(100):
            n = rng.randrange(1, 5)
            table = {}
            for q in range(n):
                for c in ('L', 0, 1, 'R'):
                    legal = [0, 1] if c == 'L' else [-1, 0] if c == 'R' else [-1, 0, 1]
                    candidates = [(q2, d) for q2 in range(n) for d in legal]
                    if deterministic:
                        table[q, c] = [] if rng.randrange(4) == 0 else [rng.choice(candidates)]
                    else:
                        table[q, c] = [x for x in candidates if rng.randrange(4) == 0]
            finals = {q for q in range(n) if rng.randrange(2)}
            target_profiles += 1
            for length in range(3):
                for relations in itertools.product(range(16), repeat=length):
                    encoded = sum((word_from_relation(2, x) for x in relations), ())
                    for positive in (False, True):
                        a = binary_accept(table, finals, encoded, positive)
                        b = pullback_accept(2, table, finals, relations, positive)
                        assert a == b, (deterministic, table, finals, relations, positive)
                        target_cases += 1
    malformed_witness = (0,)
    assert not membership(2, malformed_witness)
    malformed_ignoring_mutant = membership(2, malformed_witness[:0])
    assert malformed_ignoring_mutant
    print(json.dumps({'source_word_comparisons': source_cases,
                      'fooling_cross_pairs': fooling_cases,
                      'local_move_projection_cases': local_edges,
                      'target_profiles': target_profiles,
                      'target_acceptance_comparisons': target_cases,
                      'seed': 23202966,
                      'wrong_boundary_phase_mutant_caught': mutant_witness,
                      'malformed_ignoring_mutant_caught': list(malformed_witness),
                      'failures': [],
                      'scope': 'Finite falsification only; uniform source/cut/lifting proofs are in INITIAL.md.'}, indent=2))


if __name__ == '__main__':
    main()
