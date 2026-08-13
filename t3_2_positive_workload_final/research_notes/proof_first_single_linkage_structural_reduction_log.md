# Research log: proof-first single-linkage reduction

## 2026-08-12 02:54 PDT

- Read the scoped literature audit, the one-active multi-service repair,
  the audited exceptional two-species theorem, and the current classwise
  composition note.
- Derived the exact identity that the top stochastic tier is the highest
  deterministic tier containing an eventually enabled complex.  Hence the
  Anderson--Cappelletti--Kim inclusion fails exactly when the whole top
  deterministic tier is disabled.
- Proved structurally, using binary molecularity only, that every disabled
  divergent top complex is an active-plus-zero mixed complex.
- Refuted the proposed reduction to one divergent species with the full-rank
  one-linkage cycle
  \(0\to A+C\to B+C\to C\to0\) on \((n,n,0)\).  Recorded explicit
  executable coordinate-increment and coordinate-decrement words showing
  irreducibility on the whole nonnegative lattice.
- Classified the two-active failed faces without orientation or support
  enumeration: balanced top \(\{A+C,B+C\}\), and the two separated-scale
  singleton-top cases.
- Formulated the exact all-clock mesoscopic carrier-return lemma needed for
  arbitrary \(\ell\), common \(G_\ell^4\) drift, endpoint moments, duration,
  path-labelled boundaries, and marked no-history handling.
- Identified the remaining analytic obstruction: the carrier can branch via
  \(C\to2C\), and the subdominant cloud can have a quadratic countable base
  trace.  Existing subpower one-active Green estimates do not apply
  uniformly at a macroscopic two-cloud entrance.
- No canonical certification flag or finite selector was changed.

## 2026-08-12 03:17 PDT

- Proved the balanced two-active carrier theorem for every strong graph on
  a support between
  \(\{A+C,B+C\}\) and \(\{0,C,2C,A+C,B+C\}\).
- The proof uses an auxiliary mixed-source trace only to index histories.
  Every pure-source clock is restored as an included \(O(N^{-1})\) defect.
  Strong connectivity gives geometric internal exits and geometric neutral
  attempts; at most two mixed-to-pure exits produce a net cloud service.
- Proved centered endpoint and physical-duration moments, a
  superpolynomial included localization bound, the actual factorial-linear
  entropy decrement \(-\log N+O(1)\), and arbitrary-\(\ell\) common
  \(G_\ell^4\) drift.
- Narrowed the remaining analytic obstruction to the separated-scale support
  family, where a \(B,2B,B+C\) base trace may be quadratic and \(B\) need
  not be subpower relative to \(A\).

## 2026-08-12 03:10--03:45 PDT

- Identified the exact level \(H=A-C\) for the separated support
  \[
  \{A+C\}\subseteq{\cal C}
  \subseteq\{0,B,2B,C,2C,B+C,A+C\}.
  \]
  Zero-level source/target reactions cancel exactly, including nested
  carrier openings. Cofactor-bearing sources are not neutral and must be
  paid; the proof stops and includes their first firing.
- Derived the arbitrary-scale clean potential \(J=B+dC\), where
  \(d\in\{0,1,2\}\) is maximal pure spectator degree. Dominant macros kill
  or decrease \(J\), positive moves lose one molecular degree, and exact
  returns have a bounded directed-cut inverse.
- Closed the mesoscopic sourcewise estimate: paid sources are only
  \(C,2C,B+C\), hence have spectator degree at most one and race the
  \(A+C\)-clock at order \((1+B)/A\). Ordered Green summation pays this by
  either an old-\(A\) service or spectator factorial descent.
- Recorded that the balanced witness
  \(\{0,C,A+C,B+C\}\) is full-rank deficiency zero:
  \(m=4,l=1,s=3\).
- Froze the separated theorem during hostile audit at SHA-256
  08c216dcf5926484e39edcab22df9ab119cd45f63f3f605154d6193a01c9f558.
  It renders cleanly with Pandoc.
