# Independent adversarial audit: rank 609 / problem 30000971

Audit date: 2026-10-04 UTC. The frozen packet was received and checked independently after its five recorded approaches. No additional proof-search approach was opened. No source file, frozen public file, repository status, branch, or remote was changed.

## Verdict and scope

**PASS for the stated counterexample to the stronger obstruction-length comparison.** I found no mathematical defect in the construction. In particular, the argument establishes an entire square-zero fiber for a genuinely general projection of the fixed quadratic Veronese variety, not merely a special local map or a component of an unspecified fiber.

For X = v_2(P^40) in P^860 and a general projection X -> P^46, there is a fiber Z with algebra k[z_1,z_2,z_3,z_4]/(z_1,z_2,z_3,z_4)^2. Its ideal-sheaf regularity is 2; its obstruction module is a 10-dimensional vector space annihilated by the maximal ideal. Thus length(Q)/c = 10/6 = 5/3 < 2.

**The bundled original problem remains unsolved.** This does not prove or refute reg(Z) <= n/c+1. At the counterexample the latter right side is 23/3. Retain five approaches, 5/5, and the unresolved status of the full target. This is an independent mathematical/AI audit, not external human peer review or a novelty certificate.

The audit target is the public SHA256SUMS file with SHA-256:

    d4015b287672140ba895d1dcc6efa6a432a9d3e891065ba1c9ae088495737b8a

Every entry in that manifest verified before and after review. The original checker reproduced control-results.json byte for byte. Independent controls are in independent_check.py and independent-results.json; the audit does not import the original checker.

## 1. Parameters and the universal rank stratum

Let e >= 2, g=e(e+1)/2, n=eg, c=g-e, and m=n+c. Set H=H^0(P^n,O(2)) and S=H^(m+1). For e>=2, c>0 and m+1<=dim H. Independent ordered tuples are the frame space for Gr(m+1,H). The bad basepoint incidence in S x P^n has dimension dim S+n-(m+1)=dim S-c-1. Properness of P^n makes its image closed. Consequently basepoint-free independent tuples form a nonempty dense open in the irreducible space S.

On a source chart and a target chart with s_0(p) nonzero, the derivative of (s_1/s_0,...,s_m/s_0) is an unrestricted m-by-n matrix as the parameter varies: keep s_0 fixed and prescribe the first jets of each numerator. The relevant rank is r=n-e, with kernel dimension e and cokernel dimension m-r=c+e=g. The exact-rank stratum is smooth of codimension (n-r)(m-r)=eg=n. Its inverse image D in the universal source/parameter space is therefore smooth of dimension dim S.

The equality of dimensions alone would not establish dominance. The following separate transversality computation does.

## 2. Actual incidence dominance

Index g quadratic monomials by alpha=(i,j), i<=j. Use e coordinates z_a and n-e coordinates w_(alpha,b), one for every pair (alpha,b) except ((a,a),a). The witness map on x_0=1 has n-e coordinates w_(alpha,b) and g coordinates

    q_alpha = z_i z_j + sum_b w_(alpha,b) z_b,

where the sum includes only the existing w coordinates. The homogeneous lift has s_0=x_0^2 and linear coordinates x_0 w_(alpha,b), so all entries really belong to H.

At the origin df has an identity block in the w directions and zero otherwise. Its rank is n-e. The normal space of the matrix rank stratum is Hom(K,C). The derivative in source direction v of its normal equations is the bilinear Hessian map

    v |-> (Hess(q_alpha)(v, d/dz_b))_(alpha,b).

This statement follows directly by writing the rank equations as the Schur complement of the invertible w block. At the witness, the off-diagonal blocks vanish, so differentiating the Schur complement gives precisely this Hessian block, without an omitted correction term.

Order the rows ((a,a),a) first and the z directions first. The resulting n-by-n matrix is [2I_e,0; D,I_(n-e)]. Its determinant is 2^e. The 40-dimensional matrix for e=4 therefore has determinant 16, not merely a nonzero minor of insufficient size. All dimensions agree.

Writing local equations of D as F(s,p)=0, their differential in p is invertible. For every tangent variation ds there is a unique dp solving dF=0. Thus d(D->S) is an isomorphism. Both schemes are smooth of the same dimension, so the map is etale at the witness. Its etale locus has open image in S.

The induced quadratic map Sym^2(K)->C is invertible at the witness because the residual q_alpha are every monomial z_i z_j. This is an algebraic open condition on the exact-rank stratum. Shrinking the etale neighborhood to that open gives a nonempty open set of parameters admitting the desired corank-e point.

The witness itself need not be basepoint-free away from the origin. That does not affect the argument: its open image in S meets the dense basepoint-free independent open. No claim about a special global projection is substituted for the asserted generality.

## 3. Formal elimination gives the whole local algebra

