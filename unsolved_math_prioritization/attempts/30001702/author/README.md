# Minimal facets in triangulated tori: partial result

Problem 30001702 / OWR-4798-027 remains unresolved in this packet. It contains an authored mathematical report and exact checks, not a universal solution.

Results:
- The general bound f_d >= C(2d,d), with a vertex-count refinement.
- The exact answer (d+1)! for d=1,2 and for regular quotients of unimodular lattice triangulations.
- In dimension three, fewer than 24 facets would require five vertices, a complete underlying vertex graph, and one of exactly two necessary f-vectors: (5,27,44,22) or (5,28,46,23). Neither is asserted realizable or impossible.
- Explicit admissible torus quotients checked through dimension five; homology checks through dimension four supplement the geometric torus proof.

Run from any directory, keeping the independently supplied manifest outside this directory:

    python -I -B /path/to/safe/verify_bundle.py --root /path/to/safe --manifest /path/to/MINIMAL_TORUS_30001702_EXTERNAL_MANIFEST.json
    python -I -B -O /path/to/safe/verify_bundle.py --root /path/to/safe --manifest /path/to/MINIMAL_TORUS_30001702_EXTERNAL_MANIFEST.json

The manifest fixes an exact regular-file inventory and hashes, including the verifier. Trust the independently frozen manifest/ZIP identity, rather than treating a self-generated manifest as an authenticity guarantee. The verifier reruns the certificate and compares exact output. It does not prove imported mathematical theorems or the text of the report.

All bundled content is authored mathematical exposition, authored code and public verification metadata. No downloaded paper, copied source passage, catalog contents, dataset contents or private coordination files are included. Independent mathematical/security review is still required before publication.
