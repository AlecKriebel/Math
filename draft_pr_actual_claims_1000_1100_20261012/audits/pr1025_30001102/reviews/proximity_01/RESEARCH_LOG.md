# Independent proximity and bit-complexity review

## 2026-10-13 04:12 UTC — checkpoint (15% complete)

Task: independently test the complete rational binary-input optimization claim at PR #1025, pinned head `7769e6872c3d2f4267706dc2400be3519186cf3d`, focusing on signed proximity, attainment, recession, partial LP minimization, and bit complexity. Read the candidate proof and original Oberwolfach Problem 1 directly. Did not read the historical independent audit, acceptance files, or another current review.

Initial derivation: coordinate and row-difference conformity of the signed threshold layers is valid. The compact nearest-point argument avoids assuming mixed attainment. The finite integer domain's sufficiency uses the special bipartite/free-sign model. Primary Schrijver ring-family body is accessible; independently checking the rational arithmetic interface, rather than inferring bit complexity from a bound on operation counts alone.

No mathematical verdict yet. No external contacts or service mutations. All review artifacts stay in this directory; third-party source bodies are retained only under `sources/raw`.

## 2026-10-13 04:19 UTC — checkpoint (85% complete)

Completed independent symbolic reconstruction of the optimization argument. The compact nearest-sublevel mechanism proves attainment and proximity without presupposing an optimum. Exact projection to integer coordinates relies on the target's bipartite/free-sign form; fixed continuous slices are nonempty and finite. Derived a uniform common denominator and magnitude bound for the LP value oracle, including nonvertex relaxation outputs and component lineality. Independently inspected GLS's rational LP theorem and finite rational lattice-family minimization bodies as a direct bit-complexity route; checked Schrijver's complete Section 6 interface and reduction.

New independent finite checker passes identically under normal, `-O`, and `-OO`: 7,380 signed vectors; 331,696 difference-conformity checks; 45 models; 2,095 slice LPs; 199,661 submodular pairs; 2,474 removal layers; 2,994 uniform exact-oracle denominator/magnitude checks. Includes isolated vertices, empty graphs, all integer-coordinate selections for small models, 180-bit numerators and 127-bit denominators. These are finite diagnostics, not a polynomial optimizer or a universal complexity proof. Current work: finish deliberate source-mutation controls and write the exact verdict, pins, source-inspection manifest, and scope limits.

## 2026-10-13 04:22 UTC — final checkpoint (100% of this review complete)

Family A verdict: PASS for the optimization theorem. No required mathematical repair. Report supplies the independent proof reconstruction, explicit uniform oracle denominator/magnitude bound, directly checked rational LP/SFM source interfaces, all boundary qualifications, source pins, and original finite diagnostic artifacts. All three baseline modes agree byte-for-byte; five source-fault families reject in all three modes. Initial expected first-error labels for two mutation families were corrected after the earlier valid guards rejected them; original records and outputs are preserved, and six targeted reruns confirm exact reasons. This changes no mathematical coverage. Parent program remains incomplete until the other family, priority, paper/package reviews and publication workflow finish.