- Wrote a separate fixed-class composition theorem joining published
  pure-multiple and deficiency-zero branches, the analytic two-species
  classification and audited exception, the three-species obstruction
  theorem, balanced and separated carrier blocks, nonexplosion, compactness,
  and an explicit random-time Foster lemma. Its SHA-256 is
  f1471c0cd7373a9040264f8356ae6251580a9b9fbee10d255790a14eb7afb549.
- No finite orientation or population enumeration was used, and no
  certification flag was changed.

## 2026-08-12 03:45--04:15 PDT

- Hostile analysis found that frozen separated SHA
  08c216dcf5926484e39edcab22df9ab119cd45f63f3f605154d6193a01c9f558
  has the wrong entropy scale. On
  \(0\to B+C\to A+C\to C\to2C\to0\) with
  \(B=A/\log A\), clean service pays only
  \(-\log(A/B)=-\log\log A\), not \(-\log A\).
- Derived the corrected gap
  \(h(A,B)=\log(A/m(B))\), with \(m(B)\) the largest lower
  spectator monomial. Reworked the fourth-power proof macro by macro:
  killing pays \(G^3h\), maximal-degree spectator descent pays
  \(G^3\log B\), and lower-degree upmoves plus cofactor-source clocks are
  absorbed in ordered Green order. Large favorable spectator decreases are
  never converted into a symmetric terminal Taylor error.
- Resolved the cutoff seam: the included moving boundary terminates the
  local episode and is already paid by the Green tail. It returns to the
  global router. Fixed-scale promotion is a later state classification, not
  a continuation after the same stopping time.
- Expanded the two-disabled-top support into an all-clock bounded carrier
  theorem. A simple strong-graph path gives geometric clean attempts; the
  inactive top phase is finite, all lower competitors are included with
  \(O(A^{-1})\) weighted probability, and the endpoint gives
  \(-cG^3\log A\) drift. The alternatives are an exact
  \(A-B-C\) invariant or a frozen singleton face.
- The repair note SHA-256 is
  d86f6076913dc825f596ba3d8b3c3896881557e581813b999279415335aae9de.
  The composition theorem is now explicitly conditional, at SHA-256
  5a25515e036bf6f7b741be046595d99cb00cd253bea0c1370775786287ebf61b.
  Both render cleanly with Pandoc. No certification flag was changed.

## 2026-08-12 04:15 PDT

- Rejected the first log-gap repair after a sharper all-clock race check.
  In the cycle \(0\to B+C\to A+C\to C\to2C\to0\), the
  \(B+C\to A+C\) entry has probability \(B/A=e^{-h}\) after launch but
  raw stopped-endpoint cost \(\log A\). At
  \(B=A/\sqrt{\log A}\), its expected cost
  \(\sqrt{\log A}\) dominates \(h=\tfrac12\log\log A\).
- Therefore a cofactor-source entry cannot be stopped and paid singly.
  It must be retained as a nested carrier entry, assigned a pending
  allowance, and paired with its first subsequent active exit. A full
  all-clock carrier genealogy/operator is the remaining separated theorem.
- Marked the separated portion of the repair note REJECTED while preserving
  the logically independent bounded two-top candidate. Current note SHA is
  68e0a7e661715f86a519cf0119a23f39dd254e85ec6d56a8fd1a8cb74e057de3.
  Revised the composition note to remain explicitly conditional on the
  missing nested-carrier operator; its current SHA is
  36bee3b581e75b5813f8aeccd918f48d84f1bfb8409854b02c4c353f1a976fe8.

## 2026-08-12 04:30 PDT

- Replaced first-entry stopping by an exact pending-entry queue. Every
  lower-to-\(A+C\) entry increments \(D\); every \(A+C\)-exit consumes one
  pending unit, and the block stops only at an exit with \(D=0\).
  Pathwise, \(A=a+D\) before the stop and \(A=a-1\) at service, so the
  entire active factorial history telescopes exactly to \(-\log a\).
