# Independent audit of frozen Turns 4 and 5

Date: 2026-10-03. Scope: the length-five same-sign gap argument and the three-occurrence mixed-sign argument, their checkers, and the uses they make of the previously stated count and GL3-extension reductions. This audit does not establish those earlier count reductions independently, extend the search, or claim a full solution.

## Verdict

**PASS within the stated proper-subfamily scope. No mathematical correction is required in Turns 4 or 5.** Conditional on the earlier signed-count and GL3-extension reductions, Turn 4 proves rigidity for five same-sign occurrences, and Turn 5 proves rigidity for three mixed-sign occurrences. Neither argument settles the unrestricted universal SL3(C) problem. The explicit final unsolved status is appropriate.

The author checkers were independently executed from their frozen paths; both outputs are byte-for-byte equal to the saved TURN_4_CHECK.json and TURN_5_CHECK.json. More importantly, new controls below use a different implementation without importing author code or SymPy.

## Turn 4: coefficient, combinatorics, and arbitrary integer gaps

For tr(A^p1 B ... A^p5 B), with diagonal A having independent nonzero coordinates x,y,z, the prescribed B monomial has exactly the five rotations of the path (1,1,1,2,3). Each contributes the stated product of three consecutive x powers and one y and z power. With the total S fixed, the exponent vector associated to a directed pair (u,v) is (S-u-v,u,v). This map is injective for **all integers** u,v, including zero and negative values. Thus no arithmetic coincidence merges different directed pairs. Polynomial coefficient comparison is valid because the GL3 identity holds on the dense open invertible-B locus and the diagonal variables live in a Laurent-polynomial ring.

A directed deck determines the multiplicity of each label by its outgoing degree. Hence comparing cyclic orders of a fixed multiset is sufficient. The seven integer partitions of five give the exhaustive classification in the note:

- 5 and 4+1 have a unique cyclic order.
- 3+2 has either adjacent minority letters or separated minority letters; the decks distinguish them. In the separated case, the majority-run lengths are 1 and 2, and interchanging those two runs is a cyclic rotation.
- 2+1+1+1 has two excursions from the repeated label. Singleton successor edges determine each excursion, and their two possible orders differ by rotation.
- 2+2+1: fixing the singleton at the start leaves exactly six orders. The listed directed decks are all distinct. No further symmetry assumption about numerical labels is needed.
- 3+1+1: an edge joining the two singleton labels fixes their ordered adjacent case; without such an edge, the repeated-label runs have lengths 1 and 2, producing exactly the exceptional pair.
- 1+1+1+1+1 has a unique successor at each label.

This classification depends only on equality of labels, not their magnitudes or signs. Independently, the control enumerates the 52 restricted-growth set-partition representatives and all distinct multiset orders for each. Every collision is exactly the claimed 3+1+1 exception. The author's 30 collision classes over five available labels agree with 5 choices for the repeated label times 6 unordered choices for the two singleton labels.

The all-zero tuple, any constant tuple, and every other repeated/zero/negative pattern fall into the same exhaustive equality-pattern classification.

## Turn 4: exceptional rewrite and signs

Let P=A^(s-r), Q=A^(t-r), C=A^r B. The first exceptional word is C C P C C Q C, whose cyclic rotation is P C C Q C C C. The other is C C Q C C P C, giving Q C C P C C C. This verifies the stated orientation, including arbitrary negative r.

Writing

D3 = tr(P C^2 Q C) - tr(Q C^2 P C),
D5 = tr(P C^2 Q C^3) - tr(Q C^2 P C^3),

Cayley-Hamilton gives D5 = -e2(C) D3. The coefficient of tr(C) cancels by cyclicity, and the determinant term cancels because P and Q commute. For diagonal P and Q, direct index expansion gives

D3 = -(c12 c23 c31 - c13 c32 c21) det[(Pi,Qi,1)].

Consequently the **positive** product sign is

D5 = e2(C) (c12 c23 c31 - c13 c32 c21) det[(Pi,Qi,1)].

