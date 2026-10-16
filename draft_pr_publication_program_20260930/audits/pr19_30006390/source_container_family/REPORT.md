# Independent primary-source and container audit

Audit date: 1 October 2026 UTC. Object: PR 19, head `f1053196b6405623d5f5d8611289939765918d72`; exact BASELINE SHA-256 `9e0a930e61d849799c4395024c85d4f9c75b63ae2172321ef78ebf643f283c82`. Source reconstruction was sealed before reading historical review or SOURCE_AUDIT. This is validation of the original unsolved 2/5 package, not another central research attempt.

**Verdict: the direct source-theorem obstructions and unresolved-partial classification pass. A small source-scope annotation should be fixed before presenting the curated statement as exactly preserved.** No exact later resolution was located in the bounded current check. No exhaustive priority or current-open certification is claimed.

## Exact target and duplicate

The original primary statement is Alon's Conjecture 5, printed p. 2250 of [OWR 42/2025](https://ems.press/content/serial-article-files/52246?nt=1), in his complete contribution pp. 2249–2251. The [publisher metadata](https://ems.press/journals/owr/articles/14299518) gives Oberwolfach Rep. **22 (2025)**, no. 3, pp. 2243–2322, published 16 February 2026; the workshop was 14–19 September 2025. The TIB and publisher full PDFs retrieved independently have identical SHA-256.

