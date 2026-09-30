# Independent review: line-action additive distortion (10300025)

Date: 2026-09-30, UTC

## Verdict

**PASS for the literal displayed condition**, with the source-interpretation warning retained. The common-conjugacy proof is complete for arbitrary countable families of homeomorphisms of the real line, including orientation-reversing maps. Its application to the stated leaf-line action is valid under the usual second-countability convention for manifolds. For the earlier closed, co-oriented formulation, the conclusion also follows from a credited published theorem.

This is an independent AI mathematical review, not human peer review or a certification of novelty. The result does not settle an unidentified stronger geometric intention behind the historical remarks. Repository treatment as a credited known-result consequence/source clarification is supported; an announcement of a new solution to a still-open geometric problem is not supported.

Reviewed artifact:

- `KNOWN_RESULT.md`, SHA-256 `8b9103c862380ea8d93b9d89d6dc03e06b0b90e3d6cb8453bdf1453ba1180cf4`
- Author confirmed this frozen version and its exact controls before this verdict
- Author verifier SHA-256 `d08165d6ddec533202eb59b7c026ef2d2d54ca24d34983868b1ff8c03fd169ea`
- Author receipt SHA-256 `242ff167458285159d497bfe54504f31a9e3ad047b025eb8ada15dd68a1e55ef`

No author files, queue entries, public repository state or PRs were changed by this review.

## 1. Source and quantifier audit

The displayed formula in Calegari's [2002 Question 8.2, page 16](https://arxiv.org/pdf/math/0209081v1) allows one conjugacy of the action and an additive constant depending on the group element. Its subsequent first remark separately discusses a constant independent of the element. Thus the artifact correctly distinguishes these two quantifier patterns. The second remark suggests a toroidal obstruction to the preceding condition. The elementary theorem below applies to toroidal actions as well, so that remark cannot be reconciled with the unrestricted topological reading by mathematical inference alone. The artifact appropriately preserves the mismatch rather than inventing a geometric hypothesis.

