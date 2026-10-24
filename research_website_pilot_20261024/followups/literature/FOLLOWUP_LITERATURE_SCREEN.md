# Follow-up screening: forest degree under graph powers

Prepared 2026-10-24. Completion: **100% of the bounded literature-screening assignment**, not 100% of a mathematical discovery. This is an AI-assisted research assessment, not human refereeing or a certification of worldwide openness.

## Recommendation

Retain **one priority question** and **one secondary program**. Neither should presently be advertised as a supported directional conjecture. Their resolution could have standalone value because they concern an operation on a broad class of graphs or an entire infinite sequence. Improving the published upper bound, calculating one further exponent, or repeating the same certificate with more branching parameters would not by itself meet that threshold.

Write

\[
D_F(X)=\mathbb E[\deg_{\mathrm{FUSF}(X)}(o)],\qquad a_k(G)=D_F(G^k),
\]

where graphs are infinite, connected, locally finite, simple, vertex-transitive, all conductances are one, and the simple power joins distinct vertices at distance at most \(k\). Keep this direct forest quantity separate from any unidentified nonunimodular \(L^2\)-invariant.

### Priority: determine whether a strict increase under squaring is possible

**Precise research question:** Does there exist such a graph \(G\) with

\[
D_F(G^2)>D_F(G)?
\]

Equivalently, is the universal nonincrease statement \(D_F(G^2)\le D_F(G)\) true? The published example settles only that equality can fail in the decreasing direction. It supplies no evidence for universal nonincrease.

**Why this would matter:** A general nonincrease theorem would replace the disproved invariance assertion by a substantial surviving law. A rigorous increasing example would establish that the sign of the power operation can go either way. Prefer a construction or theorem explaining the mechanism and yielding a class, rather than a numerical oddity. A single rigorous opposite-sign example still resolves the exact dichotomy, but its standalone publication value is an editorial assessment, not established by this search.

**Necessary exclusions:** A strict example must lie outside the common-transitive-unimodular-action case and must have \(D_F(G)>2\), by the established results below. Adding an arbitrary invariant collection of edges is not the same operation as taking the simple square. Weighted or directed examples do not settle the stated question. A nonunimodular subgroup of automorphisms alone does not establish that the graph's full automorphism group is nonunimodular.

**Success criterion:** Either a proof for the full stated class, with genuine control of the complete new root neighborhood, or an explicit increasing example with independently checkable lower and upper bounds in the required directions. An upper bound for the new graph alone cannot certify an increase. A proposed structural comparison that merely assumes the desired comparison of harmonic-projection traces has transferred the central difficulty and is blocked.

**Current status:** No primary source settling this exact sign question was authenticated in this bounded search. This is a reason to investigate, not a claim that the problem is globally open or newly formulated. Do not publish “Conjecture: squaring always decreases forest degree” based on the one counterexample.

### Secondary: determine the asymptotic behavior of the power sequence

**Precise general research question:** Must \(a_k(G)\) have a finite limit as \(k\to\infty\)? If not, produce a fixed transitive graph with a provably divergent or nonconvergent sequence. If yes, identify structural hypotheses that determine the limit in a nonconstant case.

**A concrete first target:** For the published binary grandparent graph, determine the limit of \(D_F(G^k)\), with a proof valid for all sufficiently large \(k\). The parallel mathematical screening observes that, on the underlying tree \(T\),

\[
T^{2k-1}\subseteq G^k\subseteq T^{2k}.
\]

The regular-tree powers have expected FUSF degree three. This makes a limit of three a natural *candidate to test*, but graph inclusion does not compare complete expected-degree sums, so the sandwich supplies neither convergence nor that value. A claim of convergence to two is equally unsupported. No directional limit conjecture is recommended at this stage.

**Why this would matter:** A structural limit theorem would explain what becomes of the nonunimodular discrepancy as the shortcut scale grows. A nonconvergent example would demonstrate persistent scale dependence beyond the single square comparison. A result for a substantial family, or a new asymptotic comparison method already effective on the binary example, is stronger than an exact evaluation of only \(G^2\).

**Exact gaps:** Each fixed power is locally finite, but their degrees need not be bounded uniformly in \(k\). The union over powers is not locally finite and cannot simply be substituted into the free-exhaustion definition. Monotonicity of an individual old-edge resistance does not control a sum over a growing neighborhood. Even a nonincrease theorem for squaring would only make the dyadic subsequence \(a_{2^j}\) nonincreasing; it does not establish convergence of the entire sequence. The bounds \(2\le a_k\le\deg(G^k)\) alone give no useful upper bound uniform in \(k\).

**Success criterion:** An all-scale proof or counterexample, including justified limiting operations and a mechanism that predicts more than a finite table. Finite certified calculations may falsify guessed monotonicity or identify candidate behavior; they cannot establish a limit.

