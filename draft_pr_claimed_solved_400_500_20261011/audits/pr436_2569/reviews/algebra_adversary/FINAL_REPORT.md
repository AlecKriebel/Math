# Algebra adversary final report

Completed 2026-10-12 21:56 UTC. Completion estimate: 100% of this assigned algebraic verification, not a novelty estimate or human certification. Author budget remains 5/5; this review used zero new original proof-search attempts.

**Mathematical verdict: PASS for the frozen main counterexample.** No required mathematical repair was found. The positive ordinary-Grothendieck condition holds for all three F_2 PIM types, and the rank-eight PIM has no projective Z_(2)SL(2,5)-lattice lift. The complete independently reconstructed proof is [PROOF_RECONSTRUCTION.md](PROOF_RECONSTRUCTION.md). It was sealed before reading historical audit/contributor conclusions or current peers. Historical reviews were subsequently inspected as objects of review, never used as proof premises.

## Typed findings

| ID | Type / severity | Finding | Impact |
|---|---|---|---|
| AA-01 | Mathematical invalidation / none found | Central quotient exact sequence, all nonsplit types, witnesses, finite projective lift, vanishing, and real quaternionic parity all check. | Main theorem passes this family. |
| AA-02 | Source status / material | The frozen October notebook URL returns 404 today. The editors' October 6 replacement has starred *21.60 and cites an earlier negative solution confirmed by D. Rumynin. | Frozen source gate cannot serve as a current unresolved-status or current-literature gate without refresh. This does not refute the counterexample. The old gate is dated October 3; this review does not infer that its historical unstarred observation was false at that time. Root was notified before any priority audit; the linked solution was not opened here. |
| AA-03 | Exposition / optional | The candidate refers to a standard semiperfect lifting criterion. | The report supplies a direct finite-projective-cover proof, including finite generation and exact reduction. No new theorem or candidate search is needed. |
| AA-04 | Computation scope / informational | Frozen scripts use `assert` guards and unconditional positive receipt fields. | Normal-mode arithmetic is the claimed scope. An optimized run with disabled assertions alone cannot certify those checks. Root's separate reproduction family owns the complete replay. This review's targeted scalar checker uses explicit failure checks and passed in normal and optimized modes. |

## Supplemental mathematical claims

The five attempt records also pass algebraic scrutiny with their existing qualifications.

1. The regular kC_p module and p trivial copies have equal composition classes but different nilpotent ranks and coinvariants. Coinvariants do not induce the attempted ordinary-G_0 map. This correctly blocks that proof route, rather than disproving the source's proposition by itself.
2. The dense rational-basis construction in `turn_02.md` is valid. A rational form V is dense in its Q_p extension; one may choose a rational basis sufficiently close to a basis of the completed projective lattice so that all vectors lie in that lattice and form its integral basis. The finite orbit-span lattice remains contained in the completed lattice and has the same completion. Reduction is therefore the prescribed PIM. Projectivity descends from the completion: over the complete order, a lifted projective cover maps onto the candidate lattice with isomorphic reduction; Nakayama and equal underlying ranks make this an isomorphism. Faithfully flat completion then gives flatness of the finitely presented original lattice, hence projectivity. The rational-character criterion correctly uses full Galois orbits and global Schur-index divisibility. The equality of global and fixed-embedding local indices is a sufficient stated hypothesis.
3. Restriction to Q_8 is exact and exposes the even-multiplicity condition in every rational reduction for odd p. The tested PIM W⊗kP has |P| odd copies of W upon restriction. The uniform proof applies to every finite odd p-group; the saved cyclic checks merely evaluate its parity arithmetic.
4. The fourth attempt contains the main counterexample already reconstructed independently.
5. Ext^1_(RC2)(R,R)=0 while Ext^1_(kC2)(k,k)=k for trivial coefficients. The modular regular module nevertheless has another integral lift, so C_2 only refutes the unrestricted Ext-comparison step. Intersections of a rational composition flag with a lattice are saturated and have torsion-free quotients, hence reduce exactly. The actual A_5 projective lifts then provide the claimed Brauer--Humphreys filtrations, and the central exact sequence splices them for all G-PIMs. The stronger source proposition is not a main-proof input. Its displayed Ext order is also opposite the usual filtration-extension order, but the C_2 calculation already invalidates its blanket isomorphism in either order.

