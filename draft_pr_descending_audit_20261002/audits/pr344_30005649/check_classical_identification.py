"""Check the exact Pries--Ulmer/Kraft convention match, using only stdlib.

Reference: Pries--Ulmer, NYJM 27 (2021), 705--739, sections 3.2.1 and 4.1.
The primary source writes w=u_(length-1)...u_0. A v at index j gives
V(e_(j+1))=e_j, rather than a forward V-arrow. This is a classification
comparison, not proof of historical novelty or of a Witt-ring realization.
"""
import json

word = 'vvfvff'
letters_by_index = list(reversed(word))
n = len(word)
classical_f = {j: (j + 1) % n for j, u in enumerate(letters_by_index) if u == 'f'}
classical_v = {(j + 1) % n: j for j, u in enumerate(letters_by_index) if u == 'v'}
submitted_f = {0: 1, 1: 2, 3: 4}
submitted_v = {0: 5, 3: 2, 5: 4}
assert classical_f == submitted_f and classical_v == submitted_v
rotations = sorted({word[j:] + word[:j] for j in range(n)})
complement = word.translate(str.maketrans('fv', 'vf'))
dual_rotations = sorted({complement[j:] + complement[:j] for j in range(n)})
assert len(rotations) == n  # Primitive cyclic word.
assert set(rotations).isdisjoint(dual_rotations)
print(json.dumps({
    'classical_printed_word': word,
    'forward_edge_word': ''.join(letters_by_index).upper(),
    'identity_basis_operator_match': True,
    'F_nonzero_basis_images': classical_f,
    'V_nonzero_basis_images': classical_v,
    'primitive_word': True,
    'rotations': rotations,
    'dual_word': complement,
    'dual_rotations': dual_rotations,
    'dual_cyclic_class_distinct': True,
    'limits': 'Applies the published construction/duality rules; does not check qss filtration, Honda lift, literature completeness, or first priority.',
}, indent=2))