## Established theory that removes tempting “open problems”

**Unimodular power invariance is already a consequence of the existing framework.** Gaboriau works with a closed transitive unimodular group \(H\); §2.1 constructs a full measured equivalence relation on \(H\backslash(X\times V)\), and Proposition 2.9 identifies its first Betti number with half the root harmonic-projection trace. Changing a connected \(H\)-invariant edge set on the same vertex set leaves this full relation unchanged. Combined with the forest projection identities, this gives \(D_F(G^k)=D_F(G)\) for every finite \(k\). This is a deduction from the cited framework, not a verbatim graph-power theorem and not a new result. Taking \(H=\operatorname{Aut}(G)\) covers unimodular transitive graphs. [Gaboriau, arXiv v3, §§2.1 and 2.4, Proposition 2.9](https://arxiv.org/pdf/math/0405458v3).

**The zero-excess regime is stable even without unimodularity.** BLPS Theorem 6.4 gives WUSF expected degree two on every transitive network. Theorems 7.3 and 7.8 identify equality of the forests with the absence of nonconstant harmonic Dirichlet functions and express their marginals by projections. Theorem 7.7, attributed to Soardi, preserves that absence under rough isometry of bounded-degree networks whose conductances and reciprocal conductances are bounded. Fixed graph powers satisfy these hypotheses. Consequently \(D_F(G)=2\) implies \(D_F(G^k)=2\) for every finite \(k\). Conversely, a graph with nonconstant harmonic Dirichlet functions has \(D_F(G^k)>2\) at every finite \(k\); this does not force a putative limit to exceed two. [BLPS, corrected author version, Theorems 6.4 and 7.3–7.8](https://rdlyons.pages.iu.edu/pdf/usf.pdf).

**Nonunimodularity does not force failure of equality.** Tang Proposition 5.3 proves FUSF=WUSF on Diestel–Leader graphs. Thus the nonunimodular cases \(DL(q,r)\), \(q\ne r\), already belong to the stable regime just described. Tang's grandparent results concern connectedness and branching, not the present power-degree asymptotic. [Tang, arXiv v2, §5.1 Proposition 5.3 and §5.2](https://arxiv.org/pdf/1908.09889v2).

**Connectivity is not a proxy for expected degree.** Pete–Timár explicitly distinguish the Cayley expected-degree invariant from their dependence of component count on the generating set. Their theorem cannot be repackaged as the proposed degree follow-up. [Pete–Timár, arXiv v2, introduction and Theorems 1.1–1.3](https://arxiv.org/pdf/2006.06387v2).

**Historical starting point.** Abért's 2010 Question 24 asks square invariance and explicitly notes the known Cayley case. It neither states a monotonicity conjecture nor answers questions about the full sequence. [Abért, Some questions, printed p.4](https://www.renyi.hu/~abert/questions.pdf).

## Structural-invariance route: screened but not shortlisted

A request to “characterize the nonunimodular graphs with power-invariant degree” is too broad to be a good immediate public conjecture. Equality may come from harmonic-Dirichlet vanishing, and nonunimodularity alone cannot separate equality from inequality. Restricting to \(D_F>2\) removes one known mechanism but does not itself suggest a correct equivalence or sufficient invariant. A useful future theorem would need an explicit, independently testable structural hypothesis giving all-power equality or a sign rule; stating the equality of the relevant projection traces as the hypothesis would be circular. No such hypothesis was identified here with adequate evidence.

## Search record and limitations

Checked on 24 October 2026: the released source and prior attribution report, the actual primary PDFs linked above, Gaboriau's full-relation construction and computation, BLPS §§6–7, Tang's introduction and §5, Pete–Timár's introduction, and the actual Abért question. Additional searches used combinations of “FUSF/free uniform spanning forest,” “graph powers/square/squaring,” “expected degree,” “nonunimodular,” “invariance/monotonicity,” and “harmonic Dirichlet rough isometry.” Four targeted arXiv-domain searches for power/sign combinations returned no results. Broad searches mostly returned the known literature or irrelevant finite-graph material.

The AMS endpoint for Soardi's original 1993 paper was inaccessible through the web tool; its precise theorem was inspected as BLPS Theorem 7.7. The large Lyons–Peres book endpoint exceeded the web fetch limit; no new full-book coverage is claimed. Final journal-body additions, unindexed theses and talks, different terminology, and unpublished results remain search gaps. Outside expert judgment could improve novelty and editorial assessment, but no outreach was prepared or initiated.

**Public-facing recommendation:** If a short future-work note is desired, say that the sign and long-term behavior under graph powers are natural research questions. Do not label unimodular invariance open, claim nonunimodularity forces change, assign a universal limiting value, or announce either new conjecture as literature-certified.
