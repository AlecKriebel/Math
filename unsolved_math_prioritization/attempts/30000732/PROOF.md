# Corrected partial report: fast regular Maker constructions

Target: 30000732 / OWR-1536-002. The full original question remains unresolved by this work.

This is an AI-assisted, unrefereed partial-report edition. Acceptance records an independent internal AI audit after its two required hypothesis corrections were applied. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. Every written mathematical argument, formula and example in the authored report and audit is retained. Executable code, raw computational datasets, copied source PDFs or extracted source text, source renderings, raw search responses and private coordination material are not distributed. Historical finite checks support the written arguments and cannot be reproduced from this edition alone.

Source retrieval, source inspection and mathematical-check statements describe the original report and independent audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution.

## Edition and correction notice

The original report is retained in full below, after applying the audit's exact CORRECTION.patch to a separate copy. Proposition 2 now assumes that H has no isolated vertices; Lemma 6 now assumes that G has no isolated vertices. These two insertions are the only changes to the original report. The corrected report, before this editorial wrapper, is 19,703 bytes with SHA-256 a646db384b6598f66d6cdb4f26fbdc93c7b0e288e9ea1e9cc6c25c8f529f081f.

The original report's closing request for independent review is retained as a historical statement. That review has since been completed and is reproduced in AUDIT.md; its required patch has been applied here. Acceptance remains limited to the corrected partial results. The prior Feldheim-Krivelevich and Gebauer upper theorems are cited and inspected within the recorded limits, not independently fully proved or certified here. In particular, the Gebauer-derived exponential benchmark remains conditional on the cited prior theorem.

## Full corrected authored report

# Fast Maker constructions of regular graphs: reduction and obstructions

Problem 30000732 / OWR-1536-002. Research attempt dated 11 October 2026.

## Outcome

**The full problem is not solved in this report.** We prove an exact seed reduction, elementary lower bounds, and two obstructions to specific construction methods. We also separate the available exponential upper bounds from the required subexponential bound. None of these observations is claimed to be new.

The outstanding question is whether there are finite, nonempty, simple, d-regular graphs H_d whose guaranteed Maker construction time, divided by their order, is exp(o(d)). A single such graph for each d would suffice for the original infinitude requirement. No such sequence is constructed here, and no general lower bound excluding it is proved.

## 1. Correct statement and conventions

Maker and Breaker alternately claim one previously unclaimed edge of a complete graph K_N, with Maker first. Maker wins upon owning every edge of some copy of a prescribed graph G. Extra Maker edges are allowed, and the copy need not be induced. A time bound counts Maker moves; completing the final Breaker reply is unnecessary.

The target is to find a function f on the positive integers with

\[
\lim_{d\to\infty}\frac{\log f(d)}d=0
\]

and, for every fixed d, infinitely many pairwise nonisomorphic d-regular graphs G for which Maker wins in at most f(d)|V(G)| moves whenever N is sufficiently large depending on G.

The original source is Feldheim's contribution, joint work with Krivelevich, in the 2007 Oberwolfach report, PDF pages 7–9, printed pages 1079–1081. In Problem 3.1 the d is an exponent in the expression (1+o(1))^d. The author-hosted 2008 manuscript independently calls the dependence subexponential in Problem 1, page 10. The imported expression with multiplication by d is not used here. Connectedness is not required by either inspected statement.

Let τ(G) be the least integer t for which Maker has a strategy to obtain G in at most t moves on some finite K_L. This is finite, for example by the existing sparse-graph theorem discussed below. Its value agrees with the eventual minimum time for all sufficiently large complete boards: a strategy on K_L extends to larger boards by treating Breaker's outside moves as passes. The following elementary simulation makes that assertion precise.

### Lemma 1: ignoring outside moves

A winning Maker strategy on a finite board remains a winning strategy, within the same number of Maker moves, if Breaker may sometimes pass or play outside that board.

