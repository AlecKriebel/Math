# Weight-two antisymmetric Borcherds products at levels 713 and 893

## Disposition and exact target

**Problem 30003140 / OWR-14605-002 remains UNSOLVED after five substantive approach families in this investigation.** The results below are arithmetic partials and proof-route obstructions. They are not a proof or a counterexample to either requested modularity identity. No novelty, exhaustive literature coverage, human peer review, or formal verification is claimed.

The primary target is the equality of the spin L-function of each specified weight-two Borcherds form with the Hasse–Weil L-function of its specified rational abelian surface. Establishing that a function is a paramodular form is not enough. The original workshop occurred 24–30 April 2016; the report's relevant statement is on printed p.1278 [OWR]. The accompanying construction [GPY, §§7–8] supplies the pairs

\[
C_{713}: y^2=x^6-2x^5+x^4+2x^3+2x^2-4x+1,
\]
\[
C_{893}: y^2=x^6-2x^4-2x^3-3x^2-2x+1,
\qquad A_N=\operatorname{Jac}(C_N).
\]

Write their sextics as f_N. The intended forms are obtained from the F1 parameters (1,4), equivalently (-5,3), at 713 and (5,3) at 893. Their published holomorphy and cuspidality are cited inputs. No new Hecke-eigenform certification or proof of one-dimensionality of the relevant spaces is supplied here. Before attaching a spin Euler polynomial to these particular forms, that eigenform issue must be certified or imported from an appropriate theorem.

The primary literature check found no later theorem proving these two identities. [BPP, §7] proves levels 277, 353 and 587; its finite comparison primes cannot be transferred to a new conductor. [BCGP] and the later account [Gee] have a good-ordinary-at-3 hypothesis that fails for both targets, as proved below. This is a bounded search result, not a claim that no resolution exists anywhere.

## 1. The modern modularity route: exact obstruction at 3

For a genus-two curve with good reduction at p, put n_r=#C(F_{p^r}). The trace formula and Newton identities give

\[
a=p+1-n_1,\quad b=(a^2-p^2-1+n_2)/2,
\quad Q_p(X)=X^4-aX^3+bX^2-paX+p^2.
\tag{1}
\]

Here Q is the characteristic polynomial; the Euler polynomial is T^4 Q(1/T). Direct finite-field counts give

| Curve | n1 at 3 | n2 at 9 | Q3 |
|---|---:|---:|---|
| 713 | 7 | 13 | (X²+3)(X²+3X+3) |
| 893 | 6 | 12 | (X²−X+3)(X²+3X+3) |

These counts are exhaustively reproduced by two counting methods in verify.py: quadratic characters via the norm from F_{p²}, and explicit square-fiber multiplicities. Smoothness at 3 follows from the nonzero sextic discriminants established in §3.

The Newton polygons now give all slopes 1/2 for A713 and slopes 0,1/2,1/2,1 for A893. For X²+3 and X²+3X+3, the lower Newton polygon is the segment from (0,1) to (2,0). For X²−X+3 it has segments of slopes −1 and 0. Thus the former surface has p-rank 0 at 3, the latter p-rank 1; neither is ordinary. Equivalently, both middle coefficients b are divisible by 3.

Consequently [BCGP, Theorem A and Theorem 9.5.2], and [Gee, Theorem 1.5], do not directly prove their modularity. Passing to an isogenous surface or extending the local field does not alter normalized Newton slopes. A quadratic twist which again has good reduction at 3 also has the same slopes: over an extension killing the twist the two varieties become isomorphic, and normalized slopes are invariant under that extension. Those changes cannot remove this specific obstruction.

Both surfaces are ordinary at 2: the explicit smooth models in §3 give #C(F2)=#C(F4)=6 and hence

\[
Q_2=X^4+3X^3+5X^2+6X+4.
\]

