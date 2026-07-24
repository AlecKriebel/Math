# Hall-matching experiment log

## 2026-07-24

### 11:01 PDT — Experiment opened and proof criterion frozen

- Resumed the Boolean down-set route under a four-day maximum and a hard
  \(m=6,7\) computational boundary.
- Rewrote the safe-shadow collision deficit and the two unsafe-boundary
  terms as supplies \(d(P)\) and capacities \(b(P)\).
- Froze the first Hall graph as downward integer transport
  \(P\to Q\subseteq P\) with at most one deleted optional coordinate.
  Downwardness is essential: a full transport then restricts to every
  principal down-set and proves the desired inequality at that \(m\).
- Reserved exactly one possible enlargement, from at most one deletion to
  at most two deletions.
- Finite matching is explicitly classified as non-evidence unless
  alternating paths reveal a canonical all-\(m\) rule, a uniform
  bounded-congestion rule, or a genuine infinite lemma.

No outside communication occurred.

### 11:18 PDT — Raw radius-one transport succeeds at both gates

- Implemented an exact C++17 enumerator and integral max-flow verifier in
  `hall_transport.cpp`.
- For every parameter, the program independently recomputes the original
  \(e_0,e_1\) shadows and asserts the safe/unsafe identity before using its
  profile in a flow.
- At \(m=6\):
  \[
  \sum d(P)=11{,}155,\quad \sum b(P)=54{,}924,
  \]
  and the raw radius-one graph matches all \(11{,}155\) units.  Of these,
  \(713\) use a deletion edge.
- At \(m=7\):
  \[
  \sum d(P)=101{,}623,\quad \sum b(P)=384{,}072,
  \]
  and the raw radius-one graph matches all \(101{,}623\) units.  Of these,
  \(5{,}066\) use a deletion edge.
- Separate execution of `src/downset_diagnostics.cpp` exactly agrees on
  \[
  \begin{array}{c|r|r|r|r}
  m&R&e_0&e_1&\sum g\\ \hline
  6&35{,}594&51{,}901&27{,}462&43{,}769\\
  7&254{,}496&344{,}909&192{,}036&282{,}449.
  \end{array}
  \]
- The raw flows are not entirely greedy.  Their residual algorithms need
  level-five alternating paths for \(9\) units at \(m=6\) and \(209\) units
  at \(m=7\).  The final positive cross-edge supports nevertheless have
  height two in both cases.

### 11:27 PDT — Net one-deletion rule refuted; sole enlargement succeeds

- Collapsing the raw alternating relays suggests first cancelling local
  supply/capacity and transporting only the net signs of \(g\).
- The net radius-one graph fails:
  \[
  \begin{array}{c|r|r|r}
  m&\text{net demand}&\text{maximum flow}&\text{Hall deficiency}\\ \hline
  6&704&697&7\\
  7&4{,}857&4{,}699&158.
  \end{array}
  \]
- At \(m=6\), a maximum-deficiency Hall witness has the two left parameters
  \[
  \{1,4,5,6,9,10,11\},\qquad
  \{1,4,6,8,9,10,11,12\}.
  \]
  Their combined net demand is \(24\), while all nonnegative same/child
  neighbors have combined capacity \(17\).
- Spent the experiment's sole enlargement on deletion radius two.  The net
  graph then matches all demand at both \(m=6\) and \(m=7\).  A deterministic
  local-first greedy order uses respectively \(9\) and \(209\) units on
  double-deletion edges and requires no alternating repair.
- No radius-three test and no enumeration beyond \(m=7\) will be run.
- These are exact finite statements.  They do not prove an all-\(m\) Hall
  lemma and are not by themselves publication-worthy.

No outside communication occurred.

### 11:42 PDT — Independent implementation agrees

- Added a separate Python verifier using direct set semantics for
  \(\mathcal F,\mathcal A,\mathcal H\), typed boundary sets, and every
  profile-level deletion/contraction identity.
- Its flow solver is an independently implemented FIFO push--relabel
  algorithm rather than the C++ Dinic implementation.
- It reproduces all raw-radius-one and net-radius-one/two outcomes at
  \(m=6,7\), including the exact Hall witness sizes, capacities,
  deficiencies, and deterministic hashes.
- The full independent verification takes approximately 3.3 seconds on the
  local machine; additional hardware would not materially help this bounded
  capacity experiment.

No outside communication occurred.