**Proof.** Maintain a virtual play of the original game. Actual Maker edges equal virtual Maker edges. Every actual Breaker edge inside the board belongs to the virtual Breaker set; virtual Breaker may additionally own fictitious edges. An actual Breaker move to an edge still free virtually is copied. Any other actual Breaker move is replaced by an arbitrary virtually free edge, if one exists. Maker follows the virtual winning strategy, so its prescribed edges are actually free. If the virtual board becomes full, a winning strategy must already have achieved its objective. This maintains the invariants and does not add Maker moves. ∎

## 2. Infinitely many graphs reduce to one seed

### Proposition 2: disjoint-union amplification

If H has no isolated vertices and Maker can force H on K_L in at most t moves, then, for every positive integer k, Maker can force the disjoint union kH on any K_N with

\[
N\ge L+4kt
\]

in at most kt moves. Consequently τ(kH)≤kτ(H).

**Proof.** Perform k successive stages. At the start of each stage select L vertices incident to no previously claimed edge of either player. Fewer than or equal to 4kt vertices can have been touched by that time, since each round claims at most two edges. Thus at least L untouched vertices are available. On them use the t-move strategy for H, applying Lemma 1 to Breaker's outside moves. Every stage produces an H whose vertices are disjoint from the H copies retained from earlier stages. Since we ask only for a subgraph, later edges between different copies cannot invalidate them. There are at most kt Maker moves. ∎

The numerical board bound is deliberately loose. It does not incorrectly assume that Breaker leaves a prepartitioned collection of future boards untouched.

Define

\[
\alpha_d=\inf\{\tau(H)/|V(H)|: H\text{ is a finite nonempty simple }d\text{-regular graph}\}.
\]

### Corollary 3: exact reformulation

The original problem has an affirmative answer if and only if

\[
\log\alpha_d=o(d).
\]

**Proof.** An affirmative answer gives α_d≤f(d). Conversely, choose for each d a graph H_d with τ(H_d)/|V(H_d)|<α_d+1, which is possible by the definition of infimum. Proposition 2 supplies the infinitely many graphs kH_d with the same upper bound α_d+1 on their normalized times. Edge counting gives α_d≥d/2, so log(α_d+1)=o(d) whenever log α_d=o(d). The converse asymptotic implication follows from d/2≤α_d≤f(d). ∎

There is no assertion that the infimum is attained. This reformulation would be inadequate for a different question requiring connected graphs.

## 3. Elementary lower bounds and a safe counting bound

Every d-regular graph on n vertices has m=dn/2 edges, so τ(G)≥m.

### Proposition 4: an unavoidable extra move for d≥2

If G is d-regular, d≥2, and has m edges, then τ(G)≥m+1.

**Proof.** Consider Breaker's reply after Maker's (m−1)st move. To win on move m, Maker would have to use every one of its m−1 existing edges, since its final graph would have exactly |E(G)| edges. A new endpoint on the final edge would have degree one, which is incompatible with d≥2. Thus the active vertex set is already exactly V(G) in size. If a winning final move exists, its endpoints are exactly the two vertices currently of Maker degree d−1, with all remaining active vertices of degree d. That edge is unique. Breaker claims it if free. If no such edge exists, Maker was not about to win anyway. Earlier Breaker moves may be arbitrary. Edge counting excludes victory before move m. ∎

For d=1 the exception is real: an arbitrarily large matching can be claimed in exactly one move per edge on a sufficiently large board, by always using two fresh vertices. Thus α_1=1/2. Proposition 4 does not improve the asymptotic lower bound α_d≥d/2, since n is unrestricted.

### Lemma 5: Erdős–Selfridge potential criterion, with proof

In a finite unbiased Maker–Breaker game with winning sets F, if

\[
\sum_{A\in F}2^{-|A|}<\tfrac12,
\]

then Breaker can prevent Maker from completing any winning set.

**Proof.** For a position (M,B) put

\[
\Phi(M,B)=\sum_{A\in F:\,A\cap B=\varnothing}2^{-|A\setminus M|}.
\]

