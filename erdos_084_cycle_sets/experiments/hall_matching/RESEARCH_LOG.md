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
- Reversing the source and edge priority changes those double-deletion totals
  to \(7\) and \(199\) and radically changes the deletion-pair labels.
  Therefore the default \(9,209\) and their apparent coordinate patterns are
  algorithm artifacts, not canonical DC statistics.
- No radius-three test and no enumeration beyond \(m=7\) will be run.
- These are exact finite statements.  They do not prove an all-\(m\) Hall
  lemma and are not by themselves publication-worthy.

No outside communication occurred.

### 11:27 PDT — Independent implementation agrees

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

### 11:28 PDT — Twin-boundary identity proved for every \(m\)

- Proved that \(G_{m,P}(-m)=\{-m,m\}\) and, for every safe signature
  \(A\), the unsafe trace \(A\cup\{m\}\) has exactly the same
  \(U\)-join as \(A\).
- Consequently the two positive boundary families in the safe/unsafe
  decomposition are identical setwise for every \(m\) and every \(P\ni1\).
  With
  \(\mathcal B_P=(\mathcal H_P\vee U)\setminus\mathcal H_P\),
  \[
  e_0=|\mathcal A_P\vee U|+|\mathcal B_P|,\qquad
  e_1=|\mathcal B_P|,\qquad
  g_m(P)=2|\mathcal B_P|-d(P).
  \]
- The map \(A\mapsto A\cup\{m\}\) is an injective, join-commuting embedding
  of every safe collision fibre into the corresponding unsafe fibre.
- This is a genuine all-\(m\) structural lemma and reduces a typed matching
  to congestion two on one underlying boundary family.  It does not prove
  the required downward charge; the \(m=3\) obstruction has positive deficit
  and empty boundary.

No outside communication occurred.

### 11:30 PDT — Representation-aware gate and sole enlargement completed

- Added `representation_hall.cpp`, which expands collision fibres into their
  actual non-top safe signatures and retains the two typed copies of every
  boundary trace.  Every edge stores a certificate
  \((P,Q,B,B')\), and the final verifier recomputes and checks every graph
  edge from the original \(2m\) labelled generator rows.
- Corrected an ambiguity in the proposed gate.  The condition
  \(|B\mathbin\triangle B'|\leq2\) is not just one exchange: it also permits
  two additions or two removals.  Stage A therefore uses the exact local-edit
  condition
  \[
  |B\setminus B'|\leq1,\qquad |B'\setminus B|\leq1,
  \]
  while the sole enlargement, stage B, adds the two same-direction
  Hamming-two cases.  The downward parameter radius remains one.
- Reproduced every earlier \(m=3,4,5\) prototype value, including the
  \(m=5\) stage-B graph with \(56{,}669\) edges and matching \(1298/1298\).
- The exact representation-aware results are
  \[
  \begin{array}{c|r|r|r|r|r}
  m&|L|&E_A&\nu_A&E_B&\nu_B\\ \hline
  6&11{,}155&722{,}305&11{,}135&851{,}589&11{,}155\\
  7&101{,}623&9{,}145{,}839&101{,}355&
       11{,}249{,}586&101{,}623.
  \end{array}
  \]
  The stage-A residual Hall cuts have respectively
  \((|X|,|N(X)|)=(20,0)\) and \((276,8)\), giving exact deficiencies
  \(20\) and \(268\).
- Preserved the maximum stage-A matching before adding the new edges.
  At \(m=6\), the 20 repairs have alternating depths
  \(1^{11},2^9\); at \(m=7\), the 268 repairs have depths
  \(1^{69},2^{196},3^3\).  Every repair uses a new edge.  The final repaired
  matchings use 21 and 295 new edges, respectively.  All 21 at \(m=6\) are
  double removals; at \(m=7\), 285 are double removals and 10 are double
  additions.
- An independent direct-set Python implementation reproduces the complete
  \(m=6\) stage-A and stage-B edge counts, isolated vertices, and maximum
  matching cardinalities.  Strict compilation, an every-edge certificate
  audit, and ASan/UBSan checks also pass.  Peak memory at \(m=7\) was about
  \(715\) MB, so additional hardware is unnecessary.
- The shallow repairs are a useful conjecture generator, but they do not yet
  expose a unique canonical all-\(m\) rule: 32 coarse repair templates occur
  at \(m=7\), and double additions first appear among the final repairs.

No outside communication occurred.
