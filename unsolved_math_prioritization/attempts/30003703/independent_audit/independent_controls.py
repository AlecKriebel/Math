#!/usr/bin/env python3
"""Independent exact audit controls. Standard library only, no network or writes.

Does not import the authored verifier. Uses dense coefficient recurrence for
Magnus expansions and exponent-vector arithmetic in universal determinant
quotients for SL2 words. The written report supplies the universal proof.
"""
import hashlib
import itertools
import json
from pathlib import Path

EXPECTED_MANIFEST = '9770e7f73a5ffc81f52d92c38f3bebcc9714b470b854f9281e9749b4584591be'


def inv(word):
    return [-x for x in word[::-1]]


def reduced(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return stack


def comm(a, b, convention='forward'):
    if convention == 'inverse_first':
        return reduced(inv(a) + inv(b) + a + b)
    if convention == 'reverse_outer':
        a, b = b, a
    return reduced(a + b + inv(a) + inv(b))


def make_words(convention='forward'):
    def c(a, b):
        return comm(a, b, convention)
    x, y, z = [1], [2], [3]
    return c(c(c(x, y), c(x, z)), x), c(c(c(x, y), c(x, c(x, y))), x)


def magnus_dense(word, rank, bound):
    # Coefficients ordered by length; multiplying on the right by (1+X)^-1
    # is the recurrence new[w] = old[w] - new[w without final X].
    keys = [()]
    for length in range(1, bound + 1):
        keys.extend(itertools.product(range(1, rank + 1), repeat=length))
    previous = {w: int(not w) for w in keys}
    for letter in word:
        current = {}
        for w in keys:
            c = previous[w]
            if w and w[-1] == abs(letter):
                c += previous[w[:-1]] if letter > 0 else -current[w[:-1]]
            current[w] = c
        previous = current
    return {w: c for w, c in previous.items() if c}


def substitution(word, images):
    answer = []
    for letter in word:
        term = images[abs(letter)]
        answer.extend(term if letter > 0 else inv(term))
    return reduced(answer)


def compositions(word, moving, rank):
    p = {i: [i] for i in range(1, rank + 1)}
    q = {i: [i] for i in range(1, rank + 1)}
    p[moving] += word
    q[moving] += inv(word)
    return [substitution(p[i], q) for i in p], [substitution(q[i], p) for i in p]


class JetRing:
    """Z[t_1,...,t_variables]/(monomials of total degree >= order)."""
    def __init__(self, variables, order):
        self.variables, self.order = variables, order
        self.zero = (0,) * variables
        self.one = {self.zero: 1}

    def const(self, n):
        return {self.zero: n} if n else {}

    def variable(self, index):
        exponent = [0] * self.variables
        exponent[index] = 1
        return {tuple(exponent): 1}

    def add(self, *terms):
        answer = {}
        for term in terms:
            for e, c in term.items():
                answer[e] = answer.get(e, 0) + c
                if not answer[e]:
                    del answer[e]
        return answer

    def neg(self, p):
        return {e: -c for e, c in p.items()}

    def product(self, p, q):
        answer = {}
        for e, c in p.items():
            for f, d in q.items():
                g = tuple(x+y for x, y in zip(e, f))
                if sum(g) < self.order:
                    answer[g] = answer.get(g, 0) + c*d
                    if not answer[g]:
                        del answer[g]
        return answer

    def reciprocal_unit(self, a):
        answer, term = self.one, self.one
        for _ in range(1, self.order):
            term = self.product(term, self.neg(a))
            answer = self.add(answer, term)
        return answer

    def identity(self):
        return [[self.one, {}], [{}, self.one]]

    def matmul(self, a, b):
        return [[self.add(*(self.product(a[i][k], b[k][j]) for k in range(2)))
                 for j in range(2)] for i in range(2)]

    def minus(self, a, b):
        return [[self.add(a[i][j], self.neg(b[i][j])) for j in range(2)] for i in range(2)]

    def adjugate(self, m):
        return [[m[1][1], self.neg(m[0][1])], [self.neg(m[1][0]), m[0][0]]]

    def determinant(self, m):
        return self.add(self.product(m[0][0], m[1][1]),
                        self.neg(self.product(m[0][1], m[1][0])))

    def generator(self, i, omit_bc=False, exact_traceless=False):
        a, b, c = (self.variable(3*i+j) for j in range(3))
        numerator = self.neg(a) if omit_bc else self.add(self.product(b,c), self.neg(a))
        d = self.neg(a) if exact_traceless else self.product(numerator, self.reciprocal_unit(a))
        return [[self.add(self.one, a), b], [c, self.add(self.one, d)]]

    def word_value(self, word, matrices):
        value = self.identity()
        for letter in word:
            m = matrices[abs(letter)-1]
            value = self.matmul(value, m if letter > 0 else self.adjugate(m))
        return value


def matrix_profile(matrix):
    out = []
    for row in matrix:
        for p in row:
            by_degree = {}
            for e in p:
                degree = sum(e)
                by_degree[str(degree)] = by_degree.get(str(degree), 0) + 1
            out.append(by_degree)
    return out


def matrix_digest(matrix):
    data = [[[list(e), c] for e, c in sorted(p.items())] for row in matrix for p in row]
    return hashlib.sha256(json.dumps(data, separators=(',', ':')).encode()).hexdigest()


def integer_matmul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def integer_bracket(a,b):
    u,v = integer_matmul(a,b), integer_matmul(b,a)
    return [[x-y for x,y in zip(r,s)] for r,s in zip(u,v)]


def integer_word(word, matrices):
    out = [[1,0],[0,1]]
    for letter in word:
        a,b = matrices[abs(letter)-1]
        matrix = [a,b] if letter>0 else [[b[1],-a[1]],[-b[0],a[0]]]
        out = integer_matmul(out,matrix)
    return out


def run(release=None):
    w,v = make_words()
    w_lead = magnus_dense(w,3,5)
    v_lead = magnus_dense(v,2,6)
    assert w_lead.get((1,1,2,1,3)) == -1
    assert v_lead.get((1,1,1,2,1,2)) == 1
    assert {len(x) for x in w_lead} == {0,5} and len(w_lead) == 13
    assert {len(x) for x in v_lead} == {0,6} and len(v_lead) == 11
    assert magnus_dense(w,3,4) == {():1}
    assert magnus_dense(v,2,5) == {():1}
    for word,t in [(w,4),(v,3)]:
        for rank in [t,t+1,9]:
            p,q = compositions(word,t,rank)
            assert p == q == [[i] for i in range(1,rank+1)]
    assert compositions(w,1,3) != ([[1],[2],[3]],[[1],[2],[3]])
    assert compositions(v,1,2) != ([[1],[2]],[[1],[2]])

    # A genuine polynomial-identity test: truncation is strictly ABOVE each
    # polynomial's maximum degree, so no tested term is discarded.
    def bracket(ring, a, b):
        return ring.minus(ring.matmul(a,b),ring.matmul(b,a))
    r = JetRing(9,7)
    def traceless(ring,i):
        a,b,c = [ring.variable(3*i+j) for j in range(3)]
        return [[a,b],[c,ring.neg(a)]]
    X,Y,Z = [traceless(r,i) for i in range(3)]
    P = bracket(r,bracket(r,bracket(r,X,Y),bracket(r,X,Z)),X)
    Q = bracket(r,bracket(r,bracket(r,X,Y),bracket(r,X,bracket(r,X,Y))),X)
    assert P == Q == [[{},{}],[{},{}]]

    jets = {}
    for name,word,rank,N in [('w',w,3,6),('v',v,2,7)]:
        ring = JetRing(3*rank,N+1)
        matrices = [ring.generator(i) for i in range(rank)]
        for m in matrices:
            assert ring.determinant(m) == ring.one
            assert ring.matmul(m,ring.adjugate(m)) == ring.identity()
        displacement = ring.minus(ring.word_value(word,matrices),ring.identity())
        profile = matrix_profile(displacement)
        # Compute through the next degree too, rather than manufacturing zero
        # by stopping before the disputed order.
        assert all(all(int(k)>=N for k in p) for p in profile)
        assert any(profile)
        smaller = JetRing(3*rank,N)
        exact = smaller.word_value(word,[smaller.generator(i) for i in range(rank)])
        assert exact == smaller.identity()
        jets[name] = {'universal_variables':3*rank, 'vanishes_mod_ideal_power':N,
                      'next_degree_entry_profiles':profile,
                      'next_degree_matrix_sha256':matrix_digest(displacement)}

    ring = JetRing(3,4)
    a,b,c = [ring.variable(i) for i in range(3)]
    bad_det = ring.add(ring.determinant(ring.generator(0,omit_bc=True)),ring.neg(ring.one))
    assert bad_det == ring.neg(ring.product(b,c))
    bad_trace_det = ring.add(ring.determinant(ring.generator(0,exact_traceless=True)),ring.neg(ring.one))
    assert bad_trace_det == ring.neg(ring.add(ring.product(a,a),ring.product(b,c)))
    good = ring.generator(0)
    actual_trace = ring.add(good[0][0],good[1][1],ring.const(-2))
    assert actual_trace and min(sum(e) for e in actual_trace) == 2

    inverse_first_w,inverse_first_v = make_words('inverse_first')
    assert inverse_first_w != w and inverse_first_v != v
    assert magnus_dense(inverse_first_w,3,5) == w_lead
    assert magnus_dense(inverse_first_v,2,6) == v_lead
    assert magnus_dense(inverse_first_w,3,6) != magnus_dense(w,3,6)
    assert magnus_dense(inverse_first_v,2,7) != magnus_dense(v,2,7)
    x,y,z = [1],[2],[3]
    inner = comm(comm(x,y),comm(x,z))
    swapped = comm(inner,x,'reverse_outer')
    assert magnus_dense(swapped,3,5).get((1,1,2,1,3)) == 1
    raw_comm = magnus_dense(comm(x,y),2,2)
    assert raw_comm == {():1,(1,2):1,(2,1):-1}

    H,E,F = [[1,0],[0,-1]], [[0,1],[0,0]], [[0,0],[1,0]]
    C = integer_bracket(integer_bracket(H,E),integer_bracket(H,F))
    assert C == [[-4,0],[0,4]]
    assert integer_bracket(C,H) == [[0,0],[0,0]]
    assert integer_bracket(C,E) == [[0,-8],[0,0]]
    H3,E12,E23 = [[1,0,0],[0,-1,0],[0,0,0]],[[0,1,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,1],[0,0,0]]
    wrong_size = integer_bracket(integer_bracket(integer_bracket(H3,E12),integer_bracket(H3,E23)),H3)
    assert wrong_size == [[0,0,2],[0,0,0],[0,0,0]]
    numerical = [[[1,1],[0,1]],[[1,0],[1,1]],[[2,1],[1,1]]]
    w_value,v_value = integer_word(w,numerical),integer_word(v,numerical)
    assert w_value != [[1,0],[0,1]] and v_value != [[1,0],[0,1]]

    binding = {'result':'not_requested'}
    if release:
        release = Path(release)
        raw = (release/'MANIFEST.json').read_bytes()
        assert hashlib.sha256(raw).hexdigest() == EXPECTED_MANIFEST
        manifest = json.loads(raw)
        for item in manifest['files']:
            contents = (release/item['path']).read_bytes()
            assert len(contents) == item['bytes']
            assert hashlib.sha256(contents).hexdigest() == item['sha256']
        retained = json.loads((release/'verification.json').read_text())
        assert retained['w5_reduced_word'] == w
        assert retained['v6_reduced_word'] == v
        for field,expansion in [('p5_free_associative_terms',w_lead),('q6_free_associative_terms',v_lead)]:
            supplied = {tuple(term['word']):term['coefficient'] for term in retained[field]}
            assert supplied == {key:value for key,value in expansion.items() if key}
        binding = {'result':'PASS','manifest_sha256':EXPECTED_MANIFEST,'files_verified':len(manifest['files'])}
    return {'result':'PASS','method':'Independent exact integer arithmetic; no authored verifier imports',
            'binding':binding,'word_lengths':{'w':len(w),'v':len(v)},
            'magnus_coefficients':{'XXYXZ':w_lead[(1,1,2,1,3)],'XXXYXY':v_lead[(1,1,1,2,1,2)]},
            'magnus_nonconstant_term_counts':{'w':len(w_lead)-1,'v':len(v_lead)-1},
            'universal_determinant_quotients':jets,
            'universal_traceless_polynomial_identities':'P and Q zero; no possible term truncated',
            'automorphism_two_sided_inverse_checks':'PASS at base rank, base+1, and rank 9; arbitrary rank justified in report',
            'negative_controls':{
                'changed_outer_commutator_order':'wrong coefficient +1 detected',
                'inverse_first_convention':'same leading terms but distinct higher jets; not incorrectly rejected as opposite sign',
                'missing_bc_in_determinant_correction':'determinant defect -bc detected',
                'traceless_replacement_at_all_orders':'determinant defect -a^2-bc and nonzero actual trace detected',
                'distinct_outer_matrix':'[[0,-8],[0,0]] is nonzero',
                'outer_commutator_deleted':'[[-4,0],[0,4]] is nonzero',
                'size_three_extension':wrong_size,
                'commuting_magnus_letters':'XY-YX detected',
                'moving_generator_occurs_in_word':'both naive inverses fail',
                'one_degree_stronger_ideal_membership':'both nonzero next-degree matrices detected',
                'group_law_from_lie_identity':{'w_value':w_value,'v_value':v_value},
                'rank_three_false_degree_five_certificate':'v expansion through degree 5 is exactly 1'},
            'proof_role':'Reproducibility controls only; universal group/ring implications proved in AUDIT.md'}


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--release',type=Path)
    args=parser.parse_args()
    print(json.dumps(run(args.release),indent=2,sort_keys=True))