For a free board element x let p(x) be the sum of the current weights of the unblocked winning sets containing x. A Maker move at x raises Φ by p(x), while a Breaker move at x lowers Φ by p(x). The first Maker move raises Φ to at most twice its initial value, hence to less than one. Thereafter Breaker chooses a free element maximizing p. Immediately following this Breaker move, every p(x) has only decreased. The next Maker increase is therefore at most the preceding Breaker decrease. Thus Φ stays below one just after every Maker move. A completed winning set would contribute one to Φ, a contradiction. If there is no next Maker move, there is nothing further to prove. ∎

This is the standard criterion, re-proved here to make the uses below self-contained.

### Lemma 6: finite-board compression

If G has no isolated vertices and Maker can force G in t≥1 moves on some complete board, then Maker can force it in t moves on K_(4t).

**Proof.** If the original board has at most 4t vertices, apply Lemma 1. Otherwise simulate its strategy using a partial bijection between the touched vertices in the virtual large board and the actual small board. Each new endpoint requested by the virtual Maker strategy is mapped to an untouched actual vertex. Each new endpoint used by actual Breaker is mapped back to a previously untouched virtual vertex. Before Maker's jth move at most 4(j−1) actual vertices have been touched, so at least two unused actual vertices remain for j≤t. The virtual board has more than 4t vertices, so the reverse extension for Breaker is also possible. These extensions preserve both players' edge sets on all touched vertices and simulate legal play through Maker's tth move. The virtual copy is therefore an actual copy. ∎

### Corollary 7: conservative automorphism bound

Let G have n≥2 vertices, m edges, no isolated vertices, and a=|Aut(G)|. Then

\[
\tau(G)\ge\left\lceil\frac14(2^{m-1}a)^{1/n}\right\rceil.
\]

**Proof.** On K_Q the number of winning edge sets is (Q)_n/a if Q≥n, and zero otherwise. It is at most Q^n/a. For any integer t≥1 with 4t<(2^{m-1}a)^(1/n), the sum in Lemma 5 on K_(4t) is less than 1/2. Thus Breaker wins that board; Lemma 6 excludes a t-move Maker strategy on every larger board as well. Taking integer t gives the displayed lower bound, with the trivial τ(G)≥1 covering a vacuous small range. ∎

### Audit caution about the original lower bound

The 2008 manuscript's Lemma 3.1, page 9, gives a board-size-to-delay conversion with denominator 4. Theorem 2 on page 4 and its proof on page 10 use denominator 2 while citing that lemma. Those displayed statements do not by themselves supply the stronger factor. Corollary 7 is the weaker bound justified here by a complete simulation argument. This is a gap in the inspected derivation, not a claimed counterexample to the stronger theorem and not a claim that it cannot be proved separately.

The manuscript's disjoint-clique remark also calls a union of d-cliques d-regular; those cliques actually have degree d−1. For this problem the relevant family is a union of K_(d+1)'s.

## 4. What the counting bound does and does not exclude

### A single clique is an exponentially expensive seed

Put s=d+1 and G=K_s. Its automorphism group has size s!, so Corollary 7 gives

\[
\frac{\tau(K_s)}s\ge
\frac{2^{d/2-1/s}(s!)^{1/s}}{4s}
\ge\frac{2^{d/2-1/s}}{4e}.
\]

The second inequality follows by integrating log x:

\[
\log(s!)=\sum_{i=1}^s\log i\ge\int_1^s\log x\,dx
=s\log s-s+1\ge s\log s-s.
\]

Thus the choice H_d=K_(d+1) cannot itself give subexponential normalized time.

### This lower bound cannot be multiplied by the number of components

Let H be a fixed connected d-regular graph of order h≥2, and let a=|Aut(H)|. The disjoint union kH has order kh, has dkh/2 edges, and has exactly a^k k! automorphisms: an automorphism permutes the k connected components and independently acts within each.

The unrounded normalized expression in Corollary 7 becomes

\[
\frac{2^{d/2-1/(kh)}a^{1/h}(k!)^{1/(kh)}}{4kh}
\le \frac{2^{d/2}a^{1/h}}{4h}k^{1/h-1},
\]

using k!≤k^k. This tends to zero for fixed d and H as k grows. Rounding adds at most 1/(kh). Consequently this particular counting bound eventually says less than the elementary edge-count lower bound; it gives no exponential coefficient times k|V(H)|.

