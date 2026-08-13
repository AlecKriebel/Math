# Root-Probe Adversarial Review Log

## 2026-08-09 21:32:24 PDT — Review initialized (5%)

- Scope locked to `reviews/root_probe/` for all newly created or modified artifacts.
- Target claims are hypotheses: real-boundary root reduction, exact primitive-generator exhaustiveness, pointwise support rigidity, marginal-submersion, probe coherence, and automatic at-most-one-triangle.
- Independence rule: primary graph/code implementations will not be read or imported until the mathematical claims and independent test semantics have been derived from the locked definitions and theorem documents.
- Existing repository state is dirty and is treated as user-owned. No pre-existing file will be modified by this review.
- The requested review directory did not exist and was created as the dedicated effort folder.
- Initial branch observed as `codex/stc-jc-landmark-closure`; no branch operation was performed.

## 2026-08-09 21:39:19 PDT — Scope amendment (8%)

- Added an explicit intrinsic selected-strength gate at the user's request.
- Strength will be decided from the selected restriction's own admissible
  rooting census, never from dummy leaves in a chosen completion.
- The sink-plus-minimum-repair criterion will be tested in both directions,
  including alternate repairs, mixed partial repairs, supersets, and cycles.

## 2026-08-09 21:51:49 PDT — Clean-room structural census (40%)

- Derived, without primary imports, exactly one cycle event core and four
  theta event cores: TT nested/separated and TR nested/separated.
- Exhausted every segment-occupancy pattern.  With every genuine sink port
  present, the intrinsic all-rootings `S_TC` census agrees exactly with
  “contains an inclusion-minimal repair.”  This includes all alternate repair
  presentations and the cycle's two symmetric singleton repairs.
- Recovered support sizes `2,3,4,3,3` (ordered as cycle, TT nested, TT
  separated, TR nested, TR separated).  Every alternate minimal support has
  pointwise stabilizer one.
- Checked every all-tree endpoint arising from every admissible rooting of
  every minimal support graph.  Each endpoint edge admits a rooting with exact
  inverse narrow suppression; no arrowhead, DAG, LSA, or tree-child failure
  was found.
- Enumerated the current `K4-e` marking universe and found zero tree-child
  admissible rootings.  A final pass will add the trivially impossible
  leaf-to-retic arrow markings so that the serialized universe is literally
  exhaustive rather than logically pruned.
- Preserved a semantic counterexample: omitting the unique cycle sink and
  fully reducing gives a two-boundary tree with one admissible, tree-child
  rooting.  Thus sink-plus-repair is **not** a criterion for generic intrinsic
  `S_TC` membership; it is a criterion for intrinsic strength **and retention
  of the original primitive core**.
- Certificate: `root_probe_certificate.json`, SHA-256
  `a3165f0cdff404ee16fec088547abb00e5c939a8d6c7522a08ffcd9fe0d4f286`.

## 2026-08-09 21:58:44 PDT — Label-quotient obligation added (45%)

- Added an explicit symmetric-group audit for the atlas's convention of
  anchoring source labels and enumerating target permutations.
- Required checks: full target factorial orbit, fixed incoming label, literal
  pointwise source rigidity, and absence of sink/repair-role filtering or
  premature automorphism/`T` collapse.

## 2026-08-09 22:23:26 PDT — Parameter, quotient, and red_* gates (72%)

- Added `docs/LOCAL_ATLAS_THEOREM.md` to the audit at input SHA-256
  `76325d20dc0d58a385d7ef438e5e856845891d23509d05968bef2e0c8d7fed54`
  (the repository is active; the final manifest will record the final audited
  bytes separately).
- Independently checked all 14,878 bounded completion parameter maps.  Every
  physical-to-descriptor product/identity Jacobian has full row rank.  In
  13,106 completions, switching columns repeat after core collapse, proving
  that the descriptor can be redundant even though the parameter-cube map is
  an onto submersion.
- Independently checked 12,396 restrictions of strong full expansions (all
  five cores, all ordered placements of three ordinary labels, and all
  nonempty selected subsets).  Dummy-completion descriptor coverage had zero
  failures; 8,652 restrictions genuinely lost at least one reticulation under
  ancestral `red_*` reduction.
- The implementation routes every equal non-core-retaining target to
  `pending_support_completion`; strict candidates remain in the algebraic
  relation stream.  The finite claim that all pending equalities are exactly
  the cycle-source/theta-target family remains unresolved until the active
  relation compilers finish and publish complete summaries.
