# ID 30006556: two low-multiplicity planar distances

**Disposition: unsolved, 5/5 substantive approaches.**
Original: OWR-14299905-031, rank 774, Erdős–Pach Question 1 in
[Oberwolfach Report 1/2026](https://doi.org/10.4171/OWR/2026/1), printed p.69.
The imported statement matches the primary question, including n>4 and
unordered pairs. This is also the first part of Erdős problem 132; that
broader record additionally asks for a diverging number of sparse distances.

The main scoped result is an authored proof for configurations with all but
one point on a circle. Also included are a collinear-subset criterion, a
credited hull-layer corollary, and an exact 61-point specialization of the
known obstruction to using just the minimum and second-largest distances.
Neither the universal conjecture nor novelty is claimed.

Read PROOFS.md, then RESEARCH_LOG.md and LITERATURE.md. Source inspection and
prior-attempt limits are in SOURCE_VERIFICATION.json. All proofs use exact
Euclidean distances; pair counting is unordered. Finite examples do not
prove the general result.

Run with Python 3, standard library only:

    python3 verify_math.py
    python3 verify_manifest.py

The first emits deterministic JSON to stdout. Compare it with CHECK_RESULTS.json.
The second checks the complete safe-file inventory, sizes and SHA-256 hashes.
Independent mathematical/source audit is pending; author checks are not an
auditor's approval. Source PDFs, full-text extracts, images, raw datasets,
selected records and private coordination are intentionally excluded.
