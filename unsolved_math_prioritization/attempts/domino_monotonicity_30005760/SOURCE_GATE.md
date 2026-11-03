# Row 1890 source and prior-work gate

Recovered on 21 October 2026: problem 30005760 / OWR-14298158-005, Inversion Monotonicity in the Domino Subclass. Ordered predecessor is row 1889, problem 30005097; successor is row 1891, problem 30000903. The recovered queue marks this row queued, 0/5. This stale label is not evidence of lifetime attempt count.

## Exact mathematical target and cautions

The original problem is Anders Claesson's item in Justin Troyka's Open Problems report, Oberwolfach Report 6/2024, printed pp.284–285 (DOI https://doi.org/10.4171/OWR/2024/6). The report asks whether fixed-inversion counts are weakly increasing as LENGTH increases by one. It is not monotonicity as the inversion count increases.

A literal ungridded interpretation is D = Av(1324) intersect Grid([Av(132) | Av(231)]), where the split is by position: some prefix avoids 132 and the remaining suffix avoids 231. For each k fixed, ask whether the number of length-n members of D with k inversions is at most the length-(n+1) number, for every n. Empty cells should be stated explicitly under ordinary grid-class convention.

The global Av(1324) condition is explicit in the original and must be restored to the curated statement. The PDF itself really prints 231, verified visually, so this is not an OCR error. The report does not explicitly say to count choices of gridding separately. A proof must declare the counting convention and must not silently replace the literal class by the standard domino ensemble.

The structural paper by Bevan, Brignall, Elvey Price and Pantone defines a vertical domino as a GRidded permutation with a 213-avoiding top cell and a 132-avoiding bottom cell, globally avoiding 1324. Its transpose uses 213, not 231, and distinguishes multiple grids of the same permutation. This mismatch is a source ambiguity, not permission to correct the source without qualification. Standard domino enumeration alone does not settle the literal ungridded 231 target.

## Primary literature checked

Claesson–Linusson–Ulfarsson–Verkama, arXiv:2604.01143v1 (1 April 2026), proves inversion monotonicity for {1324,231} and {1324,2314,3214,4213}, plus restricted-range results. Its extracted full text contains no domino occurrence; its introduction and final open-problem section do not identify a solution to this target. Results on a different avoidance class do not automatically transfer to D.

The structural paper arXiv:1711.10325v3 (10 May 2019) supplies domino definitions and enumeration, not the requested fixed-inversion injection.

Fresh search also located Robert Brignall's arXiv:2610.02535v1 (1 October 2026), claiming upper growth bound 13.167248 via shuffle automata, and Charles C. Norton's arXiv:2608.20292v3 (4 September 2026), claiming lower bound 10.412263. Abstracts and targeted full-text inspection do not establish the domino inversion target. Norton's v3 explicitly withdraws earlier larger bounds; do not quote obsolete v1/v2 claims. These are publicly posted manuscripts, not independently certified here.

Gil–Lopez–Weiner, A positional statistic for 1324-avoiding permutations, https://arxiv.org/abs/2311.18227v3 and https://doi.org/10.46298/dmtcs.12629, gives a related primitive/domino correspondence. Only its primary abstract and publication metadata were inspected in this gate; no claim that its positional statistic resolves inversion monotonicity.

No complete prior solution to the exact target was located. This is a bounded search result, not a global open-status or novelty certificate.

## Duplicates and prior repository work

The full local corpus has one exact target record, 30005760. Nearby 30005759 concerns full Av(1324) and Av(1324,231), not this domino restriction. Its cleaned displayed inequality mistakenly advances k rather than n; use the original report's length-monotonicity convention. No research_results.json entry keyed by OWR-14298158-005 and no full-text domino-subclass match were found.

All-state AlecKriebel/Math PR queries on 21 October 2026: 30005760, OWR-14298158-005, exact phrase inversion monotonicity, and 30005759 each returned no matches. Query domino returned only unrelated compact-alphabet PR https://github.com/AlecKriebel/Math/pull/462. Query 1324 returned unrelated issue-number match https://github.com/AlecKriebel/Math/pull/1324 and related but distinct diagonal-permuton problem 30005770 at https://github.com/AlecKriebel/Math/pull/1343. These bounded searches do not prove absence of unindexed or differently named work.

## Gate outcome

Proceed only with the explicit literal-class/global-avoidance/fixed-k/length-monotonicity specification, maintaining the standard-domino ambiguity as a separate scope. No mathematical investigation turn or lifetime count is assigned by this recovery. No queue edit, commit, push, PR mutation, external communication or publication was performed. Copied PDFs, text extractions and the dataset record remain private; only this authored gate and the source-metadata companion are publication candidates.
