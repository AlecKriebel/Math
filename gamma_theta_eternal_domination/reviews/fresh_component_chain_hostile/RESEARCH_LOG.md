# Research log: hostile audit of fresh-component chains

## 2026-07-28 (PDT)

- Read the complete frozen candidate and independently reconstructed the
  accepted C-079 odd-fan/side-purity, C-103 boundary-parity, C-133 bridge,
  and C-140 turning-ridge inputs from their pinned sources and hostile
  reviews.
- Rechecked every component membership, bipartition side, exact response
  list, selected color, collision edge, path parity, distinctness
  condition, and C-103 quantifier used by the candidate.
- Found that the original Theorem 3.2 omitted its binary/exact-two
  endpoint hypothesis.  Singleton sources \(\{w\}\) and \(\{v\}\) are
  additional terminal possibilities outside that scope.  Also required
  the first-reentry summary to distinguish a lollipop return from a
  two-unit trace ending at a separately pinned component.
- Required correction of three broken internal equation references and
  one malformed positive-marker label.
- Audited the revised candidate bytes.  The binary/exact-two restriction,
  singleton guardrail, conditional first-reentry wording, references, and
  marker text are now exact.  The downstream C-103 theorem already
  assumed a second exact \(\{u,w\}\) bridge source and needed no
  mathematical change.
- Wrote a clean-room set-based checker importing no campaign evaluator.
  It reconstructs both graph6 records, all five parameters, greatest
  kernels, the restricted 52-state family, every one-guard obligation,
  response lists, complement components and sides, list colorings,
  exposed positive mates, and dominating pairs.
- Independently confirmed `HEhbtjK` has parameter vector
  \((3,3,3,3,3)\), a 48-state greatest triple family, and 288 obligations.
  Its same-list sources see opposite target sides but are joined in the
  complement and hence have opposite source colors.
- Independently confirmed `HFzvvn{` has parameter vector
  \((2,2,3,3,3)\), an 83-state unrestricted greatest triple kernel, the
  claimed 52-state restricted eternal family with 312 obligations, zero
  compatible response-list colorings, and exactly 26 dominating pairs.
- Replayed both candidate checkers and the clean-room checker
  byte-for-byte.  Final verdict:
  `PASS_AFTER_REQUIRED_SCOPE_CORRECTIONS`, strictly local.  Arbitrary
  chains, lollipops, bicycles, complete \(k=3\), and the universal
  conjecture remain open.
