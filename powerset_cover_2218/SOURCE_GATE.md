# Source gate: Erdős Problem 624

Audit date: 2026-10-21 UTC. Target: queue 1866, database ID 2218, EP-624. This is source recovery and applicability checking, not a new solution.

## Verdict

**OPEN-AS-INDEXED; LIVE STATUS NOT VERIFIED; ORIGINAL/TRACKER VARIANT DISCREPANCY.** No full proof or refutation of the divergent excess was located. Direct official problem, LaTeX and discussion retrievals returned HTTP 403. Search-indexed official text says open, with last-edit date 27 October 2025; its crawl/access dates are older than this audit. Therefore do not advertise this as a fresh live confirmation of open status. Current mirrors likewise say open, but are not substitutes for the official live record.

## Exact target and quantifiers

Use H_u(n) for the minimum integer h for which there exists ONE function f:P(X)→X, |X|=n, such that for EVERY Y⊆X with |Y|≥h, f(P(Y))=X. Empty A is included; A=Y is included; f(X) exists. Equivalently the last condition says: for every such Y and every x∈X there exists A⊆Y with f(A)=x. The choice of f may depend on n, not on Y. The requested limit means for every real M there exists N such that for every integer n≥N, H_u(n)−log₂n>M. It is not merely unboundedness along a subsequence or a one-unit excess on powers of two. Defining H as the least threshold removes the tracker's mild wording ambiguity.

The indexed official formulation and the recovered target agree on this unrestricted model. The formal-conjectures source defines this minimum explicitly, labels the result open, and ends in `sorry`, so formalization is not a proof. Public source: https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/624.lean

## Original source and different model

Erdős–Hajnal, *Egy kombinatorikus problémáról / On a combinatorial problem*, Mat. Lapok 19 (1968), 345–348, is available at https://users.renyi.hu/~p_erdos/1968-01.pdf . Pages345 and348 require f(A)∈X\A. Thus its natural domain is proper subsets of X; applying that requirement to A=X is impossible. Empty A remains included. For proper Y, all A⊆Y are permitted, including A=Y. Write H_e for this exterior version. The English summary needs this domain repair; the 2013 presentation makes proper subsets explicit.

The original theorem gives strict H_e(n)>log₂n and the upper bound with coefficient3+epsilon for sufficiently large n. Page347 asserts coefficient2+epsilon is obtainable by a modification, without supplying its details. Page348 states the divergent-excess conjecture and says even H_e(n)>log₂n+1 was not proved. Distinguish this strict +1 question from ≥k+1 at n=2^k.

## Applicability checks, not research claims

Exterior maps form a smaller admissible class: H_u≤H_e where the natural finite conventions apply. Consequently exterior upper constructions transfer; an exterior lower bound does not transfer by inclusion alone. Replacing an internal image by an outside image can destroy coverage. For X={1,2}, f(∅)=1 and both singleton images2 make H_u(2)=1. Exteriority forces f({2})=1, so if f(∅)=1 that singleton fails; the symmetric case also fails. The exterior threshold is2. This disproves exact equality of the two parameters, not asymptotic equivalence.

Crucially, inspect the actual proof on p345 rather than only its stated hypotheses: two distinct pairs with equal images exist when binom(n,2)>n; their union has at most four points. At n=2^k, k≥4, extend that union to a k-set Y. The repeated image forces |f(P(Y))|≤2^k−1. This argument does not use exteriority, so the original proof already applies to the unrestricted ≥k+1 consequence for large k. Its reuse is not novel progress. An even simpler boundary audit works for every k≥2: the n+1 inputs consisting of the empty set and all n singletons have a repeated image among n colors. The union of the two corresponding inputs has size at most2, so it extends to a k-set. That k-set has exactly n subsets and a repeated image, proving H_u(2^k)≥k+1. The case k=1 is exceptional, as the preceding n=2 example shows. This only settles the tracker’s weak consequence, not ≥k+2 or its main divergent-excess target. Neither this fact nor a constant-fraction missing-image bound proves divergent excess.

## Tracker partial results and evidence strength

Indexed official source: https://www.erdosproblems.com/latex/624 ; indexed discussion: https://www.erdosproblems.com/forum/thread/624 . The tracker records Alon's pigeonhole proof of H_u(2^k)≥k+1. It attributes to personal communication an absolute c>0 such that for all sufficiently large k and every f on a 2^k-point set, some k-set Y has fewer than (1−c)2^k images. This implies the Erdős–Gyárfás polynomial-deficit variant: for each fixed C and sufficiently large k, every f has some Y missing more than k^C images. Separately, it reports existence of f for which every k-set sees more than 2^k/4 images. These are related extremal-image statements, not a full solution. No primary written proof of the personal communications was located. The indexed discussion says no claimed solutions in its comments; that is historical indexed evidence, not a live review of all comments.

## Historical and adjacent literature checks

Gyárfás, *Problems and memories*, 5 July2013, slide16, https://www.renyi.hu/~gyarfas/Presentations/erdos100talk.pdf , explicitly uses proper-subset exterior maps and asks H_e(2^k)>k+1, i.e. the integer inequality H_e(2^k)≥k+2. This is strictly stronger than the tracker's ≥k+1; do not merge them.

Erdős–Spencer, *On a problem of Erdős and Hajnal*, Mat. Lapok22 (1971),1–2, archive accession1972-04: https://users.renyi.hu/~p_erdos/1972-04.pdf . Its target is h(n), the largest guaranteed independent-set size: B is independent when f(A)∉B for every A⊆B. It repeats that divergent H-excess is unresolved and improves a lower bound for h, not H. The downloaded five-page PDF contains the two-page article followed by an unrelated bibliography. For unrestricted maps, allowing internal outputs changes free-set behavior radically; h must not be substituted for H.

Erdős, *A Selection of Problems and Results in Combinatorics*, Combinatorics, Probability and Computing8 (1999),1–6, DOI https://doi.org/10.1017/S0963548398003496 . Publisher metadata and abstract verified; full article not obtained. Thus exact Er99 wording remains unverified and is not asserted here.

## Gate decision

Exact target recovered. Source variants and historical +1 distinction identified. No full-solution classification justified. Before a research claim, fix the unrestricted target explicitly and obtain live official status/discussion if possible. Published personal-communication details and full Er99 text remain evidence gaps. 
