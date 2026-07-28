# Research log: order-13 single-full squeeze

## 2026-07-27 PDT

- Read the accepted full-list spoke/link, deletion, terminal-hitting,
  side-purity, and five-vertex witness notes.
- Refined the five-vertex proof using a literal one-guard attack.  If
  \(p\in A_u\) and \(y\in Y_{u,p}\), then \(y\) cannot miss a second anchor:
  attacking \(y\) from the appropriate direct full-response state leaves
  one immobile guard and two successors that each fail domination.
- Concluded that the three external witness layers are pairwise disjoint,
  improving the full-response non-neutral count from five to six.
- Built a bounded order-13 SAT probe fixing \(S=\{0,1,2\}\), \(x=3\), and
  one full response.  The first strengthened formula was UNSAT.
- Ablated uniqueness, connectedness, the old witness bound, and the
  redundant maximum-independent-state clauses.  The 9,802-variable,
  85,409-clause minimal formula remained UNSAT.
- Verified the ASCII DRAT proof with the pinned `drat-trim` executable in
  ordinary and RUP-only mode.  Retained the full formula/proof and reduced
  core/proof with hashes in `NOTE.md`.
- Ran the unsorted minimal formula for 120 seconds.  It timed out; this is a
  nonclaim.  Wrote the complete \(S_9\) covariance and orbit-representative
  proof for the four-bit signature sorter.
- Removing one-guard closure makes the formula SAT.  Removing the
  clique-cover gap also makes it SAT and yields the exact positive equality
  control `LF\|ul\XzVsaqJ`.
- Exact-\(|Q_S|\) discovery splits and fixed witness-layer cores were used
  only to extract the human anchor-purity theorem.  They are not promoted as
  finite results.
- Stopping status: human theorem proved; order-13 full-target exclusion has a
  checked solver certificate but awaits clean-room reconstruction and hostile
  coverage audit.  No global order-13 or universal claim.
