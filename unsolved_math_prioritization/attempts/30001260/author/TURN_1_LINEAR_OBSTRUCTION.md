# Turn 1: rule out all orthogonal representation spheres

## Attempt and result

Try to construct the requested action as S(V) for a nonzero real S5 representation V. This approach fails in every dimension. This is a reproduction of the known linear obstruction, not a new theorem claimed against the literature.

Put t=(12), d=(12)(34),
E_A=<{(12)(34),(13)(24)}> and E_B=<{(12),(34)}>.
These are Klein four groups. Every nonidentity element of E_A is a double transposition; E_B has two transpositions and one double transposition.

Let U be the four-dimensional reduced permutation module of S5, let epsilon be the sign module, let D be the five-dimensional complement of the permutation module on vertices in the permutation module on unordered pairs, and let L=exterior^2 U. The vertex-to-pair incidence map is injective: its Gram matrix is 3I+J. Hence D is an actual real representation, not a virtual character. The following list is complete after complexification:

| Module | Dimension | trace(t) | trace(d) | dim V^E_A | dim V^E_B |
|---|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 | 1 |
| epsilon | 1 | -1 | 1 | 1 | 0 |
| U | 4 | 2 | 0 | 1 | 2 |
| epsilon U | 4 | -2 | 0 | 1 | 0 |
| D | 5 | 1 | 1 | 2 | 2 |
| epsilon D | 5 | -1 | 1 | 2 | 1 |
| L | 6 | 0 | -2 | 0 | 1 |

Here the character of U at g is f(g)-1, where f(g) counts its fixed letters. The character of D is the number of fixed unordered pairs minus f(g). The exterior-square formula gives chi_L(g)=(chi_U(g)^2-chi_U(g^2))/2. These formulas determine all seven rows on all 120 permutations. They have pairwise inner products delta_ij and squared dimensions summing to 120, so they are a complete irreducible complex character list. This calculation, reproduced exactly in `checks.py`, also avoids dependence on an unverified character-table transcription.

For any character chi, averaging gives

    dim V^E_A = (chi(1)+3chi(d))/4,
    dim V^E_B = (chi(1)+2chi(t)+chi(d))/4.

Every irreducible except L has nonzero E_A-fixed vectors. If a representation has V^E_A=0, its complexification is therefore a direct sum of L's. Every nonzero such sum has nonzero E_B-fixed vectors. Since real fixed spaces commute with complexification, no nonzero real V has both fixed spaces zero.

If 0 != v belongs to V^E, its normalization lies on S(V) and its stabilizer contains E. Thus every nonempty orthogonal S5 representation sphere has rank-two isotropy somewhere.

## Gap relative to the problem

This excludes only linear actions. A nonlinear smooth action need not have a global representation whose character encodes every fixed-set dimension. At a point, a tangent representation is a representation of that point's stabilizer, not of all S5 unless the point is globally fixed. Rank-one isotropy forbids such a global fixed point. Consequently this argument cannot be promoted to a nonexistence proof for the requested smooth action.

## Credit

The no-linear-action assertion is stated in Hambleton–Pamuk–Yalçın, *Equivariant CW-complexes and the orbit category*, introduction, and in Hambleton–Yalçın's 2026 survey, Section 8. This packet supplies its own elementary verification.
