# Fresh adversarial check of the Reeb bridge and Cartier transfer

Time: October 6, 2026, 22:30 PDT (October 7, 2026, 05:30 UTC).
Auditor: `complete_audit_review2/independent_bridge_attack`, with a separately assigned `top_form_attack` subagent.
Scoped review completion estimate: 100%. This is not a completion estimate for proving the upstream gap theorem.

Reviewed `main.tex`, SHA-256 `2ec5ab1a3db82dc97108b28f0d9a86fd0f1dc4f9aeec138eb6cf4ce2e2458f70`, especially lines 87–174. No prior complete favorable review was read before reaching this verdict. Existing bridge/transfer notes were used to locate primary sources; their conclusions were not treated as evidence. No manuscript edit, Git operation, download/cache creation, or external communication was performed.

## Verdict and scope

No substantive defect or counterexample was found in the conditional normalized-volume-to-density bridge, or its use of the Spotti–Sun Cartier-root theorem for cubic limits. This conclusion takes the unrestricted algebraic singularity gap as an external hypothesis. It does not certify or reprove that theorem, Li–Liu's full proof, Spotti–Sun's analytic compactness machinery, Fujita's classification, or the whole package.

## Primary inputs inspected independently

- [Li–Liu, arXiv:1602.05094v3](https://arxiv.org/html/1602.05094v3), Theorem 1.9 and Section 6, especially its opening hypotheses, Theorem 6.2, Lemma 6.3, Lemma 6.8 and the final limiting proof. The Reeb valuation minimizes over all real valuations centered at the vertex. Quasi-regular approximants converge smoothly and need not remain Einstein; their quotient Ricci lower bounds approach the required value. The contact-volume formula, its round-sphere normalization and that limit support the stated density identity.
- [Van Coevering, arXiv:0806.3728v3](https://arxiv.org/html/0806.3728v3), Proposition 2.3 and Section 3 including Proposition 3.2: normal affine completion, the torus from the Reeb-flow closure, and Q-Gorenstein eligibility.
- [Collins–Székelyhidi, Geometry & Topology 23 (2019)](https://msp.org/gt/2019/23-3/gt-v23-n3-p05-p.pdf), Lemma 6.1, journal pages 1384–1385: a nonvanishing pluricanonical section with positive Reeb weight gives the needed klt conclusion for an isolated Q-Gorenstein cone. Rationality alone was not used as a replacement.
- Cached `sources/spotti_sun_1705.00377v1.txt`, SHA-256 `f09d96d97db958d8277bbe049fad70ab0272f7b8fc253d628df5f3ea2d0cabfd`, independently reread against [Spotti–Sun's primary source](https://arxiv.org/abs/1705.00377): Sections 1, 2, 5.1 and 5.2. Theorem 5.2 supplies the Cartier root as well as canonical Gorenstein singularities; Lemma 5.3 treats iterated cones. The manuscript uses this as an inherited theorem, within its polarized smooth-limit setting, rather than asserting a root theorem for arbitrary Q-Fanos.

## Attempts to falsify the bridge

The finite fundamental-group branch is decisive even when the canonical bundle has nontrivial holonomy. On a smooth link of dimension 2k−1, Ric = (2k−2)g. Myers gives a finite universal cover of degree d, and Bishop gives

    Theta(Y) = Vol(Ytilde)/(d Vol(S^(2k−1))) <= 1/d.

For d >= 2 this is at most 1/2. Since b_2 = 1/2 and b_k increases for k >= 2, this branch meets the target in every needed dimension. For example, C^3/{±1} has a smooth link with pi_1 = Z/2, density 1/2 and a nontrivial canonical character. It causes no unsupported application of a genuine-top-form minimizing theorem.

The simply-connected branch was independently challenged by a subagent. On the punctured cone, the canonical connection is flat and pi_1 is zero, giving a global parallel nonvanishing holomorphic top form sigma. For E = r d/dr, the cone identity nabla E = Id gives L_E sigma = k sigma. Take the compact torus to be the closure of the Reeb flow in the holomorphic isometry group: it preserves the one-dimensional parallel-top-form space and acts by a character, which extends to its complexification. Reflexivity extends sigma across the isolated vertex. The phrase “cone torus” is therefore mathematically defensible with this choice; it does not require equivariance under every algebraic automorphism.

Even a stronger algebraicity reading is harmless. Choose a positive integral quasi-regular field in that torus. The canonical module is finitely generated over the positively graded coordinate ring with degree-zero part C. A fixed-weight component of its completion at the vertex equals the corresponding finite-dimensional algebraic graded component. Hence the homogeneous analytic germ is algebraic, and equality extends on the connected punctured cone by the identity theorem. Li–Liu expressly asks for a holomorphic top form, so this additional argument is not needed merely to match its wording.

The direction of the infimum argument is correct: global minimization supplies the equality before applying the upper gap bound. An upper bound on the infimum would otherwise have the wrong logical force. Smooth-link irregularity is covered by the actual approximation theorem; no extension to singular links was inserted. Flat C^k has density 1 and normalized volume k^k; the ODP degree valuation has volume 2 and discrepancy k−1, consistent with the normalization.

## Attempts to falsify the transfer

The transverse range k = 2,...,n is correct for the relevant KE iterated cones: a normal klt curve is smooth, and these singular strata have complex codimension at least two. A one-dimensional flat cone with a nonstandard cone angle would have a boundary contribution at the vertex, and is outside the boundary-zero KE setting. Products with a Euclidean factor preserve density. The displayed increasing b_k then gives A'(n) <= b_n.

The strict cubic threshold reduces to

    3 > (1 + 1/n)^n,

which follows from log(1+x) < x and e < 3. No equality problem occurs at n = 5 or as n tends to infinity. Keeping the Cartier hyperplane root is essential, and is an explicit source conclusion.

As an additional edge check, the cubic total-volume density lower bound is 3((n−1)/(n+1))^n > 1/3 for n >= 3. Indeed this sequence increases from 3/8: with x = 1/t, the derivative of its logarithm is log((1−x)/(1+x)) + 2x/(1−x^2) > 0, by the convergent power series on 0 < x < 1. Thus after the source's universal-cover reduction any nontrivial flat quotient has order two. The source's separate order-three quotient discussion is unnecessary in this cubic specialization. The order-two transverse surface quotient is the A_1 case with simply-connected Milnor fiber; higher transverse-dimensional isolated quotients are handled by the cited rigidity/smoothing argument. This is a check of hypothesis matching, not a new proof of that analytic argument.

## Remaining limit of the finding

The result is a clean scoped conditional check. The upstream unrestricted algebraic gap, the established inputs, priority, and full package/publication review remain separate responsibilities. No formal or conventional human-peer-review certification is supplied.
