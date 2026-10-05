# Independent audit: triangle-removal spread, problem 30005114

## Disposition

**PASS for the stated partial results and method obstructions. The general problem remains UNSOLVED; the five-turn attempt remains exhausted at 5/5.** This audit does not certify a full solution, novelty, or priority. It does not extend the research budget.

The author freeze was checked without modification: ZIP size 17,977 bytes; SHA-256 `dd3d6c99dea68a3dab8332574562c4232d14fca288bc1b61515b927a5086b48f`. All six entries of its internal manifest pass, and its seven archived files are preserved under `author_frozen/`.

Accepted claims, for sufficiently large n and the one event E_n defined in the author report:

1. For every deterministic family F of k distinct triangles, the conditional inclusion probability is at most `[100(p_m^(-2)-1)/(99n)]^k` for k >= 1. The base is O(n^(-0.98)), with a constant independent of k and F.
2. If the edge-shadow of F has maximum degree at most `n p_m^2/10`, the conditional inclusion probability is at most `(4/n)^k`. Shared edges give probability zero; shared vertices are allowed.
3. The proposed unrestricted extension of the time-varying potential fails for a dense clique decomposition. This is a counterexample to that potential inequality, not to the original spread conjecture.
4. Triangle inclusion is not automatically negatively correlated: the terminal K_5 example has marginal 1/5 and joint probability 1/15 for the indicated edge-disjoint pair.

No blocking mathematical correction was found. The accompanying clarifications make stopping, uniformity, and literature boundaries explicit.

## Independent analytic reconstruction

### The event and the imported probability estimate

Let `m=floor(n^2/6-n^(199/100))` and `p_i=1-6i/n^2`. The exact remaining-edge count is `(n^2 p_i-n)/2`; the proof does not mistake p_i for the exact density. The floor gives

`6 n^(-1/100) <= p_m < 6 n^(-1/100)+6/n^2`.

The lower bound is sufficient for the asymptotics. Positive m requires n to be extremely large; finite terminal-process tests are therefore correctly separated from experiments at this m.

The event uses only the trajectory: reach m, all pair-codegrees at least `0.99 n p_i^2`, and all triangle counts between `0.99 n^3 p_i^3/6` and `1.01 n^3 p_i^3/6`, for every i through m. It is fixed before F or k is specified and is invariant under vertex permutations.

Bohman–Frieze–Lubetzky, *Random triangle removal*, arXiv:1203.4223v3, Theorems 2.1–2.2 and their combination at the end of Section 2, were inspected directly. For fixed M=3 they give uniform estimates down to `p>=n^(-1/6)`. Their relative codegree error is a fixed constant times `zeta=n^(-1/2)p^(-1) log n`; the triangle-count relative error is O(zeta^2). On our range, zeta is at most `(1/6)n^(-0.49)log n`, which tends to zero. Thus the fixed 1% inequalities hold throughout with probability 1-o(1). The positive triangle lower bound ensures the process has not terminated. This is an application of the imported theorem, not an independent proof of its concentration argument.

All martingales below are defined under the original chain, with an absorbing zero state on the first failure of a trajectory inequality. Early termination also enters that zero state. No future-conditioned transition law is used. For large n the initial state meets the bounds deterministically, and `P(E_n)>=1/2`.

### All-k denominator proof

Put `a_i=6/(0.99 n^3 p_i^3)`. For an injection assigning a distinct time to each labeled member of F, expose the history chronologically in the killed original chain. Every forced selection contributes at most a_i; unconstrained steps contribute at most one. Future survival can only reduce the probability. The disjoint assignments therefore give

`P(F included, E_n) <= k! e_k(a_0,...,a_(m-1)) <= (sum a_i)^k`.

The increasing integrand yields

`sum_(i<m) p_i^(-3) <= integral_0^m (1-6x/n^2)^(-3) dx = (n^2/12)(p_m^(-2)-1)`.