- Constructed the ideal Schur kernel on the no-fast state \((B,D)\).
  The correct all-insertion weight is
  \(\exp\{\theta[B\log(B+e)+D\log a]\}\). An entry from a source with
  \(B\)-degree \(j\) has race times weighted cost
  \((B^j/a)^{1-\theta}\); a debt-consuming exit to \(jB\) has weighted
  ratio \((B^j/a)^\theta\). Below the moving cutoff these are exponentially
  small in the logarithmic gap.
- Summed all nested insertions by a positive Neumann resolvent rather than
  charging their raw endpoints. The terminal active cost is \(-\log a\);
  the one-sided spectator cost is \(\log m(b)+O(1)\), yielding
  \(-h=-\log(a/m(b))\).
- The candidate full operator note is
  *proof_first_single_linkage_full_all_clock_nested_carrier.md*, SHA-256
  490f42487ec5045e17a7fa0dc1e69f61f836d17d0ee5ae3ce6af304fc7c230ac.
  It renders cleanly and is explicitly uncertified pending hostile replay.
- An independent hostile audit returned strict PASS for the balanced theorem.
  Before freezing, incorporated its three specification repairs: define the
  common potential before the statement, make the physical event priority
  explicit, and state the \(O(N^{-1})\) restored-clock estimate per mixed
  race before summing over the exponentially-tailed history.  Also recorded
  the allowed constant dependence.

## 2026-08-12 03:42 PDT

- Removed an unjustified over-strong formulation which demanded order
  \(A+B\) clean services with vanishing total defect probability.  Such a
  requirement is not needed and need not hold after accumulating physical
  competitor clocks over that many windows.
- Replaced it by the exact sufficient all-clock random-time Foster contract:
  a common physical stop for every fixed factorial-linear fourth power,
  actual post-jump endpoints, included open boundaries, polynomial endpoint
  and duration moments, and direct negative powered drift.
- Identified the canonical physical net-service count
  \(N_{A+C}^{\rm out}-N_{A+C}^{\rm in}=a-A_t\).
- Proved the separated-family invariant/service dichotomy without support or
  orientation enumeration.  If no non-top carrier complex is present,
  \(A-C\) is conserved and the face cannot diverge in one fixed class.  If
  one is present, a simple strong-graph path followed by an included
  \(A+C\)-source firing gives an executable bounded-length history with net
  \(A\)-service one.  Thus the remaining gap is uniform path probability and
  weighted endpoint control, not physical accessibility.
- Sharpened the remaining obstruction.  Individual service edges have the
  correct tier entropy gap, but a quadratic killed base trace must retain
  source propensity weights.  Crude terminal-displacement bounds lose too
  many \(\log B\) factors in the full mesoscopic regime.

## 2026-08-12 04:40 PDT

- Rejected the pending-entry candidate at SHA `490f4248...`.  On
  \(\{0,C,2C,A+C,B+C\}\) with cycle
  \(0\to A+C\to B+C\to C\to2C\to0\) and
  \(B=A^{3/4}\), stopping at the first surplus \(A+C\)-exit leaves
  \((A-1,B+2,C=1)\) and has positive factorial increment
  \(-\log A+2\log B=(1/2+o(1))\log A\).  The ledger identity is exact;
  the stopping boundary, not the ledger, is wrong.
- Replaced raw insertion bookkeeping by an exact factorial tilt.  With
  \(M_x(y)=\prod_i(x_i+1)^{y_i}\), every localized open-state edge obeys
  \[
    {\lambda_{yz}(x)\over\lambda_{A+C}(x)}
    \exp\{\theta\Delta G_\ell(x;y,z)\}
      \le C r_y^{1-\theta}r_z^\theta,
      \qquad r_y={M_x(y)\over M_x(A+C)}.
  \]
  Every noncarrier complex has \(r_y\le\delta_A=o(1)\), so the **full**
  all-clock open kernel has a same-exponent row norm
  \(C\delta_A^\theta=o(1)\).  This retains arbitrary nested carrier
  branching, including critical and supercritical genealogies, rather than
  truncating them.
