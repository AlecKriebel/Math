# Global Bridge/Cut Adversarial Review Log

## 2026-08-09 21:32:36 PDT — Review opened

- Scope locked to `reviews/global_bridge/` for all new and modified artifacts.
- Review target: `independent/bridge_cut/` and the bridge/cut/global arguments in
  `docs/GLOBAL_THEOREM_DRAFT.md`.
- Method: clean-room re-derivation first, source/code comparison second,
  independent exact checks and deliberate mutation tests where useful.
- Required attack surface: zero-sum incidence kernel, stabilizers, analytic
  slices, ordinary and crossing cut points, equality from one-sided cut-set
  containment, local-to-global necessity, converse gluing, continuous target
  choice, finite-union arguments, cross-blob compensation, compatible
  simultaneous `T` germs, and effective versus physical bridge parameters.
- Initial completion estimate: 5%.

## 2026-08-09 21:42:34 PDT — Source audit and claim split

- Verified the package manifest exactly: every listed source, proof,
  certificate, report, and definitions-lock digest matches.
- Read the complete bridge/cut proof, theorem draft, bridge verifier, mutation
  verifier, and the cut compiler/sign machinery.  Audited the cut compiler's
  full-completion logic separately from the selected tensor it represents.
- Important scope distinction: `rooted_valid` and `standard_strong` are applied
  to the full graph after omitted roles are restored by zero-character dummy
  leaves.  The selected three- or four-port marginal is allowed to be weak
  after `red_*`; dummy leaves do not prove that the selected marginal itself is
  weak (or strong).
- Found a documentation gap, not yet a mathematical counterexample: the
  package states only `Cut(source) subset Cut(target)`, whereas the global
  draft uses equality.  Under the locked definition of source-relative
  containment, the reverse inclusion has a separate direct proof: every
  target cut rank equation holds on the shared source-open set, contradicting
  pointwise strict rank if that split were a source noncut.
- Found one literal overstatement to test: “arbitrary positive effective
  bridge scales” is stronger than needed and generally false for a fixed
  sliced local point; only a common positive open interval (obtainable near
  zero) is required for gluing.
- Completion estimate: 28%.

## 2026-08-09 21:59:07 PDT — Independent exact replay complete

- Wrote `exact_audit.py` without importing any `independent/bridge_cut`
  implementation module.  It uses the published JSON only as input data and
  independently rebuilds the zero-sum bridge design matrices, primitive
  orientation census, full-completion graph checks, switching masks, Fourier
  tensors, endpoint polynomials, one-active minors, and two-active blocks.
- Exact results: five independent leaf-supported bridge kernels equal the
  incidence image; removing leaf support exposes extra kernel; theta/cycle raw
  orientation counts are `102/12`; all 147 nonordinary witness graphs validate;
  129 of those use at least one dummy completion leaf; endpoint cases are
  `67 F-positive + 9 F-zero/G-positive + 1 ordinary`; all 204 one-active
  minors have the published strict sign; the two-active construction has 20
  nonzero minors up to sign and all required identities have remainder zero.
- The selected-marginal guard is explicit in the certificate:
  `selected_marginal_strength_asserted=false`.  Full strongness was checked on
  dummy-restored completions only.
- Wrote 15 independent mutation tests.  They reject illegal complementary
  zero-sum anchoring, character-specific incidence scales, omitted ordinary
  endpoint, changed graph transport/minor, `z^2 -> z`, reciprocal-only gauge,
  physical-edge recovery, dummy-implies-weak inference, coupled arms, both
  finite-union overclaims, all-positive effective-scale recovery, and omission
  of the reverse cut inclusion.
- Completion estimate: 76%.

## 2026-08-09 21:59:07 PDT — Global necessity and converse audit

- **VERIFIED:** intrinsic extraction localizes a source-open product box with
  no continuous choice of target parameters.  A finite target role union has
  one member containing a source-open full-dimensional subgerm.
- **FALSE as literally worded in `PROOF.md`:** a finite cover need not put the
  entire focal source germ in one member.  The interval cover
  `(-1,1)=(-1,0] union [0,1)` is an exact counterexample to that stronger
  sentence.  The weaker statement needed for local `preceq` is verified.
- **VERIFIED:** both cut directions.  The reverse direction uses the target
  cut rank equation on the shared source-open set; it does not reverse the
  one-sided relation.
- **VERIFIED:** no cross-blob compensation after cut equality, both by
  intrinsic projective extraction and by the independent adjacent-arm
  Jacobian.
- **VERIFIED conditional gluing lemma:** finite products of compatible local
  regular `T` germs glue simultaneously after choosing one sufficiently small
  common effective interval per bridge.  Effective and physical bridge
  parameters remain distinct.
- **FALSE mutation:** all positive effective scales need not be physical at a
  fixed sliced point.  The current global draft was concurrently tightened to
  the correct sufficiently-small-interval formulation and was audited at
  SHA-256 `a7defc76948b44f2afafc9184548469e6d38b1511e7aaca327e09a73b9134f82`.
- **UNRESOLVED:** the final global classification remains dependent on the
  separate bounded local atlas, probe coherence, and root reduction.
- Completion estimate: 94%.

## 2026-08-09 21:59:07 PDT — Final replay

- `verify_all.sh` passes for the independent audit and all 15 mutations.
- The package's bridge, cut, and mutation verifiers were replayed with outputs
  redirected into this review folder.  The outputs are byte-for-byte equal to
  the published certificates, with SHA-256 values
  `64c319b5...`, `da477332...`, and `956bf612...` respectively.
- `REVIEW.md` records explicit **VERIFIED**, **FALSE**, and **UNRESOLVED**
  statuses and all corrected deductions.
- Final completion estimate: 100%.
