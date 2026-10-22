# Directed jet curvature and real first Chern class: audited partial results

Problem 30002180 / OWR-12015-001, queue rank 717. **Unsolved, five of five substantive approaches completed.** No general solution, general counterexample, novelty, priority, peer-review or global-openness claim is made.

The target concerns positive-dimensional smooth compact projective complex manifolds with a nondegenerate singular negative k-jet metric on the tautological line, with negativity only along the directed bundle. Nonzero real c1 means a non-torsion integral class; a nonzero torsion class is insufficient. Total negativity is a stronger hypothesis and is never silently substituted.

## Reading order and preserved history

1. [Exact statement](author/STATEMENT.md), then [five-attempt log](author/ATTEMPT_LOG.md) and the five full attempt files.
2. [Independent audit](independent_audit/AUDIT.md), especially its singular-potential restriction argument. This is the controlling analytic explanation for the compressed restriction passages in Attempts 2 and 5. It uses quasi-psh canonical potentials, local boundedness on regular jets, holomorphic extension and flow coordinates, convolution and restriction limits. It does not assume total positivity or an arbitrary pullback of currents.
3. [Audit results](independent_audit/RESULTS.json), [source audit](independent_audit/SOURCE_AUDIT.json) and [publication status](PUBLICATION_STATUS.json).

The author directory is the accepted v2 packet, preserved byte-for-byte. Its historical pending-audit and no-remote-write statements describe its freeze; the separately preserved audit supplies the subsequent review. Both original author versions remain preserved at their source. Only STATEMENT.md and its manifest changed in v2, clarifying integral non-torsion. The audit's packet binding records both versions. There were no mandatory mathematical corrections. This wrapper records the later publication gate without rewriting either frozen packet.

## Retained scope and exact gap

- Kähler-induced negative holomorphic sectional curvature gives nonzero real c1 by scalar trace.
- Immersed compact curves satisfy a genus inequality, giving the affirmative dimension-one case.
- A big tautological line supplies an ample-negatively-twisted invariant jet section under that additional hypothesis.
- Real-c1-zero projective manifolds have no such twisted Green–Griffiths or invariant jet sections, relative to Calabi–Yau existence and the stated Bochner/filtration inputs.
- Complex tori and finite étale torus quotients cannot carry the specified nondegenerate metric, at any jet order.

The missing general implication is directed positivity forcing a forbidden twisted jet section, or a suitable directed current with controlled nonpositive tautological pairing. Neither implication is proved. Golota's total-negativity theorem is stronger than the target. The inspected 2026 first draft concerns geometric hyperbolic indices, not a first-Chern-class conclusion.

## Verification and limitations

Run `python3 verify_publication.py --expected-manifest HASH --self-test`, using the SHA-256 of PUBLICATION_MANIFEST.json recorded in the draft PR. The wrapper checks exact directory and file allowlists, immutable author/audit bindings, byte counts and hashes, normal-Python verifier replays, and actual corruptions in disposable copies. It works from an unrelated working directory and under `python3 -O`; frozen assertion-based child scripts are always run with optimization disabled.

The author replay has 3,274 assertions; the independent program has 8,705. Four audit integrity mutations were rejected. These are finite controls, not analytic proof certificates. The publication wrapper adds independent integrity-corruption tests.

The audit independently retrieved and matched five primary PDFs by hash and size and inspected the specified pages. The exact target website and raw AI corpora were not inspected. Source files, extracted text, page images, raw records and private coordination are excluded. Only authored work, deterministic code and public verification metadata are published.

The only existing repository file changed is QUEUE.md: this row's Status becomes `unsolved` and Turns becomes `5/5`. Findings, Chat, DOI, every other row, and all other bytes including the inherited header remain unchanged. Queue regeneration is intentionally outside this release. Publication remains a draft PR; no merge, release, DOI or outreach is requested.
