# Boyle's Pingree problem 2: five approaches, unresolved

Target: UnsolvedMath **4400008**, **AMR-043-0008**, rank 701 in the available selection catalog.

## Result

The original question is **not resolved in this packet**. Five distinct routes were worked through: periodic-orbit/measure invariants, cocycle rigidity, shadowing and finite-language stabilization, positive speedups, and flow-equivalence/return-map reconstruction. The packet gives complete elementary proofs of the reductions and negative controls it claims, and states exactly where each route stops. No novelty, global-openness, or publication-ready theorem claim is made.

The precise remaining issue is whether unrestricted topological orbit equivalence to a mixing finite-type shift forces a finite-type presentation for the other subshift. If finite type is established, mixing follows from preserved orbit data. Equivalent closing goals proved here are shadowing of the target or flow equivalence to the source. Neither is established under the question's hypotheses.

## Formulation

Use finite-alphabet, two-sided, one-dimensional subshifts, with their shift homeomorphisms. An orbit equivalence is a homeomorphism taking each full integer orbit **onto** a full integer orbit. There is no assumed continuity or boundedness of the integer jump functions; no fixed alphabet cardinality or entropy; and no factor-map, computability, minimality, or higher-dimensional hypothesis.

The original November 22, 2010 Pingree list, page 4, Mike Boyle item 2, asks whether such a target is a mixing SFT when the source is a mixing SFT. Its neighboring remarks exclude replacing expansivity by arbitrary zero-dimensional dynamics, or replacing the source SFT by a mixing sofic shift. The same finite-type question appears in Boyle's 2008 survey as Problem 23.4(5), with an irreducible source.

Primary statement: https://math.huji.ac.il/~mhochman/open-problems/pingree-open-problems.pdf

The exact catalog-page URL https://www.unsolvedmath.com/problems/4400008 could not be read directly: web retrieval failed and a local HTTPS request received HTTP 403. An indexed Dynamical Systems listing agreed with the available target descriptor and the original question. The inaccessible page's full wording and additional notes remain uninspected. The original PDF, rather than a title-based guess, determines the mathematical formulation used here.

## Files and checks

- `proofs.md`: complete authored elementary proofs, explicit examples, conditional applications of named primary theorems, and exact unresolved obligations.
- `five_approaches.md`: separate attempts, their actual outcomes, and stopping points.
- `sources.json`: public source titles, URLs, actual downloaded-byte hashes and sizes, inspection scope, and source limitations.
- `verify.py` and `verification.json`: deterministic exact-integer negative controls. These calculations check examples; they do not prove the original theorem.
- `status.json`: machine-readable unresolved status.
- `manifest.json`: hashes and byte counts of the frozen authored files, excluding itself.

Run `python3 verify.py` from this directory. Its output must match `verification.json` byte for byte. This is author verification, not independent peer review or formal proof checking.

## Prior-work and literature scope

Read-only repository checks found no confirmed previous exact-target attempt: exact-ID and title-related PR searches, exact-ID/Boyle branch searches, all 728 listed branch names, and the 61-entry default-branch attempts directory. Branch contents were not exhaustively searched. A default-branch recursive-tree request failed with a transport error. These checks are bounded evidence, not proof that no earlier attempt exists.

Primary-literature checks included the 1996 Boyle–Handelman paper, 1998 Boyle–Tomiyama paper, 2008 survey, 2010 problem list, the author's solutions page (last revised 2016), Salo's 2023 paper, and Matsumoto's 2023 paper. No complete solution of this exact unrestricted-TOE question was established in the inspected sources. Salo resolves the neighboring Hochman free-part conjugacy question; Matsumoto's finite-type preservation result concerns continuous orbit equivalence of associated one-sided normal subshifts. Neither can be substituted for the present hypotheses.

The original raw AI-result corpora were unavailable. They were not inspected, and no raw-record identity or hash match is claimed. An available selection catalog is only a descriptor, not a substitute for those source records. Source PDFs, extracts, images, raw repository responses, and private coordination material are excluded from this authored packet. No remote write was performed.