This is a limitation of the bound, not an upper bound on actual play. Likewise τ(kH)≤kτ(H) is an upper bound only. It does not justify the reverse inequality. Faster batched constructions of many components remain possible in principle.

## 5. Precise obstruction to fixed-pool, fully activated constructions

Suppose the vertices of a prescribed graph G are labelled 1,…,n. Before play, fix pairwise disjoint candidate pools U_1,…,U_n, with positive sizes c_1,…,c_n. Require the winning copy to choose one vertex from U_i for role i. The board may contain all edges of a larger complete graph, but the winning copies must respect these fixed pools.

### Proposition 8: an exponential pool requirement

If G has m edges and

\[
\prod_{i=1}^n c_i<2^{m-1},
\]

then Breaker wins this fixed-pool game.

**Proof.** There are at most ∏c_i candidate winning edge sets, each of size m. Lemma 5 applies. Extra board edges do not change the list of winning sets or the potential proof. ∎

For a d-regular G, success requires

\[
\frac1n\sum_i\log_2c_i\ge\frac d2-\frac1n.
\]

In particular, equal-size pools require c≥2^(d/2−1/n). Merely making n extremely large does not remove this exponential requirement.

### Corollary 9: full activation costs exponentially many moves

Consider the following restricted methodology: candidate pools are fixed before play; the strategy must obtain a pool-respecting copy; and by victory every vertex in every pool must be incident to a Maker edge. Any successful such strategy requires at least

\[
\frac n2\,2^{d/2-1/n}
\]

Maker moves.

**Proof.** Each Maker edge activates at most two vertices. Therefore the time is at least (∑c_i)/2. By the arithmetic–geometric mean inequality and Proposition 8,

\[
\tfrac12\sum_i c_i\ge\tfrac n2\left(\prod_i c_i\right)^{1/n}
\ge\tfrac n2\,2^{d/2-1/n}.
\]

∎

This is an obstruction to the stated restricted methodology only. General Maker strategies may assign graph roles adaptively, use unlabelled copies, leave almost all a priori available vertices untouched, or change candidate pools. In particular this is not a lower bound for α_d. The original Feldheim–Krivelevich method chooses its candidates adaptively, so the fixed-pool hypothesis must not be silently attributed to that method. Gebauer's later prescribed blow-up board does use fixed vertex roles; its large pool constants are compatible with Proposition 8.

## 6. Why a naive regularity induction fails

A tempting induction fixes an already-built part and then tries to connect a fresh vertex to two or more prescribed old vertices. The following exact pairing strategy blocks that step, independently of the number of fresh vertices.

### Proposition 10: no unprepared fresh common neighbour

Fix distinct board vertices x,y and a disjoint set U. At the start of a phase assume every edge xu and yu, u∈U, is unclaimed. Breaker can ensure that no u∈U ever becomes a common Maker neighbour of x and y during the phase.

**Proof.** Pair xu with yu for each u. The pairs are edge-disjoint. Whenever Maker takes the first edge of a pair, Breaker immediately takes its mate. If Maker moves elsewhere, Breaker can make any legal move. Inductively Maker never owns both edges in any pair. ∎

The initial-freeness assumption matters: pre-existing Maker spokes may defeat this pairing. The conclusion also concerns the fixed x,y and fixed eligible set U. It does not prevent Maker from first preparing overlapping reservoirs and only later deciding which vertices represent the target. Proposed product, matching-overlay, or local completion strategies need an explicit argument handling this obstacle; a large untouched reservoir alone does not do so.

### A related quantifier warning

Forcing some member of a family of d-regular graphs is weaker than forcing one graph whose isomorphism type was fixed in advance. The inference from

“there exists a strategy such that for every Breaker play some target occurs”

to

“there exists one target and a strategy forcing that target against every Breaker play”

is invalid in general. Here is a finite Maker–Breaker example: on board {x,a,b}, the two winning sets are {x,a} and {x,b}. Maker first takes x and then takes whichever of a,b Breaker leaves, so the union objective is won in two moves. For either single prescribed winning set, Breaker takes its other element after Maker's first move and wins. This is a logical counterexample to the inference, not a graph-theoretic disproof of the regular-graph problem. Fast minimum-degree or connectivity games cannot be substituted without an additional prescribed-isomorphism argument.

