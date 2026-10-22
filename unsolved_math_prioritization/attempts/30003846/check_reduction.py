# Hardened derivative: explicit guards survive -O/-OO; stdout only.
"""Exact finite replay of the published GS reduction, with local move guards.
No floating point arithmetic, group-isomorphism oracle, or copied source text.
"""
from check_combinatorics import diagrams, connected, is_peelable, peel
import json, pathlib, time, itertools

class Complex:

    def __init__(self, word, bumps):
        self.word = tuple(word)
        N = len(word)
        par = list(range(N + 1))

        def root(i):
            while par[i] != i:
                i = par[i]
            return i
        for l, r in bumps:
            i, j = (word.index(l), word.index(r))
            if not j > i + 1:
                raise AssertionError()
            par[root(j)] = root(i + 1)
        self.vertices = {root(i) for i in range(N + 1)}
        self.edges = {e: (root(i), root(i + 1)) for i, e in enumerate(word)}
        self.cells = {}
        for l, r in bumps:
            i, j = (word.index(l), word.index(r))
            gap = tuple(word[i + 1:j])
            self.cells[l] = [(l,), (l,) + gap]
            self.cells[r] = [(r,), gap + (r,)]
        self.moves = []
        self.mapping = {e: (e,) for e in word}
        self.validate()

    def endpoints(self, w):
        if not w:
            raise AssertionError()
        es = [self.edges[e] for e in w]
        if not all((a[1] == b[0] for a, b in zip(es, es[1:]))):
            raise AssertionError(('notpath', w, es))
        return (es[0][0], es[-1][1])

    def validate(self):
        for u, v in self.cells.values():
            if not self.endpoints(u) == self.endpoints(v):
                raise AssertionError()

    def add(self, e, w):
        w = tuple(w)
        if not e not in self.edges:
            raise AssertionError()
        self.edges[e] = self.endpoints(w)
        self.cells[e] = [(e,), w]
        self.moves.append(('add', e, w))
        self.validate()

    def rewrite(self, target, side, witness, rev=False, at=None):
        if not target != witness:
            raise AssertionError()
        old, new = self.cells[witness][::-1] if rev else self.cells[witness]
        w = self.cells[target][side]
        if at is None:
            at = next((i for i in range(len(w) - len(old) + 1) if w[i:i + len(old)] == old))
        if not w[at:at + len(old)] == old:
            raise AssertionError()
        self.cells[target][side] = w[:at] + new + w[at + len(old):]
        self.moves.append(('rw', target, side, witness, rev, at))
        self.validate()

    def substitute_all(self, e):
        if not (self.cells[e][0] == (e,) and e not in self.cells[e][1]):
            raise AssertionError()
        for c in list(self.cells):
            if c == e:
                continue
            for side in range(2):
                while e in self.cells[c][side]:
                    self.rewrite(c, side, e)

    def delete(self, e):
        top, bot = self.cells[e]
        if not (top == (e,) and e not in bot):
            raise AssertionError()
        if not all((e not in u + v for c, (u, v) in self.cells.items() if c != e)):
            raise AssertionError()
        del self.cells[e]
        del self.edges[e]
        for x, w in self.mapping.items():
            self.mapping[x] = tuple((y for a in w for y in (bot if a == e else (a,))))
        self.moves.append(('del', e))
        self.validate()

    def replay_lift(self, moves):
        for m in moves:
            if m[0] == 'add':
                self.add(*m[1:])
            elif m[0] == 'rw':
                self.rewrite(*m[1:])
            else:
                self.substitute_all(m[1])
                self.delete(m[1])

    def check_core(self, n, word, bumps):
        left, right = (word[0], word[-1])
        source = self.edges[left][0]
        sink = self.edges[right][1]
        dummy = set(word) - {e for pair in bumps for e in pair}
        if not dummy <= self.edges.keys():
            raise AssertionError()
        if not set(self.cells) == set(self.edges) - dummy:
            raise AssertionError()
        if not len(self.cells) == n + 1:
            raise AssertionError()
        inner = set(self.edges) - {left, right}
        V = self.vertices - {source, sink}
        if not len(inner) == len(V) == n + len(dummy) - 1:
            raise AssertionError()
        succ = {}
        for e in inner:
            a, b = self.edges[e]
            if not (a in V and b in V and (a not in succ)):
                raise AssertionError()
            succ[a] = e
        if not (set(succ) == V and {self.edges[e][1] for e in inner} == V):
            raise AssertionError()

        def cycle(v):
            out = []
            start = v
            while True:
                e = succ[v]
                out.append(e)
                v = self.edges[e][1]
                if v == start:
                    break
                if not len(out) <= len(inner):
                    raise AssertionError()
            if not set(out) == inner:
                raise AssertionError()
            return tuple(out)
        for e, (top, bot) in self.cells.items():
            if not top == (e,):
                raise AssertionError()
            expected = cycle(self.edges[e][0]) + (e,) if e == right else (e,) + cycle(self.edges[e][1])
            if not bot == expected:
                raise AssertionError((e, bot, expected))
        base = tuple((y for e in word for y in self.mapping[e]))
        if not self.endpoints(base) == (source, sink):
            raise AssertionError()
        return len(self.moves)

