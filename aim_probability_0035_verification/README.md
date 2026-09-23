# Potts censoring: verified counterexample, failed new-discovery priority gate

**Mathematics: PASS. New-discovery priority: FAIL.**

This audit of the user-supplied AIM-PROBABILITY-0035 candidate verifies its
negative answer to the universal finite deterministic heat-bath censoring
question. The same witness and core proof were already published by
**Anonymous on September 6, 2026**, in
[A five-vertex counterexample to ferromagnetic Potts censoring](https://doi.org/10.5281/zenodo.22546547),
version 0.1.0-candidate. The supplied answer itself acknowledges a recently
posted source. This folder records reproduction and attribution, not a new
discovery claim by Alec Kriebel.

## Result checked

On vertices A–E with edges AB, AC, AD, BC, BE, DE, use the three-state,
zero-field Potts Gibbs law proportional to 30 raised to the number of
monochromatic edges. Start all spins at 0. Compare the heat-bath word
`CEBCBAEBE` with the same nine opportunities with opportunity seven skipped,
equivalently `CEBCBABE`. With μ the full law, ν the censored law, and π the
**unconditioned five-vertex Gibbs law**, exact arithmetic gives

```text
TV(μ,π) − TV(ν,π)
  = 7905357280856578194954129502105
    / 766036711510586802141859485820665762204
  > 0.
```

Thus censoring can make the final law closer to equilibrium. This is a full
counterexample to that universal assertion, not a theorem about random-scan
mixing times or every number of colors.

## Reproduce in one command

Python 3.10 or newer; no dependencies, network access, or downloaded code:

```sh
python3 aim_probability_0035_verification/verification/run_all.py
```

From this folder use `python3 verification/run_all.py`. This runs both
implementations with normal and optimized Python, compares their retained
certificates, and cross-checks **all 243 probabilities in each of the two final
laws**. It fails with a nonzero exit status if any check fails.

- [Neighbor-count and marginal verifier](verification/verify.py): reconstructs
  the full laws and checks every supplied formula, sign orbit, and exact value.
- [Integer Gibbs-fibre verifier](verification/independent.py): reconstructs
  updates from global Gibbs weights, using a separate implementation.
- [Exact marginal certificate](verification/certificate.json) and
  [independent certificate](verification/independent-results.json).
- [Mathematical audit](audit/verification.md),
  [independent adversarial audit](audit/exact-independent.md), and
  [source and priority audit](audit/priority-independent.md).
- [Research log](RESEARCH_LOG.md) records checkpoints and completion estimates.

## Publication decision

The requested new-resolution paper, GitHub Pages site, and Zenodo upload kit
were conditional on a clean priority audit. That condition failed: the earlier
DOI archive already contains the graph, schedule, exact gap, marginal reduction,
and sign certificate. Those new-publication deliverables were therefore not
created. No release, deposit, or messages to other people were made.

The checkers were constructed separately within this AI-assisted audit and
then compared. This is computational and mathematical verification, not
unaffiliated human peer review or proof-assistant certification. No exhaustive
claim about the earliest discovery is made; one authenticated earlier exact
publication suffices to defeat a clean priority finding for this submission.

Audit date: September 22, 2026, America/Los_Angeles
(September 23 UTC). Research workspace: Alec Kriebel,
[ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).