## 7. Existing results and the remaining gap

The following are prior results, not claims proved or discovered in this attempt.

1. Feldheim–Krivelevich's 2008 Theorem 1 gives τ(G)≤d^11 2^(2d+7)|V(G)| for every d-degenerate G, with an explicit sufficiently large board. It therefore applies to every d-regular G but has exponential dependence on d.
2. Gebauer's arXiv manuscript 0909.4362, page 3, Corollary 1.8, states that for sufficiently large q a clique K_q can be forced in at most 2q^7 2^(2q/3) moves on a sufficiently large complete board. The later journal article is “On the clique-game,” European Journal of Combinatorics 33 (2012), 8–19. We use the displayed preprint bound only as a cited prior theorem, with an integer ceiling when needed. Its complete proof is not independently certified here.
3. Applying Proposition 2 with q=d+1 gives infinitely many d-regular graphs with normalized upper bound

\[
\frac{\lceil2(d+1)^7 2^{2(d+1)/3}\rceil}{d+1}
=2^{(2/3+o(1))d}.
\]

This improves the benchmark obtainable directly from the 2008 general theorem, but its logarithm divided by d tends to (2/3)log 2 rather than zero.
4. Gebauer's 2013 paper “Size Ramsey Number of Bounded Degree Graphs for Games,” Theorem 1.1, constructs a finite board with O_d(n) edges for every n-vertex graph of maximum degree d. The article explicitly describes the derived time constants as weaker than the 2008 ones. Its existence of a constant depending on d is not a subexponential bound.

The sparse-board approach is sufficient but not automatically necessary for fast construction: if Maker wins on a fixed board with M edges, then on a complete super-board Lemma 1 simulates its strategy and gives at most ⌈M/2⌉ Maker moves. A lower bound for the edges of every fixed winning board would not, by itself, be a lower bound for the time of an adaptive strategy on K_N.

The substantive attempt therefore ends at a precise gap: no construction has been given that both fixes a d-regular isomorphism type before play and uses exp(o(d)) Maker moves per target vertex. The fixed-pool/full-activation and fixed-common-neighbour methods above cannot supply such a construction under their stated restrictions. Global or adaptively relabelled strategies and possible component-batching gains are not ruled out.

## Sources

- Ohad Feldheim, joint work with Michael Krivelevich, contribution to *Mini-Workshop: Positional Games*, Oberwolfach Reports 20/2007, printed 1079–1081, [original report](https://ems.press/content/serial-article-files/46106).
- Ohad N. Feldheim and Michael Krivelevich, *Winning fast in sparse graph construction games*, author manuscript dated 6 July 2008, [author PDF](https://www.math.tau.ac.il/~krivelev/fastwin.pdf).
- Heidi Gebauer, *A Strategy for Maker in the Clique Game which Helps to Tackle some Open Problems by Beck*, [arXiv:0909.4362](https://arxiv.org/abs/0909.4362), [inspected PDF](https://arxiv.org/pdf/0909.4362); journal version [On the clique-game](https://doi.org/10.1016/j.ejc.2011.07.005).
- Heidi Gebauer, *Size Ramsey Number of Bounded Degree Graphs for Games*, Combinatorics, Probability and Computing 22 (2013), 499–516, [DOI](https://doi.org/10.1017/S0963548313000151), [institutional PDF](https://www.research-collection.ethz.ch/server/api/core/bitstreams/56e3f017-575f-4856-a832-2ffbf307c16b/content).

## Verification and limits

The proofs in Sections 2–6 are mathematical arguments, not extrapolations from computation. Authored finite minimax checks exercise the pairing-game and quantifier examples only. They do not search arbitrary regular graphs or establish the subexponential target. No third-party source code was executed. The cited literature screen is bounded, and failure to find a later settlement is not evidence that the problem is still open. An independent review is still needed before relying on this report as an accepted audit or proof patch.
