# Reciprocal rectangles: accepted bounded partial investigation

Problem 3900015 / AMR-038-0015, queue rank 928. **Unsolved, 3/5 substantive approaches.**

The unchanged [author report](original/REPORT.md), full [independent audit](audit/AUDIT.md), and [exact acceptance](audit/ACCEPTANCE.json) are preserved byte-for-byte. No patch or corrected derivative was needed.

## Accepted scope

1. Packing every finite prefix is equivalent to packing the infinite sequence, separately in each stated fixed, right-angle, or arbitrary-rotation model.
2. Finite rational axis-parallel feasibility has an exact common-denominator grid reduction covering every real translation.
3. An axis-parallel finite prefix can leave one equal-area axis-parallel square hole only at a perfect-square tail index.
4. The m=4 square-hole splice is impossible, although the three-rectangle prefix itself packs.

These are bounded reductions and a proof-route obstruction. They do not resolve infinite packing, exhibit a forbidden prefix in the original problem, improve the large finite cutoff, or establish novelty. Jiang's September 2026 late-tail preprint and its claimed Lean verification remain externally unverified here. Its late-tail claim leaves m=1 open. The original Meir--Moser 1968 full text was unavailable.

## Computation and source boundaries

The author's complete four-piece grid search records 75 states and 10,204 candidate trials. A different independent enumerator finds 3,064 labeled prefix grid placements and zero square-hole placements; a second independent implementation tests all 32,768 orientation/separation systems. These are different valid counters for different searches, not conflicting measurements. The audit includes 22 author subprocess cases and one external coordinated-tamper control per replay; its frozen receipt records 30 outer cases.

Complete byte verification covers three corpora and five public source files, including all four PDFs. Source hashes establish identity, not correctness of external mathematics. Public titles, URLs, file sizes, hashes, retrieval/inspection history, and stated status appear in the preserved metadata. No corpus records, source PDFs or extracts, screenshots, or private coordination files are published.

## Reproduction

Authenticate verify_publication.py against its independently supplied byte count and SHA-256 before execution. It pins the publication manifest and frozen inputs, enforces an exact recursive file allowlist, compares every expanded file to its archived bytes, and authenticates all content before executing any archived code.

    python3 -I -B verify_publication.py
    python3 -I -B -O verify_publication.py

Optional complete-input replay:

    python3 -I -B verify_publication.py --corpus-dir /authorized/corpora --source-dir /authorized/sources

Supply catalog.json, problems.json, and research_results.json in the corpus directory; supply junkyard.html, jiang.pdf, zhu_joos.pdf, slack_pack.pdf, and martin.pdf in the source directory. Inputs are relocated to fresh temporary directories. Without both directories, the wrapper reports source-free replay and does not claim to verify absent inputs. All outputs are metadata only.

The wrapper is an integrity/replay tool, not a proof assistant or external peer review. A replaced wrapper is not authenticated merely by its own manifest. Frozen historical statements that publication had not yet occurred remain unchanged; the research log records this later packaging step.
