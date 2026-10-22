# Independent priority audit: separator and covariance route

Audit date: 2026-10-17 UTC. Target: the exact two-real-polynomial Boolean-cube question on p.445 of [Oberwolfach Report 9/2025](https://doi.org/10.4171/owr/2025/9), with relative influences normalized by the full squared Fourier norm, including the constant coefficient. This audit asks whether an earlier primary source records the complete target resolution. It does not certify novelty from unsuccessful searches.

## Bounded conclusion

**No inspected primary source was found that states the complete target-specific inverse-polynomial overlap theorem.** This is a bounded search finding, not an absence theorem. The decisive separator and the precise covariance inequality are both prior results. In particular, the covariance lemma in the local proof can be credited directly to OSSS2005 §3.3, equation (6), rather than presented as an inequality whose literature status is unknown.

The exact local theorem is a checkable consequence of those prior ingredients. The complete ingredient portfolio was publicly available by 4 August 2026; this is an implication date, not evidence that anyone had then recorded the target-specific deduction. The classification supported here is **a target-specific corollary/deduction from known structural results, with priority unresolved**. It would be inaccurate to classify the broad separator theorem or the arbitrary-real covariance inequality as new. It would also be inaccurate to claim that the August cryptographic paper explicitly announced resolution of this precise Oberwolfach question: its complete body does not contain that announcement or the relative-influence deduction.

## Chronology and theorem comparison

| Primary source | Version/date and exact locator | Relevant content and limit |
|---|---|---|
| O'Donnell–Saks–Schramm–Servedio, [Every decision tree has an influential variable](https://arxiv.org/abs/cs/0508071v1) | v1, 16 Aug 2005, §3.3 Eq.(6), physical PDF p.8; resampling influence defined p.6 | For a tree computing a function into [-1,1], covariance with an arbitrary real function is bounded by revealments times its expected absolute resampling differences. This is the exact generality needed below. |
| Lee, [Decision Trees and Influence](https://theoryofcomputing.org/articles/v006a004/) | Published 17 Aug 2010; Theorem 1.2 p.82 | Explicit two-Boolean-function covariance inequality; useful independent cross-check, but the 2005 source already has the stronger real test-function formulation. |
| Kovacs-Deak–Wang–Yang, [Rational degree is polynomially related to degree](https://arxiv.org/abs/2601.08727v1) | v1, 13 Jan 2026 16:57:02 UTC; Theorem 4/Corollaries 3–4 pp.6–7 | Total Boolean functions. Theorem 4 gives D(F) ≤ 4 deg±(F)² rdeg(F)², and Corollary 4 gives D(F) ≤ 2 ndeg(F)² ndeg(¬F)². |
| Kothari–Kovacs-Deak–Wang–Yang, [same paper v2](https://arxiv.org/abs/2601.08727v2) | 8 Apr 2026 16:30:00 UTC; Theorem 4 p.7; Theorem 8 p.16 | Adds Kothari and improves the total-function relation to cubic up to logarithmic factors. This version is the one cited by Li et al. |
| Kothari et al., [same paper v3](https://arxiv.org/abs/2601.08727v3) | 28 Sep 2026 16:05:17 UTC; Theorem 4 p.7, Theorem 8 p.16, §5.3/Theorems 11–12 pp.20, 23–25 | Adds approximate nondeterministic-degree bounds, still for total Boolean functions. Definitions require conditions at every cube input. |
| Li–Li–Li–Liu, [Impossibility of Perfectly Complete Many-Round Key Agreement in the QROM](https://arxiv.org/abs/2608.03824v1) | Only version listed: v1, 4 Aug 2026 15:33:42 UTC; Lemma 3.5 pp.7–8 | Arbitrary real multilinear p,q of degree ≤d with pq=0 everywhere admit a depth O(d⁴) separator on their union of supports. The proof explicitly arbitrarily labels both-zero subcubes and therefore constructs a total Boolean extension. Its cryptographic application is not itself the target relative-influence theorem. |

The rational-degree paper's effective Hypercube Nullstellensatz (v3 Theorem 10 p.18) additionally assumes no shared zeros. The partial-function counterexample in its Fact 7 pp.18–19 concerns relaxing a different premise. It does not refute Li's globally disjoint-support hypothesis. A direct invocation of the total-function theorem on p/(p+q), when both p and q may vanish, has a real gap: the denominator can vanish. Calling an arbitrary completion a low-rational-degree completion simply assumes the needed structural fact. That route is blocked unless one supplies a completion mechanism such as Li's proof.

## Complete bridge, independently reconstructed

The following is my derivation connecting the sources to the audited claim, not a claim that either source printed the final target-specific consequence.

Let p,q be nonzero real functions with disjoint supports. Suppose a total h∈{0,1}, equal to 1 on supp(p) and 0 on supp(q), has a decision tree with revealments r_i and depth T. Put u=p²/Ep² and v=q²/Eq², and let μ=Eh. Then

    Cov(h,u)=1−μ,   Cov(h,v)=−μ,
    |Cov(h,u)|+|Cov(h,v)|=1.

OSSS Eq.(6), applied to 2h−1 and its negative, gives exactly

    |Cov(h,w)| ≤ (1/2) Σ_i r_i E|w(X)−w(X^(i))|,

where X^(i) independently resamples coordinate i. The factor 1/2 is necessary because h has range {0,1}, while the source normalizes its computed function into [-1,1].

For ρ_i=RelInf_i(p), Parseval and Cauchy–Schwarz give

    E|u(X)−u(X^(i))|
      = (1/2) E|(p(X)−p(X^flip_i))(p(X)+p(X^flip_i))| / Ep²
      ≤ 2 sqrt(ρ_i(1−ρ_i)) ≤ 2 sqrt(ρ_i).

The same holds for q. If δ is the largest of the relative influences of either polynomial, summing the two covariance inequalities yields

    1 ≤ 2 Σ_i r_i sqrt(δ) ≤ 2T sqrt(δ),
    δ ≥ 1/(4T²).

This uses only full L² normalization; it never divides by variance or conditions the input measure on the union of supports. The identities remain valid on the common zero set because u=v=0 there. Nonzero constant polynomials cannot form a disjoint-support pair. Thus there is no uncovered constant/zero-norm boundary case under the target's nonzero assumption.

For the quantitative Li separator reconstruction, the bounded sign-changing block polynomial has degree at most 2D, so the discrete Markov bound gives at most 8D² disjoint maximum monomials. A stage queries at most 8d³ variables and lowers the sum of the two degrees. At most 2d stages yield T≤16d⁴. Consequently δ≥1/(1024d⁸); the stated sufficient threshold 1/(4096d⁸) follows with slack. This verifies the bridge and the attribution boundary; it does not establish historical priority for making this bridge.

## Earlier and adjacent primary-source checks

- [Nisan–Szegedy (1994)](https://doi.org/10.1007/BF01263419), §§2–3: degree, block sensitivity, support-size and total Boolean decision-tree relations supply classical ingredients, not the complete target overlap statement. A primary-body copy was inspected.
- [Midrijanis (2004)](https://arxiv.org/abs/quant-ph/0403168v2), Lemma 3/Theorem 4 pp.3–4: maximum-monomial querying for total Boolean functions and the nondeterministic variant supply the degree-reduction mechanism. They do not state an arbitrary disjoint-real-support separator or the target relative-influence consequence.
- Li et al., [Toward the Impossibility of Perfect Complete Quantum PKE from OWFs, ITCS2025](https://doi.org/10.4230/LIPIcs.ITCS.2025.71), Conjecture 1/Remark 2 pp.71:2–3 and §4: proposes a one-polynomial reprogramming conjecture, proves special cases, and explicitly distinguishes it from polynomial compatibility. It does not settle the target.
- Li et al., [Cryptomania v.s. Minicrypt in a Quantum World](https://arxiv.org/abs/2504.05710), v1 8 Apr 2025 and v2 1 Jun 2026: §3's structural lemma provides a small partial assignment with a win-win nonvanishing alternative; v2 Lemma 3.4 pp.13–14. The two-round quantum-query attack bypasses a conjectural application. I found no full target-specific overlap theorem in the inspected introduction, structural argument, attack statements, or keyword scan of either body.
- [Pednekar–Podder](https://arxiv.org/abs/2605.23336v1), 22 May 2026, §§1–2 and theorem summaries: approximate nondeterministic-degree relations for specified classes of total Boolean functions. No general support promise or target overlap theorem was located. The whole body was searchable; detailed inspection was bounded to those sections and theorem/keyword locations.
- [Austrin et al. 2022](https://eprint.iacr.org/2022/218), primary abstract/Conjecture 1.2 indexed body: formulates a distribution version and records the exponential-influence regime. This audit did not obtain a byte-pinned complete PDF because direct downloads returned 403. It therefore makes no independent full-body claim for the complete version.
- [Chung–Lin–Mahmoody 2023](https://eprint.iacr.org/2023/570), primary indexed Conjecture 2.8/abstract: conditional compatibility applications, not a proved polynomial threshold. PDF downloads returned 403; only indexed primary material was inspected.
- [Bouaziz–Ermann–Grilo–Vergnaud–Vu](https://arxiv.org/abs/2311.03512), primary body §§1–3, Conjecture 2.16 and Lemma 3.4: its extended-message key-agreement theorem is conditional on polynomial compatibility. This is not an unconditional target solution.

## Search limits and decision

The query log records actual search strings, direct opens, false bibliographic leads, failures, and primary-body inspection limits. Broad searches returned tracker, review, and automated-summary pages; these were not used as proof of priority or open status. In particular, a tracker continuing to label a conjecture open is not evidence against the mathematical implication proved above.

Exact unresolved priority gap: no earlier primary text inspected here records the final normalization-plus-covariance deduction as resolution of the exact two-polynomial question. Citation graph coverage is incomplete; unpublished knowledge, talks not indexed, non-English sources, inaccessible ePrint bodies, and unsearched later citations are not excluded. Independent external mathematical input could help resolve community attribution; per project policy, no outreach was prepared or initiated.

For the local proof, add the direct OSSS2005 Eq.(6) citation. Retain the existing no-novelty/no-priority qualification. The mathematics supplies an inverse-polynomial answer to the stated target, while a publication priority claim remains unsupported by this audit.

No agents were spawned. No humans or other shards were contacted. No git, PR, release, paper, Zenodo, or tracker mutation was performed. Files were written only inside the assigned review folder; source bodies and extracts were placed under its ignored private directory before download.
