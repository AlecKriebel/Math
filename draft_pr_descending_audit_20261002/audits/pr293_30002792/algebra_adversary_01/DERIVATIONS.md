# Algebra-family adversarial derivations for PR293

This independently checks the implication in PUBLIC_TURN_2.md C1–C4. The surface-adjoint statement in Lemma B is an inherited condition, not established in this report. The sealed pre-author derivation is DERIVATIONS_PREAUTHOR.md, SHA256 72bbbe129e9dd0a829d42a11ca3fd7ee995ede643b4a9d87c76f36123b0b31db. It was written before the submitted argument was opened.

## 1. Exact conditional proposition

Let k be algebraically closed in arbitrary characteristic; S=k[x0,x1,x2,x3]; and L a nonempty finite union of distinct reduced projective lines. Put I=I(L), a=alpha(I), d=a+1. Assume alpha(I^(2))=d. Assume, separately, that each integral surface of degree e>=2 admits a nonzero homogeneous form of degree e-2 vanishing on all its reduced singular curves. Then L is coplanar or the complete pair-intersection arrangement of d distinct planes, with no three containing a line; in either case S/I is Cohen–Macaulay.

The claim is about symbolic squares, not ordinary squares, schemes with embedded components, arbitrary curves, or nonperfect fields. Nonemptiness gives a>=1 and d>=2. A single line, two intersecting lines, and coplanar unions satisfy the planar branch. Two skew lines do not satisfy the premise.

## 2. Symbolic squares and normal order

For a component line, choose linear coordinates S=k[s,t,n,m] and P=(n,m). The quotient S/P^2 is free over k[s,t] on 1,n,m. Multiplication by f not in P has, in this basis, diagonal equal to the nonzero polynomial f(s,t,0,0); it is injective because k[s,t] is a domain. Thus P^2 is P-primary and contracts from its localization. The symbolic square of the reduced union is precisely the intersection of these P^2, since its associated primes are the component primes.

After substituting x=u s+v t+a n+b m with an invertible four-vector basis, membership in P^2 is equivalent to vanishing of all coefficients of normal order zero or one. This criterion, used both in the submitted test and in a separately written vector-parametrization test, remains valid in characteristic two. It is stronger than testing values or ordinary first derivatives only at finite-field rational points.

## 3. Submitted repeated-factor argument

The radical R of a degree-d form F in I^(2) lies in I. If deg(R)<=d-2 it contradicts a=d-1. If F is not squarefree, deg(R)=d-1 is therefore the only case, and the total lost degree one forces F=P^2 G with P linear and G squarefree, coprime to P. This step cannot conceal a repeated nonlinear factor: such a factor loses at least two degrees.

If G is constant, F=P^2 and every target line lies in that plane. Otherwise some partial derivative DG is nonzero. In characteristic p, vanishing of all partials means every exponent of each monomial is divisible by p: coefficients cannot cancel across different exponents after a fixed derivative. Since k is perfect, G would then be a pth power. Nonconstant squarefreeness excludes that possibility. No division by deg(G), Euler formula, or separability of an auxiliary map is used.

For a target line outside P, P is a unit at its prime, so G is in the localized square, hence in the actual square by primary contraction above. Any derivation sends P_line^2 into P_line, by the product rule in every characteristic. Thus the nonzero form P DG vanishes on all target lines and has degree 1+(d-2)-1=d-2. Lines inside P are covered by the first factor. The submitted C1 is sound.

The pre-author derivation supplies a different conditional route: eliminate nonlinear factors first, then use a quotient of products of distinct planes to exclude the only possible repeated plane without derivatives. These routes agree and neither transfers C1 to the central adjoint input.

## 4. Nonlinear factors and the exact inherited obligation

For squarefree F and an irreducible factor Q of degree e>=2, write B=F/Q. A target line contained in some other factor is covered by B. A target line not covered by B lies on Q; at its prime, B is a unit, so Q belongs to P_line^2. In normal coordinates this says its constant and first normal terms vanish. Its tangential derivatives vanish because Q restricts identically to the line. Consequently every partial of Q vanishes there.

Because k is perfect and Q is irreducible, Q has at least one nonzero partial. Its singular locus cannot have a two-dimensional component: Q cannot divide that derivative of lower degree. A line with every partial vanishing is therefore a reduced singular curve of the integral surface. Under the inherited adjoint input there is a nonzero A of degree e-2 vanishing on it. The form AB lies in I, is nonzero in the polynomial domain, and has degree d-2. This contradiction proves C2 conditionally.

The exact gap for this family is the universal existence of A. The finite computations below do not check resolution, Picard smoothness, Albanese generation, surface Riemann–Roch, pullback integrality, or conductor duality in Lemmas A and B. No unconditional verdict on these lemmas is made here.

## 5. Completeness and multiple-plane incidences

After C2, F is the product of d distinct plane equations P_i. Since a linear equation has normal order at most one along a line it contains, every target line belongs to at least two planes. For every pair i,j, the nonzero quotient F/(P_i P_j) has forbidden degree d-2 and must fail to vanish on some target line. That line lies in both H_i and H_j and in no other plane, so equals their pair intersection. It follows simultaneously that every pair intersection is present and none is contained in a third plane. Conversely every target line is one such pair intersection. This proves C3 without counting assumptions or generic-position assumptions.

Three planes through a common line are forbidden, even if that line is included in L. Four or more planes through a single point are permitted. Distinct pair-line primes cannot coincide without a third plane containing the common line. For d=2 the arrangement consists of one line and is coplanar, consistently with the stated alternatives.

## 6. Direct syzygy proof of C4 and radicality

