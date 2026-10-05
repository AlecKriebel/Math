# Function Theory 7.4: frozen partial-result packet

**2307004 / AMR-022-7004, rank 688. Unsolved after five substantive approaches.**

The exact target is the optimal universal lower constant for the first n pure power sums of arbitrary complex numbers with one entry fixed at 1. The primary statement controls the scope.

Authored results:

- A rigorous normalization reduction and full complex n=2 optimum sqrt(3-sqrt(5)).
- A self-contained reconstruction of the known strict 1/2 lower bound, with an exact barrier for a naive scalar-invariant improvement.
- Sharp exterior-modulus and real-tuple controls at 1; a degree-dependent coefficient bound.
- An exact inverse-moment criterion and proof that the constant-moment ansatz cannot beat 1.
- A Gaussian-rational certificate specifying n=32 moments, a polynomial with root 1, and every power sum strictly below 29/40.

These do not improve the known best published bounds or determine the sharp constant. No novelty, human peer review, or full resolution is claimed.

Start with PROOF.md. RESEARCH_LOG.md records the five approaches and remaining gaps. SOURCE_VERIFICATION.json records public provenance and access limits. STATUS.json and READINESS.json bind the scope to the catalog descriptors.

## Replay

From this folder run:

    python3 -B verify_exact.py

Only Python 3's standard library is needed for this check. It reads only CERTIFICATE.json and authored code, performs exact rational arithmetic, and prints the expected VERIFICATION.json. It deliberately refuses optimized Python with disabled assertions.

build_certificate.py optionally regenerates the candidate from deterministic rational inputs and floating phase proposals; the verifier is authoritative. explore_two_block.py and EXPLORATION.json are optional, explicitly non-certifying exploration and need NumPy/SciPy. They are not necessary for replay and make no global optimality claim.

The proof is mathematical prose, not a proof-assistant formalization. Computational checks are finite controls only.

## Publication boundary

Only this safe packet is intended for possible publication after a fresh independent audit. It contains authored mathematics/code, exact mathematical certificates and public-source verification metadata. No source PDF, extracted source text, dataset corpus/record, or private coordination record belongs in a remote commit.

No remote write was performed during this investigation. FREEZE_MANIFEST.json hashes the other safe files. Audit and publication are separate later stages.
