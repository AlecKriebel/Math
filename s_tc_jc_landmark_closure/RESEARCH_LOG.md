# Research log

## 2026-08-09T20:15:00-07:00 — final-closure program opened

- Created a dedicated closure directory and branch from the verified
  weak-class release.
- Froze the sharpness theorem and its two independent verifiers.
- Rejected the withdrawn reciprocal-only bridge chart and every old atlas
  table lacking a primitive decorated graph-to-polynomial binding.
- Locked the only terminal outcomes as a fully certified positive sharp
  boundary or an exact certified `S_TC` counterexample.
- Began parallel work on corrected projective peeling, one-sided cut
  preservation, primitive generator enumeration, decorated-relation
  compilation, and adversarial counterexample search.

## 2026-08-09T20:27:23-07:00 — frozen weak theorem replayed

- Ran `../s_tc_jc_sharp_boundary/reproducibility/verify_release.py` from the
  verified release at parent commit `0c66eefc`.
- The release verifier checked the 288-file manifest, graph/class membership,
  six invariant identities, the exact quadratic interior point, all 256
  Fourier and pattern coordinates, and nonzero rank-eight minors for both
  parameterizations.
- The independent certificate SHA-256 reported by the release is
  `38266537a7966d83bdb94c6fb90fa68f93fbd227b82579f1bf311005925366d7`.
- The verifier entry point has SHA-256
  `90901ab2111c2aecf9eb27989f7136dd44f936cf2e6f9929772a8bba575fbba5`.
- This replay freezes only the theorem in `W_TC \\ S_TC`; it supplies no
  positive-classification input for `S_TC`.

## 2026-08-09T20:32:00-07:00 — independent gates dispatched

- Assigned the bridge/cut theorem to an implementation that may write only
  under `independent/bridge_cut/`.
- Assigned primitive decorated-atlas regeneration to a separate implementation
  that may write only under `independent/decorated_atlas/`.
- Assigned bounded exact counterexample search to a third implementation that
  may write only under `independent/counterexample_search/`.
- The primary implementation will not share graph canonicalization,
  switching, descendant-mask, relation-assignment, or separator-selection code
  with those implementations.

## 2026-08-09T20:45:00-07:00 — root atlas structurally reduced

- Wrote a candidate structural proof that a root-containing `S_TC` factor is
  represented by an ordinary incoming-port factor in the projective tensor
  quotient.
- The proof uses uniform-root JC reversibility, positive edge splitting, and
  the definition of `S_TC` over every admissible rooting.
- This route avoids the historically failed root weak-target promotion chain.
- Status remains candidate until a separate adversarial implementation checks
  all primitive root sites and retained-arrowhead cases.

## 2026-08-09T21:05:00-07:00 — primary generator/support layer rebuilt

- A new primary event-and-direction enumerator derived 24 normalized valid
  theta presentations, four theta classes, and the cycle core.
- The minimum repair multiset is exactly `1,1,2,2,2` across cycle/theta cores.
- A new completion compiler independently regenerated the exact
  `831/1983/4155/7909` weak-completion counts for three through six selected
  outgoing ports; every full completion is rooted binary and passes the
  standard-strong local criterion.
- A new rigid-support compiler generated 304 five-outgoing and 216
  six-outgoing decorated source presentations.  The extra 24 five-port rows
  are the support-plus-one marginals of the four-support core that the older
  direct five-port file omitted and later derived indirectly.
- Proved candidate marginal-submersion and probe-coherence lemmas.  These
  remain unpromoted pending the independent atlas and adversarial review.

## 2026-08-09T21:18:00-07:00 — ordinary T germ independently replayed

- Replayed both the historical primary triangle verifier and the independent
  JC-only release verifier in the clean environment.
- The independent output matched its frozen certificate byte-for-byte with
  SHA-256 `97097fa36e00edbf4837bbef3a255ccd756aac99136138746168ec94630df4dc`.
- Promoted only the JC common regular germ under ordinary `T`; no complete
  stochastic-image equality or richer-model statement is imported.

## 2026-08-09T21:25:00-07:00 — root reduction corrected before promotion

- Rejected the first candidate formulation because an artificial incoming
  character at a uniform root would not be observable.
- Replaced it by a real-boundary theorem: following tree/leaf children from
  an admissible tree-child root reaches an existing labelled boundary along
  an all-tree path; rerooting there reverses only ordinary arcs.
- JC reversibility then identifies the complete real boundary tensor, with
  only the corrected incidence-scaling gauge on the chosen arm.
- The correction removes the fictitious-port gap and is now the version sent
  to adversarial review.
