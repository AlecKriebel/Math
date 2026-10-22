# PR1131 / 30005455: independent priority audit

Audit date: 21 October 2026 UTC. Development cutoff: the pinned commit, 10 October 2026 11:04:21 UTC. Head: `bacae693a1f2a33c89565b0bd716620885831289`; base: `f6caddda8f8be2cdb3e91494325d8f7f365bc3fc`. All eight actual added files were read from Git objects; their exact identities are in PINNED_SCOPE.json.

## Assessment

**No blocking prior theorem for the two substantive improved bounds was recovered in this bounded audit. This is not an exhaustive novelty or priority certificate.** The potential new core is the arbitrary-weight, arbitrary-positive-rate odd-cycle exclusion and consequent universal forest bound `alpha > 4/3`, together with the universal equal-rate whisker bound `alpha >= 17/4`. Correctness of those arguments is subject to the separate mathematical audits.

There is substantial positive prior overlap. The uniform odd-cycle spectral threshold, the triangle obstruction, the even-cycle perturbation mechanism, the finite stochastic convergence/support bridge, and the least-weight/champion method predate this PR. Moreover, the 2017 whisker proof already implies an elementary strict improvement of 25, for example to **alpha > 24**; a complete bridge is given below. Thus a claim that *no improvement whatsoever* followed from prior literature would be false. This weaker consequence does not supply the PR's `17/4` bound or improve the arbitrary-rate forest threshold below 2.

| Claim | Strongest verified earlier overlap | Remaining difference in this PR |
|---|---|---|
| Arbitrary-rate finite forest for alpha > 4/3 | HK2017 Theorem 3 / Corollary 1: >2 | No prior universal improvement below 2 recovered |
| Odd m-cycle exclusion at sec^2(pi/(2m)), including unequal weights/rates and attachments | VHHKR2016 Proposition 2(iv): stability threshold for the uniform equilibrium on the bare equal-rate cycle | The weighted, attached, arbitrary-equilibrium extension was not recovered |
| Even cycle exclusion for alpha >1 | HHK2023 Lemma 2, with the same alternating perturbation in power coordinates | Unequal rates require no new cancellation mechanism; see below |
| Equal-rate whiskers for alpha >=17/4 | HK2017 stated >25; its proof plus HHK2023 implies >24 | No earlier universal 17/4 or stronger bound recovered |
| Triangle sharp lower obstruction | VHHKR2016 Proposition 2(v), Theorem 4(ii); original problem statement | Known, not new |
| Stable long paths at unequal rates | HK2017 Example 1 | PR's rational example is a scope control, not a new phenomenon |

## Exact target and scope

