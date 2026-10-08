# Prior negative resolution: proper three-colorings of pseudo-disks

**30003467 / OWR-15427-009. Disposition: already_solved, negative; 0/5 author approaches.**

The intended threshold-four primal conjecture is false by the published disk construction of Gábor Damásdi and Dömötör Pálvölgyi, *Realizing an m-Uniform Four-Chromatic Hypergraph with Disks*, Combinatorica 42 (Suppl 1), 1027–1048 (2022), [DOI](https://doi.org/10.1007/s00493-021-4846-5). This is a credited prior resolution, not new mathematics.

Read `PROOF.md` for the exact deduction, including finite-family quantifiers and open-to-closed conversion. `SOURCE_AUDIT.md` records the inspected sources and access limits. `CLAIM.json` states the exact machine-checked scope. The original target is OWR Conjecture 2, printed p.1173, not the different dual coloring question.

The decisive geometric existence theorem is an external published input. The complete relevant preprint proof was inspected, but this packet neither supplies its geometric coordinates nor independently reimplements the construction. The finite controls only verify elementary transfer calculations and scope/integrity guards. They are not a formal proof checker or human peer review.

Run, from any directory:

`python3 -B /path/to/public/verify_packet.py --expected-manifest SHA256`

Use the SHA-256 of `MANIFEST.json` recorded in the separate freeze receipt. Repeat with `-O` and `-OO`. A manifest pin must come from an independently trusted receipt or commit. Also run `python3 -B /path/to/public/test_packet.py`; it creates disposable copies outside the packet and checks corruptions, malformed inputs, wrongful claims, optimized Python, and a read-only relocation. Ordinary verification never writes into the packet.

Optional provenance replay: add `--source-root /path/to/separately-supplied/sources`. Supply the named files listed by `PROVENANCE.json`; all are required. Without it, source-byte verification is explicitly reported as not run. Source files, source transcriptions, images, imported dataset records, and private coordination are excluded from this public packet.

No remote write, PR, merge, release, or external outreach was performed in this research task. Historical observations and prior status are dated; they do not certify exhaustive worldwide literature coverage.
