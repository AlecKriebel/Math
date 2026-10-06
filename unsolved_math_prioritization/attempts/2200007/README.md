# ID 2200007: credited prior disproof of Conjecture 4

Rank 899 / AMR-021-0007 is **false by prior counterexample**, with queue disposition
`already_solved` and **0/5 new research approaches**. DannyExperiments' public
[10 August 2026 release](https://github.com/DannyExperiments/ottaviani-shapiro-sos-counterexample/releases/tag/v1.0.0)
gives a quartic sum of nine quadratic squares in ten real variables with exactly
1,152 isolated real zeros, exceeding the proposed 1,024. The construction is prior
work; this packet verifies its precise applicability and reproducibility.

Start with the [independent mathematical audit](isolated_polynomial_zeros_2200007_independent_audit/AUDIT.md)
and [exact acceptance report](isolated_polynomial_zeros_2200007_independent_audit/ACCEPTANCE.json).
The [source scope](isolated_polynomial_zeros_2200007/SCOPE_BRIDGE.md) is
[Shapiro's Problem 3 and Conjecture 4](https://arxiv.org/html/1503.05295v1).
The credited [manuscript, Theorem 1.1](https://github.com/DannyExperiments/ottaviani-shapiro-sos-counterexample/blob/41e3d18a8c536e5a859201afd5faefe2b0ecd315/paper/manuscript.tex)
has separately inspected public citation metadata crediting
[DOI 10.5281/zenodo.21875290](https://doi.org/10.5281/zenodo.21875290).
The GitHub release predates that DOI and does not itself claim it.

## What is preserved

- The exact original nine-file author freeze, ZIP, and external manifest.
- A separately pinned hardened nine-file derivative. Only README.md,
  verify_package.py, and MANIFEST.json change; the mathematics and historical
  status bytes are preserved.
- The independent eight-file audit, actual three-file patch, deterministic
  check results, exact acceptance, ZIP, and external manifest.
- Publication validation metadata, without source documents or corpus contents.

Historical `pending separate review`, `queue_modified: false`, and
`remote_writes: false` values describe the original preparation/audit stages.
The separate acceptance is the later exact-artifact disposition; this wrapper
records the draft publication and limited queue update without rewriting history.

## Replay

First verify all archive and manifest byte counts and SHA-256 values in
PUBLICATION_VALIDATION.json against an independently trusted copy. An internal
manifest is not an external authenticity root. Then, from this directory:

    python3 -I -S -B isolated_polynomial_zeros_2200007_independent_audit/verify_audit.py ISOLATED_POLYNOMIAL_ZEROS_2200007_AUTHOR_SAFE_FREEZE.zip ISOLATED_POLYNOMIAL_ZEROS_2200007_HARDENED_SAFE_FREEZE.zip

Repeat with `-O` and `-OO`. Each successful output must byte-match the audit's
CHECK_RESULTS.json. Each run produces 86 replay/adversarial observations,
including 54 ordinary mutation rejections, and independently checks 10,368 exact
equation residuals for the 1,152 points. The count of 86 is not a count of
mutation rejections. Publication checks also apply the actual patch and
byte-compare its complete output, and reject tampered original/hardened archives
before replay in all three optimization modes.

The recommended direct package invocation is:

    python3 -I -S -B isolated_polynomial_zeros_2200007_hardened/verify_package.py

Use `-I -S` before startup; `-B` alone does not stop sibling bytecode imports or
site hooks. A trusted Python interpreter/standard library and stable extracted
files remain assumptions. All portable replay is offline and standard-library-only.
Source/corpus inspection is separate from portable replay.

## Scope and disposition

The universal equality in Conjecture 4 is refuted. The exact maximum sought in
adjacent ID 2200006 is not determined, and its broader investigation was not
replayed here. No new-discovery, absolute-priority, human-peer-review, or formal
proof-certification claim is made. Verification and publication are complete
within this bounded target; the credited disproof is not a new research approach.

This draft changes only the current queue row's Status and Findings; Turns remains
0/5. All unrelated queue bytes, notes, and existing chat links are preserved.
Only authored verification prose/code, audits, the actual patch, acceptance,
and permitted public verification metadata are included. No third-party source
documents, raw datasets, or private coordination material are redistributed.
