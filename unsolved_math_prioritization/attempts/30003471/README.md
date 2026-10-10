# Dihedral comparison for convex three-polytopes

**30003471 / OWR-15427-013, rank 999: claimed_solved, 1/5.**
Publication acceptance dated 2026-10-08 UTC; extensive AI assistance, unrefereed.

The unchanged authored proof and two independent full mathematical audits establish,
relative to the stated published smooth-domain analytic input and standard
foundations, that weak corresponding dihedral-angle dominance forces complete
facet-normal Gram equality. This implies the original one-edge weak comparison.
The scope includes arbitrary nonsimple vertices in dimension three. There is no
support-number, edge-length, or whole-polytope metric-rigidity claim.

Start with PUBLICATION_ACCEPTANCE.md and ACCEPTANCE.json. Then read public/PROOF.md,
audit_a/INDEPENDENT_AUDIT.md and audit_b/FULL_INDEPENDENT_AUDIT.md. The historical
candidate still says pending audit: its ten-file freeze is deliberately unchanged.
The later acceptance here supersedes that historical status. Both complete audits
are also preserved byte-for-byte; neither requested a mathematical patch.

Brendle's published smooth-domain propositions provide the specialized black box.
Bi's recent preprint supplies the credited smoothing strategy. A recent Wang-Xie-Yu
preprint asserts related stronger comparison; it is not used as a black box and
its entire proof has not been audited here. No novelty or journal acceptance is
claimed. Computation and hashes are not substitutes for the mathematical audits.

## Reproduce

Python 3 with NumPy, SciPy and SymPy is required for the independent diagnostics.
The checked environment used NumPy 2.3.5, SciPy 1.17.0 and SymPy 1.14.0. Numerical
receipts are compared exactly to the frozen results; a different platform may
legitimately require investigating last-bit differences before acceptance.

Obtain the publication-manifest SHA-256 and wrapper SHA-256 from the PR description
or another independently trusted receipt. First authenticate VERIFY_PUBLICATION.py
against that external wrapper hash, before importing or executing it. Then run:

    python3 -I -B VERIFY_PUBLICATION.py --expected-manifest MANIFEST_SHA256
    python3 -I -B -O VERIFY_PUBLICATION.py --expected-manifest MANIFEST_SHA256
    python3 -I -B -OO VERIFY_PUBLICATION.py --expected-manifest MANIFEST_SHA256

Each invocation replays normal, -O and -OO child modes unless --mode is supplied.
Use an ordinary unprivileged account: read-only write probes must actually fail.
The baseline tree expects files 0644 and directories 0755; an all-read-only copy
uses files 0444/directories 0555 with --filesystem-profile readonly.

After authenticating TEST_MUTATIONS.py through the verified manifest:

    python3 -I -B TEST_MUTATIONS.py --packet . --expected-manifest MANIFEST_SHA256 --expected-wrapper WRAPPER_SHA256

Mutation copies are disposable and outside the packet. The wrapper is authenticated
by an external bootstrap before execution, so altering the wrapper together with
the internal manifest cannot manufacture acceptance under the original external
wrapper pin. Replacing both external trust anchors is outside this threat model.

The original audit_b/independent_controls.py requires a specific sibling directory
and nine local source PDFs. It is preserved unchanged. PORTABLE_INDEPENDENT.py and
the complete PORTABLE_CONTROLS.patch transparently adapt input selection and optional
source hashing only, preserving all mathematical computations. Without sources,
4,137 checks run and nine source checks are explicitly NOT_RUN. With --source-root
pointing at separately supplied original filenames, all 4,146 checks run. Public
metadata lists the source titles, URLs, byte counts and hashes. No source PDFs,
excerpts, images, datasets or private coordination files are in this packet.

The outer manifest binds every delivered file except itself. Fixed inner hashes
also anchor the exact original proof and audit freezes. Strict JSON typing,
duplicate keys, malformed/nonfinite JSON, symlinks, special files, unexpected
directories, bad modes, stale pins and dishonest acceptance claims fail closed.
Normal, optimized and read-only replay verify that the packet does not change.