- Verified the anchored-source quotient is surjective for outgoing sizes two
  through six: all `n!` relative target permutations occur, each from `n!`
  simultaneous assignment pairs.  No sink/repair role filter was found.
- Refuted uniqueness of the anchored representative.  Primary support record
  208 has pointwise stabilizer one but an order-two setwise label-action
  stabilizer; cycle and theta-0 supports acquire order-two setwise symmetry in
  the `T` quotient.  These cause duplicates, not omissions.
- Exhausted 8,976 two-extra-port presentations across 136 alternate labelled
  supports and found zero probe-deck coherence collisions.  Independent
  three-extra-label word tests were injective on 24, 210, and 336 ordered
  distributions for two, five, and six segments.
- Preserved four boundary/counterexample records in `counterexamples/` before
  proposing any wording corrections.

## 2026-08-09 — Incoming-role obstruction added (78%)

- Froze a new quantifier check before re-inspecting the implementation for
  this issue: individual rootability does not imply a rootable boundary
  common to a fixed source-target physical port matching.
- On the clean TT-nested minimum support, exact narrow rooting gives rootable
  real ports `{incoming, repair:p0e2}` and nonrootable ports
  `{sink:X1, sink:X2}`.  A second labelled copy can exchange these two pairs,
  leaving no matched real boundary admissibly rootable on both sides.
- The counterexample and a full support/bijection census are being serialized;
  local/global promotion is suspended pending repair of the incoming-label
  action.

## 2026-08-09 23:04 PDT — Incoming-role audit closed structurally (94%)

- Exhausted 2,808 ordered boundary bijections between all alternate minimum
  supports.  Exactly 144 have no matched rootable real boundary.  The exact
  four-port witness uses relative permutation `[2,3,0,1]`, which is in full
  `S_4` and outside the subgroup fixing structural incoming.
- Preserved `counterexamples/fixed_incoming_relative_role.json` unchanged;
  its exact SHA-256 before manifest sealing is
  `72e9c8a8d031dbc583473ee5b193b1516cff3cf7b2acbcdfd5fab899b9da209e`.
- Independently extended the completion-partition test to both incoming
  modes.  It found zero descriptor mismatches in 24,792 restrictions: 12,396
  with incoming selected and 12,396 with incoming marginalized.  Of these,
  17,304 lose at least one reticulation under ancestral reduction.
- Independently extended the parameter-cube test to the corrected bounded
  target universe.  All 42,908 maps have full row rank; 37,400 have repeated
  switching columns, confirming again that this is not a minimal tensor-image
  chart.
- The current bounded compiler source statically uses all `n+1` target
  boundary permutations and includes marginalized-incoming completions.  The
  cycle/theta union compiler still uses the old fixed-incoming four-outgoing
  enumeration and therefore cannot certify the local hard cover.
- Final verdict fixed: fixed-`INCOMING` **FALSE**, full target `S_p`
  **VERIFIED**, local theorem **UNRESOLVED**, global theorem **UNRESOLVED**.

## 2026-08-09 23:08:27 PDT — Final replay and scope closure (100%)

- `verify_all.py` completed with structural status `PASS` and
  `hard_cover_contract_satisfied=false`.  The latter is an intended verdict,
  not a replay failure.
- Final certificate SHA-256 values before manifest sealing:
  - root: `15126dea8763233b369bf15539a58d220fdc01f122144283b58268162f944700`;
  - probe: `85b0f3bb60200395a452b41faf289c6bda474929833263e363c67f853e4115b7`;
  - incoming: `55bbe8d63d783d67c31453a82c10b4e15181e8915562687fbb1e9b62e332e747`;
  - parameter: `2652537dc8232f4887601250a108278c57404a3a87e17677916d480e19b3a433`;
  - `red_*`: `45ae3349fd70538885b88abc38754c1c504daa38f4225a6e4c1717846df2f5b9`;
  - primary clean read:
    `4a280857fe0156b9219ae6e5af2d70cf46683ce0612fe86baa81ececc9408985`.
- All five preserved counterexamples remain present.  No primary theorem,
  source, certificate, or other file outside this review directory was edited
  by the review.
- The review goal is complete even though the local algebraic hard cover is
  unresolved: the requested deliverable is the adversarial verdict and exact
  evidence, not promotion of the candidate theorem.