def reduce(word, bumps):
    word = list(word)
    bumps = sorted(bumps, key=lambda pair: word.index(pair[1]))
    n = len(bumps)
    K = Complex(word, bumps)
    if n == 2:
        (a, c), (b, d) = bumps
        if not word.index(a) < word.index(b) < word.index(c) < word.index(d):
            raise AssertionError()
        i, j = (word.index(b), word.index(c))
        s = 'new_2'
        K.add(s, word[i:j + 1])
        K.rewrite(c, 1, s, True)
        K.rewrite(b, 1, s, True)
        K.substitute_all(b)
        K.delete(b)
        K.substitute_all(c)
        K.delete(c)
    else:
        l, r = bumps[-1]
        oldr = bumps[-2][1]
        ir = word.index(oldr)
        il = word.index(l)
        if not il < ir:
            raise AssertionError()
        smallword = word[:ir + 1]
        old, moves, _ = reduce(smallword, bumps[:-1])
        K.replay_lift(moves)
        cycle = old.cells[oldr][1][:-1]
        q = cycle.index(l)
        X = cycle[:q]
        Y = cycle[q + 1:]
        D = tuple(word[ir + 1:-1])
        P = tuple(word[il + 1:ir])
        image = tuple((y for e in P for y in old.mapping[e]))
        if not image[:len(Y)] == Y:
            raise AssertionError()
        rest = image[len(Y):]
        if not len(rest) % len(cycle) == 0:
            raise AssertionError()
        s = len(rest) // len(cycle)
        if not rest == cycle * s:
            raise AssertionError()
        for _ in range(s):
            K.rewrite(l, 1, oldr, True)
            K.rewrite(r, 1, oldr, True)
        if not K.cells[l][1] == (l,) + Y + (oldr,) + D:
            raise AssertionError()
        if not K.cells[r][1] == Y + (oldr,) + D + (r,):
            raise AssertionError()
        p = 'new_' + str(n)
        K.add(p, (l,) + Y + (oldr,))
        K.rewrite(l, 1, p, True)
        K.rewrite(oldr, 1, p, True)
        if not (K.cells[l][1] == (p,) + D and K.cells[oldr][1] == X + (p,)):
            raise AssertionError()
        K.substitute_all(l)
        K.delete(l)
        K.substitute_all(oldr)
        K.delete(oldr)
    K.check_core(n, word, bumps)
    return (K, K.moves, K.mapping)

def decorate(d, amounts):
    word = []
    for i, (a, s) in enumerate(d):
        word.append(('R' if s else 'L') + str(a))
        if i < len(d) - 1:
            word.extend(('d_%d_%d' % (i, j) for j in range(amounts[i])))
    bumps = [('L' + str(a), 'R' + str(a)) for a in range(len(d) // 2)]
    return (word, bumps)

def main():
    start = time.time()
    rows = []
    maxmoves = 0
    for n in range(2, 7):
        count = 0
        seen = set()
        for d in diagrams(n):
            if not connected(d):
                continue
            d, _ = peel(d)
            if d in seen:
                continue
            seen.add(d)
            variants = [[0] * (2 * n - 1), [1] * (2 * n - 1), [i % 3 for i in range(2 * n - 1)]]
            if n == 2:
                variants = list(itertools.product(range(4), repeat=3))
            for amounts in variants:
                w, b = decorate(d, amounts)
                K, m, _ = reduce(w, b)
                count += 1
                maxmoves = max(maxmoves, len(m))
        rows.append(dict(n=n, distinct_labelled_peeling_outputs=len(seen), partition_instances=count))
    result = dict(status='PASS', rows=rows, max_GS_moves=maxmoves, elapsed_seconds=round(time.time() - start, 3), limitations='Only finite instances of the stated GS algorithm. Each recorded move is checked for nonempty paths, matching endpoints, distinct witness and target cells, valid rewriting occurrence, and legal edge deletion. This does not certify the external diagram-group theorems or the all-n mathematical induction.')
    print(json.dumps(result, indent=2))
if __name__ == '__main__':
    main()