The primary [OWR report](https://ems.press/content/serial-article-files/47008), Kleptsyn's contribution, printed pp.653-655, asks for improvements of the finite forest threshold 2 and, with equal firing rates, the whisker threshold 25. The subsequent suggestion that 4/3 might be sharp does not change the literal improvement requests. The PR's two bounds answer both literal requests if correct and within the intended model. Its description as leaving a sharper interval open is mathematically informative but does not itself make these literal requests unanswered.

The model comparison uses finite simple undirected loopless graphs; positive rates; power reinforcement; and positive integer initial tallies. The PR states unit tallies. Almost-sure support claims from unit tallies extend to any fixed positive integer vector by a finite-path conditioning argument: from unit tallies there is positive probability of realizing any prescribed finite sequence of edge reinforcements leading to that vector; a positive conditional failure probability afterward would contradict the unit-state almost-sure theorem. Finite shifts do not change limiting weights or infinite reinforcement. This argument does not assert an extension to arbitrary positive real offsets. Loops and multigraphs are outside the PR's explicit scope.

Root's mandatory tracker check at 23:11:48 UTC, preceding this audit, is reported as 180 rows with zero exact-ID, alias, WARM or whisker leads. This audit does not independently certify account state or edit a ledger. The 2025 [MATRIX chapter publisher record](https://link.springer.com/chapter/10.1007/978-3-031-76738-8_29) confirms first online 3 July 2025. The [hosted author manuscript](https://www.matrix-inst.org.au/wp_Matrix2016/wp-content/uploads/2023/Aletti.pdf), pp.8-11, repeats the requests as Problems 12 and 13. Its still-future citation to the 2023 paper warns that this is not a continuously maintained status page. A secondary index's 2026 date must not replace the publisher's 2025 date.

## Positive prior mechanisms

In [VHHKR2016](https://pure.tue.nl/ws/portalfiles/portal/46706436/hofsstro2016.pdf), Proposition 2(iv) and its proof on printed pp.2500 and 2515 give the equal-rate uniform-cycle spectrum and odd threshold `sec^2(pi/(2m))`. This is a statement about one equilibrium. It does not exclude all nonuniform equilibria on an odd cycle with chords, attachments or nonconstant rates. Theorem 4(ii) addresses the triangle. Equating these with the PR's arbitrary-cycle theorem would leave exactly its central gap unsupported.

In [HHK2023](https://pure.au.dk/ws/portalfiles/portal/418609000/Hirsch_2023_Nonlinearity_36_3013.pdf), Lemma 2 on printed p.3036 already excludes fully supported equilibria containing an even cycle. Its proof sets `y_e=x_e^alpha`, adds alternating increments around the cycle, and keeps all vertex sums of y constant. Other edges remain fixed, so chords and attachments are already harmless. The lemma appears in the equal-rate section and contains an unexplained printed `delta=1`; it should not be silently quoted as a formally stated arbitrary-rate theorem. Nevertheless its exact proof extends immediately: replace equal logarithmic coefficients by the positive vertex-rate coefficients. Every logarithmic term is still constant, and strict concavity of `y^(1/alpha)` still gives the same instability. Thus the arbitrary-rate even-cycle mechanism is an elementary consequence of the earlier proof, not an independent new mechanism.

The distinction for the odd-cycle argument is concrete. The PR controls weighted coefficients by `4 sum c_v <= sum D_e`, then averages the two real Fourier directions. Neither the earlier uniform-cycle spectrum nor the alternating even-cycle cancellation alone gives that inequality for arbitrary equilibria. No inspected primary source supplied this odd-cycle bridge.

## A fully checkable earlier strict whisker improvement

This section records a consequence of [HK2017](https://researchers.ms.unimelb.edu.au/~mholmes1@unimelb/Reinforced-graphs_final.pdf), Section 5.1, pp.21-24; it is not presented as a newly published theorem. The paper's Lemma 6 proof explicitly displays the sufficient cutoff `(9/4)(exp(9/4)+1)`, about 23.6. Its other required constants are smaller. To avoid depending on decimal rounding, the following exact argument gives the weaker but sufficient cutoff 24.

Use equal rates normalized to 1. Put `c=9/4`, `a_e=q+r`, where q and r are the selection probabilities at the two endpoints. The published least-weight argument gives `a_e >=1` for any non-linearly-unstable equilibrium when alpha>2. Its diagonal condition gives

`alpha [q(1-q)+r(1-r)] <= a_e <=2`.

Thus each endpoint probability is either at most `(1-sqrt(1-8/alpha))/2` or at least its complement. For alpha>81/4, the former is strictly less than `c/alpha`: square the positive terms in `sqrt(1-8/alpha)>1-(2c)/alpha`. Since `a_e>=1`, both probabilities cannot be small. Consequently every positive edge has weight in

`[1,1+c/alpha) union (2-2c/alpha,2]`.

If a small edge has weight below `1+c/alpha`, one endpoint has probability greater than `1-c/alpha`. If that endpoint had a competing positive edge, the competitor has weight at least 1, so the first edge's probability is strictly less than

`exp(c)/(exp(c)+1)`.

These statements contradict one another whenever `alpha>c(exp(c)+1)`. Here is an exact rational bound for that cutoff. For `x=9/4`, the exponential sum through degree 12 plus a geometric upper bound for the tail is

`U = sum_{k=0}^{12} x^k/k! + (x^13/13!)/(1-x/14)`

`  = 191714244173193067 / 20206532637491200 < 19/2`.

Indeed consecutive ratios from the first tail term onward are at most `x/14`. The positive difference `(19/2)-U` is `247815882973333 / 20206532637491200`. Hence

`c(exp(c)+1) < (9/4)(21/2) =189/8 <24`.

For alpha>24 every small edge therefore has a leaf endpoint. Every large edge has weight greater than `2-(9/2)/24 =29/16 >3/2`. Two such edges cannot share a vertex: each would need endpoint probability above 1/2 there, because its other endpoint contributes at most 1. Large edges form a matching; all other edges have a leaf endpoint. Every connected component is consequently a star or a double star, hence a whisker. This is the same structural conclusion from the source's three lemmas, with sufficient constants made explicit.

Finally HHK2023 Theorem 1, printed p.3016, gives finite almost-sure convergence to stable/critical equilibria, and Proposition 1, printed p.3021, identifies infinite reinforcement with positive asymptotic growth. Their hypotheses hold for the finite equal-rate model. Thus **alpha>24 already implies almost-sure whisker support by an elementary combination of pre-PR literature**. This answers a purely literal request for *some* numerical improvement of 25, while leaving the much stronger 17/4 assertion unaccounted for. The offline verifier checks the rational exponential certificate; the structural argument is displayed here for human checking.

## Later and adjacent leads checked

The searches covered current author publication pages, arXiv versions, HAL, OpenAlex author inventories and citation chains, Crossref, exact IDs, bound variants, interacting urns, graph-based competition, hypergraph urns, and the older Friends-II terminology. SEARCH_LOG.json gives query families, discovery results and failure limits. These services are discovery aids, not proof sources. Specific leads were followed into primary text where they could plausibly matter.

- HHK's [regular-tree preprint](https://arxiv.org/abs/2009.07682), first submitted 16 September 2020 and still called a preprint on the current author pages, constructs infinite components with suitable nonconstant rates. It is not a finite universal forest/whisker improvement. The PDF retrieved under the unversioned URL visibly says November 2021 despite the arXiv v1 submission label; the two dates are recorded without assuming a new arXiv version.
- [Absence of WARM percolation](https://pure.rug.nl/ws/portalfiles/portal/672248545/20_AAP1587.pdf), published AAP 2021, Corollary 1 retains `max(alpha_0,2)` and `max(alpha_0,25)` under its additional infinite-graph hypotheses. It does not lower the finite universal thresholds.
- [Alves-Barros-Lima](https://arxiv.org/abs/2310.00159), v1 September 2023, v2 May 2025, published Nonlinearity 38 (2025), 075004, explicitly restricts its hypergraph model to **alpha=1**. Theorems 1.1-1.2 concern incidence-matrix injectivity and convergence there. Hypergraph duality does not change alpha=1 into a theorem for alpha>1.
- [Ruszel-Thacker](https://arxiv.org/abs/2201.12603), January 2022 preprint of a 2024 Journal of Theoretical Probability paper, treats one global nonlinear allocation among d bins with a time-dependent number of additions. Its fixation theorem does not apply independently at WARM vertices, whose edge counts are shared and reinforced from both ends.
- [Costa-Jordan](https://arxiv.org/pdf/2006.02685), [Kaur-Sahasrabudhe](https://arxiv.org/abs/1905.10738), and [Laruelle-Pages](https://arxiv.org/abs/1311.7367) use different interaction or replacement rules. The primary model equations reviewed do not provide the vertex-local sum of ratios needed here. [BBCL's hypergraph variant](https://arxiv.org/abs/1211.1247), Section 9.2, is linear; general nonlinear convergence machinery supplies no structural threshold by itself.
- [Planar reinforced k-out percolation](https://arxiv.org/abs/2407.12484), 2024 preprint / 2025 publication, reinforces k-tuples in rounds and studies percolation on the infinite square lattice, principally k=2. Its main results do not classify all finite WARM supports at the requested bounds.
- [Basu-Benaim 1606.04569](https://arxiv.org/abs/1606.04569) was explicitly withdrawn on 23 June 2016 for technical errors. Its historical v1 was inspected for structural leads; its claims address convergence and generic stability, not the new bounds. It is not valid evidence that a stronger universal result is already established.
- The public [warmlab repository](https://github.com/davidc789/warmlab) describes MSc simulation utilities. Its current repository tree contains no thesis or claimed structural theorem. It is not a priority-positive proof source; an unlocated thesis remains an ordinary coverage limit.

## Provider and local preparation check

The specific proposed EulerSolve alias URL `https://eulersolve.org/papers/owr-12697708-008/` returned HTTP 404 at 23:20:31 UTC. Fresh successful captures of the provider's root, papers index, root sitemap, papers sitemap and papers feed contained no case-insensitive match for `12697708`, `30005455`, `WARM`, or `whisker`. The papers index exposed 374 distinct paper slugs, including other OWR aliases. No actual theorem, author, DOI, or earlier date for this alias was recovered. A 404 and an index miss do not prove the absence of removed, differently titled or unindexed material. No provider mutation or DOI operation occurred.

Existing local PR body/metadata were inspected read-only. They describe this exact head and disclaim novelty. Historical labels and old unsuccessful searches were not used as evidence that the target was only partial or that the new bounds are original. The fresh primary statement controls the literal scope.

## Decision boundaries and remaining limits

The warranted outcome is **bounded no-priority-blocker-found for the substantive odd-cycle/forest and 17/4 improvements, with mandatory credit for known subresults**. A stronger declaration that nobody previously proved them is unsupported. No inspected theorem plus a complete bridge produced either the arbitrary-rate universal forest bound below 2 or the equal-rate universal whisker bound as low as 17/4.

Before promotion, credit HHK2023 Lemma 2 explicitly for the even-cycle method and VHHKR2016 Proposition 2(iv) for the uniform odd-cycle threshold, in addition to the references already present. Describe 25 as the earlier **stated** bound, while acknowledging that its published proof admits the small elementary sharpening above. These refinements leave the potential new contribution clear. No mathematical correctness verdict, publication authorization, ledger repair, release, DOI, outreach, or exhaustive world-absence claim is made by this audit.

Only authored analysis, metadata and a new read-only offline verifier are in this public folder. Third-party PDFs, extracted text, images, raw queries, captured manuscript files, and operational receipts remain in the separate private folder. The verifier establishes package integrity and exact internal checks; it cannot verify literature absence or independently authenticate remote history.
