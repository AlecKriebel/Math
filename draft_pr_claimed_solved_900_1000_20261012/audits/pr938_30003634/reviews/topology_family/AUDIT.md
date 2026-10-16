# Topology family: independent adversarial audit

## Verdict and exact scope

**PASS for the topological bridge and its character/framing applicability to the proposed witness. No required mathematical repair found.** This is a family verdict, conditional on the separately audited nonzero ordinary signature of the actual closure. It neither certifies that finite signature computation nor establishes priority, present open status, or suitability for publication.

The strongest result established here is the following deduction from the standard geometric 1-solution hypotheses and the published surgery/rho theorem:

> If an algebraically split ordered oriented link has an ordinary integral smooth 1-solution in Otto's sense, its ordinary Levine-Tristram signature at -1 is zero.

The proof below is universal. It does not infer a topology theorem from the finite braid computation or from finitely many controls. The actual braid is also checked independently for the elementary hypotheses needed to apply that theorem. There is no assertion that ordinary signature is a homomorphism on all string links.

The complete charter, private target body, and immutable original proof were read before writing `RECONSTRUCTION.md`. Historical audit/acceptance narratives and sibling reports were not read at any point. The original proof hash is `0492e0e0de785be263174e86d69855120b2f5c24b105c6479739cd72d64abe3b`. Author accounting remains 1/5; this family audit adds 0 positive proof-search turns. Expanding and testing the already proposed topology mechanism did not introduce a substantively new discovery route.

## Imported foundations and exact source conventions

The following published facts are imported, not proved here. Source URLs, immutable downloaded-file digests, version/page identifiers, inspected pixel digests, and query limits are in `SOURCE_PINS.json`.

