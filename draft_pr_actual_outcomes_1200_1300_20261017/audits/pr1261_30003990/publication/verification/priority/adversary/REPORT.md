# Independent priority adversary: approximation-theory / general-theory family

PR1261 / problem30003990, 2026-10-17. Initial independent seal; no other new priority-family output was read. This is a bounded source-priority audit and a checkable mathematical implication, not a final-paper or publication-workflow review.

## Verdict

**No firstness or current-openness clearance. Strong classical mechanism overlap; no full matching printed theorem located in the inspected corpus.** There is a complete alternative proof of the target upper rate using older endpoint-polynomial theory, assembled in this audit in 2026. The available evidence does not justify backdating the full convex-body SOS theorem to a 2012 publication. It also does not justify promoting the quadratic proxy, classical kernel concentration, or shell/core mass comparison as new mechanisms.

The strongest positive result is `DERIVATION.md` B-C: a classical fast-decreasing endpoint polynomial, elementary Markov core control, and relative sublevel growth imply the full normalized Lebesgue global-SOS estimate, with one global square and a degree multiplier fixed in r. Section D independently checks the elementary finite-kernel alternative. The assumptions and all degree conversions are explicit. The remaining priority gap is documentary: no inspected older work explicitly states the final arbitrary-convex-body theorem, and unindexed or unread work remains possible.

## Exact target and source normalization

For a fixed compact convex body K in R^n with interior and fixed polynomial f, set

    H_r=inf{integral_K f q dx : q global SOS, deg(q)<=2r,
                              integral_K q dx=1}.

The claim is 0<=H_r-min_K f<=C_(K,f)/r^2 for all integers r>=1. It is an existence/rate result. It does not assert an efficient minimizer algorithm, arbitrary-reference-measure rate, unrestricted composition s(f), or positive Theta rate for each f.

