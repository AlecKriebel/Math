# Independent acceptance: cyclic-powered triangles and the finite-support obstruction

14 October 2026 UTC. Row 1777 / 30005572. Review within the final shared PASS5/5, not an additional mathematical pass. No author proof, ledger, queue, or remote was edited by this reviewer.

## Verdict and frozen proof

ACCEPT the restricted statements in `pass5_symbol_calibration/CYCLIC_POWERED_TRIANGLES_AND_CALIBRATION_OBSTRUCTION.md`, SHA-256 `17c4cab7075c1886057e28fc19d680c96693a3a603857a0f92d1e5abd80830a6`.

The accepted advances are:

1. Every scalar-powered cyclic theta triangle is zero over R = Z[1/6], with an explicit exterior-square Steinberg witness that specializes at every characteristic-zero marked elliptic curve.
2. Coordinate projection is injective on the full SL2(O)-invariant finite torsion cycles on a CM square. This excludes a particular zero-marginal, external-product/fiber-supported endpoint-primitive construction.
3. At favorable unpowered CM levels, the genuine ray field has no retained roots of unity at primes dividing the level exponent. This is a unit-root uniqueness statement conditional on the actual theta entries having descended to that field.
4. For cyclic order seven, the free cross-ratio/evenness calculus has a nonzero formal quotient detected by a class of order seven. It is not a nonzero CM K2 triangle.

None of these statements computes the moving/shearing terms needed for source calibration. The full construction remains UNSOLVED.

## 1. The universal cancellation occurs in the correct group

The accepted PASS3 construction already supplies actual scalar-powered U_n values, exact family specialization, evenness, and the cross-ratio identity M_(U_n) = n[u]. The new proof does not reuse the withdrawn specialized-unit cancellation or the withdrawn divided CM-powered construction.

For an even formal system h on a group of size g, the displayed finite identity expresses g^2 Psi_h as a sum of double-delta terms with coefficients 1 and -1/4. This equality holds in the free exterior square before imposing any Steinberg relation. Repeated sign classes give identically zero delta; the proof never evaluates a degenerate cross-ratio.

On the universal cyclic exact-order-n family, g = n, and each delta is n^2 times a Steinberg wedge. Thus the finite identity reads

    n^2 Psi_(U_n) = n^2 W

in the exterior square of the universal unit group. Here W is the specified finite R-linear sum of u wedge (1-u), with no level denominator.

For K = Q(Y1(n)), n >= 4, geometric integrality gives constant field Q. The divisor sequence on a smooth projective model shows that K^times/{1,-1} is free abelian: its divisor image is a subgroup of a free group, and its constants are Q^times/{1,-1}, also free. The resulting exact sequence splits because the quotient is free. Consequently K^times tensor R and its exterior square are free R-modules. Cancellation of n^2 is valid there.

Only after this cancellation does the proof pass to K2 and kill W. It never cancels n or n^2 in a specialized K2 group. Cases n = 1,2,3 are dealt with directly and do not invoke a nonexistent fine universal moduli problem at those small orders.

## 2. Specialization is an actual unit identity

The U_n entries have the already accepted family-unit property. Distinct torsion sign classes have distinct x-coordinates on every characteristic-zero elliptic fiber, so the nondegenerate cross-ratios and their complements are units at every point where they are used.

The canceled equality therefore lies in the exterior square of units regular at each moduli point and can be evaluated there. The inclusion of this torsion-free unit submodule into the function-field unit module induces an injection on exterior squares over the localization R of Z; equivalently, injectivity can be checked after passage to the fraction field. This justifies the proof's stated equivalent local-unit formulation.

The specialization field can contain arbitrary level-primary roots of unity. Those do not affect an identity established in the universal group before specialization. Conversely, the theorem does not provide an unpowered relation merely because U_n = n theta has been separately established: that substitution only gives n^2 Psi_theta = 0 in K2.

The cyclic hypothesis is real. The proof uses both |G| = n and the rational constant field of the one-point modular curve. It does not assert the same result for a general rank-two marked torsion group.

## 3. The finite-cycle obstruction uses the actual geometric group

Over O/q^r, the SL2-orbits of vectors are indexed by their common q-adic content j. An element of minimum valuation j is a uniformizer power times a primitive row, and a primitive row can be completed to determinant one. For a projected coordinate of valuation k, the counting matrix is lower triangular with diagonal

    Q^r, Q^(r-1), ..., Q, 1.

