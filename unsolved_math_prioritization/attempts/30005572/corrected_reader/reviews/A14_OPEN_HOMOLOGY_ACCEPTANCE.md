# Independent acceptance: the integral open map at all good primes

14 October 2026 UTC. Row1777 /30005572. Review within shared PASS4/5. No additional pass or remote change.

## Verdict

ACCEPT `pass4_arithmetic_descent/OPEN_HOMOLOGY_GOOD_HECKE.md`, SHA-256:

`6a7d1119621077d1c7df59fb77c18cae793244cd2ed857a6f82c30af5a3ff271`.

Under proper unit-injective level N, with auxiliary c prime to5N, the accepted arithmetic family gives an actual auxiliary map

Pi_(c,N):H1(Y1(N),Z[1/6])->K2(O'(N)) tensor Z[1/6]

on all h Bianchi components. It satisfies the source's good-prime equation Pi_(c,N)(T_q−Nq−S_q)=0 for every q not dividingN, including primes above5, and its component-compatible central equation Pi_(c,N)S_q=R_N(q)Pi_(c,N). The statements descend to every unaugmented block already constructed by valid auxiliary cancellation.

This is an open-space theorem. It does not provide compactification or the integer-ring target at prime-power N, and it does not establish a stronger integral Gamma0-cohomology comparison at5.

## 1. The field-valued five-Hecke step uses the accepted regular theorem

The geometric five-Hecke proof supplies actual regular cochain corrections, so its identity can be specialized. The prime-to-p definition-field transfer argument gives the field-valued arithmetic identity with the direct lower-right-entry Artin action. No vertical-integrality assertion about that particular five-Hecke transfer correction is needed.

The ideal operator at a prime above5 is treated through the source's same-ideal-class replacement a' prime to5Nc and the exact product norm law. The pullback involving a itself is only used on the full field-valued regular coefficient module. It need not preserve the T5-fixed submodule. This correctly avoids reviving the non-Cartesian interchange rejected in the five-Hecke proof.

Degree-one diamond/model maps commute with scalar5. For a mixed coordinate map, independently selected primitives are compared through the normalized regular coboundary, rather than declared literally equal.

## 2. Restriction to Gamma1 does not introduce an index

At q prime toN, the upper and lower root ideals of the strict Gamma1 group both reduce surjectively modulo q. The lower-root condition uses the stated coprimality withN. Their reductions generate SL2(O/q), so both Gamma0 and Gamma1 act transitively on the q+1 kernel lines.

Thus Gamma0=Gamma1H for the Gamma0 kernel stabilizer H, and the good correspondence uses the same coset set upon restriction. The isogeny preserves the strict congruence condition because it is invertible moduloN and belongs to the upper-triangular level monoid. This verifies the restriction/corestriction diagram with no additional unit, subgroup-index, or norm factor.

On Gamma1 the ray coefficient action is trivial: the lower-right entry is a global unit moduloN. Passing to the strict group gives the same result after inverting its central-unit quotient, whose order has only2,3 as prime factors.

## 3. Why the field identity is enough for this integral conclusion

With trivial action, a field-valued one-coboundary is the zero function. Therefore equality in H1(Gamma1,K2(F(N)) tensor R) is equality of the actual homomorphisms. This is the precise point at which the Gamma0 comparison problem disappears.

The map K2(O'(N))->K2(F(N)) is injective by the localization sequence and vanishing of finite-field K2. Tensoring withR preserves the injection. The actual homomorphisms already take values in the integral localized subgroup by the accepted arithmetic theorem. Consequently their field equality is equality in that subgroup.

This uses coefficient injection, not an unproved injection on Gamma0 cohomology. The argument can also be performed one primary part at a time. Since K2(O'(N)) is finite, only finitely many parts enter the resulting homomorphism.

## 4. Coarse-space passage retains five

The stabilizer check is valid. A finite subgroup of GL2(F) with an order divisible by a prime ell≥5 would contain an element of orderell. An eigenvalue would be a primitive ell-th root with degree at most2 overF. For ell≥7 this contradicts [F(zeta_ell):F]≥(ell−1)/2. For ell=5, the only quadratic subfield of Q(zeta5) is real Q(sqrt5), which is not the imaginary quadraticF, so the degree is4. Hence finite stabilizer orders have only2,3 as prime factors.

Their higher cohomology vanishes overR. The equivariant-to-coarse comparison and degree-one universal-coefficient identification therefore give the stated coarse open homology map without inverting5. The source adjoint-pairing formulas in Section5.1 are purely algebraic group/coset identities and now apply with this verified coefficient range.

The final operator is exactly the source T_q and S_q convention; this proof does not define any bad-prime dualU by analogy or by setting q|N.

## 5. Accepted dependencies and limits

The arithmetic theorem and geometric five-Hecke theorem are separately accepted in ARITHMETIC_DESCENT_ACCEPTANCE.md and FIVE_COMPATIBILITY_ACCEPTANCE.md. Source-sign conversion is fixed in the arithmetic input and the separate GERSTEN_SIGN_TRANSPORT_ADDENDUM.

The source's Section5.1 conventions and the corresponding group-cohomology argument were inspected in LSSW, *Eisenstein cocycles for imaginary quadratic fields*, https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . No numerical test is presented as a substitute for these structural arguments.

The full construction remains UNSOLVED: small nonadmissible levels, exceptional blocks not removed, compactification, prime-power absolute integrality, unrestricted badU, and relative calibration remain separate obligations.
