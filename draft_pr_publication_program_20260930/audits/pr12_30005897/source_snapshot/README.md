# 30005897: Shadowing without bounded distortion

**Independently AI-audited candidate theorem.** A complete proof is proposed for the exact
dissipative composition-operator equivalence, for every real exponent
`1 <= p < infinity`, over either scalar field. One independent AI audit
found no mathematical gap. Expert scrutiny and historical-priority checking
are required before treating it as established.

The source's companion aggregate-mass characterization question was already
answered negatively in July 2026. That prior result is credited separately.

## Files

- [PROOF.md](PROOF.md): complete statement, proof, new pointwise density
  criterion, original-source scope, and literature boundary
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md): exact source locations, duplicate and
  prior-attempt checks, and limitations
- [RESEARCH_LOG.md](RESEARCH_LOG.md): timestamped checkpoints and estimates
- [attempt_status.json](attempt_status.json): attempt count and disposition
- [source_record.json](source_record.json): pinned upstream record
- [source_provenance.json](source_provenance.json): dataset identity, join
  check, and source-file hashes
- [verify.py](verify.py), [verification.json](verification.json): modest exact
  rational checks of formulas, support propagation, and negative controls
- [review/REVIEW.md](review/REVIEW.md): independent mathematical audit and
  preserved reviewed snapshots, with a separately constructed moving-cut model

## Reproduce the finite checks

From this directory, run:

```sh
python3 verify.py
```

The verifier uses only the Python standard library. It is finite algebraic
and indexing evidence, not a formal proof checker or a proof of the general
theorem. No exhaustive search, external account, or paid model call is needed.

## Candidate mechanism

Two-sided shadowing implies a uniform adjoint-expansion estimate by a finite
dual telescoping argument. Localizing that estimate in orbit coordinates
forces a uniform one-sided drop of each orbit density. These drops give
contracting complementary support bands for a fixed power. A finite
intersection makes the stable band invariant under the original operator,
and a disjoint-support estimate controls the inverse on its complement.

No bounded distortion, pointwise-to-uniform inference, measurable selection
of fiberwise right inverses, or recent uninspected spectral theorem is used.

## Scope and attribution

The numeric upstream identity is `30005897`; its code is
`OWR-14298367-003`. The generalized-hyperbolicity equivalence is distinct from
the scalar aggregate-mass characterization. The separable complex `p=2`
case and the weighted-shift representation are also existing literature.

This attempt used `gpt-6-astra` at `xhigh` reasoning. The queue's original
planning budget mentioned `ultra`; this artifact does not misstate the
execution setting. It is provisional AI-assisted independent research in
the repository of Alec Kriebel (ORCID https://orcid.org/0009-0001-9320-500X).
