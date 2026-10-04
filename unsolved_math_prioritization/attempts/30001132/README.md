# Prior counterexample to admissible Gelfand-Zetlin representation

Problem 30001132 / OWR-3384-004, rank 665. **Already solved negatively, 1/5. No novelty claim.**

Read [the current-disposition addendum](RELEASE_ADDENDUM.md), [the reconstructed proof](author/PROOF.md), and [the complete independent audit](audit/AUDIT_REPORT.md). Kiritchenko's published IMRN 2010 article, p. 2522, already reports the smooth SL4 failure. The packet reconstructs X_2413 and gives a necessary-condition obstruction for each of the 24 fixed-torus Borels using the original codimension-one predecessor criterion.

The `author/` and `audit/` directories preserve every frozen byte. Historical pending-audit statements are archival; the completed audit passes without corrections. The duplicate ID 30001133 is metadata only. No union, sum, general-face, or polytope-ring conclusion is asserted.

## Reproduce

Use Python 3.10+ with its standard library, from any working directory:

    python3 -B /path/to/this/verify_release.py

This checks the entire release inventory, both frozen bindings, and original author/audit file hashes; replays the author enumeration, tangent-cone checker, six regression tests, and independent H-polytope checks for five top rows; and rejects six invalid certificate variants. Expected n=4 nonrepresentable classes are 2413, 3412, 4231; 2413 is the smooth example. The independent checks verify 72 witness instances over three n=4 top rows. Source text is not needed for portable computational replay.

The release manifest inventories every other release file by SHA-256 and byte count. Its hash is recorded in the publication receipt. `PUBLICATION_PROVENANCE.json` records fresh repository gates and queue scope. The code checks finite certificates and their general-label structure; the written source comparison, geometric smoothness proof, and quantifier analysis remain essential.

Only authored mathematics, code, full audit, and public verification metadata are included. No merge, GitHub release, DOI creation, or outreach forms part of this draft.
