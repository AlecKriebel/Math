#!/usr/bin/env python3
"""Independent exact algebra checks; no author/audit imports or network.

The written report supplies both directions of the Tietze equivalence. These
computations independently falsify sign and scope mutations in genuine free
group semidirect-product normal forms, not an abelian approximation.
"""
import json
from pathlib import Path


def inv(word):
    return word.swapcase()[::-1]


def reduce(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == letter.swapcase():
            stack.pop()
        else:
            stack.append(letter)
    return ''.join(stack)


def substitute(word, images):
    return reduce(''.join(images[e] if e.islower() else inv(images[e.lower()])
                          for e in word))


class MappingTorus:
    def __init__(self, phi, psi):
        self.phi, self.psi = phi, psi
        for e in 'abc':
            assert substitute(phi[e], psi) == e
            assert substitute(psi[e], phi) == e

    def power(self, word, n):
        for _ in range(abs(n)):
            word = substitute(word, self.phi if n > 0 else self.psi)
        return word

    def mul(self, u, v):
        return reduce(u[0] + self.power(v[0], u[1])), u[1] + v[1]

    def inverse(self, u):
        return self.power(inv(u[0]), -u[1]), -u[1]

    def evaluate(self, word, gens):
        value = ('', 0)
        for e in word:
            factor = gens[e] if e.islower() else self.inverse(gens[e.lower()])
            value = self.mul(value, factor)
        return value


phi = {'a': 'a', 'b': 'ab', 'c': 'bcb'}
psi = {'a': 'a', 'b': 'Ab', 'c': 'BacBa'}
torus = MappingTorus(phi, psi)
identity = ('', 0)
gens = {'x': ('', 1), 'y': ('A', 1), 'b': ('b', 0), 'z': ('C', -1)}

# Vertical symbols: z=A, w=B, k=C, l=D. These are letter names, not vertices.
edge_data = [('p', 'w', 'z', 'x'), ('q', 'z', 'k', 'y'),
             ('r', 'l', 'k', 'x'), ('s', 'w', 'l', 'y'),
             ('d', 'z', 'w', 'b'), ('e', 'k', 'z', 'b')]
lambda_letters = {'x': 'y', 'y': 'x', 'b': 'B'}
product_relators = {e: label + end + inv(lambda_letters[label]) + inv(start)
                    for e, start, end, label in edge_data}
assert product_relators == {'p': 'xzYW', 'q': 'ykXZ', 'r': 'xkYL',
                            's': 'ylXW', 'd': 'bwbZ', 'e': 'bzbK'}
raw_relators = {'base_commutator': 'xyXY', 'base_annulus': 'bxBY',
                **product_relators}

# Solve p,q,r. The s solution from the tree is y^-1 x z y^-1 x,
# which equals x y^-1 z x y^-1 by [x,y]=1.
vertical_words = {'w': 'xzY', 'k': 'Yzx', 'l': 'xYzxY'}
for e, word in vertical_words.items():
    gens[e] = torus.evaluate(word, gens)
relation_values = {e: torus.evaluate(word, gens) for e, word in raw_relators.items()}
assert all(value == identity for value in relation_values.values())
assert torus.evaluate('ZbxzYb', gens) == identity

# Original target generators are recovered on the nose in their normal forms.
recover_words = {'a': 'xY', 'b': 'b', 'c': 'XZ', 't': 'x'}
recovered = {e: torus.evaluate(word, gens) for e, word in recover_words.items()}
assert recovered == {'a': ('a', 0), 'b': ('b', 0), 'c': ('c', 0), 't': ('', 1)}

# Check inverse changes of generators in both free groups, before any relation.
forward = {'x': 't', 'y': 'At', 'b': 'b', 'z': 'CT'}
backward = {'a': 'xY', 'b': 'b', 'c': 'XZ', 't': 'x'}
forward_then_back = {e: substitute(word, backward) for e, word in forward.items()}
back_then_forward = {e: substitute(word, forward) for e, word in backward.items()}
assert forward_then_back == {e: e for e in forward}
assert back_then_forward == {e: e for e in backward}

# Nearby-group controls. Both are themselves automorphisms, with independent
# two-sided inverse checks enforced by MappingTorus.
wrong_sign = MappingTorus({'a': 'a', 'b': 'ab', 'c': 'bcB'},
                         {'a': 'a', 'b': 'Ab', 'c': 'BacAb'})
workshop = MappingTorus({'a': 'a', 'b': 'aba', 'c': 'bcb'},
                       {'a': 'a', 'b': 'AbA', 'c': 'aBac aBa'.replace(' ', '')})
controls = {}
for name, other in [('wrong_final_b_inverse', wrong_sign), ('workshop_aba', workshop)]:
    other_gens = {e: other.evaluate(word, {'a': ('a', 0), 'b': ('b', 0),
                                          'c': ('c', 0), 't': ('', 1)})
                  for e, word in forward.items()}
    for e, word in vertical_words.items():
        other_gens[e] = other.evaluate(word, other_gens)
    failed = {e: other.evaluate(word, other_gens) for e, word in raw_relators.items()
              if other.evaluate(word, other_gens) != identity}
    assert failed
    controls[name] = failed

# Changing c=(zx)^-1 to c=(xz)^-1 gives z=t^-1 c^-1.
wrong_c_order = dict(gens)
wrong_c_order['z'] = torus.evaluate('TC', {'t': ('', 1), 'c': ('c', 0)})
wrong_c_residual = torus.evaluate('ZbxzYb', wrong_c_order)
assert wrong_c_residual != identity
controls['wrong_c_generator_order'] = wrong_c_residual

# Local symmetry control at the raw base-square boundary.
def dihedral(word):
    return {w[i:] + w[:i] for w in (word, inv(word)) for i in range(len(w))}

base_boundaries = dihedral('xyXY') | dihedral('bxBY')
assert substitute('bxBY', lambda_letters) in base_boundaries
assert substitute('bxBY', {'x': 'y', 'y': 'x', 'b': 'b'}) not in base_boundaries
controls['wrong_lambda_b_sign_detected'] = True

# Q is checked directly, independently of the prose and historical programs.
qedges = {'p': ('B', 'A', 'x'), 'q': ('A', 'C', 'y'),
          'r': ('D', 'C', 'x'), 's': ('B', 'D', 'y'),
          'd': ('A', 'B', 'b'), 'e': ('C', 'A', 'b')}
qfaces = ['pqRS', 'dpEQ']
def endpoints(e):
    u, v, _ = qedges[e.lower()]
    return (u, v) if e.islower() else (v, u)

def qlabel(e):
    label = qedges[e.lower()][2]
    return label if e.islower() else inv(label)

def corners(face):
    return [(inv(face[i-1]), face[i]) for i in range(len(face))]

klink = {frozenset(pair) for face in ['xyXY', 'bxBY'] for pair in corners(face)}
qdirs = {v: [] for v in 'ABCD'}
qcorners = {v: [] for v in 'ABCD'}
for e, (u, v, _) in qedges.items():
    qdirs[u].append(e)
    qdirs[v].append(inv(e))
for face in qfaces:
    assert ''.join(map(qlabel, face)) in base_boundaries
    for i, pair in enumerate(corners(face)):
        assert endpoints(face[i-1])[1] == endpoints(face[i])[0]
        qcorners[endpoints(face[i])[0]].append(pair)
qlinks = {}
for vertex in 'ABCD':
    image_dirs = list(map(qlabel, qdirs[vertex]))
    image_edges = [frozenset(map(qlabel, pair)) for pair in qcorners[vertex]]
    assert len(set(image_dirs)) == len(image_dirs)
    assert len(set(image_edges)) == len(image_edges)
    assert set(image_edges) == {edge for edge in klink if edge <= set(image_dirs)}
    qlinks[vertex] = {'directions': sorted(image_dirs),
                      'edges': sorted(sorted(edge) for edge in image_edges)}
tree = {'p', 'q', 's'}
components = {v: {v} for v in 'ABCD'}
for e in sorted(tree):
    u, v, _ = qedges[e]
    assert components[u] != components[v], 'tree cycle'
    merged = components[u] | components[v]
    for vertex in merged:
        components[vertex] = merged
assert components['A'] == set('ABCD')
collapsed_q_relators = [reduce(''.join(e for e in face if e.lower() not in tree))
                       for face in qfaces]
assert collapsed_q_relators == ['R', 'dE']
assert ''.join(map(qlabel, 'dp')) == 'bx'
assert substitute('bx', lambda_letters) == 'By'

# The auxiliary f=b^-1 lambda conjugation is a group identity in H.
# lambda(u)=by; b^-1 lambda(u)b=yb=bx=v.
assert torus.evaluate('ybXB', gens) == identity

# Exact abelianization data obtained directly from exponent rows.
def exponent_vector(word, ordered):
    return [sum((1 if c.islower() else -1) for c in word if c.lower() == e)
            for e in ordered]

target_rows = [exponent_vector(w, 'abct') for w in ['taTA', 'tbTBA', 'tcTBCB']]
wrong_rows = [exponent_vector(w, 'abct') for w in ['taTA', 'tbTBA', 'tcTbCB']]
workshop_rows = [exponent_vector(w, 'abct') for w in ['taTA', 'tbTAB A'.replace(' ', ''), 'tcTBCB']]
assert target_rows == [[0, 0, 0, 0], [-1, 0, 0, 0], [0, -2, 0, 0]]
assert wrong_rows == [[0, 0, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 0]]
assert workshop_rows == [[0, 0, 0, 0], [-2, 0, 0, 0], [0, -2, 0, 0]]

report = {
    'status': 'PASS',
    'mechanism': 'independent raw boundaries, reversible Tietze proof, exact free group semidirect normal forms',
    'phi': phi, 'two_sided_inverse': psi,
    'raw_relators': raw_relators, 'raw_relation_values': relation_values,
    'vertical_generator_values': {e: gens[e] for e in 'zwkl'},
    'original_generator_recovery': recovered,
    'free_generator_round_trips': [forward_then_back, back_then_forward],
    'Q_local_isometry_link_images': qlinks,
    'Q_tree_collapsed_relators': collapsed_q_relators,
    'Q_group_and_edge_maps': 'Z; generator dp maps to bx and b^-1 y, with b exponents +1 and -1',
    'negative_controls': controls,
    'abelianization': {
        'target_relation_rows': target_rows, 'target': 'Z^2 + Z/2',
        'wrong_final_b_inverse_rows': wrong_rows, 'wrong_final_b_inverse': 'Z^3',
        'workshop_aba_rows': workshop_rows, 'workshop_aba': 'Z^2 + (Z/2)^2'},
    'limitation': 'Computations supplement the full written two-way proof. They are not a geometry or historical-priority certificate.'}
destination = Path(__file__).with_name('exact_algebra_results.json')
destination.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
print(json.dumps(report, indent=2, sort_keys=True))
