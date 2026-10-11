# Independent audit of cofinite derivative zeros

## Verdict

**PASS for the complete frozen theorem.** The Gaussian construction proves that almost every sample of the planar Gaussian entire function is transcendental and that, for each nonempty open U, every sufficiently high derivative has a zero in U. Consequently, every infinite subsequence of derivative orders has a dense union of zero sets. There is no unresolved mathematical step in this argument and no required correction to the frozen candidate's proof.

The audited input has 10,609 bytes and SHA256

    26e9ffacf6c17ed325539cb627b41113d4c2f9f34004d32b097b295c2a90d29f

The input was read in full and was not changed. The standalone PROOF.md gives all details, including a factorial bound obtained by integration rather than Stirling, an explicit annular error, a common probability-one sample event, and precise hole-event measurability. These are explanatory expansions of a valid proof, not repairs of a false claim.

## Scope and source qualification

The literal database 2376 / EP-906 statement requires only a nonzero entire function. A nonzero polynomial answers that version immediately, because its sufficiently high derivatives vanish identically. The audit addresses the stronger transcendental version and does not conflate it with polynomial triviality.

The original Erdős PDF was independently downloaded and matched the frozen hash. Its rendered physical p.14, printed p.72, was inspected. The every-infinite-subsequence quantifier is present. The same page reports an older affirmative resolution. Note (1), printed p.79, lists four Barth–Schneider papers; the original source should therefore not be described as containing no references at all. Neither the candidate nor this audit relies on that historical assertion or establishes what each of the four older papers proves. [Original source](https://users.renyi.hu/~p_erdos/1982-33.pdf)

Almeida's entire five-page April 2026 manuscript was read, and its rendered p.3 was checked to confirm the absolute-value deviation inequality obscured by plain-text extraction. The PDF and README at commit d9aefa869577e6c0135dd994046a6b59b063733f were independently fetched. The PDF is byte-identical to the frozen source. It labels itself an AI-assisted draft offered for mathematical review. The covariance/expected-zero/hole-probability/Borel–Cantelli construction is already there. This audit confirms the candidate's explicit replacements for the two cited analytic estimates; it makes no priority claim. [Inspected manuscript](https://github.com/Drill23/erdos-problem-906-proposed-solution/blob/d9aefa869577e6c0135dd994046a6b59b063733f/paper/erdos_906_proposed_solution.pdf)

Primary-site search results for the public discussion corroborate Almeida's prior posting, Chojecki's later Gaussian-route post on 25 April 2026, and his clarification on 1 June. Direct current-page retrieval returned HTTP 403, so this audit does not certify the site's current maintained open/solved status. The historical forum record and manuscript dates suffice for attribution. [Discussion](https://www.erdosproblems.com/forum/thread/906)

Hou's frozen 12-page GitHub PDF was independently downloaded at commit 27e2206b984c3a0a284eb411a92eb18d5f097e6a and matched its pin. Its introduction, theorem, attribution, and source-status discussion were inspected. A later 10-page version exists: arXiv:2607.20816v5, revised 25 August 2026. Its PDF was downloaded and its first two pages were read and visually inspected. The older pinned GitHub PDF should not be described as the latest arXiv version. Both inspected versions credit the April Gaussian proposals. Hou's bounded-coefficient proof and separate Lean development are not dependencies and were not audited as complete proofs here. [Pinned GitHub version](https://github.com/erichou1/cofinite-derivative-zeros/blob/27e2206b984c3a0a284eb411a92eb18d5f097e6a/paper.pdf), [arXiv v5](https://arxiv.org/abs/2607.20816v5)

## Adversarial checks

1. **Derivative covariance.** The coefficient after n differentiations is sqrt((n+j)!)/j!, and the variance is sum (n+j)! r^(2j)/(j!)^2. Independent-variable Leibniz differentiation gives exactly n! exp(r^2)L_n(-r^2). The n! factor and the Laguerre argument sign are correct. Positivity K_n>=n! rules out degenerate point marginals.

2. **Uniform annular estimate.** The upper comparison with exp(2r sqrt(n)) is correct. The retained term k=floor(r sqrt(n)) lies in [1,n/2] for all sufficiently large n, uniformly on a fixed annulus. The product correction is bounded by b^2, and the factorial loss is only logarithmic. The standalone proof establishes a precise lower bound 2r sqrt(n)-4-2log(b sqrt(n))-b^2. No unproved uniform asymptotic or exceptional-radius assertion remains.

3. **Expected zero measure.** The normalization is correct: Delta log|g|=2pi times the zero measure, while E log|g|=(1/2)log K plus a spatial constant. This produces 1/(4pi) in the mean formula. The error is integrated against Delta phi. It is never differentiated. Compact support away from zero gives Delta|z|=1/|z|, with a strictly positive leading integral and no boundary term.

4. **Singular logarithms.** Each nonzero analytic sample has isolated zeros and locally integrable log modulus. E|log|Z|| is finite. Weighted Tonelli proves all expectation interchanges and measurability of the zero statistic. The Gaussian normalizer is not holomorphic, but no step applies a zero-count identity to that normalizer.

5. **Deviation centering and constants.** The apparently uncentered integral of log|Z_n| is exactly centered because integral Delta phi=0. Jensen against |Delta phi|/L and Tonelli give the uniform exponential moment bounded by E(|Z|+|Z|^(-1))=3sqrt(pi)/2<3. The complex Gaussian radial law is essential and is stated correctly. The resulting tail has exponent -2pi lambda/L. There is no hidden independence assumption.

6. **Hole reduction.** A zero-free disk forces the nonnegative smooth zero statistic to vanish. It is immaterial that a zero somewhere in the disk might lie outside the support of phi: only this one direction is used. L>0 and the leading coefficient A=integral phi/|z|>0. One can take mu_n>=A sqrt(n)/(4pi) eventually and obtain P(hole)<=3exp(-A sqrt(n)/(2L)).

7. **Summability and quantifiers.** The bound exp(-c sqrt(n)) is summable. First Borel–Cantelli needs no independence. Countably many rational disks avoiding zero suffice because every nonempty open set contains one. This family is technically a pi-base rather than a neighborhood base at zero; the candidate uses only the valid containment property. No uncountable intersection is made. The final equivalence with every infinite subsequence is deterministic and exact.

8. **Exceptional samples and measurable events.** One coefficient-tail event supplies entire convergence simultaneously on all compact sets. Intersecting the nonzero-coefficient events makes every derivative nonzero. A harmless exp(z) definition on the common null exceptional set gives a jointly measurable field everywhere. Hole events are complements of countable unions of zero-minimum events on compact subdisks, where each minimum is an infimum over a countable dense set. These details introduce no additional hypothesis.

## Reproducible bounded diagnostics

The authored verification script checks all frozen byte counts and hashes, independently retrieved copies of the three frozen PDFs, and the later arXiv PDF pin. It performs exact rational covariance-coefficient comparisons for n=0,...,30 and m=0,...,60 and finite numerical spot checks of the explicit Laguerre bounds. It also runs negative controls against changed bytes, truncated bytes, wrong byte counts, wrong digests, and a deliberately incorrect covariance normalization. No source-author code is executed.

The checks were rerun in normal Python and in both optimization modes, -O and -OO, with identical results. Each run passed 1,891 exact covariance comparisons, 70 numerical upper-bound comparisons, 40 numerical lower-bound comparisons, all eight input-pin checks, and all five negative controls. CHECK_SUMMARY.json records only aggregate verification metadata.

These diagnostics only check arithmetic instances and provenance. They are not a proof of an infinite theorem, a formal proof checker, or a substitute for the analysis in PROOF.md. The script uses explicit failures rather than Python assert statements, so optimization cannot erase its checks.

## Residuals and acceptance boundary

- Mathematical residual: none for the stated transcendental/cofinite existence theorem.
- Mandatory proof correction: none.
- Editorial refinement: distinguish the frozen 12-page Hou source from arXiv v5, and use “countable pi-base” if a technical topology label is desired.
- Attribution: retain Almeida and Chojecki, with Almeida's earlier posting acknowledged. The construction and main mechanism are prior work.
- Publication status: the inspected records establish proposed/preprint manuscripts. This audit does not establish journal acceptance, an official status change, or a prize decision.
- Exclusions: no deterministic sample formula, bounded-coefficient theorem, claimed finite-type bound, complete Hou audit, Lean certification, or adjudication of Boas–Reddy is part of this acceptance.

This packet contains only the authored proof, audit, acceptance report, and public verification metadata. Copied third-party documents, source extracts, page images, raw datasets, scripts, and private coordination material are excluded.
