# Modern primary-literature priority check

Audit checkpoint: 2026-10-06 America/Los_Angeles (2026-10-07 04:31 UTC).
Assigned scope: independently check 2025–2026 primary literature and citation chains for exact duplication of the three unweighted targets in `PROJECT_BRIEF.txt`. No external individual was contacted. No upstream file or Git state was changed. Best-guess completion of this assigned audit: 85%; exact full-text access to two relevant subscription papers remains unresolved. This percentage measures audit work, not mathematical correctness or novelty.

## Comparison claim

For every fixed \(n\geq3,p,q>1\) with
\[
\frac1{p+1}+\frac1{q+1}>1-\frac2n,
\]
the project seeks (A) universal distance/gradient estimates for every nonnegative classical solution of the unweighted two-equation system on every proper Euclidean domain, (B) nonexistence for arbitrary classical nonnegative zero-Dirichlet half-space solutions without an a priori boundedness/growth condition, and (C) a uniform Dirichlet solution bound on every fixed sufficiently smooth bounded domain. Assertions restricted to stable solutions, bounded/strip-bounded solutions, energy solutions, radial solutions, scalar equations, or a smaller exponent region do not exactly duplicate this claim.

Important logical check: (A), even without gradients, implies the full entire Liouville theorem. Restrict any entire solution to \(B_R\(x_0\)\), apply (A) at \(x_0\), and send \(R\to\infty\). Conversely the established PQS transfer turns bounded-entire Liouville into (A). Thus a purported modern exact duplication of (A) must also settle the entire conjecture in the project range. This is a deduction, not evidence that searches are complete.

## Sources with exact statements inspected

### Li–Li–Wei: a new higher-dimensional exponent region

