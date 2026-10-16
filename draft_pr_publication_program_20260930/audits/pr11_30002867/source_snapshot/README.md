# Matrix characterization of complete intersections

A complete candidate rank criterion for UnsolvedMath problem **30002867** (OWR-13678-008) is given in [CANDIDATE.md](CANDIDATE.md). It answers the precise affine complete-intersection characterization using the first two maps of the Koszul complex of the shifted multiplication matrices.

**Research status:** mathematically checked characterization; independent review passed. Novelty and first-resolution priority are not established. The key algebraic ingredients are classical. The review is AI-assisted; no external human peer review or formal proof verification is claimed.

## Contents

- `CANDIDATE.md`: exact statement, complete proof, scope, examples, and references
- `check_koszul.py`: standard-library-only exact rational checks
- `check_results.json`: reproducible output for 13 examples
- `independent_review/`: independent review and 20 separately coded exact examples
- `source_records.json`: pinned source record and duplicate record 30002868
- `SOURCE_AUDIT.md`: original-source, literature, prior-attempt, and error audit
- `readiness.json`: source hashes and scope evidence
- `turn_ledger.json`: one substantive proof attempt, yielding the candidate
- `RESEARCH_LOG.md`: timestamped checkpoints and completion estimates
- `independent_review/`: independent mathematical audit and 20 exact stress tests

## Reproduce

From this folder run:

```sh
python3 check_koszul.py > /tmp/check_results.json
cmp check_results.json /tmp/check_results.json
```

No packages, downloads, floating-point arithmetic, or large computation are needed. The independent checks can be run with `python3 independent_review/independent_checks.py`. The proof file is frozen at its reviewed hash; its initial pending-review header is superseded by the completed review and this status summary.

## Independent verification

From the `independent_review` subdirectory run:

```sh
python3 independent_checks.py
```

The candidate author's 13 exact examples and the reviewer's independently implemented 20 examples all pass. The two suites overlap and are not claimed to comprise 33 distinct algebras. No computational check substitutes for the proof or establishes novelty.

## Attribution

The source records are derived from *UnsolvedMath: A Curated Collection of Open Mathematics Problems*, UnsolvedMath Contributors (2026), dataset `ulamai/UnsolvedMath`, revision `37e53eabe540fb458758e198be61634bd02ee008`, under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Underlying papers retain their own terms. Their full text is not redistributed in this package.