The [OWR contribution](https://ems.press/journals/owr/articles/16633), printed pp.2991-2993, asks about the general-convex-body regime. The two displayed density constraints omit the value of the mass even in the rendered PDF. The probability formulation and [arXiv:1905.08142v2 Eq.(3)](https://arxiv.org/pdf/1905.08142v2) support the explicitly restored unit-mass convention. This is a scope repair, not an OCR correction.

## Material expansion beyond the old audit

The decisive additional source reading was the distinction between interval doubling and doubling centered only on a set in [Totik-Varga 2012](https://doi.org/10.1016/j.jmaa.2012.03.006). In the latter case, singleton {0} is permitted. The candidate's cumulative inequality therefore meets an actual older endpoint-Christoffel upper-bound hypothesis. The older construction, rather than the bare norm bound, yields the normalized moment consequence after the additional proof in `DERIVATION.md`.

The old endpoint zero-spacing route still needs stronger interval assumptions. It cannot be invoked just by renaming one-ended cumulative growth as interval doubling. `DERIVATION.md` F supplies an absolutely continuous, full-support counterexample to that generic implication. This counterexample is not claimed to arise from a convex-body proxy.

The final 2012 [Totik survey](https://doi.org/10.1090/conm/578/11471) contains a concrete shell proof comparing polynomial norm tails to the mass of a small core. This substantially overlaps the cancellation pattern. The candidate's explicit finite trigonometric polynomial and its dimension-dependent fixed power are not identified with every Jackson kernel in the literature; the point is classical concentration and relative mass control, not an unsupported identity of formulas.

Additional primary expansions include the 2018 simulated-annealing paper's explicit quadratic proxy proof; the 2020 publisher-formatted worst-case paper and its interval sharpness proof; the 2022/2023 polynomial-kernel construction framework; and a current 2025-online/2026-issue paper on homogeneous Christoffel functions for symmetric convex bodies. Their exact scope and remaining gaps are in `CLAIM_COMPARISON.md`.

## How far the older theory reaches

The 2026 deduction uses the following genuine implication, rather than an equivalent endpoint claim left unsupported:

1. An older endpoint concentration theorem supplies degree-m polynomials uniformly bounded by 2 and decreasing faster than every fixed power away from scale m^-2.
2. Classical Markov derivative control gives a positive core of width proportional to m^-2.
3. The pushforward sublevel distribution satisfies F(t)<=(t/s)^n F(s), by a homothety of the original convex body about a minimizer of the quadratic upper proxy.
4. Each first-moment tail shell is bounded by that same F(h), times a summable fixed sequence. Dividing by core mass cancels F(h).
5. Composing with a quadratic costs a factor two in square-root degree. Squaring gives a global SOS density; m=floor(r/2) fits the target order. Small r uses the constant density.

The proof imports the precise published endpoint theorem and the standard Markov inequality. The endpoint theorem's complete printed proof was read, but its cited 1990 symmetric premise could not be read in the missing original body. The direct finite-kernel proof independently bypasses that premise. Thus no unsupported “general endpoint result” is being used to hide the central difficulty.

The result should be described, if used, as a direct proof or a consequence of classical approximation ingredients with the exact convex-volume argument supplied. The evidence here does not determine the novelty of that complete consequence. It does establish that novelty must not be attributed to the proxy or the broad concentration/shell mechanism.

## Specific close comparisons

- [Slot-Laurent, arXiv:1905.08142v2](https://arxiv.org/abs/1905.08142), Theorem 11, states the same general-body hierarchy with O(log^2(r)/r^2). Its proof's final normalization/tail step was inspected. That weaker printed result is evidence of its own scope, not proof of current openness.
- The original-objective pushforward paper [arXiv:2001.11289v2](https://arxiv.org/abs/2001.11289) analyzes s(f). The new density is built from s(g), where g is the quadratic proxy. The unrestricted theorem does not automatically remove the logarithm in the former hierarchy for arbitrary nonconvex f.
- [de Klerk-Hess-Laurent 2017](https://doi.org/10.1137/16M1065264) uses the cube, product Chebyshev measure and a weighted preordering cone. [de Klerk-Laurent 2020](https://doi.org/10.1287/moor.2018.0983) supplies ordinary-SOS cube results and the classical Lebesgue-interval linear-objective sharpness example. Neither inspected general statement is T.
- [Gribling-de Klerk-Vera, arXiv:2605.31496v1](https://arxiv.org/abs/2605.31496) gives a constructive ordinary-SOS upper bound on the Chebyshev cube in Proposition 14. Its complete printed proof was read and credited in that scope. Its coefficient/lower-hierarchy log^3 estimate is a different claim. No same-scope full-target preprint was located; dates alone establish no disclosure lineage.
- The [final 2026 overview](https://doi.org/10.1007/978-981-95-1446-5_8), Table 1 printed p.159, still lists the logarithmic general-body rate. It cannot certify present firstness or openness.

The interval lower example is existing mathematics. Together with T it clarifies optimal worst-case exponent over the full class, while constants and many objectives may have faster convergence. Constant objectives have zero error.

## Search, body reading, and omissions

`QUERY_LEDGER.json` records 19 actual search calls containing 76 literal query strings. Queries cover exact hierarchy/rate phrases, endpoint Christoffel and zero-spacing theory, one-sided doubling, classical and multivariate kernels, arXiv/current work, Zenodo and EulerSolve. Some searches returned unrelated hits; those calls are retained rather than silently upgraded into useful coverage. `BODY_READ_LEDGER.json` separately records web open/find/click invocations. Download receipts and `SOURCE_INVENTORY.json` separately give primary payload bytes, hashes, versions and honest reading scopes.

The EulerSolve index captured on 2026-10-17 contained no “Lasserre” or “16633” match in the inspected text; its source-ID route probe returned 404. This is bounded retrieval evidence only. It does not show absence from every hosted paper, alternate route, later index, Zenodo record, private circulation, or the wider literature.

Missing full bodies include Ivanov-Totik 1990, Mastroianni-Totik 2010, and Kroo 2016. An attempted 2023 journal-version kernel URL returned non-PDF HTML; its arXiv v1 pp.1-3 were obtained and read. A guessed nonexistent arXiv v2 and a DOI typo were corrected using primary metadata, with both failures preserved. No body is claimed read from an abstract or search snippet. No whole work's entire proof collection is certified.

## Integrity and next boundary

All authored outputs belong to this family root. Retained primary copies, renders and raw tool results are ignored under `_local/`; their separate inventory is not an authored finding. No source-author code was executed. Only audit-authored retrieval, extraction and inventory programs ran. No external contact or publication/account/repository mutation occurred. The requested material-status report to the supervising root agent did not share another family's findings with this family.

`BIBLIOGRAPHY_QA.md` distinguishes online, arXiv and issue dates, corrected DOI/page errors, and publisher versus preprint theorem numbering. The independent audit is ready for a later reverse cross-challenge after both initial families are sealed. No cross-challenge is claimed complete here.
