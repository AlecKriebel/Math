# 30001678: audited partial results for perfect-product smoothness

**Disposition: unsolved, 5/5 substantive approaches.** This draft preserves the authored proof packet and separate adversarial AI audit, with the controlling clarification below. It establishes restricted results and an exact reformulation, not an unrestricted solution or a counterexample satisfying all the source hypotheses. No novelty, priority, human peer review, or present global-openness certification is claimed.

This release guide controls the interpretation of the frozen packets. Statements inside the author packet that an independent audit is still required describe its earlier state; the accompanying audit now supplies that review, conditional on the explicit preliminary correction adopted here. Historical statements that no remote write had occurred likewise refer to packet preparation.

## Controlling Cantor-extraction clarification

In `author_packet/PROOF.md`, section 0, replace the root-interval choice in “Elementary Cantor extraction” with the following construction, as required by `independent_audit/AUDIT.md`:

Let U be the specified nonempty relatively open subset of A. Write U = A intersect O, with O open in the real line. Choose a point a in U and a bounded closed interval I such that a lies in the interior of I and **I is contained in O**. Begin the interval construction with I.

Each child interval must still lie in its parent's interior, have interior meeting A, be disjoint from its sibling, and have diameter tending to zero. Merely having the root interval meet U would not ensure containment in U. With I contained in O, all nested branch limits belong to A by closedness and to I by compact nesting, hence to U. Persistent splitting and shrinking diameters give the asserted Cantor subset.

The audit rechecked all uses. In Proposition 3, the chosen portion U_n has diameter at most delta_n; the corrected extraction yields P_n contained in U_n, preserving that diameter bound and the full H-box argument. Corollary 3.1 and the other extraction uses remain valid. The original nine author files are left byte-for-byte unchanged so the audit's exact bindings remain checkable. This guide and the audit jointly adopt the correction rather than silently interpreting the original interval condition as sufficient.

## Retained mathematics and exact gap

The five substantive routes are:

1. Closed-orbit classification for continuous Polish-group actions, including compact groups, and arbitrary Borel pullbacks into that restricted class.
2. Coordinatewise perfect antichains for native products of countable Borel equivalence relations, including products of countable discrete-group actions.
3. Small perfect boxes contained in a single translation orbit, including native weighted l^p and c_0 actions, using the corrected extraction above.
4. E0/E1 tail and diagonal obstructions to tempting limit or nonrectangular shortcuts. E1 is nonsmooth on every full perfect product, but is excluded as a qualifying counterexample by imported Kechris–Louveau Theorem 4.2. That theorem does not require the entire target orbit graph to be Borel.
5. Full countable-coordinate fusion, continuous reading, compact-class classification, and the exact equivalence between existence of a smooth perfect-product restriction and existence of a closed equivalence-graph restriction on some full Cantor product.

The missing step is obtaining the closed restriction from arbitrary Borel reducibility to a Polish-group orbit relation. Continuous reading of the given orbit reduction does not make the target orbit graph closed. The equivalence in route 5 does not establish its own existence clause. Finite controls do not prove any infinite category or fusion argument.

## Source boundaries

The locator is supplied rank 705, ID 30001678, OWR-4792-006. The independently inspected primary formulation is Zapletal's Question 2, printed page 100 of *Set Theory*, Oberwolfach Report 02/2011, on work with Kanovei and Sabok. Smoothness means Borel classification on a countably infinite rectangular product of nonempty perfect factors.

The exact unsolvedmath page returned HTTP 403 and its live statement remains uninspected. Raw AI corpora were not inspected. These are locator bindings, not claims of byte identity with unavailable records. Source metadata records four fresh independent PDF downloads and inspection of a retained published Kechris–Louveau PDF after its fresh retrieval failed; all five inspected PDFs matched the author metadata. PDF bytes and source extracts are not published here.

The published KSZ preview supplies restricted positive classes; the full published Chapter 9 proofs were not inspected. Its early draft contains incomplete proof placeholders and supplies historical context only. The KLy preprint assumes already-smooth inputs. The audit identifies an overstrong parenthetical in its Example 2.2, which is not a dependency of this packet. The related publisher text was not obtained or identified with the inspected preprint. Bounded searches establish neither global openness nor exhaustive prior-attempt clearance.

## Contents and reproduction

- `author_packet/`: nine frozen author files, including proofs, five-route log, source metadata and explicit controls.
- `independent_audit/`: seven frozen audit files, including proof review, bindings, source checks and independent controls.
- `RELEASE_STATUS.json` and `FROZEN_BINDINGS.json`: controlling disposition and immutable input digests.
- `RELEASE_MANIFEST.json`: SHA-256 and byte inventory of this directory, excluding itself.
- `verify_release.py` and `REPLAY_RESULTS.json`: portable integrity/replay checks and their output.

Using Python 3.11+ and its standard library, from any working directory:

    python3 -B /path/to/30001678/verify_release.py --self-test
    python3 -B -O /path/to/30001678/verify_release.py --self-test

The wrapper verifies both pinned manifests and all frozen file bindings, replays 47,729 authored exact/example assertions and seven author packet mutations, and replays 2,932 independent model assertions and eleven independent mutations. Additional release-boundary corruption controls are executed on temporary copies. Normal and optimized replay outputs match, and relocated runs do not require original research folders or source PDFs. These are reproducibility and integrity checks, not automated proof or source-resolution certificates.

The parent release-manifest digest is recorded in the draft PR and a separate verification receipt because a manifest cannot hash itself. Only authored analysis, code/results, and public-source verification metadata appear here. No source PDFs, source extracts, images, raw records, raw search responses, or private coordination records are included.

## Release checkpoint, 2026-10-05 UTC

Five of five mathematical routes are complete. The unrestricted discovery goal remains unresolved; no meaningful numerical completion estimate for that theorem is supported. Scoped packet preparation and audited corrections are complete (100%). The queue patch changes only this row's Status to `unsolved` and Turns to `5/5`, preserving all Findings, Chat, DOI, other rows, and the existing embedded header. No queue regeneration or extra research turn is performed. Intended publication is one draft PR only; merging, releases, new DOIs, and outreach are outside this checkpoint.
