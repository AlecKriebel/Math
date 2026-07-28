# Research log

## 2026-07-27 PDT

- Began a clean-room hostile audit of the separated-port extension scan.
- Reconstructed the response-list predicate from the one-guard definition.
- Identified and checked the anchor-incidence subtlety: because the anchor
  triple is independent, membership of a dominating direct-swap state itself
  forces the corresponding move edge.
- Added an implementation-independent tuple/set checker for both labeled
  scopes, the exact parameters of every positive case, and the ancillary
  canonical-class counts.
- Replayed all 14,336 labeled cases.  The exact per-row
  augmentation-sensitive witness counts matched the source manifests.
- Independently recovered the positive parameter distributions
  \((1,3,3,3)\) and \((2,3,3,3)\), with no positive graph of domination
  number three.
- Replayed every canonical graph6 record through `labelg`; all records and
  the four reported canonical-class counts matched.
- Final verdict: PASS for the bounded statement.  Recorded the sole
  nonmaterial defect, a `26` versus `27` typo in a source docstring.
- Rechecked the revised source after that typo was corrected.  The source
  now consistently says \(27\cdot2^9\); executable logic and frozen outputs
  are unchanged.  Final revised-source verdict remains PASS.

## Two-vertex addendum

- Independently decoded all \(2^{19}=524{,}288\) induced two-vertex
  extensions of the fixed old complement.
- Derived a separate exact \(K_4\) filter from the unique old triangle and
  the possible one-new/two-new \(K_4\) forms.
- Reproduced exactly six static \(\gamma=\alpha=3\) survivors and directly
  recomputed both parameters.
- Replayed literal one-guard greatest-kernel deletion with ordinary sets.
  Every survivor had 62 dominating triples, deletion histogram \(45,17\),
  empty final kernel, and reference-state deletion rank two.
- Matched all six target codes, complement neighborhoods, and graph6
  records.  Verdict: PASS for the precise bounded computation; universal
  implications remain explicitly excluded.
- Rebound the main hostile review to the final separated-port note bytes,
  whose only later change records the completed independent verification.
