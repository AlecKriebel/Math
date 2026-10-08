# 10300043: short geodesics and taut foliations

**Unsolved, 5/5 substantive approaches. Independent mathematical review pending.** No universal isotopy or homotopy threshold, geodesic counterexample, novelty, or formal verification is claimed.

The main useful result is an exact leaf-space reformulation of the restricted cooriented closed-manifold homotopy problem: it asks for a uniform hyperbolic length gap for deck transformations that send every leaf to an incomparable leaf. The other approaches prove a fibration-period bound, a calibrated meridional area inequality, a disk-filling transverse-core criterion, and a countercheck showing why arbitrarily short arbitrary knots cannot replace geodesics. See PROOF.md for every hypothesis, proof, attribution, and missing step.

Known special cases are explicitly credited. In particular Otal's genus-dependent bundle theorem, as stated in Breslin, is not converted into a genus-independent solution; the complete original Otal proof was not inspected.

## Reproduction and boundaries

The packet contains authored mathematics, public hash metadata, and small regression checks. No source PDF, source extract, dataset contents, or private coordination file is included. The enclosing freeze contains an external manifest and bootstrap. Authenticate the bootstrap against the separately supplied SHA-256 receipt before executing it; it pins the external manifest, authenticates every packet member, and only then runs the packet verifier. This is an integrity boundary, not a proof-assistant certificate or protection against simultaneous replacement of all external trust anchors.

Run `python3 bootstrap.py` from the enclosing freeze. Ordinary, `-O`, and `-OO` execution are supported and give identical results. `python3 controls.py` runs the independent-of-payload integrity mutation suite and read-only relocation checks. Direct `python3 packet/verify.py --input candidate.json` tests the strict claims schema but does not authenticate the proof packet.

If the separately retained primary sources and corpus files are supplied, `python3 packet/verify_inputs.py --sources SOURCE_DIRECTORY --corpora CORPUS_DIRECTORY` matches all full-file hashes and the unique selected record/report pair. This optional replay does not perform a new literature search or certify the mathematical content of external sources.

Finite arithmetic, group, and parser controls are regression tests only. No network writes, publication, merge, or external outreach is performed by the scripts.
