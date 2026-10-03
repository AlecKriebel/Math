# Toda stopping-time partials — 8000011 / AMR-079-0011

**Reviewed scoped partial results; original problem unsolved after 5/5 author turns.** This is AI-assisted mathematical work checked by a separate AI adversarial audit, not human peer review. No historical-priority claim is made.

All statements concern the **first simultaneous crossing** T=inf{t>=0: max_i b_i(t)<epsilon}. They do not concern permanent decoupling, one-end deflation, or a maximum of individual first-crossing times.

## Results and exact scope

- For every fixed n, a two-term small-epsilon mean expansion C_n log(1/epsilon)+B_n+o_n(1), with explicit spectral coefficients and an integrable deterministic error envelope.
- For n=2, an exact one-dimensional quadrature for the mean at every epsilon>0.
- For every fixed n and fixed epsilon>0, explicit expectation bounds and finiteness of every positive moment.

The unresolved target is the general-n finite-positive-tolerance mean beyond bounds, or a comparably sharp general characterization. No uniform growing-n/tolerance result or full-diagonalization universality theorem is claimed.

The model is a_i~N(0,2), b_i~chi_(n−i), independently, with Lax clock J'=[B,J], B upper-positive and lower-negative. All normalization conversions are explicit in the proofs.

## Read in this order

1. [Current erratum and status](ERRATUM.md)
2. [Mathematical result summary](random_toda_lattice_8000011/packet/RESULT.md)
3. [Five frozen proof turns](random_toda_lattice_8000011/packet/turns/)
4. [Independent full review](review_toda_stopping_time_8000011/REVIEW.md)
5. [Public source summary](PUBLIC_SOURCE_SUMMARY.md)

The frozen author summary's review-pending language is historical and superseded by the included completed review and this entrypoint. Historical percentage estimates are not calibrated mathematical claims and are not adopted here.

## Verification

Run `python verify_publication.py` from this directory. Python 3 plus mpmath, numpy and scipy are needed for all floating diagnostics. The author supplied **2,559 exact finite comparisons**, represented by 2,238 executed Python assert statements, and four floating diagnostics. The independent review adds 2,049 exact predicates and 47 floating predicates. Floating computations are diagnostics, not interval-certified proofs; finite exact checks supplement the analytic arguments.

Two nonmathematical working-provenance files are omitted. Every included frozen author/review file is unchanged. PUBLICATION_PROVENANCE.json records omissions transparently; the original manifests remain intact. The additive portable verifier validates all included files and all five turn manifests and replays their scripts without depending on omitted material. The archived original verifiers expect the original complete local arrangement; use the portable verifier for this public package. Raw source PDFs and imported reading copies are not included.