At a point in that open incidence, n-e independent fiber equations may be used as formal coordinates w'_1,...,w'_(n-e). After quotienting by them the completed regular local ring is B=k[[z_1,...,z_e]], and the remaining g equations generate J contained in m_B^2. Their degree-two terms span m_B^2/m_B^3, so m_B^2=J+m_B^3.

For M=m_B^2/J, this equality gives M=m_B M. The module is finite over the Noetherian local ring B. Nakayama therefore gives M=0, or **J=m_B^2 exactly**. This does not merely identify an initial ideal, nor assume that higher terms can be ignored. The local algebra is Artinian, so completion changes neither it nor its length.

Every basepoint-free tuple gives a finite morphism: f^*O(1)=O(2), while a positive-dimensional proper fiber would contain a curve on which that line bundle is both ample and trivial. Equivalently, the proper morphism has no positive-dimensional fibers and hence is finite.

## 4. Exclusion of extra support

For p!=q, quadrics surject onto the first jet at p plus the value at q. Indeed first-jet surjectivity at p is immediate, and L^2 for a linear form L vanishing at p but not q changes the value at q while having zero first jet at p. Only these data are prescribed.

Holding a denominator s_0 with nonzero values at p,q fixed, this gives unrestricted values f(p), f(q), and derivative df_p. On a common target chart, equality of the values has codimension m independently of the rank-exactly-(n-e) condition, which has codimension n. Finite source/target charts cover the equality locus. Allowing the distinct points to vary adds 2n parameters, so the full extra-support incidence has dimension dim S-c.

The image is constructible; the dimension of its closure cannot increase above dim S-c. Its complement is thus dense open. This is valid even though the distinct-point locus is not proper and q may approach p in its boundary. One takes the closure of the image, not an unjustified closed-image assertion.

Intersecting this complement with the open from Section 2 excludes every second geometric point in the chosen fiber. Since the map is finite over an algebraically closed field, there are no other hidden components without support points. The entire fiber, including its scheme structure, is the Artinian local scheme computed in Section 3.

As a diagnostic, two *full* first jets of quadrics at p and q are not independent. With p=[1:0:...] and q=[0:1:0:...], the cross monomial x_0 x_1 is shared by the two jet maps. The exact ranks are n+2 for one first jet plus one value and 2n+1 for two full first jets, whose target has dimension 2n+2. The independent checker confirms this one-dimensional failure, including ranks 42 and 81 versus 82 when n=40. The proof uses precisely the valid assertion.

## 5. Passage to general centers

The independent-tuple locus maps openly to Gr(m+1,H), with fibers GL_(m+1). Postcomposition by a projective target automorphism preserves the fiber property. Taking the union of all translates of the good open is an invariant nonempty open still satisfying the property. Its image is a nonempty open in the Grassmannian.

Under the duality between subspaces of H and projection centers of v_2(P^n), the basepoint-free condition is disjointness of the center from X. Hence the argument genuinely reaches an open set of centers for the one fixed embedded variety. For e=4, the center has dimension 813 in P^860 and a fiber linear space has dimension 814 and codimension 46. Thus the excess codimension is 46-40=6, as required.

## 6. Full conormal module, including all source variables

In completed source coordinates write R=k[[w_1,...,w_(n-e),z_1,...,z_e]] and I=(w)+(z)^2, with A=R/I. There are m=n-e+g minimal generators. The linear fiber space has codimension m, so its conormal restricted to Z is A^m, **not A^(m+1)**. Restriction surjects onto I/I^2. Applying Hom_A(-,A) therefore gives the required injection and cokernel definition of Q.

The dual conormal is the module of assignments to the minimal generators satisfying their syzygies. Each w generator may be assigned an arbitrary element of A: the other coefficients in its mixed pair relations vanish in A. Each quadratic generator must have image in m_A. For i!=j the relation z_i z_j^2-z_j(z_i z_j)=0 forces the corresponding constant terms to vanish; these relations cover all squares and mixed quadrics. Conversely every syzygy has coefficients in the maximal ideal, and m_A^2=0, so every assignment of quadratic generators to m_A is permitted.

Equivalently, in a minimal generator basis the image of the dual conormal is

    A^(n-e) direct-sum (m_A)^g  inside A^(n-e) direct-sum A^g.

Any two minimal presentations by m generators differ by an invertible matrix over the local ring, so this computes the actual natural cokernel up to isomorphism. It follows that **Q is isomorphic to k^g**, not just that its length happens to be g. The local Hom dimension is (n-e)(e+1)+ge. For e=4 these numbers are 36*5+40=220, while A^m has dimension 46*5=230. Thus length Q=10 and q=10/6. No free summand, ambient/source contribution, or other support contribution is omitted.

Finite presentation and flat completion justify computing Hom and its finite-length cokernel after completion. The conclusion returns to the algebraic fiber unchanged.

