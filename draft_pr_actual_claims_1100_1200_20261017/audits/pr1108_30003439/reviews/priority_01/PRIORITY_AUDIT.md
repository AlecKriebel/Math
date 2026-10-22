# Bounded independent priority audit — PR #1108

Completed: 2026-10-17 17:23:43 UTC. Bounded-audit completion estimate: 100%. Worldwide priority/novelty coverage remains unquantified.

**Disposition: no priority-blocking predecessor or direct existing-theorem implication identified in the inspected primary sources.** This is a bounded source finding, not a certification of novelty, worldwide priority, or present-day openness. The manuscript already disclaims novelty and priority. Preserve that restraint; add Roy–Xiao's explicit prior self-concordant barrier on the same cone family to the credit discussion.

## Exact audited claim

The pinned `input/PROOF.md` has SHA256 `9577476ee2c0fd2e3d12ab1265201d8b99f6ef50a9060e245c46f872dd673302`. The target is Tunçel's existential question on printed p. 799 of [OWR 14/2017](https://www.math.uwaterloo.ca/~ltuncel/publications/OWR-2017-14.pdf): an algebraic regular convex cone admitting a normal barrier with directional third-derivative negative curvature, although the cone is not a polynomial hyperbolicity cone in its original space.

The submitted example is

\[
K=\{(x,y,z)\ge0:xy^2\ge z^3\},\qquad
F=-25\log(xy^2-z^3)-25\log z.
\]

The claimed parameter is 100, and the sign condition is universal in base point, cone direction, and test vector: \(D^3F(a)[h,u,u]\le0\) for \(a\in\operatorname{int}K,h\in K,u\in\mathbb R^3\). Exclusion concerns every homogeneous hyperbolic defining polynomial in \(\mathbb R^3\), not merely the displayed cubic. This review addresses scholarly dependencies and priority only; independent mathematical reviewers own the proof-verification conclusion.

## Strongest prior overlap and required credit