Put Q_i=F/P_i and J=(Q_1,...,Q_d). For a polynomial relation sum a_i Q_i=0, reduce modulo P_i. Since S/(P_i) is a domain and no other P_j is proportional to P_i, Q_i is nonzero modulo P_i. Hence P_i divides a_i. Write a_i=P_i b_i. Cancelling nonzero F gives sum b_i=0. The entire syzygy module is therefore freely generated by P_i e_i-P_d e_d, i=1,...,d-1. These generators are independent, because their first d-1 coordinates are nonzero linear forms times the corresponding coefficient. This gives the exact graded resolution

0 -> S(-d)^(d-1) -> S(-(d-1))^d -> S -> S/J -> 0.

This independently verifies the submitted Hilbert–Burch conclusion, without relying solely on the computed maximal-minor signs. The zero locus of J is exactly the pair-intersection lines: at a point with at most one vanishing plane equation one generator is nonzero, and at a point with at least two all generators vanish. Thus J has height two. At the homogeneous maximal ideal, the displayed resolution is minimal and gives projective dimension two, so Auslander–Buchsbaum gives depth two and dimension two.

For an associated prime q of S/J, localize the same resolution. Its projective dimension is at most two. Depth of (S/J)_q is zero, so Auslander–Buchsbaum gives ht(q)<=2, while the support forces ht(q)>=2. All associated primes have height two and are the pair-line primes; no embedded prime, including at the cone vertex or a multiple-plane intersection point, is possible. At a minimal prime (P_i,P_j), all other P_t are units by the no-three-line condition, and Q_i,Q_j generate that localized prime. The localization is reduced. A nonzero nilradical would have an associated prime among those of S/J and survive at one of these localizations, contradicting reducedness there. Hence J is radical and equals I(L).

The Hilbert series is [1-d t^(d-1)+(d-1)t^d]/(1-t)^4, with degree d(d-1)/2. This is consistent with the number of distinct line components. Nothing in the resolution or the argument uses characteristic zero; minus signs become plus signs harmlessly in characteristic two. Coplanar reduced unions have ideal (h,g), where g restricts to the product of the distinct line equations in S/(h); this is a regular sequence and a complete intersection, including the single-line case.

Standard implications were checked against the primary Stacks statements [Auslander–Buchsbaum, tag 090U](https://stacks.math.columbia.edu/tag/090U), [Cohen–Macaulay modules have no embedded primes, tag 0BUS](https://stacks.math.columbia.edu/tag/0BUS), and [reduced iff R0 and S1, tag 031R](https://stacks.math.columbia.edu/tag/031R). The direct derivation above also explains explicitly why their hypotheses apply.

## 7. Authenticated submitted computation

The original snapshot manifest is 17,475 bytes, SHA256 8fe845421a5802daed352e99b4903797eb7ac98c1bc88592ac639d8f20fb0d1a. All 19 snapshot files were authenticated by byte count, SHA256, Git blob hash and mode against it. The reviewed code is 7,401 bytes, SHA256 08744c44e2a0c057ac8d25b315c5a0c282ce60a32ce5c9bdd7546fc0b3668b4d; the proof SHA256 is 56d7aee2dbb567f1574952bfe905b5407c0f0b06ec60e4b53b72acda48c245e1. The code was fully read before executing that exact source in an unoptimized Python process (-E -B, no -O).

Actual child PID 78558 exited zero. Its complete JSON equals SMALL_CHARACTERISTIC_CHECKS.json, including all counts, proof hash, and qualifications: 3,888 assertions comprise 24 exact initial-degree configurations, 60 maximal-minor checks, 987 derivative-kernel monomial checks, 2,541 Riemann–Roch integer controls, 90 line-independence checks and 186 invertible-coordinate checks. These are controls, not proofs of the geometric lemmas. The 24 examples include skew lines, a missing tetrahedron edge, a four-plane cone and five-plane star in characteristics 2,3,5.

## 8. Materially independent bounded falsification

The separately authored independent_GF2.py represents the 35 projective F2-rational lines by their two-dimensional vector subspaces, not by inversion of defining-form matrices. It expands all monomials formally in a spanning-vector/complement basis and extracts the coefficients of normal order below the specified multiplicity. Binary Gaussian elimination computes ranks; no finite-point evaluation substitutes for polynomial restrictions.

Actual child PID 78559 exited zero, reporting 60,182 explicit checks. All 7,175 unions of one, two or three rational lines were classified. The equality cases were precisely 35 single lines, 315 intersecting pairs, 525 coplanar triples, and 420 noncoplanar concurrent triples. The remaining 280 pairs and 5,600 triples failed the premise. The 420 concurrent noncoplanar triples are exactly three-plane pseudostars.

All 15,488 multisets of rational planes of total degrees 2 through 5 were tested on their maximal reduced double-line locus. Every repeated-factor or triple-line degeneration of degree at least three had a form of degree d-2; squarefree arrangements without a triple line had alpha=d-1 and exactly binomial(d,2) line components. Degree-two boundaries remained coplanar. The test covers 2,478 squarefree, no-triple-line arrangements across degrees 2–5. Digests of the full enumerations are in the complete native JSON. This finite exact evidence does not certify configurations over all fields or the surface-adjoint input.

## 9. Original problem scope

The primary Janssen paper, [arXiv:1306.4387v2](https://arxiv.org/pdf/1306.4387v2), explicitly works over algebraically closed fields in arbitrary characteristic; Question 3.1 asks whether a line configuration with the stated initial-degree gap can fail to be ACM. Its Definition 2.1 permits many planes through a point while excluding three through a line. The present conditional conclusion addresses precisely that question. Its Theorem 2.13 retains an ACM hypothesis, so using that theorem alone would be circular; neither independently derived reduction nor the submitted C1–C4 uses it. This is a scope check, not a priority audit. The private fetched PDF and HTML bodies must not be redistributed with the finding.