All entries on this diagonal are nonzero divisors in R. The argument cancels a scalar in a free divisor module, rather than in K2, and never inverts Q.

CRT gives the general ideal case by a tensor product of the local matrices. Its determinant is nonzero, so the map is injective over R. The finite semilocal group SL2(O/c) is generated by elementary matrices, and each such matrix lifts to SL2(O). Thus the invariance group has not been silently enlarged beyond the actual full same-curve geometric group.

Every external product of two degree-zero divisors has zero coordinate marginal. The conclusion remains true if its support is enlarged and then cancels in the final finite cycle, or if a finite field-extension trace is applied. Therefore no nonzero invariant finite torsion cycle of the specified kind can have the required zero marginal. Enlarging finite torsion support does not evade the theorem, because one common scalar annihilator contains that support.

This is expressly a theorem for E x E and full SL2(O). It is not an assertion about every smaller congruence subgroup or the mixed products E_r x E_1 on all Bianchi components.

### Repaired coordinate-direction error

The first review draft defined projection by [x,y] -> [y] but described its collapsed fibers as {T} x E. Those fibers map isomorphically under that projection, so the sentence was incorrect. The author repaired it: the second projection collapses E x {T}; the analogous first projection collapses {T} x E. The standard auxiliary cycle has a nonzero marginal for both projections. Hence the intended exclusion of a one-direction fiber-supported primitive is valid after the repair. The frozen hash above includes this correction.

The obstruction does not rule out moving chains with more general support, arithmetic-specialization identities, or the original construction.

## 4. Ray-field roots are separated from K2 torsion

If the accepted norm-coefficient ideal criterion is satisfied and p >= 5 divides the additive level exponent, p splits in F and exactly one prime above p divides N. The ray field F(N) is unramified at the other prime. Since the local field of F there is Q_p, adjoining mu_p is ramified of degree p-1. Therefore mu_p cannot be contained in F(N).

This proves injectivity of multiplication by the level exponent on F(N)^times tensor R. It gives uniqueness of an unpowered unit satisfying U_n = n theta when that unit is already constructed and descended there. It supplies neither existence nor descent of that theta entry, and no corresponding injectivity statement for K2 is asserted.

For order seven, the two cross-ratio vectors have wedge -7 Psi. All nondegenerate quadruples use the same four sign classes; their permutations give the same Steinberg relation up to sign. The relation lattice is precisely R(7 Psi), and Psi is primitive. The displayed functional to R/7R verifies that its formal quotient class is nonzero of exact order seven. Further Steinberg relations in an actual field can still kill its image. This is a method limitation, not an arithmetic counterexample.

## 5. Calibration, signs, and homology remain outside the theorem

The report consistently preserves the accepted source reciprocal-tame convention for geometric cocycles. The new degree-zero support argument and pure symbol identities do not identify any positive raw pair with a positive source-sign cocycle.

In particular, the exact swap formula remains a swapped-basis transition. Its specialization does not evaluate the full moved primitive, whose shear transitions have not been computed. The raw level-four factor 576 and the required three-term factor 624 remain distinct on individual edges. The prior cyclic-four potential gives a relative map with zero absolute restriction, not a proof that the canonical geometric absolute map vanishes on represented balanced chains.

No Bianchi homology generation, all-component transport, unrestricted unpowered-root descent, full relative extension calibrated to the geometric map, or integer-ring absolute target follows from this paper.

## 6. Verification and source boundary

The proof, corrected coordinate sentence, author checker, and accepted dependencies were inspected. Independent exact sparse-exterior checks cover every cyclic n = 2 through 17, every triple and pair, all degenerate-sign quadruples, and the explicit double-delta witness. Separate independent counts check integer quotient rings and the general local projection determinants. These checkers use explicit exceptions rather than Python assertions and produce identical results under ordinary Python, -O, and -OO. The author checker is replayed separately.

Primary-source checks: Sharifi–Venkatesh, *Eisenstein cocycles in motivic cohomology*, §§6.3–6.4, explicitly work with a GL2(Z)-invariant corrected cycle and external products. Their group is not the full CM SL2(O). Source URL: https://math.ucla.edu/~sharifi/eisensymbol.pdf . The inverse-tame sign was checked at equation (2.4). LSSW §3.4 was inspected for the actual moved primitive: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf .

Finite algebra verifies the stated identities and support counts. It does not compute an actual number-field K2 group, a sheared arithmetic cocycle value, or a full homology comparison. No novelty or literature-exhaustiveness certificate is given.
