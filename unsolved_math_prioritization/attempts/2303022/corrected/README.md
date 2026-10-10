# Fuchs's radial-obstacle problem: unresolved checkpoint

Problem 2303022 / AMR-022-3022, queue rank 572. 4 October 2026.

**Status: unsolved. Five substantive approaches were attempted; no complete
resolution or new sharp constant is claimed.** This is an AI-assisted research
checkpoint, not a refereed paper. Its elementary partial results are not claimed
novel or stronger than the existing literature.

The target asks for the largest probability that planar Brownian motion starting
at the origin reaches the unit circle before hitting an interior closed obstacle
that intersects every radius. Arbitrary disconnected obstacles are allowed.
The published solution for a single continuum does not settle this question.

## Contents

- `proof.md`: exact formulation, full proofs of the partial results, and exact gaps.
- `approach_log.md`: five approach families, findings, failures, and budget accounting.
- `sources.md`: provenance and bounded literature review, including access limits.
- `controls/verify.py`: standard-library exact rational controls.
- `controls/verification_results.json`: recorded controls output.
- `controls/explore_two_arcs.py`: optional NumPy/SciPy finite-difference experiment.
- `controls/two_arcs_results.json`: numerical results with explicit limitations.
- `SHA256SUMS`: immutable content manifest, excluding itself.

## Main proved partials

1. For every admissible obstacle, the escape probability is at most 15/16.
   A self-contained non-sharp radial Green-potential proof is supplied.
2. Two explicit semicircular obstacles have escape probability greater than
   1/(2 * 3^31). Joining their endpoints can reduce escape to zero. Thus adding
   connectors is not a harmless reduction to the known connected problem.
3. Any compact obstacle intersecting each radius exactly once is a Jordan
   separator and has zero escape probability. Selecting one point per ray cannot
   generally preserve compactness and the relevant escape behavior.
4. Subject to the stated published connected-set theorem, a union of k continua
   has hitting probability at least C_conn/k, where C_conn is approximately
   0.977126698498665669. This estimate does not remain useful as k grows.
5. Exact arithmetic encloses the associated rectangle short-side probability in
   (0.0228733015013343, 0.0228733015013344). This is a control for the connected
   special case, not the answer for arbitrary obstacles.

The finite-difference experiment yields no candidate global extremizer. Its
mesh values, inner truncation, and floating-point residuals are not continuum
error certificates. The sharp universal supremum remains undetermined.

## Reproduce

From this directory:

    python3 controls/verify.py
    python3 controls/explore_two_arcs.py
    sha256sum -c SHA256SUMS

The first command uses Python's standard library only. The optional second
command requires NumPy and SciPy; the recorded run used Python 3.12. Numerical
output may vary slightly by platform. No network access or private source files
are required to rerun either script. Source documents and catalogue corpora are
not redistributed in this package.
