# Independent audit: simultaneous clearing and central specialization

Checkpoint: 2026-10-06 22:43 PDT / 2026-10-07 05:43 UTC. Auditor: upstream_arithmetic. Read-only source: `/Users/alec/Desktop/math`, verified HEAD `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Scope completion estimate: **100%** for this requested algebraic audit, including the independent child stress test; confidence in the full pointwise theorem is **not** a completion percentage. No external communication or upstream edits.

All references below are to `preprints/A-pointwise-2-converse-for-elliptic-curves-with-rational-two-torsion-September-24-2026/build/sections/` at that commit. Read all 1058 lines of `pointwise.tex`, `ring-determinants.tex` 1160–1769, and the evaluation package in `ring-limits.tex` 630–979. Also checked `ring-determinants.tex` 892–936 and 1021–1073, `cyclotomic.tex` 60–168 and 597–785, and the odd stabilization/coefficient-field clauses in `coefficients.tex` 138–300, 534–641, 755–794.

## Result and limits of this audit

I found no concrete algebraic counterexample to the bounded-complex clearing lemma, Laurent/Schur estimate, binary constant-term transfer, constant-rank derived specialization, or all-sequence/outer evaluation. Their proofs can be reconstructed with the hypotheses stated in the source. This is a scoped, conditional result. It does **not** verify the arithmetic production of every finite Heegner/Selmer/duality diagram, the theta bridge, or every coefficient contraction identity. The exact unresolved interface is identified below rather than silently promoted to a theorem.

Independent adversarial check: `/root/upstream_arithmetic/clearing_adversary`, with this preliminary verdict withheld, independently reconstructed the clearing and transfer proofs and found no counterexample. Its own tail subagent independently confirmed the Laurent convolution, including a sharp M-c error example. Their report is `agent_notes/central_clearing_adversary.md`. The checks agree on the same substantive applicability boundaries and do not certify the arithmetic inputs.

The source does not assert one determinant scalar common to the cyclotomic and anticyclotomic deformations. They are different coefficient representations and complexes. What is required, and asserted, is one scalar family across every character of a **fixed finite binary family** within each deformation. The two resulting valuation interfaces are combined numerically in `pointwise.tex`. Requiring equality of the two scalars would add an unnecessary hypothesis.

## 1. Algebraic coefficient models and central evaluation

Write Lambda = Z_2[[t]], O = completed Lambda_(2), and G = (Z/2)^b. There is no map O -> Q_2 obtained by setting t=0. This is explicitly acknowledged at `cyclotomic.tex` 68–75. Central values are defined first for elements of Lambda[1/2].

For the cyclotomic family, `cyclotomic.tex` 597–627 constructs one coordinate u of a wedge in the inverse determinant of a perfect Lambda[G]-complex. Its character coordinates lie in Lambda[1/2]. Separately, the universal integral Kato construction places 2^C u in O[G]. Fourier inversion places each group-basis coefficient of u in Lambda[1/2], possibly with b-dependent denominators at this intermediate step; intersection O intersect Lambda[1/2] = Lambda then recovers 2^C u in Lambda[G] with the *original* C. There is no hidden extra 2^b loss. This is the elementary proof of `cy:fourier`, lines102–118.

The ring-class construction uses a universal class and paired functional before character evaluation (`ring-determinants.tex` 1218–1266). Comparing finitely many evaluated models through their maps to original cochains is enough for a fixed G. No inverse limit as G grows is asserted. A rational generic coordinate can be evaluated at t=0 only after regularity away from (2) puts it in Lambda[1/2]. The functional is separately represented over Lambda_(t) for specialization, rather than evaluated as an arbitrary O-cochain: lines1062–1073 explicitly make this distinction. This is the correct algebraic distinction. Agreement of the two functional representatives is still conditional on the retained global duality and local comparison maps.

For `rd:derived-specialization` (892–936), let A=Lambda_(t). It is a DVR with residue Q_2. A bounded free A-complex splits into invertible disks, nonunit disks, and free cohomology summands. A nonunit disk contributes one additional central class in each of its two adjacent degrees. Thus equality of generic and central rational cohomology dimensions degree by degree excludes every nonunit disk. The generic determinant tensor of an integral cycle and closed functional is regular and specializes to their central tensor. Over Z_2, the torsion elementary divisors remain in the determinant and must be counted. The displayed Tor exact sequence is valid because Lambda/(t) has projective dimension one. No naive quotient H^1/tH^1 is substituted for derived specialization.

Boundary case: generic acyclicity with a central rank-one jump does *not* satisfy this constant-rank lemma. The source defines the generic acyclic coordinate to be zero and treats that branch separately in the missing-vertex proof. This is legitimate for that zero coordinate; it cannot be used to identify a nonzero special Kummer class in a jumping family.

## 2. Laurent expansion and simultaneous elimination

`rd:schur`, lines1337–1394, has the correct coefficient topology. Modulo 2^M, O is (Z/2^M)((t)); negative support is finite at each precision, although the full expansion can have infinitely many negative coefficients tending 2-adically to zero. Its valuation is the minimum coefficient valuation.

For a block A_j whose residual determinant has t-order d_j <= h, write det(A_j)=t^d_j v_j+2w_j, with v_j a power-series unit. C_j=adj(A_j)/(t^d_j v_j) has pole at most h. For B=A+2E, BC=1+2F, with F having the same pole bound. Therefore

    B^-1 = C sum_(j=0)^(M-1) (-2F)^j mod 2^M,

and the jth summand has pole at most (j+1)h. Matrix size affects the number of sums, not the pole of a product, so the bound -Mh is independent of the number of new local blocks. This also bounds P-QB^-1S when P,Q,S are power-series matrices.

For a Lambda[G]-matrix whose augmentation is A, a sign evaluation differs from A by 2E_x with E_x over Lambda. The nilpotent augmentation ideal in the residual group ring does not invalidate invertibility: O[G] is local with maximal ideal (2, augmentation ideal). If S_0=0, Schur elimination has augmentation P_0 exactly. This is precisely the mechanism preventing a growing central denominator from the many new-prime blocks.

The bound is sharp in the scalar toy case B=t^h+2: its inverse modulo 2^M has final term (-2)^(M-1)t^(-Mh). Arbitrarily many diagonal copies give the same bound.

The remaining premise in `rd:family-clearing` is arithmetic/model-theoretic: the augmented universal complex must be presented by the old complex as a subcomplex plus the direct sum of the stated new singular blocks, and a free model of this presentation must lift over Lambda[G]. Given a genuine derived localization triangle with bounded free models, the asserted lift is a standard stable-basis operation: add contractible disks, identify the augmented minimal complexes by invertible degreewise matrices, and lift those matrices over the local group ring. It cannot be deduced merely from matching Euler characteristics. The source explicitly requires the actual diagrams; this audit has not independently reconstructed all of them.

## 3. Reconstruction of bounded-complex clearing

`rd:clearing`, lines1396–1461, permits zero-divisor pivots and does not assume generic rank is constant on all characters.

Put the central Z_2-complex into elementary-divisor bases. The sum of positive pivot valuations is bounded by its total torsion length h_1. Lift the constant unimodular bases. Cancel the same pivot positions in the universal complex formally, expressing every subsequent pivot and basis change by rational expressions in the original differential entries. There are at most r_0 cancellations. A product P of bounded powers of the pivot numerators clears all these denominators. The number and degrees of those powers depend only on r_0. Its augmentation is a power series and P_0(0) is a product of nonzero central pivots, with valuation bounded by r_0 and h_1.

This formal computation can be interpreted in the localization at P even if P is a zero divisor in O[G]. Localizing kills the bad character components; alternatively every cleared expression is obtained by adjugate identities and is polynomial before evaluating characters. On characters with P_x != 0, the remaining complex has one free module in each of degrees1 and2. If its remaining differential is nonzero, the projected cycle is zero, and the coordinate is zero. If the differential is zero, the coordinate is the product of the projected cycle and functional with the recorded pivot determinant factors. Thus

    u_x = 2^(-a_0) eta_x Q_x/P_x

on the good components, with Q integral. Set f=2^a_0 P^2 and d=eta P Q. The identity f_x u_x=d_x also holds on every bad component since P_x=0 makes both sides zero, irrespective of the coordinate there. There is no attempt to recover the bad component's coordinate from the rational formula.

The numerator can have uncontrolled negative Laurent support. Only f needs a bound; it is a polynomial of bounded degree in the bounded differential entries. All unused-prime correction factors and eliminated-block inverse determinants are O[G]-integral units/multipliers and can be inserted into eta, hence into d rather than f. Their potentially large central valuations do not enlarge v(f_0(0)).

Stress test of the bad-pivot case: take D^0=R, D^1=R^2, D^2=R with d^0=(1+g,1-g)^T and d^1=0 for G=C2. At augmentation, the first pivot is2, with one torsion class of length1 and the required rational lines in degrees1,2. At the other character the first pivot vanishes but the second equals2, so the required rational rank pattern persists. A cycle along the first basis vector has zero generic class at augmentation and nonzero generic class at the other character. Squaring P=1+g kills the latter component; the clearing identity remains valid. This addresses the most plausible rank/codimension counterexample to the proof. It is not a counterexample.

If central torsion length is allowed to grow, the uniform central bound cannot follow. If a constituent has extra generic cohomology, the rank-one coordinate formula is not covered. Both exclusions are explicit hypotheses.

## 4. Unused primes and constant-term transfer

The identity (1+a z+z^2)(1+a z^-1+z^-2)=(a+z+z^-1)^2 in characteristic2 is an identity in the entire commutative residual group ring, not just its residue field. Consequently l/e^2-1 is divisible by2 before character evaluation. Each factor

    1 + ((l/e^2-1)/2)(1+g_q)

is integral and evaluates to the desired correction at an unused character and to1 at an active character. Hence there is no accumulating inertia-projector denominator. The residual nonconstant scalar establishes invertibility in O[G]. This verifies the algebra of `rd:unused` (1268–1335), conditional on the preceding local determinant comparison.

For `rd:binary-transfer` (1650–1699), test the L(M)+1 coefficients of f in degrees -L(M),...,0 and the constant coefficient of d. The binary lemma has q=L(M)+2 tests and requires b>q(2^M-1). At the resulting nonzero character, every negative coefficient of f is divisible by2^M, and f's constant coefficient has valuation c=v(f_0(0)) because M>c. Thus v_O(f_x)<=c and, since d_x is integral, v_O(u_x)>=-c. The same holds for the base. Because u_x is in Lambda[1/2], it has no negative powers and all coefficients have valuation at least -c.

The constant-term convolution is a convergent 2-adic sum: the negative coefficients of f tend to zero and the positive coefficients of u have a common lower bound. Its terms with negative f-degree have valuation at least M-c. The coefficient matches then give

    v(u_x(0)-u_0(0)) >= M-2c.

Dividing by f_0(0) is valid. The chosen coefficient match also implies f_x != 0, so the selected vertex cannot be among the killed-pivot components. No negative-support bound on d is needed.

Essential boundary: replacing u_x in Lambda[1/2] by merely u_x in O breaks the argument. O has negative Laurent tails and no t=0 map, so positive f-degrees and negative u-degrees can contribute to the constant term. For example 2/(1-4/t) belongs to O and has Laurent constant2, while its rational expression 2t/(t-4) is regular at t=0 with value0. The source's away-two pole cancellation is therefore substantive, not a cosmetic hypothesis.

The binary lemma itself is valid: character functions have Boolean monomials with coefficient divisible by2^|I|; the jth binary digit is a polynomial of degree <=2^j. The sum of degrees for M digits and q tests is <=q(2^M-1). A Boolean polynomial of degree below b has even sum, so the common zero set, containing0, contains another address. See `cyclotomic.tex`121–168.

## 5. All-sequence and outer evaluation

`rl:evaluation`, `ring-limits.tex`630–717, retains the actual finite-model-to-cochain contraction maps. For each arbitrary sequence g,h, the evaluation matrices have bounded source sizes and integral entries, so the fixed ultrafilter gives their limits. The two cochain identities involve finitely many products and sums, hence survive for every g,h. There is no diagonal choice over infinitely many group elements.

A finite detecting list exists by finite-dimensional linear algebra applied to pairs (class, possible coboundary vector). Its map to the two-term evaluation complex has residual H^0 isomorphism and H^1 injection. The cone has residual cohomology zero in degrees<=0; canceling unit blocks makes it start in degree1. After any coefficient field extension it still starts there, giving H^1 injection. The finite list proves injectivity; arbitrary-sequence identities prove that the image consists of actual crossed cocycles. Those are distinct roles.

For `rl:outer-evaluation` (781–856), the ultraproduct quotient by elements of valuation tending to infinity is a DVR: a nonzero class has valuation equal to a single finite integer on a large set, and is2^n times a unit. Products add these valuations; every nonzero ideal has a smallest valuation. The uniformizer2 never becomes zero. Evaluation of approximate cycles is valid because the degree-two matrices remain integral, so the errors still have valuation tending to infinity. The detecting-cone contraction uses unit pivots over each O_j; its inverses and homotopies stay integral. Bounded sizes let these actual matrices pass to the outer quotient.

Restriction to exact kernels uses a constant central scalar with a fixed finite valuation. For a central scalar z acting as u^4, the cocycle identity gives (u^4-1)b(g)=(g-1)b(z). Since u^4-1 is a nonzero fixed 2-adic number, it stays nonzero in the outer fraction field. This justifies the restriction injection. A merely convergent-to-trivial kernel would not suffice; the source defines the exact stagewise kernel explicitly.

These arguments depend on the finite cochain maps, the bounded free models, and the integral cone contractions actually existing. An abstract limiting complex with the same Euler characteristic would not provide evaluation maps or the asserted injectivity.

## 6. Finite-stage graph specialization and its effectiveness

`pointwise.tex`499–551 fixes one ultrafilter, a bounded-size elementary label alphabet, and binary truth tables at every finite weight cutoff. Finiteness at each cutoff selects one table on a large set; selected tables agree under restriction because they are selected using the same ultrafilter. The bounded-weight witness survives. Freshly ramified K is disjoint from the old label normal closure at stages where the moving detecting prime avoids K's ramification; this provides the claimed compatible odd-label lifts. The stationary companion is fixed *before* b.

For each b, the finite address networks have a finite maximum weight W_b. The finite intersection of the corresponding large sets gives an actual stage, with the same tables and adequate precision, before primes are realized. This is the correct quantifier order:

    fixed K and depth constants; for every finite b, some actual stage and finite prime realization.

It does not require one stage for all b or an intersection of infinitely many large sets. The coefficient field does not silently grow its residue alphabet with precision: `coefficients.tex`281–284 fixes the root-character field, and 774–777 explains binary phase-removed tests. The extra detecting-prime restriction is quadratic, not of increasing order.

This is an existential construction. It does **not** provide an algorithm that computes the selected ultrafilter table, the least stabilized simple count, or a stopping certificate for stabilization. Once the finite truth tables, labels and networks are supplied, coefficient checks and finite Chebotarev realization can be searched effectively in principle; extracting those tables from an ultrafilter is not made effective. The pointwise theorem and missing-vertex arguments as written need only existence of cubes, so this absence of an algorithm is not itself a contradiction. It would become an exact gap if one claimed an effective universal graph program from this proof alone.

The final uniform upper bound is a numerical combination of separate interfaces: odd unit j(P_h)<=w(h)+C, even unit v(L_*(hk))<=2w(h)+C with fixed k, and height comparison 2j_h(k)-2j(P_h)=v(L_*(hk))+O(1). Hence 2j_h(k)<=4w(h)+C, uniformly in b. Nonnegative finite Sha lengths give the requested bound for the ring transfer. There is no extra arithmetic scalar asserted between the two coefficient systems.

## Exact outstanding gap for a promotion of the full converse

The checked algebra does not close the independent validation of `rd:assembly` (1546–1605), which asserts actual finite arithmetic diagrams with the required simultaneous class, orthogonal lift, local boundary witnesses, duality, specialization comparisons and Schur model. In particular, the statement that the O-representative and Lambda_(t)-representative define the same generic paired functional must be verified from those maps, not inferred merely from published duality or from a central trace equality. The theta/trace/contraction engine used for the simultaneous odd/even unit graphs also remains dependent on its separately audited construction. Thus the full pointwise2-converse remains unaccepted at this checkpoint, although the algebraic tail of its transfer mechanism with stated interfaces has survived this independent falsification attempt.
