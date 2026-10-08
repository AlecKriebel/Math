# Squarefree split-circle lattice clusters: accepted partial results

Problem 30003279 / OWR-15174-012; queue rank 996. **Unsolved, 5/5 routes.** Publication checkpoint: 2026-10-08 UTC.

The three-point subproblem is settled by a credited consequence of Cilleruelo–Granville and Booker–Browning: infinitely many admissible circles have three points at arc scale R^(1/3), with sharp limiting constant 16^(1/3). Sharp four-point and general cluster attainability remain unresolved. No positive-density or novelty claim is made.

Start with [publication acceptance](PUBLICATION_ACCEPTANCE.md), the [author report](original/REPORT.md), and the [independent audit](independent_audit/AUDIT_REPORT.md). The [research log](RESEARCH_LOG.md) records the five-route disposition and the separate publication checkpoint.

## Frozen slices

- `original/`: unchanged historical author packet, manifest 1e69db6319607fb6cb9a207193701dbb2fc38e5fe3cd0c799df44a49f6963799.
- `independent_audit/`: unchanged independent audit, manifest 18faf24968d91825ecade1c0858c6e461e316610146f05ac2c8b67eb85affa25.
- `hardened/`: exact separate replay of [VALIDATION_HARDENING.patch](independent_audit/VALIDATION_HARDENING.patch), manifest 025af598dc60fc050dc1f7c4f718bff01cdad761d842854014fd8078eac58f54.

The patch fixes input validation, including seven reproduced re-pinned weaknesses. It makes no mathematical change. The audit is the later acceptance record; historical “audit pending” author text is intentionally preserved.

## Reproduction and trust boundary

Use Python 3.10+ with its standard library. No network, installed package, raw dataset or source PDF is needed. First authenticate `BOOTSTRAP.py` and the publication-manifest SHA-256 independently, using the pinned digests in the PR. Copy the authenticated bootstrap outside the packet. It authenticates `VERIFY_PUBLICATION.py` against its embedded fixed digest before executing any packet code. The manifest alone cannot authenticate a verifier that has itself been replaced.

From an unrelated directory, run:

```sh
python -I -B /trusted/TRUSTED_BOOTSTRAP.py --packet /absolute/path/to/30003279 --expected-manifest PUBLICATION_MANIFEST_SHA256
```

This verifies exact inventory and all frozen anchors, replays every supplied patch byte, runs each original and hardened exact verifier and hostile harness, and replays independent mathematics and regressions. It also tests read-only relocated slices using unchanged frozen pins. `--check-only` skips mathematical replay; it is an identity/structure check only. The default `--mode all` covers normal, -O and -OO child processes. Repeat the outer command with Python `-O` and `-OO` to test the launcher and wrapper under optimization too.

For a full-packet read-only relocation, copy the packet, set files to 0444 and directories to 0555, use `--filesystem-profile readonly`, and run as an unprivileged user. An actual write refusal is required; chmod alone is not treated as proof.

The externally bootstrapped mutation suite is:

```sh
python -I -B /absolute/path/to/30003279/TEST_MUTATIONS.py --packet /absolute/path/to/30003279 --expected-manifest PUBLICATION_MANIFEST_SHA256
```

Run this only after authenticating the whole packet. It copies a trusted launcher outside all mutated packets and tests each case in normal, -O and -OO. See [MUTATION_RESULTS.json](MUTATION_RESULTS.json). Recomputing a manifest is an explicit change of trust anchor; fixed frozen anchors remain independently enforced.

## Scope

Source PDFs, extracts, screenshots, datasets and private coordination files are absent. Public titles, URLs, PDF sizes/hashes, dataset hashes/byte counts/match findings and retrieval history are provenance metadata only. Finite diagnostics and AI-assisted audits do not replace the mathematical arguments or cited analytic theorem and are not human peer review, formal certification or an exhaustive novelty review.
