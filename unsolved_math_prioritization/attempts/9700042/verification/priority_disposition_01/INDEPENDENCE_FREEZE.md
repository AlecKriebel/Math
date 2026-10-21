# Independent priority/disposition freeze

Frozen at 2026-10-15T14:25:55Z (source-first assessment; no other current priority-family folders or candidate/audit verdicts read).

## Exact question

The original flow model is the northeast-oriented square lattice with independent Bernoulli(p) capacities and the precise source/sink convention stated on Aldous's problem page. The target is

`1-v(1-q) ~ sqrt(2q)` as `q -> 0`.

The supplied finite dual has forward northeast costs Bernoulli(1-q), free reverse southwest steps, and corner passage value `T_N`. Its deficit is `D_N=2N-T_N=max(K-B)`, where K counts zero-cost **forward** edges and B counts backward steps. This is different from symmetric Bernoulli FPP, whose deficit charges twice for backward steps (with additional rewards if reversed open edges are traversed). Equality of the leading coefficient does not identify the models.

## Sources inspected before this freeze

1. The complete supplied Aldous problem-page HTML, including exact endpoints, normalization, heuristic, and 2004 history.
2. Basdevant--Gouere--Theret, arXiv:2106.12266v1 (23 June 2021), complete relevant Sections 2.2--2.5 and 3.1--3.4; also introduction/main statements and Appendix A.2. PDF SHA-256: `9d78c8dd86aaa62dbaa7bfcaf40195c901c3cc9dee025bffd4a6e29af64339ba`.
3. Visual inspection of complete PDF pages 16, 23, 24. In (19), and Item 5 of Lemma 19, the negative part is applied to **each increment** before summing; it is not the negative part of the total increment. The equation (33) m=0 weight is `r^(h-1+sum ell)`.
4. Read-only publication-metadata verification: the publisher's AAP 32(6) issue and the authors' institute list identify the 2022 article, pages 4535--4567, DOI 10.1214/22-AAP1795. The publisher full HTML wrapper did not expose mathematical text. No final-published-PDF equation comparison has yet been performed.

## Frozen old-source assessment

The named Theorem 1/Lemma 18 does not directly imply the target. However, the numerical union/Chernoff sum (33) supplies a universal bound for open-tail sequences with Lemma 19's constraints; it is not intrinsically a symmetric-passage-time statement.

There appears to be a complete routine corollary using that **unchanged** numerical sum, rather than a new central extension. The crucial cancellation is:

- In a simple target path every reward has its own forward-edge tail, so `K <= p + delta_origin` (not the symmetric bond estimate `2(p+1)`).
- Greedy strict-tail anchors yield an oriented strict-chain score at least `h-1+delta_origin`; hence `D_N-S <= sum ell - B`.
- The geometric quantity X in (19) is at most `2B`; multiplying the preceding inequality by two places an anomalous target path inside Lemma 19 Item 5 with m=0, at twice the excess threshold. Local optimality gives Item 4, in fact a stronger version.
- Tail-open probability is `r=1-(1-q)^2`. The site/strict-chain score already has coefficient 2 at scale sqrt(r). Thus the finite comparison would give the exact coefficient sqrt(2q) after division by 2N.

The next document must check all details, especially the artificial terminal `(N+1,N+1)`, origin rewards, strict chain realizability, simple-path reduction, and the meaning of m=0. This is a freshly derived corollary from old public inputs. It is not evidence that the authors, or anyone else, previously stated or recognized the canonical flow conclusion. No automatic `already_solved` queue change is warranted merely from this reduction.

Completion estimate for this priority/disposition assignment: 65%. Strongest checked result at freeze: the coefficient is covered by old strict-chain asymptotics, and the target sequence constraints appear to fit the old numerical counting sum with no change of kernel. Remaining gap: finish and adversarially audit the deterministic implication and its normalization.
