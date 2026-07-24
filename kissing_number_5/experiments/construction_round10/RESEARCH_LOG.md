# Construction round 10 research log

All statements in this log concern floating-point discovery unless explicitly
marked otherwise.

## 2026-07-23 21:58 PDT — mechanism selected

Started an independent two-sided construction challenge for
\(N=41,42,43,44\).  The structured variable is a general matrix
\(B\in\mathbb R^{m\times5}\) applied to a finite root shell
\(R\subset\mathbb R^m\), with every image row renormalized.  Equivalently the
shell is measured by the rank-at-most-five PSD metric \(BB^{\mathsf T}\).
Unlike an orthogonal hyperplane projection, all five nonzero metric
eigenvalues are free.

The continuous metric step is alternated with a discrete exact-cardinality
subset step.  The final selected images are released into unrestricted
coordinates on \((S^4)^N\).  E6, D6, and D7 were retained as genuinely
different finite shells.

## 2026-07-23 22:05 PDT — implementation audit

Checked the analytic metric gradient against centered finite differences at
three step sizes.  The directional derivative agreed to better than
\(6\times10^{-11}\).  Added unit tests for the E6 shell, the gradient, and
the discrete-swap descent invariant.  All three tests pass with Python
3.14.6, NumPy 2.5.1, and SciPy 1.18.0.

## 2026-07-23 22:11 PDT — first local-basin diagnosis

Several E6 starts at \(N=41\) converged to the same structured value near
`0.542474097937`.  Their subset is the entire 40-root D5 slice plus one E6
half-root.  The map has four equal numerical singular values near
`1.0396426442` and one near `0.8225403877`; the \(10^{-8}\) top-contact graph
is a 10-edge star plus 30 isolated vertices.

A separate 42-point structured basin is already smaller, near
`0.542028093184`.  Deleting one point from this larger output produces a
41-point child below the direct 41-point structured basin.  This is a
concrete counterexample to interpreting the one-swap N=41 termination as a
meaningful obstruction.  Added a cross-cardinality challenge that exhausts
all one-, two-, and three-point deletions from larger stored outputs before
reoptimizing the metric and releasing all coordinates.

## 2026-07-23 22:15 PDT — 120-start portfolio complete

Completed ten seeds for every pair in
\(\{E6,D6,D7\}\times\{41,42,43,44\}\).  The best structured maxima were
`0.5424740979369884`, `0.5420280931836461`,
`0.5680492861305548`, and `0.5679865766440254`.  None reaches \(1/2\).

After unrestricted smooth-minimax continuation and epigraph SQP, the best
stored maxima were:

```
N=41  0.5220692609969377
N=42  0.5343035874522938
N=43  0.5366600203477839
N=44  0.5274711925362580
```

The 44-point endpoint has the same \(10^{-8}\)-active degree histogram and
Gram spectrum as the previously recorded 44-point basin.  The other three
values are worse than prior numerical records.  Consequently the new finite
shell mechanism finds no code and no numerical record.

The main artifact passed the independent checker: 120 structured runs and 12
released runs were reconstructed, renormalized, and rehashed.  SHA-256:
`98dec446c70bf8b99aa73d461bdaa971f0d234af8eb43614c46d8fc52f8888d0`.

## 2026-07-23 22:16 PDT — cross-cardinality audit complete

Exhaustively enumerated every deletion of one to three points in the retained
larger-cardinality parents, then reoptimized the metric and released the two
best children at each target size.  The six final runs gave best values
`0.5220692609969371`, `0.5423261445466410`, and
`0.5411611830417189` for targets 41, 42, and 43.  No child reaches \(1/2\) or
improves the prior repository records.

The independent cross-result checker reconstructed all six structured
children and all six released endpoints.  SHA-256:
`a9332eadac1ea10e94d7f983030cf39f166b3f283165d06c33ed8fd8b10ebe10`.

Conclusion: no exact, interval-certified, or floating candidate meeting the
kissing threshold emerged.  The principal positive information is diagnostic:
the root-shell subset landscape contains strong multi-swap and
cross-cardinality traps, so failure of a locally optimized projected shell
cannot support an upper-bound argument.
