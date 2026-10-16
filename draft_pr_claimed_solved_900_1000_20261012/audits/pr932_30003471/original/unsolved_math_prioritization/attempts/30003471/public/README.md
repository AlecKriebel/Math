# Dihedral comparison: candidate proof and source audit

30003471 / OWR-15427-013, queue rank 999. Date: 2026-10-08.

A complete author candidate proves the stronger statement that weak coordinatewise domination of corresponding interior dihedral angles of combinatorially equivalent convex three-polytopes forces equality. It does not require a smooth map at nonsimple vertices. The argument adapts Bi's smoothing method with a new compatible auxiliary normal map, and uses Brendle's published smooth-boundary Dirac result. It is awaiting a fresh independent full mathematical audit.

Read PROOF.md for the full argument, SOURCE_STATUS.md for exact target/source qualifications, and RESEARCH_LEDGER.md for the bounded duplicate gate and one-approach accounting. STATUS.json is the controlling machine-readable qualification. No novelty, journal acceptance of the candidate, completed independent audit, or formal verification is claimed.

The packet contains authored mathematical discussion/code and public verification metadata only. It excludes source PDFs/extracts/images, dataset records and private coordination material. The external freeze receipt binds MANIFEST.json by SHA-256. Run:

    python3 -B verify_packet.py --manifest-sha256 HASH_FROM_RECEIPT --self-test
    python3 -B -O verify_packet.py --manifest-sha256 HASH_FROM_RECEIPT --self-test
    python3 -B -OO verify_packet.py --manifest-sha256 HASH_FROM_RECEIPT --self-test

The verifier reads all packet files without modifying them. Its optional negative tests use temporary copies outside the packet. The controls check exact finite Clifford identities, elementary finite logic, numerical spherical-contraction diagnostics, and fail-closed package/status handling. They do not certify Sobolev, Dirac, compactness or infinite-dimensional arguments. Independent mathematical review is essential.
