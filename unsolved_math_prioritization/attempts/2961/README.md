# KP-4.85: unresolved after two approaches

The problem still asks for a closed orientable smooth four-manifold whose **full** identity component of diffeomorphisms has unbounded commutator length. This package does not supply one.

[PARTIAL.md](PARTIAL.md) explains why the familiar surface examples do not transfer by taking a product with S2: every stabilized element f×id has ambient commutator length at most four. This follows from classical commutator compression. The note also identifies the missing defect term in direct invariant-measure averaging and distinguishes subgroup, covering-group and fragmentation conclusions.

[SOURCE_AUDIT.md](SOURCE_AUDIT.md) records two useful corrections: known uniform-perfectness results include S1×S3 and other four-manifolds without 2-handles, and record **30004403 / OWR-17471-009** is the exact same target and must not receive a duplicate attempt.

Run `python check_algebra.py` to reproduce 6,570 exact finite assertions. These diagnostics support the displayed identities and negative control; they do not solve the original problem.

Separate adversarial review is pending. This is a source-qualified unresolved partial with no novelty claim. The actual model was gpt-6-astra at xhigh reasoning.