The independently computed formal cubic and quintic differences contain respectively 12 and 72 nonzero monomials and agree with these factorizations exactly.

The three exponent values s-r, t-r, 0 are distinct. Their six permutation monomials remain distinct even if the differences have opposite signs or sum to zero. The alternant is therefore nonzero. The other two factors are nonzero polynomials. Their product is nonzero in the integral domain C[x1^±1,x2^±1,x3^±1,c11,...,c33]. Restricting C to det(C) != 0 cannot make this product identically zero: it is a dense open subset. For each invertible diagonal A, B=A^(-r)C is invertible exactly when C is. Thus the nonvanishing gives a legitimate GL3 pair, and the earlier scalar normalization transfers the separation conclusion to SL3. This does not assume that a directed-deck collision is a trace collision.

## Turn 5: canonical format and coefficient identities

After a simultaneous inversion of b if necessary, exactly one b letter is negative. Cutting immediately after that occurrence gives a^p b a^q b a^r b^-1. Cyclic reduction forces p != 0 and r != 0; q=0 is permitted because the two adjacent positive b letters do not cancel. The unique negative occurrence fixes the cyclic cut. The same format applies to companions only through the earlier independent signed-count invariant, as the note correctly acknowledges.

An independent expansion uses

F = sum_(i,j,k) Pi Qj Rk b_ij b_jk adj(B)_ki,

and expands adj(B)_ki as (-1)^(i+k) times the 2-by-2 minor deleting row i and column k. This gives exactly:

- coefficient of b12 b13 b21 b31: -Q1(P2-P3)(R2-R3);
- coefficient of b11 b12 b23 b31: Q1(P1 R2 + P3 R1 - P3 R2).

No independent-matrix entries were replaced by sampled powers for this check. Substituting Pi=xi^p, Qi=xi^q, Ri=xi^r proves the two formulas for all integer exponents. Subtracting the second coefficient with P and R exchanged is Q1 det[(Pi,Ri,1)], with the sign given in the note.

## Turn 5: arbitrary-exponent reconstruction and edge cases

Because p,r are nonzero, both x2^p-x3^p and x2^r-x3^r are nonzero Laurent polynomials. Their product cannot vanish. Every term of the first coefficient has x1 exponent q, so equality forces q=q'. This works also for q=0 or q equal to another gap.

The known total then fixes h=p+r=p'+r'. Subtracting the common pure terms x2^h+x3^h gives equality of x2^p x3^r+x2^r x3^p and its primed counterpart. Laurent-monomial independence identifies the unordered exponent pairs, with multiplicities. In particular:

- p=r gives a monomial of multiplicity two and is handled without division;
- p+r=0 gives common pure contribution 2 and still determines the two mixed monomials;
- negative gaps introduce no loss of independence;
- zeros in p or r are excluded by cyclic reduction, rather than silently handled by a false nonvanishing claim;
- an all-zero triple is therefore not an admissible mixed-sign cyclically reduced three-occurrence word.

The only possible remaining ambiguity is swapping p and r. If distinct, p,r,0 are three distinct integers, so the six alternant monomials are distinct and the second coefficient separates the orientations. If equal, there is no ambiguity. No exception arises from q=0, repeated gaps, opposite gaps, or arbitrary negative exponents.

## Evidence files

- independent_gap_controls.py: fresh standard-library sparse integer-polynomial and equality-pattern controls; no author imports or symbolic-algebra dependency.
- independent_gap_controls.json: successful results, 52 set-partition patterns, five contributing paths, exact cofactor formulas, both formal factorizations, and cyclic rewrite.
- TURN_4_CHECK.reproduced.json and TURN_5_CHECK.reproduced.json: byte-identical reproductions of the author's saved check results.

The new finite pattern enumeration is exhaustive for equality-pattern combinatorics by injective relabeling. Neither it nor the author’s finite integer windows is used as a replacement for the arbitrary-integer Laurent argument above.
