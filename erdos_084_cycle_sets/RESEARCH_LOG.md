# Research log

All times are America/Los_Angeles.

## 2026-07-23

### 12:00 PDT — Program initialized

- Created a dedicated research folder on the repository's `main` worktree.
- Recorded the exact target and the requirement that no incomplete argument be
  represented as a solution.
- The original workspace was on a dirty unrelated branch, so work was isolated
  in the already-existing clean `main` worktree without touching those changes.

### 12:08 PDT — Protected framework recovered

- Reconstructed the exact generator
  \[
  G_{k,P}(b)=\{b,-b\}\cup((b-P)\cap[-k,k])
  \]
  and union family \(\mathcal F_k(P)\).
- Independently reproduced in-memory all previously recorded \(S_1,\ldots,S_7\).
- Recovered the geometric protected construction, eight-way lift, sharper
  union-shadow recurrence, and trace statistic.
- Recovered candidate exact values of \(E_m\) and the trace totals through
  \(m=7\); repository-level independent verification is now being built.
- Identified the next proof target as an averaged collision-energy bound, not a
  pointwise fiber bound.

No outside communication occurred.

### 12:55 PDT — Exact verification and first collision falsification

- Added and ran the standard-library exact verifier:

  ```sh
  python3 -m unittest discover -s tests -v
  python3 src/signature_counts.py --max-k 7
  ```

- All five tests passed. Exact enumeration reproduced \(S_m\), \(E_m\), and
  the trace totals through \(m=7\).
- Defined restricted-witness mass \(W_m\), collision energy \(Q_m\), and
  distinct output count \(D_m\). Global Cauchy--Schwarz shows that
  \(Q_m=O(mW_m)\) would imply trace mass \(\Omega(8^m/m)\).
- Exact exhaustive enumeration at \(m=8\) found
  \[
  W_8=3{,}145{,}728,\qquad Q_8=26{,}055{,}940.
  \]
  Therefore the appealing constant-one guess \(Q_m\le mW_m\) fails for the
  first time at \(m=8\), by \(890{,}116\). The theorem-strength
  \(Q_m=O(mW_m)\) target remains open.
- Separated a second logical gap: trace mass must still be converted to
  union-shadow excess. The pointwise inequality \(e_0(P)\ge R_m(P)\) is
  false; an aggregate version is supported by small computations but is not
  proved.

No outside communication occurred.

### 13:02 PDT — Second moment abandoned; support size survives

- Added an independent C++17 verifier for restricted collision fibers. It
  exactly cross-checks the Python values through \(m=7\).
- Extended exact enumeration through \(m=10\):
  \[
  Q_m/W_m=8.282960,\ 15.580217,\ 30.387826
  \quad(m=8,9,10).
  \]
  The near-doubling makes \(Q_m=O(mW_m)\) implausible; the unweighted second
  moment is dominated by a growing high-multiplicity tail.
- In contrast, the exact distinct-output counts satisfy
  \[
  mD_m/8^m=0.743034,\ 0.713559,\ 0.679569
  \quad(m=8,9,10).
  \]
  The theorem-scale conjecture \(D_m\gg8^m/m\) therefore survives. The active
  techniques are now truncation, entropy, and canonical representatives.

No outside communication occurred.

### 14:15 PDT — Full shadow enumeration and proof-target refinement

- Added an independent C++17 full-family verifier and extended exact counts
  through \(m=10\). In particular,
  \[
  \begin{aligned}
  S_{10}&=5{,}021{,}202{,}766,\\
  E_{10}&=626{,}972{,}078,
  \end{aligned}
  \]
  and \(mE_m/S_m\geq1\) for every \(2\leq m\leq10\)
  (the value at \(m=10\) is approximately \(1.248649\)).
- Consequently, the exact finite data support the single aggregate inequality
  \(mE_m\geq S_m\). If it holds eventually, the protected recurrence gives
  \(S_m/8^m\gg m^{1/4}\), and hence the lower half of Erdős Problem 84.
- A rank-pairing inequality and a Boolean down-set inequality were isolated as
  possible routes to the aggregate estimate. They were marked as conjectural
  pending exact stress tests.
- Audited publicly indexed descriptions of Dunås's 2026 thesis. The abstract
  reports a computable lower bound and numerical evidence for the conjectured
  limit, but the primary PDF could not be retrieved in this environment.
  Therefore no novelty or priority claim is made.

No outside communication occurred.

### 14:38 PDT — Rank route refuted; orbit route isolated

- Exact rank-pair tests refuted the proposed pointwise pairing:
  the minimum paired ratio falls below \(1\) at \(m=9\), reaching about
  \(0.784321\) at \(m=10\). This route is no longer treated as viable.
- For the cyclic/complement multiset orbit
  \[
  \mathcal O^*(P)=\{\rho^jP,\rho^j\overline P:0\leq j<2m\},
  \]
  exhaustive computation for \(5\leq m\leq8\) supports the precise lemma
  \[
  \sum_{Q\in\mathcal O^*(P)}e(Q)
  \geq \frac{a(P)}{2m^2}
       \sum_{Q\in\mathcal O^*(P)}q(Q),
  \]
  where \(a(P)\) is the cyclic equal-adjacency defect count. The minimum
  normalized ratio at \(m=8\) is approximately \(0.585695\).
