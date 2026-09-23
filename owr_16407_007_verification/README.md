# Verification of OWR-16407-007

**Verdict: the displayed identity is true and already proved. The supplied candidate is incomplete, and its novelty claim fails.**

Audit date: 22 September 2026, America/Los_Angeles (23 September UTC).
This is a verification record, not a new mathematical result.

The candidate correctly applies Lagrange–Bürmann inversion to the proposed
series. It then assumes that its resummation equals the function defined by
the model. That identification is precisely the missing step. The original
paper's equation (31) is the conjectured expansion, not an independent
definition of the function; the defining system is v1 equation (26).

Panzer and Wulkenhaar supplied the additional integral verification in
[arXiv v2, §5.2, Lemma 10 and Proposition 11](https://arxiv.org/html/1807.02945v2#S5.SS2),
dated **4 November 2018**. It verifies the actual defining equation, beyond
resumming a guess. Formal uniqueness then gives the requested identity to
every order. The [journal article](https://doi.org/10.1007/s00220-019-03592-4)
was published online on **30 October 2019**, in *Communications in Mathematical
Physics* 374, 1935–1961 (2020).

The [problem listing](https://www.unsolvedmath.com/problems/OWR-16407-007)
still displayed “Open” when inspected. Its literature assessment overlooks
the separate proof in the revised paper. This audit concerns the displayed
formal identity; it does not assert uniqueness of all nonanalytic solutions
of the quantum-field model.

## Check the conclusion

1. Read the [formal proof audit](audit/formal_proof_review.md) for the exact
   logical gap, coefficient recursions, existing repair, and endpoint checks.
2. Read the [priority audit](audit/priority_review.md) for the historical
   equation map, original Oberwolfach source, dates, and the bridge between
   the old and revised definitions of the integral.
3. Run the verifier below. It checks the inversion and composition
   coefficients **symbolically through order 10**, the removable endpoint
   at zero, and **12 numerical coefficient integrals from the defining
   equation** (orders 1–4 at three positive arguments).

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python code/verify.py --order 10 --output evidence/verification.json
```

Run these commands from this directory. The recorded run used Python 3.9.6,
SymPy 1.14.0 and mpmath 1.3.0; see [machine-readable results](evidence/verification.json).
Numerical quadrature is supporting evidence without certified error bounds.
Finite checks are not an all-orders proof; the proof and priority conclusions
come from the mathematical audit and cited sources.

## Publication decision

The user's requested resolution paper, GitHub Pages site, and Zenodo upload
package were conditional on complete verification and clean priority.
Those conditions fail. No new-resolution manuscript, site, Zenodo metadata,
release, or DOI deposit was created. The audit and verifier are retained in
this dedicated top-level repository folder. The theorem's credit remains
with Erik Panzer and Raimar Wulkenhaar. No individuals were contacted.

The [research log](RESEARCH_LOG.md) records checkpoints and completion
estimates; [source observations](evidence/source_observations.md) record
access details. The independent reviewers' notes are preserved as separate
reviews rather than merged into an apparent new proof.
