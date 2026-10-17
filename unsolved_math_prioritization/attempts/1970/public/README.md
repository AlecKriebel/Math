# Forbidden triples {n,2n,3n}: interim checkpoint

**Erdős Problem 168 · record 1790 · ID 1970 · EP-168 · reconstructed 15 October 2026**

**UNSOLVED.** For each positive integer N, maximize the size F(N) of a subset of {1,…,N} containing no complete triple {n,2n,3n}. The limit alpha=lim F(N)/N exists. Its rationality or irrationality is not settled here.

This is a partial interim mathematical checkpoint, not a completed study or a solution. It contains newly authored reconstructed proofs and synthetic certificates; no historical byte-identity claim is made.

## Reading order

1. [Mathematical reader](ERDOS_TRIPLES_READER.md): exact question, proved reductions, examples, and remaining gap.
2. [Results index](RESULTS_INDEX.md): the mathematical supplements and their precise scopes.
3. [Status and scope](STATUS_AND_SCOPE.md): quantifiers, provenance, and unresolved assertions.
4. [Sources](SOURCES.md): the classical exact series and source-version limitations.
5. [Reproducibility](REPRODUCIBILITY.md): finite replay, interpreter modes, and rejection controls.

Only authored mathematics, synthetic examples, code, and public bibliographic/verification metadata are included. Source PDFs, copied third-party text, external dataset contents, private sources, personal information, and private coordination records are excluded. Acceptance means the independent mathematical review documented with this package, not external peer review or a priority claim.

## Local verification

Python 3.10 or newer, standard library only, no network:

    python3 -I -B verify_package.py
    python3 -I -B run_checks.py
    python3 -I -B check_tamper_controls.py

The wrapper replays the complete included finite certificate, rather than extrapolating an all-scale conclusion from a sample. All-scale statements are justified by the written proofs and their explicit finite reductions. The manifest and acceptance report must agree on the precise final edition.