Hence the joint-probability base is `50(p_m^(-2)-1)/(99n)`. Dividing by `P(E_n)>=1/2` costs a single factor two, and `2<=2^k` for every integer k>=1 gives the stated base. No error is exponentiated without a uniform bound. The integral and elementary symmetric-function estimate do not require fixed k; they apply through quadratic k, including the source's `n^2/12` example whenever meaningful. If k>m, inclusion is impossible. If k=0, the probability is exactly one.

### Protected-edge counting

For a live target packing, write r for the remaining target count, U for its 3r protected edges, d for a lower codegree bound on these edges, and Delta for the maximum degree of U. A selected non-target triangle meeting U spoils inclusion permanently.

For each bad triangle S let a(S) be its number of protected edges. Sum the protected-edge codegrees and subtract the 3r incidences of target triangles. This gives `sum_bad a(S)>=3r(d-1)`. Since a(S)<=3, `b>=r(d-1)`.

For the sharper estimate, each `a-binomial(a,2)` is at most the indicator that S is bad. Protected-edge pairs inside a triangle are wedges in U. Therefore

`b >= sum_bad a(S)-sum_bad binomial(a(S),2) >= 3r(d-1)-sum_v binomial(deg_U(v),2) >= 3r(d-Delta)`.

These are deterministic incidence counts; no independence or negative association is assumed. Remaining-target shadows are subgraphs of the original shadow, so the maximum-degree hypothesis persists along every live history.

### Sparse-family supermartingale and uniform powers

Let `w_i=2/(n p_i^2)`. Give a live history with r remaining targets weight `Z_i=w_i^r` and a killed or spoiled history weight zero. Completion is r=0, not a stopping rule that drops later trajectory tests. If all targets are selected and E_n holds, the terminal weight is one. Other histories contribute nonnegative weight, so this terminal weight dominates the desired indicator.

At a live history, exactly r current triangles are successful targets, b spoil the event, and Q-r-b preserve r. Before possible next-step killing, the conditional next expectation is exactly

`(w')^r [1-r(1+b/r-1/w')/Q]`.

Let `h=6/n^2`, `a=((p-h)/p)^2=w_i/w'`, and `p_*=p_m<=p`. The asserted bounds reduce to

`1+3(0.99 n p^2-0.1 n p_*^2)-n(p-h)^2/2 >= (1.01 n^3 p^3/6)(1-a)`.

An independent expansion gives the exact difference between the two sides:

`1+(9/20)n p^2-(3/10)n p_*^2+(201/100)n p h-(1/2)n h^2`.

For `0<h<p` and `p_*<=p`, this exceeds `(3/20)n p^2`. This verifies the author's constant margin without relying on rounded decimals.

Consequently the next expectation is at most `(w')^r[1-r(1-a)]`. Bernoulli's inequality `a^r>=1-r(1-a)` then bounds it by `w_i^r`, for every integer r>=0. There is no small-r asymptotic expansion. As a consistency check, the degree hypothesis implies `6r<=n Delta<=n^2 p_*^2/10`, whence `r(1-a)<=p/5<=1/5`. Thus the intermediate linear bound is nonnegative throughout the admissible range; a hidden large-r sign problem cannot arise.

Killed histories remain zero; when r=0, further killing only decreases the weight. The finite deterministic horizon gives `E Z_m<=Z_0=(2/n)^k` by iterated expectations, without any unbounded optional-stopping issue. Final conditioning and `2<=2^k` give `(4/n)^k`. Again k=0 is separate.

The weaker fixed potential `d_*^(number of selected targets)`, with `d_*=0.99 n p_m^2`, also passes: its one-step relative drift is `[r(d_*-1)-b]/Q<=0`. Its conditional base is `2/d_*=O(n^(-0.98))`, not C/n.

### Dense-family obstruction

For a triangle decomposition of an s-clique inside K_n, with n=2s, `r=s(s-1)/6`. Every bad triangle has two or three clique vertices. Hence

`b=binomial(s,3)+binomial(s,2)(n-s)-r=r(3n-2s-3)`.