## 7. Regularity and threshold checks

For any closed embedding of this square-zero local scheme into an affine chart, the centered coordinate images generate m_A as a vector space: they generate its algebra and all products vanish. In the Veronese embedding, the sections x_0^2 and x_0 t_i explicitly give the constant and these linear classes. Degree-one ambient sections therefore span all e+1 sections on Z. Degree zero spans only the constant. The ideal-sheaf interpolation criterion gives regularity exactly 2. This is the source convention; the regularity of the homogeneous coordinate ring would differ by one.

For every e>=4, q=(e+1)/(e-1)<2. For e=2 the comparison holds with q=3, and for e=3 it is equality with q=2. These positive and boundary controls are essential because they detect a missing division by c.

The independently computed derivation space has dimension e^2. Thus (e+1)+e^2/c=n/c+1, consistent with the fixed-scheme bound in Beheshti--Eisenbud 0911.3924, Theorem 1.1. It also agrees with the corank threshold e(e+c)=n. Neither consistency check is used as a substitute for incidence dominance.

## 8. Remaining partial proofs

- P1 passes: before affine degree filtration reaches the finite algebra, its dimension strictly increases. This gives interpolation by length minus one and ideal regularity at most length.
- P2 passes using the cited licci equality and general-projection Q bound. The attribution and restricted scope are correct.
- P3 passes: e>=3 forces n>=3(c+3); when c=1, e>=4 forces n>=20. In the remaining embedding-dimension-three case, eliminating independent linear equations leaves at most four generators, to which the cited licci result applies. The c>n conclusion also follows from the multigerm bound. Endpoints are not accidentally included.
- P4 passes: the separating product H_i kills every unwanted local algebra and is a unit in the intended one. Truncating local centered coordinates at their nilpotency exponent gives total interpolation degree at most sum(nu_i)-1. It proves only the displayed interpolation lemma; the missing generic budget remains missing.
- P5 passes: Eisenbud--Harris Theorem 0.1 applies to the actual coordinate ring and projection ideal. Because the intercept is an integer, the main conjecture is exactly the eventual containment with exponent floor(n/c). No bound on the intercept follows merely from eventual linearity.

## 9. Source verification and normalization discrepancy

The private source PDF hashes all match SOURCE_PROVENANCE.json. The OWR contribution at printed pages 1440-1442 states the characteristic-zero setting and both questions. The catalogue record is genuinely bundled. Beheshti--Eisenbud 0806.1928v3 defines q as length(Q)/c for a finite projection fiber and states the stronger comparison in Conjecture 1.4. The cited linkage, corank, and ideal-power results support the particular applications above.

The last line of Example 4.7 on printed page 12 identifies q with 6 when e=3,c=3. I verified that this is present in the rendered PDF, not an extraction artifact. Directly, its tangent dimension is 18 and the source conormal has dimension 6*4=24, so length Q=6 and q=2. Thus the line has an apparent normalization error: 6 is length(Q)=mu(Q), not q. The proof under audit correctly uses the definition and independently computes the module.

The 2024 Ein--Lazarsfeld draft does label the weaker bound Conjecture 4.2.15. The 2015/2018 Ran paper concerns local embedding dimension at most two and general fibers in a fixed-length stratum. An additional audit search found Ran's 2022 paper arXiv:2205.06751: it states length bounds and local order-one/order-two equations under its embedding hypotheses. It does not state the requested sharp regularity or Q comparison and does not invalidate this counterexample. No claim of exhaustive literature coverage or novelty is justified by these searches.

Primary links:

- https://ems.press/content/serial-article-files/46169
- https://arxiv.org/abs/0806.1928v3
- https://arxiv.org/abs/0911.3924v1
- https://arxiv.org/abs/0807.4243v1
- https://arxiv.org/abs/1503.06352v3
- https://arxiv.org/abs/2205.06751v1
- https://www.math.stonybrook.edu/robert.lazarsfeld/LSGAV.Prelim.Draft.pdf

## 10. Reproduction and correction boundary

Run python independent_check.py and compare with independent-results.json. All arithmetic is exact; the largest normal matrix is 126 by 126. The independent implementation differentiates the polynomial terms rather than filling the expected block matrix, generates the full monomial conormal pair relations including the w variables, computes derivation constraints, builds interpolation images by multiplication, and tests valid and invalid jet-surjectivity assertions.

The original checker correctly tests its determinant and syzygy ranks. Its Hilbert values and derivation dimension are inserted from proven formulas, so it should not be described as independently computing those particular quantities. The new audit control fills that verification gap. This is an evidence-description refinement, not a defect in the proof.

There are no required proof repairs. CORRECTIONS.md records optional source and reproducibility clarifications. All review outputs are separate from the frozen packet. The final publication/queue gate remains the parent's responsibility, and the full bundled target must remain unsolved.