Its assumptions are: large **prime-power** q, n=q²+q+1 points of a projective plane of order q, and independent Bernoulli(1/2) retention **per point**, shared among every incidence of that point. The target is a transversal B contained in that same retained point set R. Its minimum size divided by q should exceed a function tending to infinity with probability tending to one; the suggested stronger rate is a positive constant times log q. The same target appears as Conjecture 3.2, p. 4, in the [Alon author note](https://web.math.princeton.edu/~nalon/PDFS/remark191.pdf), and Conjecture 4.7, p. 13, in the [Alon author survey](https://web.math.princeton.edu/~nalon/PDFS/sum280.pdf).

Both supplied IDs 30006390 and 30006391 contain the same contiguous original Conjecture 5 after whitespace normalization. Their titles and summaries differ; they are duplicate catalogue entries for one mathematical target. `duplicate_certificate.json` checks the exact common conjecture text in the supplied records without storing a new copy of it.

Two scope changes must be distinguished from a literal typography repair:

1. Both clean statements omit the source's prime-power restriction. The candidate's elementary deductions are valid for any existing projective plane order, so this broader baseline is legitimate. It should be identified as an extension, while the original conjecture should retain its stated domain.
2. The source asks to hit all line sections without explicitly excluding empty ones. The catalogue defines hitting only nonempty sections. Since the probability of any empty line section is at most n·2^−(q+1)=o(1), these conventions give the same asymptotic probability target. They are not identical for every finite realization.

The inherited `statement_verification` claim that only typography was changed is therefore literally too strong. Recommended repair: annotate these two changes in the first-party SOURCE_AUDIT or equivalent source note; preserve the imported records as provenance. These are source-fidelity issues, not counterexamples to the candidate baseline.

## Complete direct container hypotheses

I read the linked [50-page revised author PDF](https://www.math.tau.ac.il/~samotij/papers/efficient-containers-revised.pdf), including definitions, Sections 3–4 and the full Section 7 construction. I also retrieved the journal-form [arXiv:1910.09208v2](https://arxiv.org/pdf/1910.09208v2), 9 December 2020, 56 pages, linked by the [Discrete Analysis 2020:17 publisher page](https://discreteanalysisjournal.com/article/17354-an-efficient-container-lemma). The relevant constants, domains, inequalities, and conclusions agree between these two distinct files. The former places Theorem 1.6 on pp. 6–7; the journal form places it on p. 7. Theorem 2.1 is on p. 9 in both.

For nonempty s-uniform H, with s a positive integer, let N=v(H), M=e(H), and Δ_t be its maximum t-set degree. Theorem 1.6 assumes

\[
\alpha,\beta,\eta\in(0,1),\quad E\ge N,\quad
\alpha\beta\eta N\ge10^9s^7,\quad 10^4s^5\eta\le\beta,
\]

\[
\Delta_t(H)\le\left(\frac{\eta}{10^6s^5}\right)^{t-1}\frac EN,
\qquad 2\le t\le s.
\]

Here η renames the theorem's q to prevent collision with the plane order. Its conclusion is a covering family of independent-set containers of size at most

\[
\exp\!\left(10^4s^5\beta^{-1}\log(e/\alpha)\eta\log(e/\eta)N\right).
\]

Each container C either has |C|≤αN or has W⊆C with |W|≥(1−β)|C| and e(H[W])<E. The derivation regularizes a robustly dense induced hypergraph (Lemma 2.2), applies Theorem 1.1 with K=2s/β, and iterates shrinking containers. This does not dispense with the displayed scalar size threshold.

In the degree-measure notation, σ_H^(t)(T)=deg_H(T)/(binom(s,t)M). It is a probability **density with respect to counting measure** on t-subsets. Its Euclidean norm squared is the sum of squared coordinates, without an additional division by the number of t-subsets. Multiplicities are permitted and counted in both degrees and M.

Theorem 2.1 assumes p,δ∈(0,1) and the entire chain

\[
300s^4\sum_{t=1}^s\binom{s-1}{t-1}
 \left(\frac{5000s^3}{p}\right)^{t-1}\|\sigma_H^{(t)}\|^2
 \le\frac1{\delta N}\le\frac p{500}.
\]

It produces signatures g(I)⊆I of size at most 30s²pN and a signature-dependent f satisfying I⊆g(I)∪f(g(I)) and |f(g(I))|≤(1−δ)N. It also has the stated consistency condition: mutually contained signatures for two independent sets must coincide. Sections 3–4 justify the norm estimates, pruning, geometric convex-combination bound, signature reconstruction, and induction to uniformity one. This audit checked the exact application hypotheses against that complete proof; it does not claim a separate new proof of the full published container theorem.

## Checkable parameter impossibility

For the complete-line hypergraph of the plane, N=M=n=q²+q+1 and s=q+1. Each vertex degree is s; consequently σ_H^(1)(v)=s/(sn)=1/n and ||σ_H^(1)||²=1/n exactly. For 2≤t≤s every collinear t-set is on a unique line, giving the additional exact identity ||σ_H^(t)||²=1/[n·binom(s,t)]. These normalizations are checked independently by rational arithmetic in four prime-order planes in `parameter_certificate.py`.

For every q≥1, s²−n=q>0. Since αβη<1,

\[
\alpha\beta\eta n<n<s^2<10^9s^7.
\]

Thus Theorem 1.6's necessary scalar inequality fails for every choice of its permitted parameters. Checking E or higher codegrees cannot repair that failure.

All summands of the technical hypothesis are nonnegative. Its t=1 term gives precisely

\[
\frac{300s^4}{n}\le\frac1{\delta n}\le\frac p{500}<\frac1{500},
\]

because p<1. It would require n>150000s⁴, contradicting n<s². All signs in the exact-head BASELINE are correct. An exact positive-polynomial certificate for the contradiction is

\[
150000(q+1)^4-(q^2+q+1)
=150000q^4+600000q^3+899999q^2+599999q+149999>0.
\]

The certificate script also checks 8,320 finite point subsets for the ordinary-blocker/complete-line-independent-complement equivalence. Finite checks support normalization and translation; the universal inequalities above prove the parameter failure. They do not prove either conjectured asymptotic lower bound.

**The conclusion is limited to these direct complete-line invocations.** It does not rule out other container theorems, auxiliary constructions, additional structure, or a substantially new mechanism. Repeating all line edges with a common multiplicity leaves degree measures unchanged. Using shorter collinear subsets changes the independent-set condition and needs an additional valid reduction; it is not supplied by this obstruction.

## Independent incidence and epsilon-net scope

Alon's Theorem 2.1 and Claim 2.2 in the author note, including their full proof pp. 2–3, retain a separate random subset on **each** line. These line subsets are mutually independent. The argument finds many lines containing few points of a fixed small B and multiplies their independently generated failure probabilities. That mechanism cannot be used for shared point retention. For distinct original lines L,M, joint emptiness has probability 2^−(2q+1), twice the product 2^−(2q+2). More decisively, for any fixed ordinary blocker B, the condition B⊆R already makes every line section intersect B; conditional per-line failure probabilities are zero. The candidate correctly preserves this distinction.

The Balogh–Samotij epsilon-net theorem (1.3 and its full Section 7 proof) constructs specially chosen planar grids and sparse random subsets, followed by trimming, with uniformity growing far more slowly than the number of vertices. The [Balogh–Solymosi journal-form arXiv:1704.05089v2](https://arxiv.org/pdf/1704.05089v2), 11 October 2018, Theorem 2.2 and Section 6 pp. 11–13, likewise uses a high-dimensional integer grid, a sparse retention parameter, and trimming before projection. Their existential line-range lower bounds apply to those constructed point systems. Neither theorem asserts the required typical transversal lower bound in the Bernoulli half of every finite projective plane. The weak-net discussion's use of a real projective completion also does not identify that construction with a finite plane of order q.

## Classical attribution and remaining gap

The original [Bruen 1970 full paper](https://www.ams.org/journals/bull/1970-76-02/S0002-9904-1970-12470-3/S0002-9904-1970-12470-3.pdf), Bull. Amer. Math. Soc. 76, 342–344, proves the square-order bound and equality characterization, and explicitly announces the general arbitrary-order q+√q+1 bound in its final remark on p. 344. Thus attributing this lower bound to Bruen is supported by a primary original source. The candidate also supplies a checkable elementary proof and does not depend on the announced proof or equality characterization. There is no novelty claim to assess for this classical lower bound or the standard alteration upper bound.

The strongest audited package result is a classical lower bound of order q and a standard upper bound of order q log q, together with exact reductions and direct-method failure certificates. The weighted enumeration of small minimal blockers remains unsupported. Its desired first-moment estimate transfers the central difficulty to a new counting claim; that route is blocked without new evidence. Neither a growing lower ratio nor a logarithmic lower rate has been established. An exact later resolution, if positively verified, would require reclassifying the original target as already solved; this bounded search found none.