[Hildebrand's Theorem 3.2, family 5](https://arxiv.org/html/1305.4814) already contains exactly this cone, at \(p=3,q=3/2\) with \((x_1,x_2,x_3)=(x,z,y)\). The manuscript's cone credit is correct. His hyperbolic affine spheres use a different meaning of hyperbolic; the family listing does not imply real-rootedness of a defining polynomial, nor the required third-derivative sign.

A closer additional predecessor is [Roy–Xiao, January 30, 2018, Theorem 2, PDF p. 3](https://optimization-online.org/wp-content/uploads/2018/01/6441.pdf). Put \(m=x^{1/3}y^{2/3}\). Their result supplies the parameter-3 LHSCB

\[
B=-\log(m-z)-\tfrac23\log x-\tfrac13\log y-\log z
\]

on exactly \(K\). The entire nine-page paper was inspected. Its theorem and proof establish self-concordance, not the mixed cone-direction negative-curvature property. Its other main theorem concerns the sign-symmetric generalized power cone. Thus neither the cone nor existence of an explicit LHSCB on it should be presented as new.

[Nesterov 2006/30, §4 example 3, (4.8)](https://optimization-online.org/wp-content/uploads/2006/04/1358.pdf) already gives

\[
H=-\log(m-z)-\log x-\log y
\]

on the unrestricted geometric-mean hypograph \(z\le m\), with parameter 3. Adding \(-\log z\) gives a parameter-4 LHSCB on \(K\). [Chares' 2009 thesis, Remark 3.1.2, printed pp. 92–93](https://research.dial.uclouvain.be/bitstreams/3cee3b2d-84f2-4b1c-b8f9-68c15b654a07/download) explicitly repeats that construction and credits Nesterov. These are prior self-concordant-barrier constructions. Their compatibility estimates do not assert the missing mixed sign condition.

## The direct-consequence challenge

The relevant added property is the universal cone-direction third-derivative sign for the submitted barrier. It is not supplied by logarithmic homogeneity, positive Hessian, boundary blow-up, or scalar/mixed self-concordance bounds.

There is an exact comparison with the closest prior barrier. Write \(f=F/25\) and \(t=z/m\in(0,1)\). Then

\[
f=B-\log y-\log(1+t+t^2).
\]

This is not an addition-of-convex-barriers argument: for the remainder \(R=-\log y-\log(1+t+t^2)\),

\[
R_{xx}(1,1,1/2)=-110/441<0.
\]

The exact arithmetic is independently recorded in `remainder_check.txt`. It only rejects this naive additive route, not every conceivable alternative representation. More decisively, the inspected sources do not first establish negative curvature of \(B\) or \(H\), so the known curvature-preserving sum rule cannot be invoked on them.

[Nesterov–Tunçel §9.2](https://arxiv.org/html/1412.1857) preserves negative curvature under direct products, intersections, linear pullbacks and linear restrictions. Starting only with polynomial hyperbolicity cones, these operations remain in the hyperbolicity-cone class whenever the ordinary full-dimensional/interior hypotheses hold: products multiply hyperbolic polynomials, and pullbacks/restrictions compose with linear maps. They therefore do not directly manufacture the required nonhyperbolic cone. The same paper's nonnegative-polynomial example puts its log-det curvature barrier on the dual Hankel spectrahedron; its primal log-det construction is lifted. Neither dualization nor projection is a licensed curvature-preserving shortcut here.

[Dahl–Andersen §5](https://link.springer.com/article/10.1007/s10107-021-01631-4) gives an explicit exponential-cone LHSCB counterexample to negative curvature. It reinforces the distinction between self-concordance and the target's extra sign property; it is not an algebraic-cone solution. Canonical/universal-barrier existence and affine-sphere constructions likewise do not establish that extra sign merely by furnishing an LHSCB. No inspected primary theorem was found that turns these older constructions into the target's answer without a further substantive curvature proof.

## Current sources and representation identity

Fresh retrieval confirms the [DTV arXiv version record](https://arxiv.org/abs/2509.10263) lists v2 as June 12, 2026. The [arXiv v2 PDF](https://arxiv.org/pdf/2509.10263v2) and [Waterloo PDF](https://www.math.uwaterloo.ca/~ltuncel/publications/2509.10263.pdf) are byte-identical: 700527 bytes, SHA256 `df11c946ad11073881ad5274a08edc3f25f4f1cbb153a5c36388d24ea717ad76`. Both internally say revised June 16, 2026.

The separately retrieved [v2 HTML](https://arxiv.org/html/2509.10263v2) internally says revised August 24, 2026. This discrepancy is real in the fetched representations; its cause was not established. Keep the PDF and HTML identities separate. The existing manuscript accurately describes its inspected June 16 PDF and should not retroactively be relabeled as an August edition.

Both inspected representations retain a broader concluding question about whether every convex cone admits an LHSCB with negative curvature. That does not establish that the narrower 2017 existential question is currently open. Conversely, answering the present existential question does not answer their universal question.

## Suggested manuscript wording

“The cone belongs to Hildebrand's pre-existing family 5. Explicit self-concordant barriers for the same nonnegative power-cone family are also known, including Roy and Xiao's parameter-3 barrier (Theorem 2). The present proof directly certifies the additional cone-direction negative-curvature property for the displayed polynomial-logarithm barrier and excludes every homogeneous hyperbolic defining polynomial in the original space. No novelty or priority claim is made.”

Add the Roy–Xiao reference. Nesterov/Chares can be mentioned if space permits. This is a credit improvement, not a mathematical correction to the submitted proof.

## Limits and reproducible audit artifacts

The exact queries, primary-source locators, retrieval hashes and checkpoint estimates are recorded in `SEARCH_LEDGER.md`, `SOURCE_LEDGER.json`, `SOURCE_LEDGER.md`, the three retrieval JSON files, and `RESEARCH_LOG.md`. Full PDFs, page images, and copied full texts were deliberately not retained. The Hildebrand habilitation URL returned 404. His 2026 “Three Different Views” publisher record and bibliography were checked, but its subscription version of record was not read. The related OpenReview prepublication endpoint returned HTTP 403 to ordinary retrieval and redirected web.open to browser verification; indexed snippets were not treated as inspected full text. The one-page ICOMP 2024 institutional poster was retrieved and fully inspected in memory: it treats canonical barriers, self-concordance and geometric equivalences, with no negative-curvature claim. These three representations remain distinct. Güler 1997 and Hildebrand 2014 canonical-barrier sources were checked at publisher-record/abstract level and through inspected downstream originals. These are explicit coverage limits, not claims that the inaccessible works contain no relevant result.

The strongest defensible conclusion is: **the exact additional curvature certificate and same-space nonhyperbolicity answer were not found as a prior theorem or direct consequence within this bounded primary-source audit.** The exact remaining historical gap is worldwide literature coverage, including inaccessible and unindexed sources. No contact or outreach was initiated; no PR, release, commit or push was performed.
