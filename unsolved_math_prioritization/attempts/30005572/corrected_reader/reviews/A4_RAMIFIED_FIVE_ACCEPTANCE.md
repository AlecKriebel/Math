# Independent audit: ordinary ramified-five cocycle lifting

Date: 14 October 2026 UTC. Row 1777 / problem 30005572. Shared PASS 2/5 verification, consuming no extra pass. This supplements RESIDUE_AND_GEOMETRY_ACCEPTANCE.md. No author proof, queue, pass ledger, or remote repository was modified.

## Verdict and combined outcome

Accept the ordinary cocycle-lifting theorem and the exact two-stage invariant-representative criterion in the pinned files below. No substantive mathematical defect was found.

The hypothesis that a full-CM-trace-fixed residue primitive eta_c exists is discharged by the independently accepted RIGHT_END_LIFTING.md. Consequently, for every source CM product and auxiliary c, including when 5 ramifies in F, the canonical constants-quotient cocycle has a genuine ordinary K_2(L(A)) tensor Z[1/6]-valued lift with precisely the prescribed residue. The ordinary H^2(Gamma,K_2(L) tensor Z[1/6]) obstruction vanishes.

This does not establish trace-fixed values, canonical constant normalization, or compatible integral lifts across Hecke operators, CM/Galois descent, and component-changing isogenies. It is an ordinary geometric cocycle theorem, not the requested arithmetic map. The original problem remains UNSOLVED.

Pinned inputs:

- ORDINARY_LIFT_AND_REMAINING_TRACE_OBSTRUCTION.md: SHA-256 8c3a64691290a558216e812aabf770e7e019ed55d13baa1c30ea3da56198b634.
- TRACE_REPRESENTATIVE_TEST.md: SHA-256 c5e289aec74fa62d1406fd65dd1d8322f6b9d6907af50a66db400a24ed748347.
- RIGHT_END_LIFTING.md: SHA-256 ee853634d28da3c9d324f25cc90a7a9d9aed95875bc385782746aad73cf720f4.

The first two files were kept unchanged during this audit. The accepted PASS 1 constant-quotient repair and exact constant kernel are dependencies as recorded in the companion acceptance.

## 1. The fivefold invariant lift

A single exceptional monoid is sufficient for the whole quotient cocycle: its input eta has one exceptional element, and the accepted residue-lifting operator works on that same fixed module. Enlarging the exceptional element to include 5 causes no problem.

For admissible rational integers m, the common ideal of m^4-1 in R is exactly (5). All are multiples of 5; CRT excludes every prime at least 7 and supplies an m congruent to 2 modulo 25, proving exact five-adic valuation one. Therefore the stated finite operator B, annihilating constants and having augmentation 5, exists over R.

For a fixed quotient value q and any ordinary representative x, Bx is independent of x because B annihilates constants. The commutation identity

(T_alpha-1)Bx = B(T_alpha-1)x = 0

is valid for every allowed alpha because the inner difference is constant. Its quotient is 5q. This proves an R-linear, Gamma-equivariant trace-fixed lift of the fivefold quotient cocycle and hence 5 delta[theta-bar] = 0. The sample formulas using 2 or 3 have the correct signs and denominators.

The stated canonical twenty-fivefold lift also checks: any two invariant lifts of 5q differ by a trace-fixed constant, which is killed by 5. Multiplication by 5 therefore makes the result independent of the choice. This proves additivity and the stated naturality for maps preserving constants and the trace-fixed filtration. It does not provide an unmultiplied invariant lift.

## 2. Local Gersten trivialization

After a finite base-field extension, a rational point T outside the support of Z_c has a regular local ring B of dimension two, essentially smooth over a characteristic-zero field. The equicharacteristic Gersten theorem applies integrally, in precisely the classical case required here. In particular, the middle local Gersten cycle eta_B lifts to an ordinary element a of K_2(Frac B) because its final residue at T is zero.

For H fixing T, its L'-linear automorphisms preserve B and act trivially on its residue field. If x_h are ordinary representatives of the quotient cocycle, then

z_h = x_h - (ha-a)

has every local height-one residue zero. It therefore belongs to K_2(B) tensor R. Evaluation along B -> L' is canonical Quillen K-theory functoriality, is H-equivariant, and restricts to the identity on constants. Evaluating z_h gives a one-cochain r with dr equal to the field restriction of the original constant-valued defect k on H.

There is no requirement that all globally occurring divisors avoid T. They were restricted to the local Gersten complex and canceled there by a. Likewise, no global divisor residue is being confused with a point evaluation. This is a legitimate local splitting of this particular obstruction.

## 3. Auxiliary point and the two prime-to-five degrees

The field-theoretic choice of prime is valid for every imaginary quadratic F. Its intersection with Q(zeta_5) is Q because the unique quadratic subfield of the latter is real. Chebotarev in their compositum therefore supplies infinitely many rational primes splitting in F and congruent to 2 (or 3) modulo 5, after excluding any finite set. A prime q above one of them has norm n congruent to 2 or 3 modulo 5 and can be chosen prime to c.

Maximal CM gives A[q] a two-dimensional vector-space structure over O/q. Galois and Gamma both act O/q-linearly. Thus the full q-torsion field degree divides the order of GL_2(O/q), and the Gamma-orbit degree of a point divides the order of the corresponding reduction image. That ambient order is n(n-1)^2(n+1), prime to 5 under the chosen congruence. The argument needs neither scalar Galois action nor surjectivity of Gamma reduction.

Any nonzero q-torsion point lies outside A[c], since coprimality of the ideals makes their torsion intersection zero. It is also outside the origin, so it has coefficient zero in Z_c. The local lemma applies to its stabilizer H.