The exact one-step potential ratio is

`(1-6/n^2)^(-2r) [1-(r+b)/binomial(n,3)+r/(binomial(n,3)w_1)]`.

Since `r~n^2/24`, its limit is `(5/8)exp(1/2)>65/64>1`. The estimate uses the strict exponential-series bound. All one-deletion graphs obey the fixed trajectory tests for sufficiently large n, so the killing mechanism does not remove the positive first-step drift. The target count is asymptotically n^2/24 and eventually lies below m. This disproves only the unrestricted supermartingale assertion.

The independent finite witness uses affine lines in F_3^5, on s=243 vertices, rather than the author's Bose system on s=201. Every pair is covered once, yielding 9,801 target triangles in K_486. Exact rational comparison gives positive drift; its diagnostic ratio is approximately 1.0287527957. The finite m from the original question is negative at n=486, so the asymptotic argument, not this finite horizon, establishes the method obstruction.

## Computational verification

The author verifier was replayed in the extracted freeze and its JSON output agrees exactly with the recorded result. Independent code imports no author code and uses different representations:

- Backward dynamic programming on the available-triangle set recovers terminal size distributions, one-point marginals, and the selected pair's joint inclusion for n=3 through 7.
- Enumeration of target packings first, then all containing graphs, checks 141,040 graph/family pairs on six vertices. Both hazard inequalities and the intermediate incidence/wedge comparisons pass. There are 270 target packings.
- Exact rational identities test the drift margin, Bernoulli comparison, admissible-r bound, and integer stopping convention at n=7^100, 10^100, and 100^100. These checks supplement the universal analytic inequalities above.
- The affine Steiner witness separately checks pair coverage, exact positive drift, and survival of the first two trajectory tests.
- Full source-file hashes, dataset counts, selected-record uniqueness, statement hash, canonical review hash, catalog Git-blob identity, and absent exact prior-report matches were rebuilt. The source corpora themselves are excluded.

## Literature and provenance audit

The official OWR PDF was freshly retrieved, hashed, and visually inspected at printed p.1226 (PDF page 62). The source asks for one high-probability event and a C/n bound uniformly over prescribed families, explicitly including quadratic k. The nearby Hales–Jewett remark belongs to the preceding problem. The imported original extraction is contaminated by neighboring text; the clean statement matches the actual target.

Fresh BFL and Jain–Pham PDFs agree byte-for-byte with the author's hashes. The latest Sah–Sawhney–Simkin arXiv v2 was additionally downloaded and its introduction/Section 1.2 inspected. It continues to discuss a modified process and iterative absorption; its binomial restriction changes the output law. Jain–Pham constructs optimal-order spread measures, with distributional choices different from ordinary triangle removal. Neither inspected construction proves the requested statement about this law. Their full proofs were not independently audited. The adjacent Latin-rectangle abstract likewise concerns a different model.

On 2026-10-05, bounded web searches by exact process name, spread, conditional probability, random greedy matching, and the proposer did not identify a resolution of the exact target. This is not an exhaustive literature or absence theorem. Public source metadata and search boundaries are in `SOURCE_AUDIT.json`.

Complete retained public dataset files were rehashed against a freshly read manifest at the pinned repository commit. The selected statement and full `[problem, prior_report]` canonical review hash agree with the catalog. The separate 6,701-entry research corpus has no exact selected-code key or selected-ID/code match in a value. Fresh GitHub searches by ID, code, and title/topic found no earlier attempt artifact, branch, commit, or PR. The pinned attempts directory has 63 entries without this ID. The historical review is a desk assessment, not an earlier proof artifact. These checks do not exclude unpublished, deleted, unindexed, or differently named work.

## Public-safe boundary

The archive contains authored mathematics, independent code, exact-check results, manifests, and public verification metadata. It contains no source PDF, source extraction, source image, raw corpus, secret, or private coordination file. The original freeze remains unchanged. No remote write was performed.