Primary sources: [arXiv record](https://arxiv.org/abs/2510.06613), [v1 full text](https://arxiv.org/html/2510.06613v1).
Earliest verified public version: v1, **2025-10-08 03:47:34 UTC**. The record showed only v1 at the audit date.

Theorem 1.1 asserts entire nonexistence for \(n\geq5,p,q\geq1\) under
\[
\frac1{p+1}+\frac1{q+1}\geq1-\frac2n+\frac4{n^2}.
\]
Theorem 3.2 replaces 4 by each fixed \(c_0>2\), provided \(n\geq N(c_0)\). Their introduction explicitly attributes the bounded-to-arbitrary entire reduction to PQS and identifies earlier dimension-four and exponent-region results. Their mechanism combines Obata-type integral inequalities, Picone's identity, scaling, and coefficient selection.

**Overlap:** an unconditional entire theorem in a substantial subset of the project's range; established transfer theorems consequently already furnish universal estimates in that subset. It is incorrect to imply that universal estimates in *any* higher dimension or in *all dimensions for some subcritical exponents* are new. **Nonduplication:** the positive-width near-critical band remains outside both stated ranges. No arbitrary-half-space or bounded-domain all-range theorem is stated here. Their references include Li–Souplet's half-space paper and PQS. Proof validity was not independently re-proved in this literature audit.

### Huang–Zou: stability/decay and annular energy

Primary sources: [arXiv record](https://arxiv.org/abs/2512.16566), [v1 full text](https://arxiv.org/html/2512.16566v1), [JLMS record](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.70412).
Earliest verified public version: v1, **2025-12-18 14:06:56 UTC**; version of record first online **2026-01-22**. A manuscript received date (2024-12-16) is not a public-priority date.

For \(N\geq3,p,q>0,pq>1,a,b>-2\) in the weighted subcritical range, solutions are in \((C^2(\mathbb R^N\setminus\{0\})\cap C(\mathbb R^N))^2\). Theorem 1.2(i) excludes positive solutions stable outside a compact set in their weak sense under either \(\min\(p,q\)<1\) or \(0\leq a-b\leq(N-2)(p-q)\). For \(a=b=0\), exchange components to arrange \(p\geq q\): the weight condition is automatic, but the stability assumption remains. Theorem 1.2(ii) excludes positive solutions with both exact scaling decays \(u=O(|x|^{-\tilde\alpha}),v=O(|x|^{-\tilde\beta})\). Theorem 1.4 instead assumes a uniform energy bound on fixed annuli for rescaled solutions.

**Overlap:** full subcritical unweighted Liouville for special solution classes, not all solutions. **Nonduplication:** neither stability nor the annular-energy/pointwise-decay premise is established for an arbitrary target solution. Transferring the desired universal estimate into the decay premise and presenting that as a proof of the universal estimate would be circular. Section 3.2.3 uses PQS/Phan–Souplet/Phan techniques to derive decay for stable solutions, explicitly preserving the special-class premise. This paper does not supply the three arbitrary-solution targets.

### Sciunzi–Vuono: weaker directional boundedness in the scalar half-space problem

Primary sources: [arXiv record](https://arxiv.org/abs/2510.01865), [v1 full text](https://arxiv.org/html/2510.01865v1).
Earliest verified public version: v1, **2025-10-02 10:12:09 UTC**.

Theorem 1.2 excludes nonnegative solutions of the scalar zero-Dirichlet equation \(-\Delta u=u^q\), \(n\geq2,q>1\), if, up to rotations, \(u\in L^\infty(\mathbb R^{n-2}\times K)\) for every compact \(K\subset\{x'=0,x_n\geq0\}\). This weakens full strip boundedness for the scalar problem. Theorem 1.4 gives normal monotonicity for the corresponding locally Lipschitz \(f\) under the same directional assumption.

**Overlap:** prior progress that prevents advertising all-power scalar half-space nonexistence under directional boundedness as new. **Nonduplication:** it remains scalar and assumes directional boundedness; it is not arbitrary two-equation Lane–Emden half-space nonexistence.

### Bhattacharyya: bounded nonsmooth-space estimates

Primary sources: [arXiv record](https://arxiv.org/abs/2608.08527), [v1 full text](https://arxiv.org/html/2608.08527v1).
Earliest verified public version: v1, **2026-08-09 06:57:40 UTC**.

Theorem 3.1 and Corollary 3.1 concern the transformed variables \(u=f^{-\alpha},v=h^{-\beta}\), require positive upper and lower bounds \(\lambda_u\leq u\leq\mu_u,\lambda_v\leq v\leq\mu_v\), and give log-gradient estimates with constants involving those bounds. Corollary 3.2 assumes \(\alpha=t^p,\beta=t^q\), \(1/3<p/q<3\), both transformed upper bounds at most 1, and takes \(t\to0^+\). Here \(\alpha,\beta\) are this paper's original nonlinearity/transform parameters, not the project's scaling exponents.

**Nonduplication:** these solution-dependent boundedness premises and small-parameter conclusion do not give universal arbitrary-domain estimates with \(C=C(n,p,q)\), or either Dirichlet target. No validation of its asserted small-parameter rigidity was needed to establish this mismatch, and none is claimed.

### Xu–Luo: 2026 higher-order-system paper

Primary theorem preview: [publisher](https://doi.org/10.1016/j.jde.2025.113823); primary author bibliography: [Huxiao Luo's institutional page](https://mypage.zjnu.edu.cn/20184403/zh_CN/lwcg/141116/content/17980.htm). Authors are Yating Xu and Huxiao Luo. The author page states publication **2025-10-10**; journal issue is 2026-02-05. Crossref DOI creation on 2025-10-10 supports bibliographic identification but does not itself certify earliest public text. No earlier preprint was located.

Theorem 1.1(i) in the publisher's theorem preview concerns orders \(0<2k+\alpha,2l+\beta<n\), with self-coupling exponents \(0\leq p\leq p_q\), \(0\leq s\leq s_r\), not both endpoint, and cross-coupling \(q,r>0\), where
\[
p_q=\frac{n+2k+\alpha+2a-q(n-2l-\beta)}{n-2k-\alpha},\quad
s_r=\frac{n+2l+\beta+2b-r(n-2k-\alpha)}{n-2l-\beta}.
\]
**Specialization check:** setting both orders to 2, weights to zero and self-couplings to zero forces \(q,r\leq(n+2)/(n-2)\), not both equal. This recovers an individually-subcritical rectangle, not the entire subcritical hyperbola. The "sub-critical order" phrase refers to operator order. Remaining full-text proofs were not audited. No exact duplication is established by this preview.

## Relevant subscription sources whose exact theorem ranges remain unverified

### Wen Wang, boundary manifolds (2026)

Primary [publisher record](https://link.springer.com/article/10.1007/s12220-026-02487-w), DOI 10.1007/s12220-026-02487-w, J. Geom. Anal. 36, 242.
Earliest public date verified here: **2026-05-29** version of record. Received 2025-07-10 is not public priority. An index gives June 19; use the publisher date.

The primary abstract limits coverage to all nonpositive exponents and certain positive exponents and assumes convex boundaries/nonnegative Ricci curvature for its Liouville application. It generalizes Lu's 2025 paper to Dirichlet conditions. Its exact positive range, precise meaning of Dirichlet data, function spaces, and whether any half-space subclass is strictly stronger than the known statements could not be checked because the publisher supplied a subscription preview. The normal PDF URL returned that same HTML preview; no access controls were bypassed. Search found no accessible author manuscript. **Status: unresolved exact-comparator audit.** The abstract provides evidence of restricted coverage; it does not authorize claiming a theorem-level exclusion of every possible overlap.

### Zhihao Lu, manifold estimates (2025)

Primary [publisher record](https://link.springer.com/article/10.1007/s12220-025-01967-9), J. Geom. Anal. 35, 129.
Earliest verified public date: **2025-03-18** publisher version of record (index date April 2 is later). Primary abstract says all nonpositive indices and only partial positive indices, with Ricci curvature assumptions. Exact theorem ranges could not be obtained through the public preview. **Status: unresolved exact range; no basis to upgrade title/abstract to full-hyperbola coverage.**

Outside input could help resolve these two full-text gaps. The independent-research policy prohibits external communication, and no outreach was prepared or initiated.

## Version check of the modern half-space comparator

The [Li–Souplet arXiv record](https://arxiv.org/abs/2408.17007) currently lists v1 **2024-08-30 04:40:04 UTC**, v2 **2025-06-05 15:09:25 UTC** (minor typo corrections). It explicitly retains boundedness on finite strips in v2. Search indexes may misleadingly show v2 in September 2024; the authoritative current arXiv history differs. Thus the parent audit should use the June 2025 v2 date and should not infer an arbitrary-growth theorem from the all-\(p,q\) range.

## Search coverage and evidence limits

Searches performed on the checkpoint date combined "Lane-Emden system"/"Lane–Emden conjecture" with 2025, 2026, universal estimates/bounds, a priori estimates/bounds, half-space, zero Dirichlet, full subcritical, higher dimensions, and all dimensions; searched each recent paper identifier/title and followed their accessible bibliography entries. Secondary indexes were used only to locate primary sources. Current OpenAI family 370/371 pages also appeared and are separately assigned to the parent audit; they are not counted as independent traditional literature here.

Other recent hits were scalar, fractional/mixed local-nonlocal, weighted graph, Neumann, free-boundary, planar-large-exponent, or least-energy work. Their subject mismatch prevented using them as exact comparators. A title/abstract mismatch is weaker evidence than checking theorem statements; no general absence claim is based on excluding these hits.

**Strongest verified conclusion:** the accessible exact statements above do not duplicate all three unrestricted project targets, and Li–Li–Wei materially strengthens the prior unconditional subset. **Exact remaining gap:** inaccessible Wang/Lu theorem statements; exhaustive citation/priority coverage is not certified. This scoped search is not proof of novelty. Even if the upstream full-entire theorem validates, the present targets should be framed as consequences of that theorem and established transfer machinery, with any genuinely new work isolated separately.

## Local evidence

Owned captures use `sources/priority_modern_*`: arXiv HTML and PDFs for the three principal exact-statement papers, HTML for Sciunzi–Vuono, and publisher preview HTML for Wang/Lu. PDFs were extracted with `/opt/homebrew/bin/pdftotext -layout`. A hash/URL manifest is `sources/priority_modern_manifest.json`. Captures are local review evidence; permission to redistribute third-party full text in a publication package is not asserted.