Nevertheless the residual-image conditions of [BCGP, Theorem 8.3.2] fail for a direct application: §4 gives S3×S3, which cannot contain A5, and S6, which is not contained in S5. This does not rule out all other modularity-lifting arguments.

The conductor-713 sextic appearing in [BCGP, p.221] is exactly X^6 f713(1/X). It is therefore the same curve under (x,y)↦(1/x,y/x³). That occurrence is a local mod-2 construction in Lemma 10.3.6, not a stated modularity theorem for this surface. Confusing the occurrence with such a theorem would give a false resolution.

## 2. The Borcherds-input route: the two 713 entries are one form

For the positive-entry theta blocks of [GPY], write

\[
\operatorname{TB}_2(d_1,\ldots,d_{22})
=\eta^4\prod_{j=1}^{22}(\vartheta_{d_j}/\eta).
\]

For both 713 parameter pairs, the nonzero entry multiset for φ is

1,1,2,2,3,3,4,4,5,5,6,6,7,8,8,9,10,11,12,13,14,16.

The corresponding inflated multiset for Ξ is

1,2,2,3,4,4,5,6,6,7,8,9,10,11,12,13,14,15,16,18,20,24.

The inflation factors attached to zero entries multiply to m=1. Therefore both parameter pairs have exactly the same φ and Ξ, not merely the same weight and index, so that

\[
\psi=(\phi|V_2-\Xi)/\phi
\]

and the normalized Borcherds product are identical. This follows by commutativity of multiplication of theta factors; the absolute-value convention is the source's convention. The equality does not require a numerical Fourier cutoff.

For 893 the two multisets are, respectively,

1,2,2,3,3,4,4,5,5,6,6,7,8,8,9,10,11,12,13,14,16,19

and

1,2,3,4,4,5,6,6,7,8,9,10,12,13,14,15,16,18,19,20,22,24.

The sums of squares are 2N and 4N. There are exactly two zeros in each original 24-tuple, so the weight is 2 and the Fricke eigenvalue supplied by the construction is −1. Each block has q-order 2, because η contributes q^(1/24) and θ_d contributes q^(1/8): 4/24+22(1/8−1/24)=2. Their leading Laurent products are nonzero.

These checks remove an apparent extra example at 713 and pin the exact source inputs. They do not prove the products are Hecke eigenforms or identify any eigenvalues with those of A_N. Holomorphy and cuspidality remain credited to [GPY], rather than being inferred from these sums of squares.

## 3. The local-geometric route: conductor, bad factors and typicality

**Arithmetic partial theorem.** The two displayed Jacobians are semistable, of conductors 713 and 893 respectively. Both have geometric endomorphism ring Z. Their bad Euler factors are

| N | p | Euler polynomial Pp(T) |
|---:|---:|---|
| 713 | 23 | (1+T)(1−4T+23T²) |
| 713 | 31 | (1−T)(1+7T+31T²) |
| 893 | 19 | (1−T)(1+5T+19T²) |
| 893 | 47 | (1+T)(1+3T+47T²) |

Their global root numbers are both −1. These statements concern the surfaces only; no matching automorphic bad factors are asserted.

**Proof.** Completing the square gives integral models y²+h y=g with

| N | h | g |
|---:|---|---|
| 713 | x³−x²+1 | x²−x |
| 893 | x³+x+1 | −x⁴−x³−x²−x |

The identity f=h²+4g is exact. In characteristic 2 an affine singular point would satisfy h=0, y²=g and h' y=g'. Eliminating y gives h=0 and (g')²+(h')²g=0. The gcd of these two polynomials is 1 in F2[x] for each model, so no such point exists even geometrically. In the infinity chart u=1/x, v=y/x³, the coefficient of v is 1 at u=0 and the right side is zero. There are two infinity points, and the derivative with respect to v is 1. Thus both curves have good reduction at 2.

An exact resultant calculation gives

\[
\operatorname{disc}(f_{713})=2^{12}\,23\,31,
\qquad \operatorname{disc}(f_{893})=2^{12}\,19\,47.
\]

