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
