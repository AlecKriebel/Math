# Independent surface surgery review of PR 371

Frozen head: `51fddd150e8da33f4cf17b1a642a0ffd3466bf5d`. Author target: `problems/30006025_geometric_chapuy`. Family: intrinsic geometry, local cut/glue, curvature, area/perimeter and random-surface scope. Review date: 2026-10-03 UTC.

**Scoped PASS. No candidate correction required by this review. The packet does not solve the original geometric Chapuy question.** Its strongest accepted geometric theorem gives `P>=4pi sqrt(g(g-1))` for the stated smooth curvature -1 one-face direct realization, excluding exact source perimeter 12g at every g>=12. Its Dirichlet consequence excludes adaptive bounded-stretch repairs on o(g) edges with probability tending to one. The classical regular-polygon realization remains a valid geometric construction but its short-curve count law is separated from the WP limit by a persistent positive total-variation gap.

## Independent ordering and frozen binding

The original [OWR report](https://publications.mfo.de/handle/mfo/4255), printed 2404-2406 and visually verified Question 4 on 2405, was read before candidate proofs. Source routing hashes/addenda identified the needed primary sources. `SOURCE_FIRST_BASELINE.md` was sealed at 2026-10-03T10:43:21.541180+00:00, before any TURN proof. All five TURN proofs were then fully read and reconstructed. `MATHEMATICAL_VERDICT.md` was sealed at 2026-10-03T10:49:18.672593+00:00, before candidate code, results, states, final disposition, historical/root/sibling conclusions. Both document hashes and ordering attestations are in `SEALS.json`.

After sealing, all five complete author programs were inspected. The frozen snapshot manifest's listed input files were verified by SHA-256, and all target author work was copied only to ignored private directories. No frozen source file was changed. No branch operation, commit, push, shared edit, or external communication occurred. Complete acquisition metadata is in `SOURCE_ACQUISITION.json`; source PDFs, raw extracted text, rendered pages and copied author input remain private.

## What was checked and why the geometric scope survives

The sealed verdict reconstructs every universal TURN proof. Key points include the unique maximal holonomy exponent with a nonzero half-angle coefficient, analytic null sets on the fixed-perimeter simplex, CFF signs/copy multiplicity, regular dessin face degree and orientation-preserving subgroup index, translation-length monotonicity under subgroup inclusion, integer-count zero-mass convergence, and the full adaptive top-k mass argument. Classical transcendence, classification, limit and intrinsic isoperimetric theorems are explicitly credited inputs, not asserted outputs of finite checks.

[Izmestiev](https://arxiv.org/abs/1409.7681), Theorem 1 and its definitions, applies to the **intrinsic cut disk**. There are no interior cone points in the candidate application. Positive sectors at boundary occurrences include reentrant corners and a 2pi leaf tip. Injective development is unnecessary. Every edge, including a bridge, has two boundary copies. The graph has area zero, and smooth closed curvature -1 fixes the disk area at 4pi(g-1). Combining the source disk inequality with that area yields the accepted perimeter bound.

The source paper's triangulation/deformation proofs and its development-overlap warning were read. The necessary external definitions and statements from Chapuy/CFF, BGL, Mirzakhani-Petri, uniform dessins, Philippe and Delaygue were independently checked, including visual checks of the exact cone theorem, triangle-group p=3 formula, MP density, and classical transcendence statements. This is not an independent rederivation of the complete Philippe classification, MP asymptotic theorem or Lindemann-Weierstrass theorem.

The new controls in `GEOMETRIC_CONTROLS.md` add concrete boundaries rather than repeating the author checks: an all-g>=12 source-perimeter hyperbolic cone realization with negative glued defects; a genuine flat disk with geodesic boundary whose development overlaps twice and has no interior cone point; a full-turn slit tip; a geodesic cone four-gon violating the unmodified Euclidean inequality when positive interior curvature is allowed; and graph/filled-surface shortcuts and relations. These affirm that smoothness, intrinsic topology and the precise metric correspondence matter. One post-seal correction to this audit's own exposition labels its radial round-cone examples as auxiliary limits because their boundary is circular; a valid geodesic-boundary four-gon is supplied directly. The candidate claims are unaffected.

## Complete replay and preserved failure

The default Python initially lacked SymPy. Its failed turn-1 stderr and all five complete run outputs/parsed JSON are preserved in `AUTHOR_REPLAY_INITIAL_FAILURE.json`; the initial turn 3 used its frozen historical turn-1 examples, so that route is not counted as successful fresh verification. No dependency was installed.

A new private run used an existing Python 3.14.6/SymPy 1.14 runtime. It generated a fresh TURN_1_CHECKS input for turn 3. All five exits were zero, all stderr empty, every stdout parsed completely, and all outputs were byte-identical to the historical author CHECKS JSONs:

| Turn | Assertions |
|---|---:|
| 1 | 467 |
| 2 | 1,004 |
| 3 | 961 |
| 4 | 1,136 |
| 5 | 12,050 |
| Total | 15,618 |

`AUTHOR_REPLAY_RECEIPTS.json` contains whole stdout, stderr, parsed JSON, input/output hashes, timestamps, exit codes and durations. `HISTORY_SOURCE_AND_REPLAY_COMPARISON.json` preserves the complete five historical states/manifests, source manifests/addenda, final author manifest and output comparison. Original author progress estimates 8%, 10%, 12%, 16%, 18% remain historical estimates, not independently measured solution completeness. Their disposition evolves from unresolved to unsolved after five turns and matches the final scoped wording. Final and additive reviewed wrappers do not inflate the problem disposition.

The new exact controls pass **3,775 assertions**, with a complete generated receipt. They supplement the universal proofs and explicit constructions. Their finite genus scan is not a proof of the all-genus cone escape; monotonicity and the exact rational comparison provide that proof. A further harmless wording correction to the immutable source baseline: its short quoted Question 4 has 13 words, not the stated 19; the quote itself is accurate and below the 25-word excerpt limit.

## Source credit and remaining gap

The combinatorial input is [Chapuy/CFF](https://arxiv.org/abs/1202.3252); the finite Janson-Louf graph regime and [metric ribbon graph law](https://doi.org/10.1017/fms.2025.31) are distinguished from normalized WP volume. The regular dessin representation is credited to [Girondo-Gonzalez-Diez-Hidalgo](https://arxiv.org/abs/2306.09543), the triangle-group lower bound to [Philippe](https://doi.org/10.5802/aif.2424), the WP statistic to [Mirzakhani-Petri](https://webusers.imj-prg.fr/~bram.petri/RandSurf.pdf), and the disk bound to Izmestiev and the earlier Alexandrov/Bol/Weil lineage. The classical Hermite-Lindemann/Lindemann-Weierstrass statements were checked in [Delaygue's introduction](https://arxiv.org/abs/2210.12046v2); no new E-function theorem is used. Acquired BGL journal bytes vary because of download stamping; the law, theorem, pagination and DOI agree, and the mismatch is recorded rather than erased.

The original source asks an informal broad construction question. This packet neither constructs a controlled geometric tree/map-to-hyperbolic-surface law compatible with WP, nor proves every such construction impossible. Variable real angles, extensive or unbounded length changes, different correspondences, curvature choices and weaker asymptotic comparisons are outside the ruled-out classes. Necessary perimeter/mass conditions are not sufficient realization criteria. No claimed historical novelty was verified or invented. The appropriate release is an independently checked scoped partial-result packet, with the original discovery gap explicit.
