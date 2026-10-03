# Maximum twin-width of n-vertex graphs: partial research checkpoint

Alec Kriebel · [ORCID](https://orcid.org/0009-0001-9320-500X)

Problem 30004980 / OWR-9790352-030. This checkpoint does not solve the exact maximum problem. It records attempted proof mechanisms, a six-vertex obstruction to a stronger fixed-matching lemma, and independently implemented finite certificate checks. Four of five substantive attempts are complete. The results have not yet received independent mathematical review.

## Exact target and convention

For every n>=1 determine M(n), the maximum standard twin-width of a finite simple undirected n-vertex graph. Initially edges are black; a quotient pair is red exactly when its original bipartite adjacency is mixed. Twin-width minimizes the largest red degree over all binary contraction sequences. Sparse, linear, directed, and pre-red variants are excluded.

## Source and status corrections

The official [Oberwolfach report](https://ems.press/content/serial-article-files/46939?nt=1), printed p.66, asks the exact maximum; it already records Paley examples and a leading n/2 upper bound with a lower-order error. The live [problem page](https://www.unsolvedmath.com/problems/30004980) returned HTTP 403 on 2026-10-03, so its current body was not verified.

[Ahn, Hendrey, Kim, and Oum, v2](https://arxiv.org/abs/2110.03957v2), Theorems 1.1, 1.3, 1.4, give the strict upper bound (n+sqrt(n ln n)+sqrt(n)+2 ln n)/2, asymptotically matching random-graph lower bounds, conference-graph lower bound (n-1)/2, and exact Paley equality. The leading asymptotic M(n)=n/2+o(n) is therefore already known, not a new resolution.

[Heinrich, Ihringer, Rassmann, and Volk, v2](https://arxiv.org/html/2504.02342v2), Theorem 4.7, proves equality for self-complementary vertex- and edge-transitive graphs. Conjecture 5.2 proposes the universal upper bound (n-1)/2 with equality exactly for conference graphs. General conference equality is conjectural in that source. The conjectured universal bound is not by itself an exact formula attained at every n: twin-width is integer and conference orders are restricted. Small n also requires care with any claimed equality characterization.

The 2026 [bounded-VC-dimension paper](https://arxiv.org/html/2606.21640v1) gives sublinear bounds for a restricted class and does not settle the unrestricted maximum. This is a dated bounded primary-literature check, not a guarantee that no later result exists.

## Checkable artifacts

- attempts/turn_01.md: degree-defect identity and failure of naive quotient induction.
- attempts/turn_02.md: exact pair-update formula and involution sufficient criterion.
- attempts/turn_03.md: cyclic obstruction to every ordering of one near-twin matching.
- attempts/turn_04.md: finite exhaustive and seeded-sample search.
- checks/twinwidth.py: exact quotient-state search.
- checks/verify_small.py: independent incremental red/black-state verification.

Run from checks: python twinwidth.py; python verify_small.py. No nonstandard packages are required. Output files are regenerated in checks. Finite search does not prove an unbounded statement. No novelty is claimed for recovered small maxima, first-contraction bounds, or symmetry families. The explicit method obstruction is not a counterexample to the original problem.

OpenAI tools assisted research, drafting, and code. This is an unrefereed partial research record. No source PDFs, screenshots, corpus files, or private context are included.
