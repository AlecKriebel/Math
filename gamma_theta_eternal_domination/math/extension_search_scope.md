# Complete one-vertex-extension kill test

## Status

Coverage proof and finite search specification, drafted 2026-07-25. The
enumeration result is not yet claimed here.

## Host universe

The audited MMV (2022) Table 9 catalog contains exactly 55 connected graphs
\(H\) satisfying

\[
 \alpha(H)=\gamma^\infty(H)=3<4=\theta(H).
\]

Their domination numbers split as follows:

- two order-10 and 51 order-11 hosts have \(\gamma(H)=2\);
- two order-11 hosts have \(\gamma(H)=1\).

Every connected one-vertex extension \(G\) of a host \(H\) is obtained by
adding a new vertex \(x\) whose nonempty open neighborhood is an arbitrary
subset of \(V(H)\). Conversely, every nonempty subset produces a connected
one-vertex extension because \(H\) is connected. Thus enumerating all
\(2^{|V(H)|}-1\) nonempty neighborhoods is a complete labeled cover.
Canonical labeling with pinned nauty/Traces 2.9.3 and global deduplication are
intended to remove only isomorphic copies. Before an empty run is labeled
`CERTIFIED-FINITE`, a separate coverage audit must reconstruct every raw
extension and independently verify its isomorphism to the stored canonical
representative.

The raw finite universe has

\[
 2(2^{10}-1)+53(2^{11}-1)=110{,}537
\]

labeled extensions before isomorphism removal. The 55 empty-neighborhood
extensions are disconnected and are excluded by the proved connected
reduction.

## Exact counterexample test

Because \(H\) is an induced subgraph of \(G\),

\[
 \alpha(G)\geq\alpha(H)=3,\qquad
 \theta(G)\geq\theta(H)=4.
\]

If \(D\) dominates \(H\), then \(D\cup\{x\}\) dominates \(G\), so

\[
 \gamma(G)\leq\gamma(H)+1.
\]

Consequently, an extension of either \(\gamma(H)=1\) host has
\(\gamma(G)\leq2\) and cannot be a counterexample with common parameter
at least 3. These 4,094 raw extensions may be generated for coverage and
parameter-delta logging, but are soundly pruned from the decisive game test.

For each of the remaining

\[
 2(2^{10}-1)+51(2^{11}-1)=106{,}443
\]

raw extensions of \(\gamma(H)=2\) hosts, one has \(\gamma(G)\leq3\). Such an
extension is a counterexample if and only if all three conditions hold:

1. no vertex pair dominates \(G\), so \(\gamma(G)=3\);
2. no independent 4-set exists, so \(\alpha(G)=3\);
3. a nonempty one-guard eternal family of 3-sets exists, so
   \(\gamma^\infty(G)=3\).

Indeed, the inherited bound \(\theta(G)\geq4\) then gives

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3<\theta(G),
\]

and the parameter chain automatically gives \(i(G)=3\). No coloring
computation is needed to establish the strict clique-cover gap, although any
candidate will receive a fresh exact \(\theta\) computation and certificate.

Conversely, if an extension of a domination-two host is a counterexample,
equality collapse gives
\(\gamma(G)=\alpha(G)=\gamma^\infty(G)\).  The inherited inequality
\(\alpha(G)\geq3\) and the extension bound \(\gamma(G)\leq3\) force this
common value to be 3.  The three conditions above are therefore necessary as
well as sufficient.

## Reproducibility and termination gate

- Generate and checkpoint one host at a time.
- Canonicalize every extension with pinned nauty/Traces 2.9.3.
- Store the raw count, canonical stream hash, origin multiplicities, and
  unique count.
- Independently audit that every host has exactly the prescribed mask
  interval, each raw record reconstructs from its host and mask, every raw
  record is isomorphic to its stored canonical record, and every unique
  canonical record has exactly one exact evaluation.
- Run both independent implementations on every graph reaching the decisive
  three-condition filter.
- Freeze the first candidate before minimization.
- Initial budget: 45 minutes wall time, one CPU-heavy process, and 1 GiB
  campaign memory. If that gate is exceeded, stop at a completed host
  checkpoint and profile before resuming.

An empty result proves only that this explicitly delimited extension universe
contains no counterexample. It does not prove the order-12 slice or the
universal conjecture.