At all other odd primes except these four, the monic even-degree hyperelliptic models are smooth, including their two infinity points. At each remaining prime there is one double root r and four distinct remaining roots. Write f=(x−r)²g_p modulo p. The normalization is z²=g_p(x), a smooth genus-one curve with rational infinity points. The following exact table specifies all the needed reductions; quartic coefficients are in Fp.

| N,p | r | gp(x) | gp(r) | #normalization(Fp) |
|---|---:|---|---:|---:|
| 713,23 | 7 | x⁴−11x³+5x²−10x+8 | 7 | 20 |
| 713,31 | 15 | x⁴−3x³−4x²−x+4 | 2 | 39 |
| 893,19 | 4 | x⁴+8x³+8x²−9x+6 | 11 | 25 |
| 893,47 | 7 | x⁴+14x³+4x²−21x−23 | 38 | 51 |

Each quartic is squarefree and its value at r is nonzero, proving the singularity is an ordinary node. These models have connected irreducible nodal special fibers, with elliptic normalization and one loop in the dual graph. Standard semistable Jacobian theory gives toric rank one and Swan conductor zero; hence local conductor exponent one. Good reduction elsewhere now proves the two conductor claims. This uses the semistable Jacobian/conductor theorem, not a claim that a curve discriminant automatically equals its Jacobian conductor.

Let ε be +1 for a split node and −1 for a nonsplit node. It is the quadratic character of g_p(r), and the four ε values in the table are −1,+1,+1,−1. The Frobenius eigenvalue on the one-dimensional graph cohomology is ε. On the elliptic normalization its trace is p+1 minus the displayed count. The standard semistable inertia-invariant decomposition therefore yields

\[
P_p(T)=(1-\varepsilon T)(1-a_E T+pT^2),
\]

which gives the claimed bad factors. The local root number at a single node is −ε. Every good local root number is +1; the archimedean sign for an abelian surface is (−1)²=+1. Their products are −1.

For simplicity, at p=11 the characteristic polynomial of A713 is

X⁴−2X³−6X²−22X+121,

which is irreducible modulo 3, and hence over Q. At p=5 the polynomial of A893 is

X⁴+4X³+11X²+20X+25.

It is irreducible over Q. By Gauss's lemma a factor would be monic integral. Linear factors are excluded by checking the divisors of 25. For quadratic factors (X²+uX+a)(X²+vX+b), ab=25, u+v=4, uv+a+b=11 and ub+va=20. Up to interchange the constant pairs are (1,25), (5,5), (−1,−25), (−5,−5). The first forces u=2/3; the second forces u,v to have sum 4 and product 1; the third yields u=−1,v=5 and the wrong middle coefficient; the fourth has the wrong linear coefficient. Thus there is no factor. Both calculations are verified exactly.

If a surface decomposed over Q up to isogeny into elliptic curves, every good characteristic polynomial would factor into their two integral quadratics. These irreducible polynomials therefore prove Q-simplicity. The surfaces are now simple, semistable, and have nonsquare conductor. [BPP, Lemma 4.1.1] implies geometric endomorphism ring Z. This last inference is an explicitly imported theorem; its proof uses the endomorphism classification, conductor multiplicities and Ribet's semistable descent result. ∎

The sign −1 is compatible with the source's rank-one interpretation. It is not by itself a proof of analytic rank exactly one, of the algebraic rank, of BSD, or of modularity.

## 4. The residual-representation route: different comparison problems

**Residual partial theorem.** In the natural permutation action on the six Weierstrass points, Gal(Q(A713[2])/Q)=S3×S3, whereas Gal(Q(A893[2])/Q)=S6. The former four-dimensional mod-2 representation splits as two two-dimensional summands; the latter is absolutely irreducible.

**Proof for 713.** There is an exact factorization

\[
f_{713}=(x^3+x^2-1)(x^3-3x^2+4x-1).
\]

