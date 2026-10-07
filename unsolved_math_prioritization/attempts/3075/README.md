# OPG-605: audited partial for the bounded-cell average graph diameter

Problem 3075, rank 925. **Unsolved, partial/stalled, 3/5 approaches.**

Read [the exact authored report](original/REPORT.md) and [the independent audit](audit/AUDIT_REPORT.md). The accepted partial gives a signed defect identity in every dimension, an exact nonnegative-slack criterion in dimension three, and an eight-line obstruction to arbitrary-deletion induction. Both witness averages remain below two. It does not refute the original conjecture or suitable-deletion induction, prove a new universal regime, or establish novelty or minimality.

## Exact accepted bytes

The six immutable archives/manifests are in `releases/`. Original ZIP and manifest, full independent audit, accepted derivative, actual [loader patch](audit/ISOLATED_LOADING.patch), and [acceptance record](audit/ACCEPTANCE.json) are preserved exactly. `original/` and `audit/` are byte-identical extractions. Only `verify.py`, its documentation paragraph, and `MANIFEST.json` differ in the derivative. Mathematics, witness, and geometry algorithms are unchanged.

The original passes normal and optimized replay but fails isolated modes with `No module named 'arrangement'`. These are two expected findings, not two successful executions. The accepted derivative compiles previously authenticated source bytes and passes normal, optimized, isolated, and isolated-optimized replay. The frozen audit records 88 artifact checks and eight supplementary acceptance checks.

## Fail-closed replay

Requires Python 3 with its standard library and the standard `patch` program. Obtain the publication-manifest SHA-256 and wrapper SHA-256 independently from the publication receipt before execution. Do not infer trust from a manifest delivered together with untrusted code.

    python -I -B verify_publication.py --expect-manifest EXTERNALLY_OBTAINED_SHA256
    python -I -O -B verify_publication.py --expect-manifest EXTERNALLY_OBTAINED_SHA256

The wrapper binds the externally supplied manifest, every publication byte, and all six hardcoded artifact pins before executing any packet code. It validates all ZIP members (including nested archives), reads the exact acceptance record, replays the actual patch into a fresh original copy, and checks every reconstructed derivative byte. It then runs the frozen original, accepted derivative, and independent exact enumerator in all four Python modes from unrelated temporary directories. Original isolated failures must recur with the specific recorded import error. All validation uses explicit exceptions, not removable assertions.

For a fresh full-input check and full 88-check adversarial matrix, provide the exact three original corpus snapshots and all six pinned public-source files, obtained separately:

    python -I -O -B verify_publication.py --expect-manifest EXTERNALLY_OBTAINED_SHA256 --corpus-dir CORPUS_DIRECTORY --source-dir SOURCE_DIRECTORY --full-artifact-matrix

`--integrity-only` skips execution explicitly. Omitting the input directories is not fresh corpus/source verification. Reading previously frozen verification metadata is likewise not a fresh source retrieval or literature search.

## Provenance and scope

[Corpus verification](audit/CORPUS_AUDIT.json) includes whole-input sizes/hashes, exact-ID uniqueness and the full unprojected record/report-pair digest. [Source retrieval history](audit/SOURCE_RETRIEVAL_AUDIT.json) covers six public sources and distinguishes the graph-diameter conjecture from Euclidean-diameter work. Direct UnsolvedMath retrieval returned 403; an alternate 2026 PDF returned 404; the pinned accessible sources and exact complete corpus were used. Negative search evidence does not certify novelty or unresolved status.

This packet contains authored mathematical work, correction code, an authored finite witness, and public verification metadata only. It excludes raw corpus contents, copied third-party PDFs/HTML/source text, private sources, and private coordination material. Historical statements that no GitHub writes occurred describe the author/audit stage. This publication stage proposes one draft PR; no release, DOI, merge, or outreach is part of it.

The canonical queue change is restricted to rank 925's Status (`queued` to `unsolved`) and Turns (`0/5` to `3/5`). Findings and all unrelated queue bytes are preserved. See [publication log](RESEARCH_LOG.md) for the remaining mathematical gap.