The contributor's supplemental rational Wedderburn decomposition agrees with the newly read Eisele--Kiefer--Van Gelder Section 5.2 (printed p18, PDF p19). The unique faithful degree-four component is M_2((-1,-3)/Q). Its odd-unit Hilbert symbol at 2 is +1, and it ramifies at 3 and infinity, so the global index is two while the 2-adic index is one. The Hamilton degree-six component remains division at 2; base change of the degree-two Hamilton component to Q_2(sqrt(5)) kills its local invariant. The stated global and local splitting fields are consistent. These facts are supplementary; the main obstruction only needs real parity.

## Complete frozen-file inspection

All 26 files matched the capture receipt; their individual hashes and byte sizes are in [FROZEN_READ_RECEIPT.json](FROZEN_READ_RECEIPT.json). The following table states what was inspected, without treating saved PASS fields as proof.

| Frozen file | Inspection outcome / scope |
|---|---|
| COUNTEREXAMPLE.md | Complete theorem and all mathematical implications reconstructed; PASS. |
| SOURCE_GATE.md | Exact target matches primary sources; present notebook status is stale, AA-02. |
| README.md | Main claim and base-field qualification correct; replay scope must retain stated dependencies. |
| RESEARCH_LOG.md | All five substantive turns preserved, with candidate in turn four and genuinely substantive fifth turn. |
| turn_01.md | Class/isomorphism distinction, coinvariant warning, and rationality of projective character correct. |
| turn_02.md | Dense rational descent and global/local character criteria correct. |
| turn_03.md | Uniform odd-p-group restriction obstruction correct. |
| turn_04.md | Full main candidate correct. |
| turn_05.md | Ext warning and saturated-filtration claims correct; no dependence in main theorem. |
| verify_counterexample.py | Exact arithmetic implementation read; actual representation relies on described SU(2) construction; normal-mode assert scope. |
| counterexample_results.json | All reported scalar/group/vector fields agree with written proof and source inputs. |
| verify_controls.py | Rank computation and parity-only control scope correct. |
| control_results.json | Finite instances correctly instantiate the uniform recorded arguments. |
| contributor_checks/check_character_data.py | Table consistency, matrix inversion, reciprocity, fusion and Hilbert-symbol formula read; representation-existence premise is explicit. |
| contributor_checks/character_checks.json | Full ordinary/decomposition/Cartan data consistent; Schur labels require source input, not merely scalar arithmetic. |
| contributor_checks/CHECK_REPORT.md | All mathematics checked; supplementary arithmetic source read freshly. |
| independent_audit/independent_audit.py | Full construction, span, Gram, idempotent, top-rank, central-rank and character code inspected; parent reproduction owns replay. |
| independent_audit/independent_results.json | Correct described mathematical scope; saved booleans not used as proof. |
| independent_audit/a5_idempotents.json | All 60 permutation records/180 exact coefficient inputs read; Table 5 page inspected; numerical multiplication independently delegated by root. |
| independent_audit/INDEPENDENT_AUDIT.md | Every theoretical claim checked after independent reconstruction; no circular reliance. |
| independent_audit/PORTABILITY.md | Adaptation described as input/packaging, not new mathematics. |
| independent_audit/PORTABILITY_REVIEW.md | Historical replay/47-assertion statements inspected; not reused as current replay evidence. |
| PUBLICATION.md | Candidate/human/priority qualifications correctly scoped historically; current source status requires root reconciliation. |
| status.json | Main mathematical labels supported; historical review labels are metadata. |
| verification.json | Recorded historical environment/PASS claims are receipts, not independent present proof. |
| MANIFEST.json | File list, lengths and hashes inspected; independently matched capture for all actual 26 files. |

## Actual work and remaining gap

This review performed exact group-order, order-count, square-map, norm, indicator, inner-product, forced-character, witness and regular-dimension arithmetic in [check_algebra_arithmetic.py](check_algebra_arithmetic.py), passing both `python3` and `python3 -O` with identical displayed results. These scalar checks take source-checked character/modular vectors as mathematical inputs. They do not claim a fresh full module/table reconstruction or full original-script replay.

There is no remaining mathematical gap in this review family. Root must combine independent families and handle the material current-source/earlier-solution finding after its mathematical gate. No source/gate/status/PR/paper/Zenodo/GWS/index/remote mutation, external communication, or frozen-byte edit occurred. Foreign PDFs, HTML, extracted text and page images remain in this reviewer's private source folder and are excluded from the positive public allowlist.
