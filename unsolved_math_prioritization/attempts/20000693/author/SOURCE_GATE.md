# Source and eligibility gate

Checked 2026-10-03 UTC. No author proof work occurred before this gate. The subsequent self-contained synthesis is counted as substantive turn 1, not hidden as source triage.

## Exact primary target

American Institute of Mathematics, *Moments of zeta and correlations of divisor sums*, §5, Problem 5.3, attributed to **C. Turnage-Butterbaugh**:

> Develop a heuristic for moments of imprimitive $L$-functions, or if your $L$-function factors into degree $1$ factors, e.g.
> $$\int |L(\tfrac12+it,\chi_1)\cdots L(\tfrac12+it,\chi_k)|^2\,dt$$
> (or different powers).

Primary URL: <http://aimpl.org/zetamoments/5/>. The HTTP page was retrieved directly and its embedded primary problem object inspected; HTTPS and web-tool fetches timed out. The source has no quantified exponent range, integration bounds, smoothing, modulus restrictions, growing-conductor limit, or demand for a proved asymptotic/all lower-order terms. These must be supplied openly in an actual heuristic. The source's unquantified parenthesis is not a requirement to handle all negative powers. The 2016 workshop context includes Conrey--Keating divisor correlations, but Problem 5.3 does not explicitly require that particular mechanism (contrast neighboring 5.1).

The source's phrase "imprimitive" can mean reducible products of primitive L-functions, while an imprimitive Dirichlet character also means deletion of finitely many Euler factors. Our formula covers both readings in fixed degree one.

## Dataset provenance

UnsolvedMath numeric ID 20000693, problem number AIM-ANALYTIC_NUMBER_THEORY-0057. Exact statement matches the primary object after whitespace normalization. Title "Multiplicity-sensitive moments of products of Dirichlet L-functions" is the imported descriptive title, not the original AIM wording.

Before fetching/restoring the approved fallback, the live repository manifest was read at `unsolved_math_prioritization/manifest.json` (Git blob 55589bae6bad2d3e2f696e08645330ff1219b709). It identifies dataset `ulamai/UnsolvedMath`, revision `37e53eabe540fb458758e198be61634bd02ee008`, and:

- problems.json: 68,931,837 bytes; SHA-256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`.
- research_results.json: 80,334,822 bytes; SHA-256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`.

The problems payload was fetched at the pinned revision and both its length and hash verified. The existing full research_results cache was rehashed to the published hash, then the exact problem-number record was selected. These imports have been read in full. They are third-party machine-generated aids, not user attempts or proof certificates. Dataset attribution: UnsolvedMath Contributors (2026), CC BY 4.0; underlying sources retain their own terms. AIM page footer identifies CC BY-SA 3.0.

## Live row and actual prior-user-work check

Live QUEUE blob `34888539d9c0163e100aac91942f827e0693932b` showed rank 423, queued, 0/5, impact 5.0, EV 0.1320. Catalog/state/assessment were fetched from main commit `d3d3b5537543f57968505232a6e2b2c8427e047d`. Catalog review hash is `488ff96b1a2ff002694935bc6a4f7bff7966127059d0dab01eb9e5e1dfad31b2`; statement hash is `7466e7057e14363e3f112bc119050821f0360d920d14495df1f4859171e23e9c`. There was no state entry, readiness hold, or related-target-group entry for this ID.

Repository root directories and the complete nontruncated attempts subtree (9,181 entries) had no path for this ID or Dirichlet/moment subject. All 440 branch names across five pages were checked; no matching target/topic branch was present. GitHub default-branch code search for the ID and all-state PR searches for ID, exact problem code, and L-function/moment terms found no relevant prior attempt. A broader Dirichlet/moments query returned only an unrelated SPDE PR 352. User-history retrieval found no relevant actual user work. This is a documented search result, not a claim that every historical file on every branch was exhaustively read. The imported report's "attempt 1" does not consume the user's turn budget.

## Prior coverage, and why turn 1 is appropriate

1. **Heap, 2013 preprint / 2021 publication.** *Moments of the Dedekind zeta function and other non-primitive L-functions*, <https://arxiv.org/abs/1303.6119>, journal DOI <https://doi.org/10.1017/S030500411900046X>. Introduction (18)--(24), Conjecture 4, and §7 (176)--(188) already give a constituent-wise moment heuristic. The primitive constituents are distinct Selberg-class functions, integer multiplicities are `e_j`, and the outer real parameter is `k`. The predicted exponent is `sum_j (e_j k)^2`. These are different roles, not interchangeable quantifiers. The journal publisher verifies publication online 15 November 2019, volume 170 (2021), pp. 191--219.
2. **Sahay, version 3 (2022).** *Moments of the Hurwitz zeta function on the critical line*, <https://arxiv.org/abs/2103.13542>. Definitions p.4; Theorem 1.3 pp.5--6 explicitly retains imprimitive Euler deletions; Conjectures 1.4 and 1.6 pp.7--8; conditional Theorem 1.7 p.8 gives the Euler-product/Barnes-G constant for every nonnegative integer tuple of characters modulo a fixed common q. Section 4, pp.17--18, gives the independent primitive-zero random-matrix heuristic. The text explicitly calls 1.7 a conjecture despite its theorem heading.
3. **Keating--Snaith (2000).** <https://people.maths.bris.ac.uk/~mancs/papers/RMTzeta.pdf>, formulas (6) and (10)--(12): real-power unitary characteristic-polynomial moments and Barnes-G asymptotics. This supports nonnegative real rather than only integer weights at the model level.
4. **Topacogullari (2019/2021).** <https://arxiv.org/abs/1909.11517>, proves two-factor asymptotics, useful normalization evidence. It is not a theorem for all multiplicities.
5. **Hagen (2026-09-10 preprint).** <https://arxiv.org/abs/2609.11619>, introduction and Theorems 1--2: distinct fixed GL(1)/GL(2) factors, positive real powers, sharp lower bounds generally and upper bounds in a restricted degree-weight range. This is current corroborating literature, not a proof of our conjectural leading constant. Related sharp conditional bounds: <https://arxiv.org/abs/2409.19780>.

Thus the central idea is already known. Heap alone does not literally spell out arbitrary different modulus-level characters with all their local factors, and Sahay's displayed general statement has a common modulus and integer weights. Rather than claiming a fully quantified prior theorem applies without qualification, turn 1 explicitly writes that adaptation and real-power heuristic. This is a credited synthesis, with no novelty claim. A demand for a proved general asymptotic would be a substantially different problem.

## Proposed disposition

A complete heuristic candidate for fixed arbitrary Dirichlet characters and fixed nonnegative real powers is frozen in HEURISTIC.md after **1/5** substantive turns. Independent audit must check scope, finite local factors, constants, branch conventions and the conjecture/theorem distinction. Until that audit, do not mark it verified or describe the asymptotic as proved.
