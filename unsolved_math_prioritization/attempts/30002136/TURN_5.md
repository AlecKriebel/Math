# Turn 5: mixed-sign three-occurrence rigidity and final boundary

2026-10-03 07:48 UTC. Substantive author turn 5/5. **NO FULL RESOLUTION; author budget exhausted.** Completion estimate: 12%, a planning estimate only. No novelty claim.

## Final partial theorem

Let u∈F2. If, in some free basis, a cyclically reduced representative has either

(i) at most three total occurrences of one generator and its inverse, with arbitrary signs; or

(ii) at most five occurrences of one generator, all of the same sign,

then any v∈F2 with tr rho(u)=tr rho(v) for every rho:F2→SL3(C) is conjugate to u.

The other generator's exponents are unrestricted; total word length is unbounded. No restriction is placed on v at the outset. Turn2's independent unsigned cyclic-letter count and signed exponent-sum invariants force its corresponding counts. Condition(ii) is proved in Turn4; Turn3 handles condition(i) through count2. This turn proves the remaining mixed-sign count3 case. Simultaneous free-basis changes preserve both conjugacy and universal trace equivalence, so the stated automorphic version follows.

## 1. Canonical mixed-sign format

If all three signs are the same, use(ii). Otherwise invert b simultaneously if necessary, leaving two positive and one negative occurrence. For each cyclically reduced word, rotate to begin immediately after the unique negative b. The representative is

u=a^p b a^q b a^r b^-1.

Here p,r≠0 because the negative b cannot cancel either neighboring positive b cyclically; q may be zero. An arbitrary trace companion has the same signed counts and therefore the same format, with exponents p',q',r' obeying the same restrictions. Exponent-sum equality gives p+q+r=p'+q'+r'.

## 2. Extract the middle gap from a generic-adjugate coefficient

By the Turn1 extension, the identity holds on all GL3 pairs. Put A=diag(x1,x2,x3), with independent nonzero variables, and write B=(b_ij) generic. Multiplying the trace by det(B) replaces the final B^-1 with adj(B), giving the polynomial

F_(p,q,r)=tr(A^p B A^q B A^r adj(B)).

The coefficient of b12 b13 b21 b31 is

−x1^q (x2^p−x3^p)(x2^r−x3^r).

The factor in the last two variables is nonzero because p and r are nonzero. Equality with the companion coefficient therefore forces q=q': all its monomials have x1-exponent exactly q, and Laurent monomials are independent. Then p+r=p'+r'. Subtracting the equal pure-power terms from

(x2^p−x3^p)(x2^r−x3^r)
 = x2^(p+r)+x3^(p+r)−x2^p x3^r−x2^r x3^p

shows that {p,r}={p',r'} as multisets. This is valid also when q=0, p+r=0, p=r, or the exponents are negative.

## 3. Recover the orientation

If the ordered pairs agree, all gaps agree. The only other possibility swaps p and r. The coefficient of b11 b12 b23 b31 in F_(p,q,r) is

x1^q [x1^p x2^r+x3^p x1^r−x3^p x2^r].

Subtracting the swapped coefficient gives

x1^q det[(xi^p,xi^r,1)]_(i=1)^3.

If p≠r this determinant has six distinct Laurent monomials, since p,r,0 are distinct. Hence it is nonzero. If p=r there was no distinct ordered pair to begin with. Thus universal equality forces p=p',q=q',r=r'. The canonical cyclic representatives agree, proving conjugacy.

Both coefficient formulas follow by direct generic3×3 adjugate expansion; check_turn_5.py verifies them symbolically with all diagonal factors independent before substituting powers. The mathematical deduction is coefficient comparison, not finite-matrix interpolation.

## 4. Exact checks

The checker verifies both full symbolic coefficient identities, the alternant difference, and all252 triples p,r∈{−3,−2,−1,1,2,3}, q∈[−3,3] for the two-coefficient reconstruction with the common exponent sum. It also gives an exact rational separated example with a zero middle gap. These checks support the proof for arbitrary integer gaps, but they do not substitute for its universal argument.

## 5. Full target remains unresolved

No fixed nonconjugate universal SL3-trace-equivalent pair was found. No proof that all nonconjugate pairs can be separated was found. The five-turn budget is exhausted and this work stops rather than hiding further search inside review.

The remaining unrestricted family includes words for which, in every free basis, both generators occur at least four times if mixed signs occur, and at least six times in any generator that occurs with only one sign. This describes the complement of the proved sufficient exclusions; it does not claim such a family is empty or classify it. Recovering arbitrary cyclic order from all3-state path coefficients, or proving a universal separation theorem, remains unsupported. The positive-word reduction from Lawton–Louder–McReynolds is still conjectural and cannot eliminate the mixed-sign remainder.

The fixed-pair exact Laurent identity test from Turn1 remains available, but without a length bound or a suitable candidate it does not resolve existence. No search-bound improvement, general reversal exclusion, full resolution, or novelty claim is made. Final audit should distinguish correctness of these proper-subfamily lemmas from eligibility for a claimed solution to the original question.