Each cubic is irreducible by the rational-root test, and their discriminants are −23 and −31. Each splitting field has group S3 and its unique quadratic subfield is respectively Q(sqrt(−23)) and Q(sqrt(−31)). Their intersection is Galois and a quotient of each S3. The only nontrivial possibilities would be the common quadratic subfield or the full S3 splitting field; both would force the two quadratic subfields to agree. They do not. Thus the splitting fields are disjoint and the group is S3×S3, acting on two triples. The cubic resultant is 64, which also checks the sextic discriminant identity.

For six branch points, A[2] is the space of even subsets, represented as W={v∈F2^6:Σv_i=0}, modulo the all-ones vector. The direct sum of the even-coordinate-sum subspaces on the two triples has dimension four. It intersects the all-ones line trivially because each triple has odd size. It maps isomorphically onto W/<1>, giving the claimed invariant 2+2 decomposition.

**Proof for 893.** Reduction modulo 3 is irreducible of degree six. Modulo 7 the factor degrees are 1,5. Modulo 349 they are 1,1,1,1,2. All three reductions are squarefree; full factors are recorded in certificate.json. Thus the transitive Galois group contains a 5-cycle and a transposition. It is primitive: any nontrivial block size would be 2 or 3, but an element of order 5 cannot act nontrivially on either the corresponding set of blocks or inside a block. The graph whose edges are all conjugates of the transposition has connected components forming blocks. Primitivity makes this graph connected, and its edge transpositions generate S6. Hence the full group is S6.

The standard faithful identification S6≅Sp4(F2), via the even-subset quotient, now identifies the representation with the natural four-dimensional one. It is absolutely irreducible: an invariant subspace over an algebraic closure containing a nonzero vector v contains a nonzero rational vector u by applying a symplectic transvection t_u and using t_u(v)−v=<v,u>u. Some rational u has nonzero pairing with v. Sp4(F2) is transitive on its nonzero rational vectors, which span the representation, so the invariant subspace is the whole space. ∎

The modular-form residual representations have not been computed or identified with these surface representations. In particular, the absolutely irreducible residual comparison used for the 587 example in [BPP] cannot simply be reused at 713. At 893 the surface passes that one image-type condition, but the automorphic residual identification and the conductor-specific obstruction extensions are still missing. Group order alone is not a modularity certificate.

## 5. The Euler-comparison route and its finite-check limit

The certificate supplies all surface good Euler factors for p=2,3,5,7,11,13,17,29,37,41, as well as the four bad factors. For example the first two good Euler polynomials are

\[
P_{713,2}=P_{893,2}=1+3T+5T^2+6T^3+4T^4,
\]
\[
P_{713,3}=1+3T+6T^2+9T^3+9T^4,
\qquad P_{893,3}=1+2T+3T^2+6T^3+9T^4.
\]

They are **surface-side data**, not a table of matched form-side eigenvalues. No numerical or algebraic automorphic Euler comparison is silently assumed. The author-maintained Ryan–Tornaría F713− directory was retrieved through an alternate public read after web-reader failures. It explicitly bases its L-series data on the Hasse–Weil L-series of a curve. Such Dirichlet coefficients cannot be treated as an independent automorphic-side match. The listed Fourier coefficient file was not inspected and is not used as evidence. Neither a finite matching-prime set nor a residual comparison certificate was obtained for either target.

Here is a precise negative control on a possible finite-prime shortcut. Let S be any finite set of good rational primes. There are infinitely many primes q≡1 modulo 8 times the product of the odd primes in S, avoiding both conductors. This is Dirichlet's theorem. The q-quadratic twist of A_N has identical Euler factors at every prime of S: the quadratic character is trivial there, including at 2. Yet at the new odd prime q the original surface has good reduction, while inertia acts as the nontrivial quadratic scalar on the twist. Its invariant subspace is zero and its tame conductor exponent is four. At all old bad primes twisting is unramified, and q≡1 mod 8 makes the twist trivial at 2. Thus the twisted conductor is Nq⁴, not N. In particular it is not Q-isogenous to A_N.

