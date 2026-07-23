# Discovery Experiments

This directory contains search and exploratory code.  Its output is never
theorem-level by itself.

Every experiment added here must record:

- command and software version;
- deterministic seed;
- exact input or its SHA-256 hash;
- objective and constraint normalization;
- best candidate coordinates and Gram spectrum;
- maximum inner product with enough digits to diagnose, but not certify,
  feasibility;
- active-pair/contact information;
- whether the method imposed symmetry or another restriction.

Certificate generation, if successful, must be separated from verification.

`construction_round2/` records independent searches using asymmetric
spherical layers, projections and rank-five linear maps of \(D_6,E_6,E_7\)
roots, projective-line optimization, and an ansatz motivated by the sharp
abstract deep graph \(C_5\sqcup18K_2\). No feasible 41--44 point code was
found; all outputs are explicitly numerical evidence only.

`construction_round3/` records 152 unrestricted Riemannian
augmented-Lagrangian searches for \(N=41,42,43,44\), including asymmetric
Gaussian starts, perturbed public benchmarks, higher-root projections, and
round-2 warm starts.  It stores complete coordinates, histories, active
graphs, spectra, seeds, software versions, and hashes.  Every maximum remained
strictly above \(1/2\); the directory is numerical evidence only.

`search_local_hybrid_degree3.py` is the discovery-only MILP/separation search
that produced the independently verified degree-three triple
pseudo-distribution.  Its solver status is not used by the certificate.

`search_local_deep_energy.py` explores inexpensive scalar relaxations of the
deep-edge row energy with deterministic seeds.  Its SLSQP outputs are
numerical diagnostics only; the exact envelopes used in proofs are derived
and verified separately.
