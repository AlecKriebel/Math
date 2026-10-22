# Publication package: initial odd-ear prefix

The current research note is **NP-completeness of the initial odd-ear prefix**,
Alec Kriebel (ORCID0009-0001-9320-500X), version1.0.0, 22 October2026.
Read [the six-page paper](publication/initial-odd-ear-prefix.pdf) and
[editable source and exact verification](publication/initial-odd-ear-prefix-source-and-verification.zip).
The expanded editable package is also in [publication/source](publication/source/README.md).
No Zenodo publication or DOI is asserted by this file.

The theorem proves NP-completeness of the variable-threshold decision
beta(G)>=t for finite loopless2-vertex-connected graphs. Hardness already
holds on simple cones with a specified universal apex and connected bipartite
base. Beta counts the initial circuit and one-edge OPEN ears and stops at
the first even ear. This resolves the computational question in Sebo's
OWR2014Question4 and Benchetrit--Sebo2015Question3.3. No P!=NP, fixed-threshold,
closed-ear, maximum-total-odd-ear or general matroid result is claimed.

The note imports the classical Lovasz all-odd open-ear characterization and
Set Cover NP-completeness, and gives full proofs of the cone identity and
reduction, including all preprocessing outputs within the cone subclass,
private-element perfect matchings and arbitrary partial-block omissions.
Finite exact diagnostics supplement the universal proof; they do not replace
it. The source README describes offline reproduction and its precise bounds.
The six release products in publication/ were reproduced byte-for-byte from
the reviewed source; the builder copies the frozen PDF.

The original fourteen files at this directory's top level are preserved
byte-for-byte from PR1372 commit
d34aba3697196aff2e4fc06e29f71afb5d793499. They are historical proof/audit
materials. Their MANIFEST.json and recursive verify_manifest.py describe
only that original fourteen-file snapshot: running the legacy verifier on
this expanded directory will correctly report the newly added files as
extras. To replay that historical verifier, use a separate copy containing
exactly those fourteen original files from the pinned commit. The current
publication uses publication/source/source-manifest.json and its own
reproduction instructions. The current paper includes the cone-class
preprocessing convention and the publication-specific scope and references.

Extensive AI involvement in research, proof development, computation,
literature investigation, writing and adversarial auditing is disclosed in
the paper. This is an unrefereed preprint without formal independent human
peer review or proof-assistant certification. Primary-source priority work
is bounded, with no exclusive-firstness certification; exact inspected
versions and access limits are in DEPENDENCIES.md and PRIORITY.md. Authored
prose is CC BY4.0 and authored code MIT licensed.
