# Research log: QQ1 anchor–auxiliary ladder

- **2026-07-28 PDT — checkpoint 1.** Audited the exact discovery
  encoder behind the order-\(16\)/\(17\) CEGAR cores.  The formula
  includes \(i\)-extension, \(\alpha\le3\), literal family domination
  and one-guard closure, activity, the canonical QQ1 core, seven named
  retained states, one omitted state, and only selected
  pair-nondomination constraints; it is not a full encoding of
  \(\gamma\ge3\).  A discovery-only order-\(16\) ablation shows that
  \(i\)-extension, family closure, and activity are individually
  essential to that finite UNSAT outcome, while the additional named
  state units are not individually or collectively essential.
  Estimated completion of this focused all-order-gate audit: **35%**.

- **2026-07-28 PDT — checkpoint 2.** The same exact formula is SAT at
  order \(18\), refuting the proposed all-order anchor--auxiliary
  obstruction.  Froze the labeled model instead of extending the
  uncertified finite UNSAT lane.  Its stronger accidental property is
  that no dominating pair touches any vertex of the distinguished
  independent endpoint \(T=\{x,p,q\}\), yet thirty pairs away from
  \(T\) dominate.  Estimated completion of the focused refutation:
  **70%**.

- **2026-07-28 PDT — checkpoint 3.** Built an isolated bitmask verifier
  which decodes the fixed graph6 record, canonicalizes it with pinned
  nauty, recomputes all five parameters, all one-guard deletion waves,
  the 473-state greatest triple family, every named QQ1/bridge/bow-tie
  state and rank, all selected common-nonneighbor sets, and all thirty
  dominating pairs.  Identified three exact two-cycles in the
  anchor-witness relation, explaining why a naive fresh-vertex descent
  is not well-founded.  Estimated completion of the focused
  refutation package: **90%**.

- **2026-07-28 PDT — checkpoint 4.** The strict package replay passes:
  pinned canonicalization, graph6 and edge-list hashes, five exact
  parameters, all kernel waves, every named state and pair witness,
  the full dominating-pair list, package hashes, and scope labels were
  checked from the fixed graph.  The candidate is ready for a separate
  hostile review before central-ledger promotion.  Estimated completion
  of this focused refutation package: **100%**.