Write e for the torsion field degree and d for [Gamma:H]. Field transfer first gives e times the restricted original obstruction; group corestriction then gives ed times that same original class. The coefficients are trivial under the geometric Gamma action, and both transfers have their usual integral restriction-transfer identities. As ed is prime to 5, integer Bezout combines ed delta = 0 with 5 delta = 0 to prove vanishing. Neither e nor d is inverted in R.

The concrete Q(sqrt(-5)) example with norm-two prime checks, as does simultaneous adjoining of q-torsion for a finite h^2 tuple. The latter extension has Galois group inside a product of prime-to-5-order groups, so no component forces a hidden factor of 5.

## 4. Explicit cochain correction and transfer sign

The cochain construction lifts the specified quotient cocycle pointwise, not merely its cohomology class. The identities du=5k and dr_0=e k|H follow directly from the fivefold lift and local evaluation.

The transfer homotopy has the correct sign. For right-coset representatives t and decompositions t gamma = h_1 t', t' delta = h_2 t'', write

A_t(gamma) = k(t,gamma) - k(h_1,t').

Applying the two-cocycle identity, or multiplying lifts in the associated central extension, gives

k(h_1,h_2) = k(gamma,delta) + A_t(gamma delta) - A_t(gamma) - A_t'(delta).

Summation over t permutes the t' representatives, yielding exactly

Tr(k|H) = d k - d_group A_k.

Consequently v=Tr(r_0)+e A_k satisfies d_group v=ed k. For integers a,b with 5a+ed b=1, the corrected cochain Theta=x-a u-b v is a genuine cocycle. Both corrections are constant-valued, so it still projects to theta-bar and has the original Gersten residue.

The companion CHECK_TRANSFER_IDENTITY.py verifies this formula by exact integer arithmetic in 19 finite-group/subgroup cases: cyclic groups with integral carry cocycles and coboundary perturbations, and S_3 with a nonnormal order-two subgroup. All 1,550 pair checks passed, after checking the cocycle identity itself. These tests are sanity checks; the preceding general calculation is the proof.

## 5. Comparison after inverting 5

The number-field constant group K_2(L) tensor R is torsion by the localization sequence and finiteness of the tame kernel. Its decomposition into the 5-primary and prime-to-5 summands is canonical. Multiplication by 5 is an automorphism of the latter summand.

Thus the correction of the prime-to-5 part of the constant cocycle 5Theta-S(theta-bar) is well-defined and preserves the cocycle and residue properties. Afterwards this difference is 5-primary, so it vanishes after extending coefficients to Z[1/30]. Dividing the fivefold invariant lift by 5 in that enlarged coefficient ring then identifies the result with the unique source geometric cocycle for the same residue.

This accepted comparison does not divide arbitrary 5-primary constants. The remaining difference between normalized lifts can still be a 5-primary constant cocycle. In particular, agreement after inverting 5 is not a proof of equality over R or of arithmetic compatibility there.

## 6. Exact two-stage invariant-representative criterion

The supplement is accepted with its explicit fixed-monoid interpretation.

For q in Q_beta and x representing it, 5x-Bx is constant and changes by 5c if x changes by c. Thus its class o_B(q) in C/5C is well-defined and necessarily zero for any M_beta-fixed representative. If it is zero, a constant correction gives y with By=5y.

Its remaining defects f(alpha)=(T_alpha-1)y are killed by 5. Because 5 ramifies and beta excludes the primes above it, N(alpha)^2 is 1 modulo 5, so the monoid action on C[5] is trivial. The cocycle relation for defects therefore becomes an additive monoid homomorphism M_beta -> C[5]. Two eligible choices y differ by C[5] and hence have identical defects. The combined criterion o_B(q)=0 and f=0 is both necessary and sufficient for an M_beta-fixed representative.

For B=(16-T_2)/3 the displayed first defect is (T_2-1)x/3, and the correction forces T_2 y=y exactly. The supplement correctly declines to infer vanishing of every other defect from this one identity. Eventual invariance still requires the criterion to hold after some enlargement of beta. No nonzero obstruction for an actual theta value has been computed here.

## 7. Final acceptance boundary

The former ordinary group-H^2 obstruction is removed for these actual auxiliary cycles on every component, now without a conditional eta hypothesis. The surviving invariant-representative obstruction and 5-primary constant ambiguity are real remaining proof obligations, not disproved possibilities. In particular this audit does not promote the ordinary lifts to the canonical trace-fixed Hecke-compatible system proved in the unramified case.

Nothing here completes arithmetic ray descent, auxiliary removal, integer-ring absolute integrality, all-level compactification, the actual bad-U identity, or the prescribed relative theta-symbol construction. The accepted PASS 1 nonzero trace-fixed constant kernel remains unchanged.

## Standard-source verification

The local theorem was checked against Charles Weibel, *The K-book*, Chapter V, (9.3.1) and Theorem 9.6 (Quillen), https://sites.math.rutgers.edu/~weibel/Kbook/Kbook.pdf . It supplies Gersten exactness for the regular local ring used here. The application needs no mixed-characteristic extension of that theorem.

The prime-existence input was checked against J. S. Milne, *Algebraic Number Theory*, Theorem 8.31 and Example 8.34, https://www.jmilne.org/math/CourseNotes/ANTc.pdf . The linear-disjointness calculation above verifies that the required simultaneous Frobenius condition exists; density is then positive.

The source geometric construction and its coefficient scope were inspected in LSSW Sections 3.1–3.4, https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf , as recorded in the companion audit. The local trivialization and transfer argument above are independently audited authored mathematics, not assertions imported from the source's Z[1/30] theorem.
