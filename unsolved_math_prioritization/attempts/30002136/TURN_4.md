# Turn 4: resolving the five-gap reconstruction exception

2026-10-03 07:44 UTC. Substantive author turn 4/5. **NO FULL RESOLUTION.** Completion estimate: 10%, a planning estimate only. No novelty claim.

## Theorem and its scope

If a cyclically reduced word has at most five occurrences of one generator, all with the same sign, then any universal SL3-trace companion is conjugate to it. The other generator's exponents may be arbitrary integers. The new work in this turn is the five-occurrence case; Turn2 handles smaller counts. Letter-count and scalar-normalization reductions retain their prior credit.

Write a five-occurrence word, after changing b to its inverse if necessary, as a^(p1)b ... a^(p5)b. Any companion has the same form and same total gap sum S, by Turn2. Gap exponents may vanish or repeat.

## 1. A coefficient giving the directed-pair deck

Use the GL3 extension, set A=diag(x,y,z) with independent nonzero variables, and let B be generic. The coefficient of b11^2 b12 b23 b31 in the word trace is

Σ_(i mod5) x^(p_i+p_(i+1)+p_(i+2)) y^p_(i+3) z^p_(i+4).

Only the five rotations of the closed index path(1,1,1,2,3) contribute. Because S is fixed, equality of these coefficients is exactly equality of the multiset of directed adjacent gap pairs (p_i,p_(i+1)). Thus every companion has the same directed-pair deck.

Unlike length4, that deck is insufficient at length5: (r,r,s,r,t) and (r,r,t,r,s), for three distinct values r,s,t, are not cyclic rotations but have the same deck. This is an obstruction to this particular reconstruction statistic, not a trace-equivalent pair.

## 2. Classifying all five-gap deck collisions

A length5 cyclic sequence is determined by its directed-pair deck up to rotation, with exactly the preceding exceptional pair type. Here is a complete equality-pattern proof:

- Five distinct entries: every symbol has one outgoing edge, so the directed cycle is fixed.
- Multiplicity4+1 or5: only one arrangement up to rotation.
- Multiplicity3+2: the two occurrences of the minority value are either adjacent or separated; the loop/transition counts distinguish these arrangements. In the separated case, the two majority runs have lengths1 and2, equivalent under rotating the minority start.
- Multiplicity2+1+1+1: cut the cycle at the repeated symbol. Its two directed excursions are determined by the singleton successor edges. The possible orderings of two excursions are related by a cyclic rotation. A repeated-symbol loop is one of these excursions.
- Multiplicity2+2+1: rotate the singleton t to the start. The six possible sequences are trrss, trsrs, trssr, tsrrs, tsrsr, tssrr, with r≠s≠t≠r. Their directed-pair multisets are pairwise different, as direct inspection shows.
- Multiplicity3+1+1: call the repeated value r and the others s,t. If s,t are adjacent, their directed edge fixes their order and all r's form the complementary run. Otherwise, they are separated by positive r-runs of lengths1 and2. The two orderings are the exceptional pair above and have identical decks.

The checker additionally enumerates all5^5 symbol assignments, which covers every equality pattern by injective relabeling. It finds precisely30 distinct-deck collision classes; each is the stated exception for one repeated label and an unordered pair of other labels.

## 3. The exceptional trace difference is nonzero

For gaps(r,r,s,r,t), put p=s−r and q=t−r. These are nonzero and distinct. Set C=A^r B. As B ranges over GL3 with A fixed, C is arbitrary in GL3. Cyclically rotating the trace converts the two exceptional words into

tr(A^p C^2 A^q C^3),    tr(A^q C^2 A^p C^3).

Let e2(C) be the second elementary symmetric coefficient of C. Cayley–Hamilton gives C^3=tr(C)C^2−e2(C)C+det(C)I. In the difference Δ, the C^2 and I terms cancel by cyclic invariance of trace and commutation of A^p,A^q. Therefore

Δ=−e2(C)[tr(A^p C^2 A^q C)−tr(A^q C^2 A^p C)].

For A=diag(x1,x2,x3), direct expansion yields

tr(A^p C^2 A^q C)−tr(A^q C^2 A^p C)
 = −(c12 c23 c31−c13 c32 c21) det[(xi^p,xi^q,1)]_(i=1)^3.

The determinant is a nonzero Laurent polynomial: its six monomials are distinct permutations of the three distinct exponents p,q,0. The cycle difference and e2(C) are nonzero polynomials in independent C entries. Their product is nonzero because the Laurent-polynomial ring is an integral domain. Hence Δ cannot vanish identically on invertible A,C; those form a dense open set. The exceptional pair is not universally trace equivalent.

All directed-deck possibilities are now covered, proving the five-occurrence theorem. No finite numerical experiment is being used as a universal identity certificate.

## Checks and remaining gap

check_turn_4.py verifies the five-state coefficient formula by all243 closed paths, the3125 equality-pattern classifier, the generic symbolic Cayley–Hamilton trace reduction and determinant factor, and a concrete rational separated exceptional pair.

This still gives only a proper subfamily. At six and more gaps, a three-state trace coefficient merges several gap exponents and the deck reconstruction need not retain arbitrary order. Mixed-sign words with at least three minority-generator occurrences also remain outside Turns1–4. Final author turn will address the first mixed-sign boundary by exact generic-adjugate coefficients; no claim that resolving finitely many such boundaries settles the unrestricted target.
