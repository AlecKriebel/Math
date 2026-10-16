# Classification and invariant audit: PR301/problem30004365

## Disposition

**CONDITIONAL CLASSIFICATION PASS; ADDITIVE SOURCE/PROOF CORRECTION REQUIRED.** The submitted complete numerical key is correct for nonzero finite-dimensional gentle bound quivers over the fixed source field, conditional on correct surface construction and winding computation. Its genus-one gcd, higher-genus branches, paired end records, and component multiset extension are justified. No classification counterexample to that key was found. The basis encodings and raw handle windings must remain certificate data, excluded from comparison, as the candidate already specifies.

The standalone appeal to the printed final APS7.4 sufficient direction must be replaced by the all-end compact-core LP1.2.4 + APS6.1/7.2 derivation. That published truncated iff is actually false when p>0; it is not merely harmless indexing ambiguity. A concrete exact witness and the additive corrected argument are provided in this namespace without editing submitted files.

## Independent proof and source record

Independent obligations were established from TURN_1.md and original Plamondon Problem3.4 before historical review. Full original OWR printed161–164, final APS§§3,6,7, and LP§§1.1–1.2 including proof were read. Formula pages were inspected visually. Full EMS, final publisher APS, and PPP PDFs were independently acquired and their hashes match original pins. LP was acquired as the extra primary topology source. Native source/request/start/PID/UTC/duration/exit/full stdout+stderr/hash custody is in evidence/.

The strongest theorem proved here is in INDEPENDENT_CLASSIFICATION_THEOREM.md: exact K equality if and only if derived equivalence, with arbitrary puncture permutations, positive marked-boundary versus zero-mark puncture distinction, correct APS/LP orientation conversion, handle independence, full radical/spin conditions, and intrinsic connected-factor preservation. It invokes only established topology/classification results and does not manufacture novelty from them.

PRINTED_RANGE_COUNTEREXAMPLE.md gives A(3,5) versus A(4,4), formed from bridge-connected full-relation cycles. Both have8 vertices,9 arrows, dimension20, genus0, one boundary, two black punctures, seven white boundary marks, and boundary winding6. Their puncture winding multisets{-3,-5} and{-4,-4} disagree. The candidate correctly distinguishes them. The printed APS7.4 with equality only on j<=b and the workshop's omitted peripheral summary do not.

## Exact supplementary controls

The final source is check_classification.py, SHA256effc769c7565a6d1643b135ed6829ea73e75c9a188bff6fc6e5593bf883a156f. Native controls_03 completed with **457,019 actual assertions**, plus **983,040 separately counted orbit-edge evaluations**. CONTROL_RESULTS.json records the full result. These are finite exact algebraic checks, not a surface algorithm implementation or universal proof.

- All quadratic refinements in symplectic dimensions2,4,6 satisfy the quadratic identity, the Arf zero-count formula, and every tested symplectic transvection. Arf class counts are3/1,10/6,36/28.
- Adding a radical class with q=0 leaves handle Arf unchanged; q=1 changes it in32 of64 tested lifts. This falsifies a handle-only Arf invariant outside the candidate's guarded spin branch.
- Genus-two mod4 refinement orbit sizes match the LP branches: peripheral q=0 gives6,10,240; q=1 or3 gives256; q=2 gives16,240. These controls include peripheral handle shifts.
- Rank-two winding ideals survive integer shears, sign/swaps, and peripheral corrections. An explicit control shows omitting w(c)+2 changes the invariant under a peripheral detour.
- The exact quiver witnesses satisfy gentle degree, predecessor and continuation conditions, have permitted path counts8,9,2,1, and seven maximal finite permitted paths each.
- A paired-record trap confirms separate marginal count/winding multisets would lose information; the candidate correctly keeps pairs.

controls_01 failed with a final list-versus-integer TypeError and produced no PASS result; its failed source and streams are preserved. controls_02 passed but its total mistakenly included orbit-edge evaluations under the assertion label. controls_03 corrects that bookkeeping and is the authoritative final count. No earlier run is hidden or retroactively relabeled.

## Mandatory versus optional findings

Mandatory for the claimed complete-key proof: use CLASSIFICATION_ADDENDUM.md's all-end LP argument (or an equivalent explicitly proved consequence), rather than relying on the false literal printed APS7.4 iff. This is a proof/source repair requiring no numerical algorithm change.

Optional precision: explicitly restrict the opening input promise to nonzero algebras, or output the empty multiset for the empty quiver; state that the workshop's total per-boundary marks are twice the candidate's white count; replace the categorical-central-idempotent shorthand by the projective-detection factor proof. The isolated field model is consistent with one dissection arc and key(0,1,0,{(2,2)},empty).

After the independent derivation was recorded, the historical INDEPENDENT_REVIEW.md was read. It agrees on paired records, puncture necessity, basis data exclusion, field, and component scope. Its conclusion that no mathematical alteration is required understates the sourcing gap: it repeats the printed sufficient-condition argument without an exact counterexample or the full LP compact-core deduction. Its Arf-only controls do not test peripheral radical descent or the mod4 orbit branches. This audit adds those checks without treating historical control totals as mathematical acceptance.

## Remaining gap and blocked routes

Remaining work for whole-candidate acceptance is with the other approach families: PPP/APS convention and surface reconstruction, total effective PL enumeration/acceptance, winding computation for every certificate, and translation to quiver walks if required. This audit is complete within its classification scope and does not certify those components.

The route “the literal printed APS7.4 iff suffices even when puncture winds are dropped” is **blocked**, with the A(3,5)/A(4,4) exact counterexample. The route “take integer-linear homology winding values and omit peripheral corrections” is **blocked**, with the pair-of-pants identity and explicit gcd control. The route “use handle Arf in every even case” is **blocked**, with nonzero radical lift controls. None is reopened here; the materially different all-end LP mechanism closes the classification gap.

No external individual communication, Git/index/shared-control writes, original snapshot edits, remote mutation, release, or priority claim occurred. Only this assigned namespace was written. Size remains below20MiB excluding primary PDFs.