The earlier [2000 paper, Section 1.1 and Question 5.3.19](https://msp.org/gt/2000/4-1/gt-v4-n1-p17-p.pdf), uses closed orientable manifolds and co-oriented foliations. Its question permits choosing a parameterization of the leaf line and a separate error bound for each element. Co-orientation makes the action increasing; compactness gives finite generation. No extra regularity or coarse-control restriction on the parameterization appears in the displayed question.

[Deroin–Kleptsyn–Navas–Parwani, Theorem 8.5](https://arxiv.org/pdf/1103.1650v3), reprint page 23, supplies one conjugacy with Lipschitz maps and displacement bounded over the line for each element of an irreducible finitely generated increasing action. Irreducibility means absence of a common fixed point. Adding translations by 1 and an irrational number produces a finitely generated minimal action, to which the theorem applies; restriction returns the desired conjugacy for the original subgroup. Their theorem's proof explicitly uses this enlargement strategy. The claimed literature implication is therefore valid. I verified its statement and applicability, not every stochastic theorem in its dependency chain; the deterministic proof makes the present conclusion independent of that chain.

Primary PDFs were accessed independently through the web tool, and corresponding local text was compared at the cited locations. The prior imported report's vague phrase about uniform distortion must not be substituted for the source's explicit element-dependent formula.

## 2. Independent reconstruction of the countable proof

Let f_1,f_2,... be any countable family of line homeomorphisms. Write e_j=+1 for an increasing map and e_j=-1 for a decreasing map. These are the only possibilities for a continuous bijection of the line. Choose R_0=0, R_1=1, and recursively R_{n+1}>R_n+1 so that both the image and inverse image of [-R_n,R_n] under every f_j with j<=n lie inside (-R_{n+1},R_{n+1}). Finite unions of compact sets ensure that this recursion is possible at every stage, independently of how fast individual maps grow.

Define H to be odd and affine on consecutive positive-radius intervals, with H(R_n)=n. Strict growth of the radii gives positive slopes. The endpoint definitions agree, R_n tends to infinity, and H(R_n) tends to infinity. Thus H is continuous, strictly increasing and onto the entire line, with continuous inverse. There are no gaps, accumulation points of knots in a bounded interval, or completion/endpoint issues. In particular the metric pulled back from the new Euclidean coordinate is complete, although no relationship to an old geometric metric is asserted.

Fix j. For R_n<=|x|<=R_{n+1}, n>=j+1:

1. The stage n+1 image inclusion gives |f_j(x)|<R_{n+2}.
2. If |f_j(x)|<R_{n-1}, the stage n-1 inverse-image inclusion would imply |x|<R_n, a contradiction. Hence |f_j(x)|>=R_{n-1}.
3. The stage j inverse-image inclusion places the unique root f_j^{-1}(0) strictly inside (-R_{j+1},R_{j+1}). Since |x|>=R_{j+1}, monotonicity gives sign(f_j(x))=e_j sign(x).

It follows that |H(x)| lies in [n,n+1] and |H(f_j(x))| lies in [n-1,n+2], with the aligned signs just proved. Therefore

|H(f_j(x))-e_j H(x)| <= 2.

On the remaining core |x|<=R_{j+1}, stage j+1 bounds |H(f_j(x))| by j+2 and |H(x)| by j+1. A global bound B_j<=2j+3 follows. The endpoints belong to these closed bounds, so the annular/core transition causes no omission.

Putting F_j=H f_j H^{-1}, the reverse triangle inequality yields

abs(|F_j(u)-F_j(v)|-|u-v|)
<= |F_j(u)-e_j u|+|F_j(v)-e_j v|
<= 2B_j.

Taking C_j=2B_j+1 ensures positivity even for identity maps. The same H was constructed before j was fixed, so the conclusion genuinely has one common conjugacy. There is no exchange of a separate conjugacy for each map. Enumerating a countable group image handles all its elements; faithfulness, finite generation, properness, invariant measures and absence of fixed points are unnecessary. A finite group/family can be enumerated with repetitions.

The inverse-image condition is essential to this proof: a forward-only exhaustion controls escape above but not arbitrarily rapid contraction. Orientation reversal is also handled essentially by comparison with -u; ordinary displacement from u would be unbounded even for a reflection.

## 3. Finite-generator proof and application

The maximum envelope F(x)=max(x+1,s(x):s in S), for a finite symmetric set of increasing generators, is continuous, strictly increasing and onto. The upper bound at negative infinity uses finiteness of the family; at positive infinity it is immediate from x+1. F(x)>=x+1 makes its positive and negative iterates escape to the corresponding ends. The fundamental-interval definition of H therefore gives a global increasing homeomorphism satisfying H F H^{-1}(u)=u+1.

Symmetry of S supplies F^{-1}(x)<=s(x)<=F(x), hence displacement at most 1 for every generator after conjugacy. Composition adds displacement bounds. The word-length estimate and the two-point additive-distortion estimate follow, including the identity case. This proof is valid without irreducibility or an invariant measure, and makes no Lipschitz claim.

A second-countable 3-manifold has countable fundamental group: its countable triangulation has only countably many finite combinatorial loops, which represent all fundamental-group elements. In the smooth closed source setting a finite triangulation suffices. The image of the holonomy representation is therefore countable. A chosen leaf-space homeomorphism followed by H proves the literal inequality. If second countability were dropped from an unconventional use of the word manifold, the countability assertion would need a separate hypothesis; this is not a gap for the cited setting.

## 4. Independent controls and adversarial boundary checks

The frozen author script was copied with the proof into `author_reproduction/` and rerun there, preserving the author directory. It reproduced all **6,665 exact rational assertions** and the bound artifact hash.

The separately written `independent_controls.py` imports no author code. It passed **20,173 exact rational assertions** on 15 maps and 24 radii. Maps include unequal rational piecewise-affine slopes, shifts, both orientations, identity, reflection and strong contraction. Tests cover inverse identities; image and inverse-image inclusions; lower/upper annular bounds; tail signs; signed displacement; and the reduction to two-point distortion. On each compact core it checks every breakpoint of the composite signed-error function, giving a complete finite PL certificate on that core rather than only a sample there.

Negative controls verify that forward image bounds alone do not prevent unbounded contraction error in an inadequately chosen coordinate, and that reflection requires the signed reference. These computations are diagnostics, not a replacement for the infinite-family proof above. Arbitrarily nonlinear homeomorphisms and all countable families are covered by the compactness/monotonicity proof, not by finite sampling.

## 5. Publication boundaries and final recommendation

No essential mathematical correction is required for the frozen artifact. Preserve all of the following in any PR or queue summary:

- The target is the literal common-topological-conjugacy, per-element additive-error statement
- The finite-generated increasing case is a consequence of credited existing literature
- The toroidal remark's mismatch is unresolved at the level of historical intent
- No uniform bound across elements, control relative to an ambient transverse metric, or ambient leaf-distance theorem is proved
- The countable extension does not assert simultaneous Lipschitz regularity
- No claim of novelty or human peer review is justified

Minor typesetting tokens such as `(operatorname{sign}` should be cleaned if rendering the manuscript; their mathematical meaning is unambiguous and they do not affect this PASS.

Review completion: 100% for the supplied artifact and stated scope; historical-intent reconstruction is explicitly outside the verified conclusion.

## Final formatting/status diff audit, 2026-09-30 07:06 UTC

PASS extended to final KNOWN_RESULT.md SHA-256 `3cf3b548da6d0fbddd0577f02b7cfae056e30bee44ca0af2ba967d304c2fdbb8`. The full unified diff against the frozen snapshot was inspected: only the review-status header, inline math delimiters and missing LaTeX backslashes changed. No mathematical claim, bound, quantifier, hypothesis or argument changed. The unchanged verifier was rerun in final_reproduction/; all 6,665 assertions passed, and its receipt matches the prior receipt after excluding the artifact hash. The original review limitations and independent controls remain applicable.