- Added a separate exact orbit verifier. It corrected the \(m=8\) bookkeeping
  to \(2{,}068\) total orbits, of which \(2{,}067\) are nonalternating, and
  extended the check to \(m=9\), where the minimum is
  \(0.519819418576>1/2\).
- A further exhaustive run at \(m=10\) refuted the attractive constant
  \(c=1/2\): the minimum is \(0.428738331457\), at defect \(a=16\).
  The conditional reduction only needs some fixed \(c>0\), so the route
  survives, but the observed decline is now an explicit falsification risk.
- Proved the unconditional orbit baseline
  \(\sum_{\mathcal O}(e_0+e_1)\ge|\mathcal O|/2\), by pairing orbit elements
  under complementation and using the empty signature whenever \(1\in P\).
  Its corresponding constant is exponentially small, so it does not solve
  the harmonic-gain problem.
- Strengthened this to the rigorous additive defect bound
  \[
  \sum_{\mathcal O}(e_0+e_1)
  \geq2^{(m-1)a(P)/(4m)-1}.
  \]
  It uses independent safe rows exposed by \(00\)-edges and cyclic window
  averaging. It is still not weighted by \(q_m\), so it remains insufficient.
- Refuted the proposed pointwise skew-shadow lemma at
  \(m=10,\ P=[10]\): \(V(P)\) has no reflected pair, but
  \((e_0,e_1,R_m)=(41,9,52)\), giving deficit \(-2\).
- Reindexed the generator system so that a cyclic shift aligns the Toeplitz
  parts of adjacent rows exactly. This calculation shows that both fixed
  markers still shift; their union discrepancy can have \(\Theta(m)\)
  coordinates governed by the chosen row set rather than by defects of
  \(P\). This pinpoints why a naive cut-rotation injection fails.
- Added a sparse exact evaluator for a specified cyclic/complement orbit.
  Four-run continuations through \(m=14\) have
  \(\Lambda=0.3802,0.3535,0.2935,0.2959\) for \(m=11,12,13,14\),
  respectively, while \(m\Lambda\) stays near \(4\). This makes the explicit
  four-run family a plausible asymptotic counterexample to the fixed-constant
  orbit lemma.
- The low-transition exceptional family is already controlled rigorously by
  \[
  2\sum_{j\leq\delta m}\binom{2m}{j}
  \leq 2^{1+2mH_2(\delta/2)}.
  \]
  Thus the orbit lemma, with any fixed positive constant in place of
  \(1/2\), would prove the required global shadow estimate after discarding an
  exponentially negligible exceptional set.
- The remaining obstruction was identified precisely: cyclic rotation of
  \(P\) is not a symmetry of the generator family because the distinguished
  endpoints and the truncation cut move. A proof needs a bounded-congestion
  contraction across that cut.
- For the alternative Boolean down-set route, an exact deletion/contraction
  identity isolates the only negative term as a collision deficit among safe
  rows. The two positive terms are unsafe-row boundary expansions. The most
  obvious representative-preserving injection already fails at \(m=3\), so a
  successful proof must change representatives, use rank-preserving swaps, or
  prove a non-injective cardinality bound.
- A later audit corrected the associated row-migration description:
  \(p=m\) has no row \(b=0\), while at \(p=2m\) the endpoint row is already
  unsafe. Those two coordinates require separate deletion cases.
- Added an independent exact Boolean zeta-transform diagnostic. Both the
  down-set inequality and coordinatewise monotonicity survive through
  \(m=10\). At \(m=10\),
  \[
  \sum_{P\ni1}g_m(P)=99{,}485{,}474,
  \]
  the unique zero down-set is \(P_0=\{1\}\), and the minimum nontrivial first
  difference is \(352\).
- An independent line-by-line audit found the fan reduction, both protected
  bands, the free exponent, the eight-way lift, the union-shadow recurrence,
  the normalization, and the exceptional-set argument sound. The audit caught
  two omitted explanatory details: the base \(H_m(\{1\})\geq0\) for the
  down-set implication and injectivity of the full signatures arising from
  distinct new old-window shadows. Both were added to the proof notes.

No outside communication occurred.

## 2026-07-24

### 13:00 PDT — Program paused and public checkpoint prepared

- Closed the bounded Hall experiment at its prescribed \(m=6,7\) gates.
  No \(m=8\) matching enumeration, larger edit radius, or further template
  mining was performed.
- Classified the all-\(m\) twin-boundary identity and join-commuting fibre
  embedding as useful future-proof infrastructure, the one-local-edit
  mechanism as exactly refuted, and the Hamming-two matching as conjectural
  despite exact finite success.
- Recorded that the route remains at least two global mechanisms away from
  Erdős Problem 84: the trace lower bound and the trace-to-excess bridge are
  separately missing.
- Completed a publication audit. The correct artifact is a public research
  report, not a paper or preprint: there is no asymptotic improvement, and
  the sole clean all-\(m\) lemma has no independent consequence.
- Repeated the novelty audit against Alvin Dunås's 2026 thesis. The primary
  record and abstract confirm material overlap risk, but the 33-page PDF
  remained inaccessible after direct, browser, and proxy attempts.
  Consequently no component is described as literature-cleared novel.
- Prepared the paused-state status, resume criteria, literature audit, public
  page, social-preview image, source links, and site-index entry.

No outside communication occurred.
