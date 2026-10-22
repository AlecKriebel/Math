# 10400081: integral skein torsion, scoped partial results

**Original conjecture remains unsolved after five substantive approaches.** No new complete proof or manifold counterexample is claimed.

Read PROOF.md for the full authored deductions and exact remaining gap. SOURCES.md records the primary-source audit through September 2026, with explicit distinctions between Z[A±1], Q[A±1], generic coefficient fields, atoroidality, and absence of all essential closed surfaces. APPROACH_LOG.md records the five attempts.

The strongest reusable deductions are:

- torsion-freeness is preserved by suitable filtered skein-module unions, even without injective transition maps;
- an integral generating set whose size equals generic rank is automatically a basis;
- torsion in a presentation is precisely its saturation quotient;
- maximal-rank minors of a full finite relation matrix annihilate torsion;
- complex specialization and height-one-localization tests can miss nonzero integral torsion.

These deductions do not bridge the manifold hypothesis to integral saturation. Classical product-surface cases and published topology are credited. Abstract obstruction modules are not manifold counterexamples. No historical novelty is asserted.

## Reproduce

Run `python3 verify.py` from this folder. It uses only the Python 3 standard library and produces the deterministic CONTROL_RESULTS.json content. The author run passes 7,396 exact assertions. This verifies local tangle identities, arithmetic and algebraic control models. It does not compute an unknown manifold's skein module or formally verify the imported literature.

MANIFEST.json binds all other files in this author packet. An independent audit is required before any publication. This frozen author packet makes no claim that such an audit has already passed.

The packet excludes scholarly source files, raw source extracts, screenshots, raw datasets and private coordination. No remote write was made in preparing it.
