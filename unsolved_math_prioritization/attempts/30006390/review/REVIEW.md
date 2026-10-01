# Independent review: random projective plane transversals

**Problem:** 30006390 / OWR-14299518-003; duplicate 30006391.
**Review date:** 30 September 2026.
**Reviewer:** a separate gpt-6-astra agent at xhigh reasoning, not the author of the submitted analysis.
**Disposition: PASS for unresolved partial analysis.** The claimed baseline results and reductions pass mathematical review. The original conjecture remains unresolved in this work. The author applied the single minor theorem-transcription correction recorded below; the corrected snapshot has been verified.

## Reviewed snapshot and scope

The initial reviewed branch was `dot/math-30006390`, commit `d1b4473c68344b67174a1d445fb27784184af113`. The initial `BASELINE.md` SHA-256 was `f9c49d798cdd74c39af6ce06351c6672116421fa4895f06e608d667a5a1398ed`. The submitted `check_small_planes.py` SHA-256 was `6241b9de1f8463e24c399674c85a9abbf8575c6655c54d37da2a0208f27f9e04`.

This review audits the complete baseline proof, source model, weighted counting reduction, numerical container obstructions, and reproducible finite diagnostics. It does not certify novelty, exhaustive current open status, or a solution of either conjectured lower bound. No author artifact was edited by the reviewer.

## Source and probability model

The original source is Noga Alon's contribution to [Oberwolfach Report 42/2025](https://ems.press/content/serial-article-files/52246?nt=1), pp. 2249–2251, Conjecture 5 on p. 2250. I read the contribution and visually inspected the conjecture. The same target appears in the author-hosted [Blocking partial designs and block-compatible sequences](https://web.math.princeton.edu/~nalon/PDFS/remark191.pdf), Conjecture 3.2, and [Problems and results in Extremal combinatorics V](https://web.math.princeton.edu/~nalon/PDFS/sum280.pdf), Conjecture 4.7. The checked versions explicitly leave it open.

There is one independently sampled set of retained points. A point shared by two lines has the same retention status in both sections. This differs from the independent-incidence construction in the nearby partial-design theorem. The submission preserves that distinction correctly. Its elementary baseline is valid for any projective plane of order q, so its use of this slightly broader class does not weaken the source target, which states prime-power orders.

The source asks to hit all sections; the catalogue uses all nonempty sections. The exceptional probability of an empty section is at most n 2^(-(q+1)), tending to zero. Thus the convention change is explicitly justified and does not silently alter the asymptotic problem.

## Classical lower bound

Every ordinary blocking set B has k(q+1) >= n, hence integer k >= q+1. If B contains no whole line, a point outside B on a given line has q other lines through it, with disjoint portions outside that line. Consequently each line has at most k-q points in B.

Writing a=k-q-1, the submission correctly sums

\[
r_L(r_L-1)\le(a+1)(r_L-1)
\]

using the two exact projective-plane identities

\[
\sum_Lr_L(r_L-1)=k(k-1),\qquad
\sum_Lr_L=k(q+1).
\]

Independent expansion gives

\[
(a+1)\bigl(k(q+1)-n\bigr)-k(k-1)=q(a^2-q).
\]

The resulting bound k >= q+sqrt(q)+1 is valid, including when q is not a square. No equality classification, Desarguesian assumption, or extra regularity hypothesis is used. Attribution to the classical Bruen bound is appropriate; Bruen's [Partial Spreads and Replaceable Nets](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/partial-spreads-and-replaceable-nets/52A3802B5E2B5420E92F8E446BE5460F) recalls this bound for arbitrary finite projective planes.

The probability that R contains a whole line is also at most n 2^(-(q+1)). Outside the union of these two exceptional events, every eligible blocker in R satisfies this bound. The ratio of this lower bound to q tends to one, so it does not prove the requested divergence.

## Alteration upper bound

Each line-section cardinality is binomial with q+1 trials. Hoeffding's bound at deviation sqrt(3(q+1) log q), followed by a union bound over n lines, gives failure probability at most 2n q^-6. Independence between lines is unnecessary. Together with concentration of |R|, this gives m=(1+o(1))q/2 and |R|=(1+o(1))n/2 simultaneously.

For a fixed such realization, rho=log(q+1)/m lies in (0,1) for large q. Sampling a temporary subset of R and adding a retained point on each missed line produces an actual blocker in R. Repeated additions can only reduce its size relative to the upper estimate. Linearity of expectation requires no independence between missed-line events. The calculation

