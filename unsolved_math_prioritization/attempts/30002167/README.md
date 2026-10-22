# Problem 30002167: a scoped disk-tour counterexample

**Partial result only.** Six distinct rational points strictly inside the Euclidean unit disk refute the printed squared-edge Hamiltonian-cycle bound 8. The queue remains **unsolved, 1/5** because the separate perfect-matching bound 4 and other-convex-body questions are unresolved by this work.

The analytic three-cluster cut proof gives every closed tour cost at least `20667/2500 > 8`. The exact minimum over all 60 undirected tours is `41839/5000`. The configuration has optimal matching cost `3/10000`, so it does not refute the matching question. A limiting family proves that any universal replacement tour constant must be at least 9; sufficiency of 9 is not proved.

## Evidence

- [Analytic proof](author/PROOF.md), independent of enumeration
- [Independent adversarial audit](independent_audit/AUDIT.md)
- [Source provenance and caveats](independent_audit/SOURCE_AUDIT.json)
- [Scoped publication status](PUBLICATION_STATUS.json)

All 11 author files and 8 independent-audit files are preserved byte-for-byte. Original pending-audit and no-remote-write notices are historical; no correction to their original bytes is made. The independent audit found no mathematical flaw within its stated scope. The fixed-cardinality limiting construction includes every even cardinality at least four.

The source formulation is a radius-one planar disk, a closed Hamiltonian cycle, and the sum of squared Euclidean edge lengths. The subsequent four-point remark supplies no new explicit hypothesis. The EMS and TIB PDFs have distinct byte hashes, preserved separately, although the inspected subsection text agrees. The exact aggregator returned HTTP 403, and raw AI corpora were unavailable and uninspected. Record correspondence, novelty, historical priority and global current openness are not certified. The Bern-Eppstein author version inspected is dated 1992, distinct from its 1993 proceedings metadata.

## Portable offline replay

Run `python3 -B /path/to/30002167/verify_publication.py`, then with `-O`, from any working directory. Python 3.8+ and the standard library suffice; no PDFs, private inputs, packages or network are needed. The wrapper checks a closed file set, both immutable manifest anchors, all byte counts and hashes, audit input bindings and scope; then replays the original author and independent programs in normal and optimized modes. It passes the relocated author directory explicitly to the audit program, leaving its historical default path unchanged.

Expected: 172 author checks, 8 author negative controls, independent enumeration of all 5,005 six-edge subsets (60 connected tours after degree/connectivity filters), independent dynamic programming from all six starts, all 15 matchings and 15 independent negative controls. Replay corroborates finite computations; the written proof establishes the general cut argument. Tests are not peer review or a proof of a universal upper bound.

The publication manifest binds all payload files except itself. It is an integrity inventory, not a cryptographic signature; the remote commit identifies the full publication. The wrapper independently pins the two original manifest hashes. This packet includes authored analysis, code and public verification metadata only. Source PDFs, extracts, images, raw external records and private coordination are excluded. No merge, release, DOI deposit or external outreach is part of this draft.