1. [Otto, Definition 2.3](https://msp.org/agt/2014/14-5/agt-v14-n5-p05-s.pdf), printed pp. 2631-2632 / PDF pages 5-6, supplies the integral homology isomorphism, embedded oriented surfaces with trivial normal bundles, and both sets of surface groups in the ordinary nth derived subgroup. The following paragraph defines string-link solvability by standard closure. This is the required smooth integral model.
2. [Toffoli](https://epub.uni-regensburg.de/52299/1/the-atiyahpatodisinger-rho-invariant-and-signatures-of-links.pdf), (1.1)/Theorem 2.6(ii), gives rho = ordinary signature minus twisted signature for a rank-one unitary representation extending over an oriented bounding manifold. Definition 2.2 uses the Hermitian intersection form, with its radical treated through the absolute-to-relative homology map.
3. In the same source, Theorem 4.24, Remark 4.25/(4.21), and Corollary 4.28 give the compatible integral surgery formula. The character domain is every unit complex number other than 1. Example 4.5 and Definition 4.12 fix Seifert framing by negative sums of relevant linking numbers. Definition 4.19 makes every one-colored link component-to-color algebraically split.
4. [Cha, Section 8 / Theorem 8.2](https://ems.press/content/serial-article-files/31720), printed pp. 599-602 / PDF pages 45-48, independently corroborates the finite 2-character Witt-defect vanishing. Lemma 8.4 supplies the broader p-group rank statement. Remark 8.1 says the arguments do not use spin or the stated quadratic self-intersection condition. This corroboration is optional; the direct deduction below does not depend on Cha's theorem.

Elementary cellular homology, the integral universal coefficient theorem, Poincare-Lefschetz intersection theory for a unitary rank-one local system, and invariance of real symmetric inertia under extension from Q to C are standard imported foundations. Their needed specializations are spelled out below; they are not computer-verified axioms.

The Toffoli file is the publisher's online 37-page layout hosted at the institutional repository, carrying the Cambridge DOI footer and a first-page `page 1 of 37` label. Its page 31 contains (4.21), and page 32 contains Corollary 4.28. These are not final-volume pagination 404-440. The failed DOI landing-page read did not impede access to these actual publisher pages.

## Direct deduction and attempted falsifications

### 1. Character extension uses the actual integral H1 map

Let W be a connected oriented 1-solution with boundary the zero surgery M_L. Write the integral surface basis as L_i,D_i for 1 <= i <= r. Thus H2(W;Z) is free of rank 2r. A disconnected closed component of a proposed W could simply be discarded; connectedness of the boundary component is the relevant case.

For an algebraically split m-component link, the zero-surgery presentation matrix for H1 is the zero m by m linking/framing matrix. Consequently H1(M_L;Z)=Z^m with the meridians as a basis. The homomorphism sending every basis vector to -1 in {+1,-1} is well-defined and factors through this abelianization. The inclusion-induced map i_*:H1(M_L;Z)->H1(W;Z) is an isomorphism by the solution hypothesis. Define

    alpha_W = alpha_M composed with i_*^{-1} composed with abelianization of pi1(W).

Its restriction is the specified character. No extension of a nonabelian representation is being assumed. The same isomorphism makes H1(W;Z)=Z^m, eliminating 2-torsion exactly where it will be needed. A choice of a basepoint changes restrictions only by conjugation; a rank-one abelian character is unchanged by conjugation.

### 2. The finite-CW rank comparison is valid in every degree

A compact smooth W has a finite CW model. After choosing cell lifts, the universal-cover differential is a matrix over Z[pi1(W)]. Applying alpha_W evaluates every group element as +1 or -1, hence gives an integer matrix d_j^alpha. Reducing it modulo 2 gives the ordinary cellular differential over F2: both signs reduce to 1, and every integral group-ring coefficient is treated by augmentation modulo 2.

If an s by s minor of the ordinary matrix is nonzero over F2, the matching determinant of d_j^alpha is odd. It is therefore nonzero over Q. Thus

    rank_Q(d_j^alpha) >= rank_F2(d_j ordinary),

including the zero-rank cases. If c_j is the number of j-cells, the chain dimensions agree, and

    b2(W;Q_alpha) = c2 - rank_Q d2^alpha - rank_Q d3^alpha
                  <= c2 - rank_F2 d2 - rank_F2 d3
                   = b2(W;F2).

No Euler-characteristic, acyclicity, Alexander polynomial, or approximation hypothesis is concealed in this inequality. Both relevant differential ranks have the same inequality direction.

The integral universal coefficient short exact sequence in degree 2 is

    0 -> H2(W;Z) tensor F2 -> H2(W;F2)
      -> Tor(H1(W;Z),F2) -> 0.

The left term has dimension 2r because the integral surface classes form a basis. The right term is zero because H1(W;Z)=Z^m. Therefore b2(W;F2)=2r, which gives the desired upper bound b2(W;Q_alpha)<=2r. Torsion in H2 is also excluded by the integral basis hypothesis; it cannot be discarded silently.

The importance of the H1 condition has a concrete falsification control. For the usual cellular model of RP2, with generator t of its double cover, the boundaries are d2=1+t and d1=t-1. At t=-1, twisted rational b2 is 1; ordinary rational b2 is 0; ordinary mod-2 b2 is 1. Its H1 has 2-torsion. The proposed inequality with ordinary rational b2 would be false there; the actual mod-2 inequality and UCT step remain correct. This control is not claimed to be an oriented 1-solution.

The script also exhausts 6,561 small signed group-ring 2 by 2 matrices to look for a reversed-rank or parity mistake. These diagnostics do not establish the universal determinant argument, which is the proof above.

### 3. Surface classes exist with the required local coefficients

The representation is abelian, so it kills [pi1(W),pi1(W)]. Both pi1(L_i) and pi1(D_i) lie in this subgroup by the n=1 solution requirement. The restriction of Q_alpha to each surface is therefore trivial. Choosing a nonzero coefficient at one point and transporting it across the surface gives a globally defined flat section. Multiplying this section by the oriented fundamental cycle gives a twisted class in H2(W;Q_alpha). This is an absolute class: the solution surfaces represent absolute integral H2 classes. A relative surface with nonempty boundary would not satisfy that basis requirement.

Changing a whisker or lift changes a chosen flat coefficient by a sign. This only rescales its twisted class by +/-1. Distinct surface images are disjoint except for the specified dual intersection points. Therefore all cross-pairings between different dual pairs are zero, and all same-type pairings are zero. A framing supplies a disjoint small normal push-off, so both types of self-pairing vanish. There is no additional group-ring self-intersection contribution from a framed embedded surface: the push-off has no intersections in the base, hence none in any cover.

At the unique transverse intersection of L_i and D_i the local-coefficient contribution is the orientation sign times the ratio of two parallel transports. Each transport is +/-1. The result is epsilon_i in {+1,-1}, not a sum capable of cancelling. Rescale D_i by epsilon_i. The resulting twisted pairing matrix is exactly

    direct sum, i=1..r, of [[0,1],[1,0]].

This normalization does not affect any already-zero pairing.

As a separate lift-factor check, in the double cover take the anti-invariant cycles x=L^+-L^- and y=D^+-D^-. Matching sheets give intersection 1+1=2; nonmatching sheets are disjoint. If the selected sheets were swapped the value would be -2, removable by the same sign change. It is not zero. Projector-normalized cycles (1-tau)/2 and the normalization of the covering intersection form introduce positive factors of 2 or 1/2. They cannot alter linear independence or signature. The direct local-coefficient computation fixes the convention with off-diagonal +/-1 and avoids mistaking either cover normalization for the base pairing.

### 4. Independence, radicals, and the complex signature

A relation among the 2r classes can be paired with each of them. The displayed invertible hyperbolic matrix forces every coefficient in the relation to vanish. This proves linear independence even if the ambient absolute intersection form were initially allowed a radical. Together with the rank upper bound, it forces these classes to be an entire basis of H2(W;Q_alpha). Thus the ambient twisted form has no additional summand or radical, and its signature is zero.

Extending scalars from Q to C preserves homology and sends this real hyperbolic matrix to the Hermitian matrix in Toffoli's definition. Its inertia is (r,r,0); the complex twisted signature is zero. The ordinary integral basis gives the same hyperbolic ordinary form and sigma(W)=0. When r=0, both homology groups in question are zero by the same dimension bound, so the conclusion remains valid.

This reasoning does not require the boundary character to be acyclic or a boundary Alexander polynomial to be nonzero. Boundary twisted homology and its maps may be nontrivial. Toffoli's absolute-form convention allows that situation; the proof separately establishes that the W form has no radical.

### 5. Surgery, nullity, and the point -1

Give all components one color and take omega=-1=e^(2 pi i * 1/2). For an algebraically split link, every term in the Seifert-framing sum is zero, so the compatible Seifert surgery is exactly the zero surgery M_L. Its entire framed linking matrix Lambda is zero. Its signature, sum of entries, and every corresponding linking/framing correction are zero. Remark 4.25/(4.21), equivalently Corollary 4.28, therefore specializes to

    rho_alpha(M_L) = -sigma_L(-1).

The bounding-manifold formula is

    rho_alpha(M_L) = sigma(W)-sigma_alpha(W) = 0.

Hence sigma_L(-1)=0.

The printed character domain in Theorem 4.24 and Corollary 4.28 excludes 1 only. The compatibility condition has been checked using the actual Seifert framing, and -1 is a nontrivial unitary value in that domain. No Alexander-root, nonzero determinant, or local-constancy hypothesis appears. Theorem 2.6(ii) and (1.1) use this same rho convention; no kernel-dimension/nullity term is to be appended to their statements. Definition 2.2 and the surrounding discussion explain the intersection-form radical directly. Replacing the author's eta convention with a different reduced eta convention and then importing its formula without conversion would be an error; the candidate consistently uses Toffoli's formula.

The ordinary link signature at -1 is the signature of the symmetrized Seifert matrix: (1-omega)V+(1-conjugate(omega))V^T becomes 2(V+V^T). The positive scalar does not affect signature, and any global reversal of the signature convention leaves this zero-obstruction unchanged.

Cha's Section 7 uses an averaged Levine-Tristram knot-signature convention at roots. That should not be substituted for Toffoli's pointwise link-signature statement. The optional Cha corroboration here is the vanishing of the actual 4-manifold Witt defect at n=1,p=2,d=2, where Q(zeta_2)=Q; it does not depend on identifying Cha's separate knot-signature convention with the one used in the finite Goeritz calculation.

## Actual-witness applicability and logical scope

The independent script builds the nested commutator from the generators, reducing adjacent inverse Artin letters as it goes. It obtains length 104, final strand permutation identity, and signed crossing totals 0 for each of the three unordered strand-label pairs. Since oriented closure linking is one half the signed crossing total, all pairwise linking numbers are zero. Consequently the zero-framed surgery matrix is zero, H1 is Z^3, and the character and corrections used above have exactly the required values. `FINITE_CHECKS.json` records these checks.

There is also a universal group-theoretic explanation independent of this crossing count: pairwise linking numbers on pure braid closures are additive under stacking, hence vanish on every pure-braid commutator. The nested expression consists of pure braids, and its outer commutator is therefore algebraically split. Normality of each ordinary derived subgroup places c,d,e in P3^(1), u,v in P3^(2), and beta in P3^(3). No statement about an unbased closed-link group is needed.

Otto defines F_1^3 by the standard ordered oriented string-link closure, which agrees with the ordinary pure-braid closure in this application. Thus a separately verified nonzero signature of this actual closure proves beta is outside F_1^3. A value of either -2 or +2 under a globally reversed convention gives the same contradiction. This family has not accepted the finite -2 computation as an axiom for the universal lemma.

Adding separate split trivial strands preserves pairwise linking zero and supplies extra meridians assigned -1. The same universal proof applies. Split unknots add only null directions to a standard Seifert form and do not alter its signature, so the stated extension at n=1 is sound if the original nonzero signature is verified. No claim about failure at every higher n follows or is required. The m=1,2 pure-braid positive-derived degeneracies are compatible with this conclusion.

## Required changes, optional clarifications, and exact remaining gap

**Required mathematical fixes: none within this family's scope.** The proof's universal bridge survives the rank, UCT, torsion, lift, intersection, framing, radical, APS, and -1-domain challenges.

Optional expository improvements for any later package are to name Toffoli's online-PDF pagination, spell out the UCT short exact sequence, and add the one-sentence local-coefficient surface-class construction. They improve checkability; the immutable proof already contains enough of each argument for this audit. If citing Cha as a direct alternative, keep the Witt-defect argument and Remark 8.1 distinct from its averaged knot-signature convention.

The exact gap outside this family is the independent certification of the nonzero signature of the actual displayed braid closure, plus the primary question/model scope review. Neither is inferred from historical acceptance strings. Publication or priority conclusions remain outside this audit. No outside input, person, sibling agent, remote write, tracker write, publication action, or shared Git/index/branch mutation occurred.

## Authentication and release boundary

At the start, all 44 selected files matched actual blobs at immutable commit `2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b`, their disk copies, and inventory SHA256 values. The actual Git subtree also contains exactly these 44 paths. End authentication reruns the closed-tree comparison and the three explicit charter digest pins. Current shared HEAD is recorded observationally; it is not substituted for the immutable source commit. Only this family's directory was written.

`PUBLIC_ALLOWLIST.json` is the explicit public map. `MANIFEST.json` lists hashes of its 14 settled public companions and excludes itself. Its final SHA256 is reported externally to the parent, where it can be pinned without a self-referential seal. Raw PDFs, extracts, renderings, private source body, receipts, caches, and other unlisted files are not part of the public package. The final family completion estimate is 100% of the assigned topology audit, conditional only on the stated separate-family work, not 100% of a discovery or priority claim.

## Diagnostic hardening addendum

At the parent's request, the finite checker and the authentication helper now use explicit fail-closed checks and emit JSON to stdout only. Normal replay no longer rewrites the frozen finite/authentication receipts. This is diagnostic-code hardening only: no mathematical claim, proof mechanism, source, original44 file, or family verdict was changed. The earlier family manifest pin was `dca3fb07891b932f1ac1c493f9e919adef6b890b6e310047a56f9649784aca07`; the replacement self-excluded manifest's final digest is supplied externally to the parent.

`DIAGNOSTIC_HARDENING.json` records successful normal, -O, -OO, and actual environment-inherited optimization-level-2 replays. Each mode executes all 6,561 finite rank cases, matches the frozen finite result, and authenticates all 44 immutable source blobs. Wrong word-length, wrong rank-inequality, and wrong proof-digest controls fail nonzero without success JSON in every mode. Mutations run in memory only. Curated file hashes, sizes, and modification times remain unchanged during replay. `test_topology_diagnostics.py` reproduces these controls read-only.

`REUSE_NOTE.md` resolves all three optional expository clarifications in reusable text and points to their full existing treatments: online-PDF pagination/version pins; the UCT sequence and construction of twisted surface classes; and the boundary between Cha's Witt-defect specialization and its averaged knot-signature convention. These remain expository clarifications, not required mathematical fixes.
