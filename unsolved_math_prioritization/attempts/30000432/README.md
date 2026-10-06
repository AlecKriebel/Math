# Equal-area triangulations: audited partial results

**Problem 30000432 / OWR-1194-001, rank 811: unsolved, 5/5 approaches.** The independent mathematical review accepts the scoped partial results. The general equal-area existence question for 4-connected plane triangulations remains unanswered here.

## Accepted mathematics

For a labeled cycle bipyramid of cycle length m >= 4, a selected exterior triangular face and its fixed noncollinear coordinates, there are **exactly m-2 equal-positive-area drawings**, all with explicit rational coordinates in the normalized triangle. The proof allows collinear nonfacial triples; it is not a general-position theorem. It excludes colliding vertices, collapsed faces, overlapping edges and unwanted vertex-edge incidences. The unbounded face is not required to have the common bounded-face area.

Four further results obstruct specified proof routes: everywhere-regular continuation and uniform local degree signs; unmodified equal-neighbor harmonic placement; arbitrary prescribed positive weighted-area strengthening; and reflection-equivariant symmetry or naive averaging. These are not counterexamples to the original equal-area conjecture. No historical novelty or priority is asserted.

Read [the proof](author/PROOFS.md), [the complete independent audit](audit/AUDIT.md), [source scope](author/SOURCE_REVIEW.md), and [the current verdict](VERDICT.json). Source credit distinguishes Firsching's exact theorem through 11 vertices from the current website's through-12 algebraic claim, whose coordinate data were not independently audited, and numerical results for 13-15. The broader area-universality question is not substituted for equal-area existence.

## Frozen history and operative verification

The original ten author files and the twenty-file audit packet are unchanged. Their two original ZIPs are retained in `archives/`. The audit's nested `author/` is byte-identical to the standalone author packet. The author's historical pending-audit language describes its original preparation stage; the adjacent independent report supplies the later verdict.

The operative gate is the audit's **mandatory recursive inventory and independent geometry**, supplemented by the outer publication inventory. The original checker has two reproduced coverage gaps: a small global translation evades its fixed-exterior-coordinate tests, and an unlisted FIFO evades its file inventory. Neither defect invalidates the frozen mathematical witnesses. [The separate four-line patch](audit/AUTHOR_HARDENING.patch) adds explicit exterior-coordinate and nonregular-node rejection. It is applied and tested only on temporary copies. No author v2 is substituted.

- Frozen author: 56,815 exact checks, 77 family drawings, 1,036 connectivity-deletion controls
- Independent checker: 573,677 mathematical checks, 261 drawings, 14 direct bad-geometry/intersection controls
- Independent audit: 16 integrity and 16 semantic mutation runs rejected, in addition to the original author's 20 integrity and 16 semantic rejections
- Separately hardened author: 56,896 checks; original regressions pass, and both demonstrated defects are rejected in normal and optimized modes

These counts are separate historical results. They do not certify all software behavior or establish a general-graph existence theorem. This is an AI-assisted mathematical audit, not human peer review or proof-assistant certification.

## Reproduction

Python 3.10+ and its standard library suffice, except the actual patch-application replay also uses the standard `patch` command. From this directory:

    python3 verify_package.py
    python3 -O verify_package.py
    python3 run_package_controls.py
    python3 audit/run_checks.py
    python3 replay_actual_patch.py

The package verifier checks exact files and directories, regular-node inventory, hashes, sizes, pinned frozen manifests, ZIP CRCs and every archive member's bytes, then replays the author and independent checker against their frozen output. Package controls repeat full runs after relocation, compare normal/optimized results, and test corrupted packages. The audit harness replays both original defects, all original and independent mutation controls, and separate hardening. The last command applies the actual shipped patch with zero fuzz, compares its exact result to the audit's tested hardening, runs the hardened original harness, and exercises both defects in both modes.

For the exact queue delta:

    python3 verify_package.py --queue-base /path/to/base-QUEUE.md --queue-updated /path/to/branch-QUEUE.md

Only this target's Status and Turns change to unsolved and 5/5. All other queue bytes, including the preexisting header, are preserved. The publication adds no proof-search approach. Do not write outputs or bytecode inside the packet; unlisted content is rejected. The outer manifest excludes itself and needs an external trusted Git commit or receipt; self-hashing does not authenticate a maliciously replaced verifier.

Only authored proof, code, audit, results, public verification metadata and the two safe archives are included. No copied source document, source extract, dataset or private coordination content is redistributed. Draft review only; no merge, release, DOI or external outreach is part of this publication.
