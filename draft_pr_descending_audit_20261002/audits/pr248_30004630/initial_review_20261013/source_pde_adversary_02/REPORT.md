# Fresh independent source/PDE adversarial audit: PR 248

Problem 30004630 / OWR-4990378-001. Audited submitted head: `e9c5d10978764db2cf25fa7d49cf4bd14a82d604`. Audit completed 2026-10-14 UTC (2026-10-13 Pacific). Authoritative input is the supplied 19-file frozen packet and intake. This subaudit made no repository, PR, queue, publication, release, spreadsheet, or external-communication change.

## Separate verdicts

**Mathematics: PASS for the precise submitted theorem.** The independent reconstruction finds no substantive proof defect. A fixed small constant admissible radius exists on the smooth unit ball. Zero is the unique global optimizer with the exact source critical cone {0}; the source substitute strict second-order condition holds vacuously. Feasible vanishing-amplitude centered pulses converge to zero in L^∞ and have objective gap divided by their L^2 norm squared tending to zero. The terminal-target perturbation result also holds for every choice of global optimizers. Every fixed ν≥0 in the OWR objective is covered, including existence of those optimizers.

**Source resolution: PASS as a negative resolution of the unchanged strict-critical-cone implication after deleting β₂>0; LIMITED for the broader unregularized theory program.** The literal source places its β₂=0 open statement immediately after that sufficient-condition/growth implication. No nonzero-cone requirement appears. The construction is consequently a relevant counterexample to that contextual extension. It establishes no impossibility of replacement conditions or weaker stability results. This limitation is already explicit in the submitted proof, and must remain explicit in every final disposition.

**Priority/novelty: NOT AUDITED.** No deep priority investigation was begun. Classical wave estimates and well-posedness are credited inputs. Agreement with an earlier assistant review is not historical novelty evidence or human peer review.

## Independent evidence and adversarial checks

The full initial reconstruction was recorded before opening the submitted review verdict. Its initial bytes/hash are preserved in the research log and final derivation's comparison section. The later old review agrees on the mathematical mechanism; its campaign-promotion recommendation was kept separate.

The primary PDFs were freshly obtained at their original URLs; every size and SHA256 exactly matches the submitted source manifest. Official OWR printed 438–440 was read and visually inspected; both pinned preprints were read at the relevant PDE, cone, existence, differentiation and theorem sections, with printed 8, 26, 35 visually inspected. Sources and exact scope are detailed in `SOURCE_AUDIT.md`. The publisher's final typesetting was not silently claimed inspected.

The full proof is checkable in `INDEPENDENT_DERIVATION.md`. In particular:

- The ball eigenfunction normalization, radial smoothness at the origin and Dirichlet eigenvalue are correct. No nonlinear invariant-mode claim is made.
- L^1H-to-continuous-energy/L^4L^{12} estimates plus explicit mixed-norm interpolation make the quintic map locally Lipschitz into L^1H. A full-space contraction gives uniform O(A) state and O(A^5) nonlinear error for the entire capped admissible set; concentration is covered.
- The global optimality bound uses all controls, not merely eigenmode controls. The exact density comparison has the correct sign and yields A³/(12ρ²) after the small-radius choice.
- The zero cone follows from strict positivity of the first derivative for every nonzero L^1 or L^2 equivalence class. A single exceptional time supports no nonzero such direction. The ball tangent cone is full by bounded truncations; pointwise interior is not confused with Banach-space interior.
- The pulse cost has independently derived leading coefficient π²/3+2/π² at order h^4. The L^2 norm squared is 2h^3. The optional velocity cost is O(h^20), owing to exact cancellation of its linear endpoint.
- The direct method gives strong C(L^2) position and C(H^{-1}) velocity convergence. The constant cap makes y_tt uniformly L^∞H^{-1}. Almost-everywhere state convergence identifies the weak quintic; retained L^4L^{12} plus energy gives L^1H forcing. An explicit zero-data homogeneous-wave eigenbasis argument upgrades the weak limit to the unique mild state.
- The perturbation contradiction uses an actual target change of H-distance ε, a fixed-amplitude feasible trial with objective improvement −ε²/2+O(ε³), and an O(ε^{5/4}) gradient-positive-part norm. It rules out ∥u_ε∥_2≤Kε for every fixed K. All those global optimizers also approach zero in L^2; no assertion about their L^∞ convergence is needed.

The independently authored `controls.py` passes 17 exact symbolic checks (SymPy 1.14.0). The original checker passes all 3937 assertions, with JSON structurally equal to its submitted receipt. These are finite exact consistency checks, not a PDE simulation or a calibration of unknown classical constants. All 19 submitted files match expected bytes, SHA256 and Git-blob SHA1; `PIN_LEDGER.json` contains the complete comparison.

## Strongest verified result, repairs, and gaps

The strongest verified result is the full stated nonlinear-PDE counterexample to **ordinary source strict-cone positivity ⇒ strong L^2-squared growth at β₂=0**, with zero as the unique global optimizer and with the separate every-global-optimizer non-Lipschitz target theorem. It applies to both the report's L^2 neighborhood and the full theorem's L^∞ neighborhood, and to every fixed nonnegative optional velocity coefficient.

Mandatory mathematical repairs: **none** for this precise theorem. The frozen proof's pending-review header and its metadata's unreviewed status coexist with a supplied prior review and the live intake's claimed_solved state. Those are provenance/status synchronization issues for any later parent publication decision, not proof defects; this subaudit changes none of them.

Required promotion qualification: retain the unchanged-condition scope, zero-cone vacuity, and non-certification of novelty. An unqualified assertion that all unregularized sufficient-condition or stability questions are solved is unsupported. Replacement hypotheses, enlarged/approximate critical cones, weaker exponents/norms, other local branches, Neumann/boundary controls and priority remain outside this verified result. No route is marked blocked, because no central step was transferred to an unsupported equivalent claim.

## Artifact boundary

`FINAL_AUDIT_MANIFEST.json` pins the authored public files by relative path, bytes and SHA256. `private_reading/` contains only excluded primary PDFs, extracted text and visual page copies. `excluded_reading_pins.json` records them separately; full third-party content is not part of the public authored packet. All audit work stayed in this dedicated folder. The parent may checkpoint it on main under the project workflow; this subagent did not mutate the Git index, checkout or refs and did not publish.