- The remaining proof seam is now the cofactor-free return kernel.  Its clean
  maximal-source trace has only three nonexact dominant outcomes: spectator
  descent, net active service, or killing; positive spectator moves have one
  lower source degree.  The degree-zero case must be stated separately:
  its dominant clean return is exact, and every nonexact nonservice return
  contains an already tilted open lower-source firing.  A same-weight killed
  Green theorem plus a one-sided terminal exponential transform would finish
  the separated branch without any orientation enumeration.

## 2026-08-12 07:01 PDT

- Independently replayed the one-linkage tier classification without a
  support or orientation enumeration.  A failed tier has an entirely
  disabled top deterministic tier, and binary molecularity forces every
  top complex to be a mixed divergent-carrier/zero-cofactor complex.
  Splitting by one, two, or three divergent coordinates gives exactly the
  separated singleton-top, bounded two-disabled-top, balanced tied-top, and
  ordinary enabled-top branches.
- Proved that the whole linkage cannot occupy one deterministic tier along
  an escaping sequence in a fixed class: a normalized logarithmic limit
  would be a nonzero nonnegative exact conservation vector and would diverge
  on that class.
- Found and repaired a material interface error in the current conditional
  composition.  An enabled member of the top block need not itself carry an
  outgoing lower-tier edge.  A simple path from that enabled seed to the
  first top-block exit instead satisfies the independently audited physical
  access-word lemma, including all competitor clocks, arbitrary fixed
  positive endpoint moments, duration, and common fourth-power drift.
- Strengthened the balanced rank calculation: every proper support between
  \(\{A+C,B+C\}\) and
  \(\{0,C,2C,A+C,B+C\}\) is deficiency zero; the full five-complex
  support is the unique deficiency-one case.
- Froze the durable structural audit at
  `proof_first_single_linkage_structural_exhaustion_audit.md`, SHA-256
  `5b64e251035eedb3e5afe1d37881b3e1f4db45055ac5ab9a9ab165764720f0d1`
  after mechanical TeX repair and a clean Pandoc render.  This is a
  structural PASS only and does not promote the full one-linkage theorem
  before the separated stopped input is frozen and audited.

## 2026-08-12 07:20 PDT

- Independently replayed the balanced all-clock carrier theorem at target
  SHA-256
  `266d7dccfc0157d7ebb6ac2ae6ad5c4e0d5feb82bca5591472e44dc8e4f94c83`.
  The exact launch/exit ledger, directed-cut geometric minorization,
  restoration of every pure-source clock, centered endpoint and duration
  moments, factorial entropy decrement, and common fourth-power lift all
  pass for arbitrary fixed strong orientations and positive rates.
- Froze the strict local mathematical PASS in
  `proof_first_single_linkage_balanced_full_five_independent_audit.md`,
  SHA-256
  `54d2d3b84ce4139898fb7d6a6df57e09843af87e4030226227b3b741217dd7d0`.
  The audit certifies the full five-complex balanced support and, more
  generally, every nonvacuous sub-support in Theorem 5.1.
- Found one typesetting-only publication repair: the target places
  `\\tag{5.3}` inside an `aligned` environment.  Tectonic reproduces the
  `amsmath` error `\\tag not allowed here`.  Moving the tag outside the
  inner environment does not change the theorem or its mathematical PASS.

## 2026-08-12 07:30 PDT

- Applied only the audited tag relocation.  A direct diff against target
  SHA `266d7dcc...` contains no other change.  The header-identical
  derivative is frozen at SHA-256
  `8a34f9934f9ffdd078850070de561aa3cf3f734a9fbeb2e4f08bc68c5e106262`.
  With Pandoc's single-backslash-math reader enabled, Tectonic compiles the
  full ten-page note successfully.
- Updated the balanced audit to record exact derivative transfer and
  re-froze it at SHA-256
  `933c14cad99b8cf5bc1e2237f3be417aebfb344d1751f7c58be2b284c562d5ab`.
  Its seven-page Tectonic render succeeds.  The mathematical PASS is
  unchanged.
