# The γ–θ Conjecture in One-Guard Eternal Domination

This directory contains a 27-day, laptop-only research campaign on the
conjecture

> If \(\gamma(G)=\gamma^\infty(G)\), then \(\gamma(G)=\theta(G)\).

Here \(\gamma^\infty\) always means the standard **one-guard-moves** eternal
domination number: attacks occur only at unoccupied vertices and exactly one
guard traverses one edge to the attacked vertex.

## Campaign dates

- Day 1: 2026-07-25
- Day 3 review: 2026-07-27
- Day 7 review: 2026-07-31
- Day 14 review: 2026-08-07
- Day 21 review: 2026-08-14
- Day 27/final package: 2026-08-20

Finite verification or a graph-class theorem is a partial result, not a
resolution. A resolution requires a universal proof, a fully certified
counterexample, or a verified prior resolution.

## Trust architecture

- `src/verifier_a/`: bitset greatest-fixed-point implementation.
- `src/verifier_b/`: structurally independent colored configuration-digraph
  implementation.
- `src/search/`: exploratory and synthesis programs, kept separate from
  decisive checking.
- `math/`: self-contained proofs and adversarial reviews.
- `literature/`: source audit with an explicit model/variant ledger.
- `instances/`, `certificates/`, `results/`: immutable inputs, checkable
  evidence, manifests, and run logs.

No external person may be contacted on behalf of this project. If independent
outside verification would help, that need is recorded only as a research
note.

## Reproducibility status

The repository is under active construction. Consult `STATE.md` for the exact
verified frontier and `CLAIMS.md` for the status of every claim. The current
standard-library test suite is run from this directory with:

```text
python3 -m unittest discover -s tests -v
```

The pinned graph generator is installed locally with:

```text
tools/bootstrap_nauty.sh
```

The published 2022 catalog and its independent clique-cover certificates are
reproduced with:

```text
PYTHONPATH=src python3 -m search.validate_mmv2022 \
  --catalog instances/mmv2022_table9.csv \
  --parameters results/mmv2022_parameters.csv \
  --log results/logs/mmv2022-validation.json

PYTHONPATH=src python3 -m search.certify_mmv2022_theta \
  --catalog instances/mmv2022_table9.csv \
  --certificate-dir certificates/mmv2022_theta_k3 \
  --manifest results/mmv2022_theta_certificates.csv \
  --log results/logs/mmv2022-theta-certificates.json
```

The second command independently replays every saved proof when the
certificates already exist. It never silently replaces an invalid or
mismatched certificate.

The certified one-vertex-extension result (claim C-018) can be replayed
without rerunning or modifying the frozen search.  The first, read-only
command reconstructs all 110,537 labeled extensions and checks their 54,216
canonical-class receipts; the second checks every saved domination,
independence, and one-guard fixed-point certificate using the separately
written mathematical verifier:

```text
PYTHONWARNINGS=error python3 reviews/extension_coverage_hostile_probe.py

PYTHONPATH=src PYTHONWARNINGS=error python3 -m evaluation_checker \
  --verify-only
```

To regenerate that bounded search from the pinned 55-graph input catalog,
use:

```text
PYTHONPATH=src PYTHONWARNINGS=error python3 -m search.extension_killtest \
  --validation-gate-open \
  --batch-size 256 \
  --wall-limit-seconds 2700 \
  --memory-limit-mib 1024
```

The production search is transactionally resumable.  The replay commands are
read-only and check the installed artifacts against their recorded hashes
rather than replacing them.

Claim C-019, the complete one-edge-toggle search around the 391 closest
extensions, has the same two-layer replay:

```text
PYTHONWARNINGS=error python3 reviews/edge_toggle_coverage_hostile_probe.py

PYTHONPATH=src PYTHONWARNINGS=error \
  python3 -m edge_toggle_evaluation_checker --verify-only
```

The first command reconstructs all 25,641 labeled toggles and verifies their
19,136 canonical-class mappings.  The second independently proves
`gamma < gamma-infinity` for every class from the installed domination and
one-guard fixed-point certificates.

Claim C-020 gives a stronger local obstruction: when
`alpha=gamma-infinity=k`, every maximum independent set must survive two
adaptive attacks, not merely one.  Its compact private-region certificate
and the C-021 pruning measurements can be independently replayed with:

```text
PYTHONWARNINGS=error python3 reviews/two_step_transition_hostile_probe.py
```

That read-only probe imports no campaign evaluator.  It reconstructs the
8,587 selected edge-toggle rows and streams the complete connected-unlabeled
orders 5 through 9.  The resulting counts are labeled `OBSERVED`; they do
not exclude all graphs of order 10 or higher.
