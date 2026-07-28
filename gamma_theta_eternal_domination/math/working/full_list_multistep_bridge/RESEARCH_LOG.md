# Research log: full-list multi-step bridge

- **2026-07-28 PDT.** Read the accepted C-108, C-122, C-127, and C-128
  artifacts and reconstructed the C-128 rank-three attack tree.
- **2026-07-28 PDT.** Isolated the first closure layer absent from C-128:
  after a full response to \(x\), attacks at physical inactive vertices
  \(B=N_{\overline G}(x)\) force retained states of the form
  \(\{x,s_i,b\}\).
- **2026-07-28 PDT.** Proved the retained-palette theorem:
  every \(b\in B\) has at least two retained root-anchor partners, its
  unique spoke anchor is mandatory, and each retained partner forbids all
  \(H[B]\)-neighbors in that anchor's spoke.
- **2026-07-28 PDT.** Derived spoke independence and the two-spoke
  component theorem when \(B\) has no anchorless vertices and \(H[B]\)
  has no isolates.  C-127 supplies the latter condition in the
  equality-critical deletion branch.
- **2026-07-28 PDT.** Replayed the C-123 and C-128 controls.  Both fail at
  this exact second-attack layer.  In C-128, the failures are the
  same-spoke edge \(15\) and the non-dominating forced states
  \(\{11,1,8\}\) and \(\{11,5,8\}\).
- **2026-07-28 PDT.** Audited the accepted exact equality control
  `Ksv`f\knJVis`.  Its retained palettes all have size two and its two
  physical inactive components have different spoke signatures.  This
  cleanly locates the remaining component-palette synchronization issue.
- **2026-07-28 PDT.** A bounded discovery sweep exhaustively checked all
  \(2^{19}=524,288\) labeled two-vertex extensions of the fixed
  \(L(K_{3,3})\) deletion control, all exact ridge-covariant markings
  reached after the filters, and all full roots.  Seventy-two extensions
  passed the C-128 static layer; none passed the new full-root
  second-attack test.  This is recorded only as an observation, not as a
  universal or independently certified finite result.

