# KP-2.33: audited surface-action partial results

**Unsolved, five of five approaches used.** This packet does not provide a finitely generated torsion-free group excluded from every faithful homeomorphism action on a prescribed closed surface. It also does not prove a universal embedding theorem. The scope is arbitrary faithful C0 actions; smoothness, freeness and local-action hypotheses cannot be silently added.

Start with [the corrected proof](corrected/PROOF.md), [the independent mathematical audit](audit/AUDIT.md), and [the acceptance record](audit/ACCEPTANCE.json). All five numbered propositions were accepted as scoped partial results. The original author freeze is retained separately in `original/` and as an unchanged archive.

The audit corrected one ancillary comparison: local moving and existence of a dense global orbit are incomparable. The exact [correction patch](audit/CORRECTION.patch.txt) changes five existing files. The corrected derivative also adds `CORRECTIONS.md` and regenerates `MANIFEST.json`. Actual zero-fuzz patch replay, byte comparison, regenerated inventory, and acceptance-to-archive bindings are checked independently during publication.

## Results and limits

1. Countable left-orderable groups admit explicit faithful disk-boundary actions, hence faithful actions on every nonempty surface.
2. Hyde's credited non-left-orderable disk group is finitely generated and torsion-free, so non-orderability alone does not obstruct such actions.
3. The level-three subgroup of SL(4,Z) is an infinite finitely generated torsion-free candidate with a credited C2 obstruction. Its C0 obstruction remains unproved.
4. Le Roux's free-planar obstruction coexists with a faithful disk action for the named group.
5. A faithful locally moving torsion-free surface action forces a copy of Z^n for every n. Local moving is an extra hypothesis.

This is AI-assisted, unrefereed work with an independent scoped mathematical audit. The audit is neither peer review nor formal verification. Deep cited theorems are credited inputs; their full proofs were not independently reconstructed. No novelty or worldwide-open-status certification is made.

## Reproduction and byte integrity

The archives and extracted files are data-only mathematical exposition and public verification metadata. The historical external validator and publication verifier are separate supporting code. Neither executes archive payloads. Verification requires Python 3.10+ and GNU patch at `/usr/bin/patch`.

Externally authenticate `verify_publication.py` and the SHA-256 of `PUBLICATION_MANIFEST.json` before running. Do not derive a trusted pin from an untrusted replacement. From any working directory, run:

    python3 -I -S -B /absolute/path/verify_publication.py /absolute/path/2781 TRUSTED_MANIFEST_SHA256
    python3 -I -S -B -O /absolute/path/verify_publication.py /absolute/path/2781 TRUSTED_MANIFEST_SHA256

The verifier checks exact files and directories, rejects links and special files, checks every publication file against the pinned manifest, authenticates the three frozen archives, checks extracted bytes, replays the actual patch, and binds corrected acceptance. The input filesystem, interpreter, standard library, trusted verifier, manifest pin, and GNU patch are trust assumptions. This is not protection against concurrent privileged modification. It establishes packaging and byte identity, not mathematical truth or fresh source retrieval.

`PUBLICATION_TEST_RESULTS.json` records fresh normal, optimized, relocation, hostile-import and mutation controls. Historical audit records remain preserved as historical records, including preparation-time publication flags. The only queue changes are rank 859's Status and Turns; scores, findings, links and all other rows remain unchanged.

No copied source documents, source excerpts or images, datasets, private sources, or private coordination material are included. Public source URLs, titles, inspection histories, byte counts and hashes remain in the authored metadata. No release, DOI, merge, or outside outreach accompanies this draft publication.