The explicit prime q=120121 works for S={2,3,5,7,11,13}; primality and congruences are checked in the verifier. This is a counterexample to inferring an isogeny from arbitrary finite local agreement, **not a counterexample to uniqueness at the fixed conductor or to the paramodular conjecture**. Its purpose is to expose exactly why controlling ramification and obstruction extensions is indispensable.

A legitimate Faltings–Serre completion would first certify the specific Borcherds forms as rational eigenforms of the requisite type, identify their residual representations with the surface representations, construct the conductor-specific finite distinguishing set by bounding the allowable discrepancy extensions, and then compare the required exact Hecke traces, with correct local-global input at bad primes. None of those missing automorphic/global steps follows from our surface-side counts. Conversely, simply choosing more small primes does not supply the omitted finite-comparison theorem.

## Verification and imported foundations

The executable checks exact integer polynomial identities, characteristic-two smoothness, finite-field point counts, normalization quartics, split/nonsplit node characters, input multisets, Frobenius factorization witnesses and irreducible-reduction checks. The written arguments additionally use standard trace/Weil identities, semistable Jacobian and conductor theory, the Weierstrass-point description of 2-torsion, elementary Galois theory, Dirichlet's theorem, and the explicitly cited typicality and modularity theorems. These foundational theorems are not re-proved by Python. No GRH assumption is used.

Negative controls reject changes in local counts, bad-node signs, a Borcherds index, a residual-group claim, the global disposition and scalar types, and reject altered/missing/unlisted packet files and a wrong manifest pin. Normal, -O and -OO execution must all pass the positive test and reject the same mutations. No assert statement enforces acceptance. Source files, corpus contents, publisher text, external mathematical software data and private coordination are excluded from the public packet. The public source hashes record inspected bytes; portable replay does not re-download or authenticate those sources.

## References

- [OWR] Moduli spaces and Modular forms, Oberwolfach Report 23/2016, DOI https://doi.org/10.4171/OWR/2016/23, relevant printed pp.1275–1278. Official PDF: https://ems.press/content/serial-article-files/46626.
- [GPY] V. Gritsenko, C. Poor, D. S. Yuen, Antisymmetric Paramodular Forms of Weights 2 and 3, IMRN 2020(20), 6926–6946; published online 2019. DOI https://doi.org/10.1093/imrn/rnz011. Inspected author preprint: https://arxiv.org/abs/1609.04146. The downloaded PDF bears arXiv v1 and an internal 2021 date; the exact bytes are pinned. The publisher's final full text was not inspected.
- [BPP] A. Brumer, A. Pacetti, C. Poor, G. Tornaría, J. Voight, D. S. Yuen, On the paramodularity of typical abelian surfaces, Algebra & Number Theory 13(5), 1145–1195 (2019), DOI https://doi.org/10.2140/ant.2019.13.1145. Inspected publisher PDF carrying a notice of the 2020 correction: https://msp.org/ant/2019/13-5/ant-v13-n5-p05-p.pdf. Relevant §§4–7; the 2020 correction is explicitly acknowledged.
- [BCGP] G. Boxer, F. Calegari, T. Gee, V. Pilloni, Modularity theorems for abelian surfaces, preprint arXiv:2502.20645v1 (2025), https://arxiv.org/abs/2502.20645. Inspected author PDF: https://www.math.uchicago.edu/~fcale/papers/Modular.pdf. Relevant Theorem A, 8.3.2, 9.5.2, and §10.3. No journal-acceptance claim is made.
- [Gee] T. Gee, Modularity theorems for abelian surfaces, arXiv:2510.02756v1, https://arxiv.org/abs/2510.02756. Inspected preprint submitted to the 2026 ICM proceedings; a publisher listing was located, but the final published full text was not inspected.