\[
\mathbb E|B|\le \rho|R|+n e^{-\rho m}
=\frac{|R|\log(q+1)}m+\frac n{q+1}
=(1+o(1))q\log q
\]

is correct. An outcome no larger than this expectation exists. Natural logarithms are explicitly declared, so the leading constant is consistent.

## Minimal-blocker reduction and exact gap

On the event that every section is nonempty, an eligible set is exactly an ordinary blocker contained in R. Any finite blocker contains an inclusion-minimal blocker, giving the stated equivalence for every cardinality threshold k. Each fixed blocker is retained with probability 2^(-|B|). The resulting union bound with the empty-section exceptional term is valid.

Vanishing of the weighted sum for every fixed linear threshold Cq would suffice for divergence of the transversal number divided by q in probability. A diagonal choice of growing thresholds would then yield a deterministic function tending to infinity as requested. The weighted-sum estimate is not proved here and is correctly identified as sufficient, rather than necessary. Overlap between witness events can make the first moment substantially larger than their union probability.

The warning about naive subset counting is justified: already the size-k level contributes the useless bound binomial(n,k) 2^-k, whose logarithm is Theta(q log q) for fixed positive k/q. Minimality eliminates supersets of whole-line blockers but does not supply the missing estimate for nontrivial minimal blockers.

For two distinct lines, the union contains 2q+1 points, giving joint empty-section probability 2^(-(2q+1)), twice the product of the marginals. More decisively, conditioning on retention of an ordinary blocker guarantees all required intersections. The submission therefore correctly refuses to import the unrelated independent-incidence argument.

## Container obstruction and minor correction

I checked the degree-measure definition and visually inspected Theorems 1.6 and 2.1 in the author-hosted [Balogh–Samotij paper](https://www.math.tau.ac.il/~samotij/papers/efficient-containers-revised.pdf). For the hypergraph of full projective lines, s=q+1, the number of vertices is n=q^2+q+1, and the first degree measure is uniform. Its squared norm is 1/n.

Theorem 1.6 actually assumes alpha beta eta n **>=** 10^9 s^7. The initial baseline writes **>**. Replace that one sign with >= for exact source fidelity. Since alpha beta eta n < n < s^2, the contradiction is unchanged under the source's weaker, non-strict inequality.

The first summand of Theorem 2.1 gives the exact necessary chain

\[
\frac{300s^4}{n}\le\frac1{\delta n}\le\frac p{500}<\frac1{500}.
\]

Thus n>150000s^4 would be necessary, which is impossible. This is a valid obstruction to the stated direct applications. It is not a no-go theorem for all container methods, and the submission does not present it as one.

The epsilon-net results in Balogh–Samotij Theorem 1.3 and [Balogh–Solymosi Theorem 2.2](https://arxiv.org/pdf/1704.05089) assert existence of specially constructed planar point systems. They do not assert the present random-half-set statement for arbitrary finite projective planes. No unsupported transfer is made.

## Computational checks and disposition

The submitted diagnostic was replayed unchanged, redirecting its output to the review directory. Its JSON output matched the submitted output exactly. It checked all 128 point subsets of PG(2,2) and all 8192 subsets of PG(2,3).

An independent standard-library checker constructs the planes from affine coordinates and points at infinity, rather than the submitted homogeneous-coordinate construction. It directly enumerates retained-set submasks instead of using the submitted subset dynamic program. All 28,072 assertions pass. Checks include the exact section-transversal/minimal-blocker equivalence, weighted union bounds for every threshold in both planes, double-counted witness expectations, the dependence factor of two, complement independence, incidence identities, the Bruen calculation, and 4,394 rational alteration estimates at sampling probability 1/3. These computations are diagnostic only, not evidence for the asymptotic conjecture.

With the single non-strict inequality transcription now corrected, this package is suitable for a draft PR explicitly classified as **unresolved partial analysis**. Neither the divergent lower multiplier nor the proposed logarithmic lower multiplier has been established. No new discovery, full solution, exhaustive literature certification, human peer review, or formal proof certificate is asserted.

## Final corrected snapshot

The author changed only the requested Theorem 1.6 sign from > to >=. I compared the complete file against the frozen initial snapshot and verified the corrected SHA-256 `9e0a930e61d849799c4395024c85d4f9c75b63ae2172321ef78ebf643f283c82`. No other mathematical text changed. Final verdict: **PASS for the stated unresolved partial results**, with no outstanding correction. The original divergence and logarithmic-strengthening claims remain unproved in this work.
