# Exceptional spherical codes: scoped partial results

Problem **30001065 / OWR-2090-018**, rank 552: universal optimality of the
40-point code on S^9 and the 64-point code on S^13.

**Outcome: unsolved after five substantive approaches.** Neither original
global claim is proved or disproved. The exact primary question was recovered
from the 2008 Oberwolfach report; the catalogue web page returned HTTP 403.

## Retained results

* A complete exact computer-assisted proof that the explicit one-parameter
  40-point rival family in BBCGKS §4.1 never beats the exceptional 40-point
  code for any completely monotonic potential, with equality cases identified.
* Strict local stability when any single point of either code is moved while
  the other points stay fixed, for every nonconstant completely monotonic
  potential. This does not establish stability under collective motions.
* An all-degree obstruction to a sharp polynomial two-point LP certificate
  for the quartic potential. This is an obstruction to that method, not a
  counterexample to universal optimality. Prior non-LP-universality results
  are credited.
* Classical cubic-potential optimality recovered from exact 3-design identities,
  and a sufficient six-inequality Hermite reduction whose unrestricted
  inequalities remain unproved here.

Read [PROOF.md](PROOF.md) for full arguments and claim boundaries,
[SOURCE_GATE.md](SOURCE_GATE.md) for source identification and literature
limits, and [ATTEMPT_LOG.md](ATTEMPT_LOG.md) for the five approaches.

## Reproduce

From this directory:

```sh
python3 verify.py > CHECK_RESULTS.replay.json
cmp CHECK_RESULTS.json CHECK_RESULTS.replay.json
sha256sum -c MANIFEST.sha256
```

The checker uses only Python's standard library and exact integers/rationals.
It reconstructs both Gram matrices, verifies shell and design identities,
checks 104 tangent-frame PSD certificates, and proves positivity of 97
one-variable polynomials on complete intervals using 351 Bernstein leaves
(maximum depth 9). An elementary exact tail covers every power k>=100.
No random search or floating-point optimizer is used.

The mathematical proofs explain why these finite certificates establish the
scoped results. They do not certify the original unrestricted conjectures.
Raw source PDFs, full extracted sources, catalogue corpus, and private context
are excluded. SOURCE_HASHES.json identifies locally inspected public-source
files without redistributing them.

This is an AI-assisted, unrefereed research packet. No historical novelty,
priority, formal-proof-assistant certification, or human peer review is claimed.
The author packet is frozen for a separate independent audit; no audit outcome
is asserted by this README.
