# Problem 2303022: corrected unresolved research checkpoint

AMR-022-3022, Hayman--Lingham Function Theory Problem 3.22, queue rank 572.
4 October 2026. **Unsolved after five approaches.**

Read [the corrected proof](corrected/proof.md),
[its research summary](corrected/README.md), and
[the independent audit](audit/AUDIT.md).

The exact sharp supremum for arbitrary radial-covering closed obstacles remains
undetermined. The packet proves a nonsharp universal escape bound q(E)<=15/16,
an explicit positive-escape construction, and topological obstructions to two
naive reductions. Its finite-component bound is conditional on the cited
connected-set theorem. The full proof of that published theorem was not
independently retrieved or reverified. The exploratory finite-difference values
are not certified continuum bounds or a global optimization.

## Correction and provenance

- `corrected/` is the reviewed current packet. Its connected-theorem application
  explicitly assumes compact continua strictly inside the unit disk, avoiding 0.
  This is the scope compatible with its strict-before-outer-boundary hitting
  convention. The Brownian process is killed at its first unit-circle exit;
  obstacle hits are counted before that exit and escape is the complementary
  event. No broader boundary-contact assertion is used.
- `frozen/` preserves the original research freeze byte for byte solely as
  historical audit evidence. Its original Section 3 mixed a closed-disk theorem
  with the strict hitting convention. That text required correction and must
  not be cited as the accepted current statement.
- `audit/` is the complete independent review, exact patch, corrected proof,
  replay outputs, and verifier. It records both the original defect and the
  corrected scoped PASS. PASS concerns an unresolved research checkpoint, not
  resolution, novelty, peer review, or a sharp extremizer.

The author's post-audit verification agrees with the correction: an arc lying
on the unit circle cannot be hit strictly before reaching that circle. Restricting
the application to compact interior continua repairs the defect and is sufficient
for the finite-component argument. The universal Green-potential result does not
use the connected theorem.

Manifest SHA-256 identifiers:

- Original freeze: b5ab673a48038729e817852896c54a8467857461d280acc703f8df7c2bcd2903
- Corrected packet: 827ffe2024be7de0a259ebabe2d7b401aa42c0bac0fbf242e62d5262a1e719c8
- Full audit: f77c6569a6258a92ce7a2c7b57ec568b20c22b19fb59f4e20326683d9c0093a8

The historical logs' references to pending audit describe the original freeze,
not the final reviewed release. The full audit's no-remote-writes statement
likewise describes the audit itself. No source PDFs, catalogue corpora, or
private coordination files are included in this release.

## Reproduce from this directory

    sha256sum -c SHA256SUMS
    (cd frozen && sha256sum -c SHA256SUMS)
    (cd corrected && sha256sum -c SHA256SUMS)
    (cd audit && sha256sum -c SHA256SUMS)
    python3 audit/verify_audit.py frozen
    python3 corrected/controls/verify.py
    python3 corrected/controls/explore_two_arcs.py

The exact checker uses the standard library. The optional numerical experiment
requires NumPy and SciPy. All 27 exact controls and the numerical experiment were
replayed in this final layout; output identities are recorded in
`release_checks.json`. These checks establish their stated finite scope only.
