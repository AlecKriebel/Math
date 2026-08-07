# Verification transcripts

- `clean_quick_verification.txt`: clean release/build/package verification for version 1.1.1.
- `clean_full_verification.txt`: compositional full independent verification for version 1.1.1.  It reruns every dependency introduced by the automatic-triangle strengthening in independent Python and C++ implementations, and checks the unchanged base statistical/atlas release against its preserved clean full-adversarial transcript and byte-level file manifests.
- `base_release_full_adversarial_verification.txt`: byte-preserved clean full replay of the unchanged version-1.0 statistical and finite-atlas base.
- `automatic_triangle_primary.txt` and `automatic_triangle_independent_cpp.txt`: focused new structural theorem replays.
- `clean_pointwise_cut_adversarial.txt`: preserved independent cut-theorem replay from the hash-locked base release.

The optional `reproducibility/verify_regenerate_all.sh` regenerates every large signature stream and relation universe from primitive definitions.  The default full release command uses the preserved clean base replay for the unchanged heavy algebra and freshly reruns every newly introduced dependency.
