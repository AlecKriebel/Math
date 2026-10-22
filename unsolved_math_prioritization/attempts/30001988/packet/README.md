# Constraint sets after adjoining a differential indeterminate

Upstream numeric ID: **30001988**. Code: **OWR-11575-015**. Queue rank: **654**.

**Status: unsolved.** Five materially different approach families were investigated. This packet does not claim a solution or a counterexample to the full target, and does not claim novelty for its elementary partial results.

The title in the catalogue is potentially misleading: the target concerns differential **constraint sets**, not just ordinary polynomial factorization. The published 2014 reduction has additional hypotheses. A later primitive-element theorem improves one possible route for constant bases, but is not silently substituted for a complete audited reduction.

The strongest self-contained result here is a uniform classification of the test family `(delta Y - a z, 1)`: it is constrained exactly when `a != 0`, for every ordinary characteristic-zero differential field K and differential indeterminate z. This also supplies an explicit failure of naive specialization over a differentially closed base.

- `PROOF.md`: exact conventions, partial proofs, and remaining mathematical gap.
- `RESEARCH_LOG.md` and `turns.jsonl`: five approaches and their stopping points.
- `SOURCE_GATE.md` and `SOURCE_MANIFEST.json`: source scope, provenance, and inspection history.
- `REPOSITORY_GATE.json`: own-row and duplicate checks.
- `verify.py`: exact finite controls and status/scope guards; not a theorem prover.
- `verify_manifest.py`: packet byte-integrity check.

Run `python3 verify.py` and `python3 verify_manifest.py` from this directory. No downloaded source texts, PDFs, raw datasets, or private coordination records are included.
