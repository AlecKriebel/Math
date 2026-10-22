# Short cycles in highly dominating digraphs: credited prior negative answer

Problem **30001669 / OWR-4791-028**, queue rank **832**, is **already solved negatively** by a published theorem of **Yogesh Anbalagan, Hao Huang, Shachar Lovett, Sergey Norin, Adrian Vetta, and Hehui Wu (2015)**. This package verifies the exact match and records the credit. It claims no new solution or novelty.

## Exact deduction

Noga Alon's question asks whether every finite directed graph in which each subset of at most 100 vertices has a common predecessor must contain a directed cycle of length at most 100. The witness points to every vertex of the subset.

In *Large Supports are Required for Well-Supported Nash Equilibria*, APPROX/RANDOM 2015, LIPIcs 40, pp. 78–84, the authors define `(k,l)`-digraphs on printed page 80 and prove their finite existence in **Theorem 11, printed page 83**. Set `(k,l)=(101,100)`: every subset of at most 100 has the required common predecessor, and every directed cycle has length at least 101. This settles the exact question negatively.

The construction uses positive walks of lengths **1 through 99**, with base girth at least **9901**. A cycle of length at most 100 in the power would lift to a nonempty closed base walk of length at most **9900**, strictly below the girth bound. The independent audit checks the orientation, finite nonempty vertex set, empty and singleton subsets, direct recursion for every size through 100, and loopless simple-digraph interpretation.

The complete authored argument is in [the author report](author/REPORT.md); the separate AI [independent audit](audit/INDEPENDENT_AUDIT.md) and [acceptance](audit/ACCEPTANCE.json) accept the prior-resolution identification without mathematical corrections. These AI checks are not a claim of human peer review of this package.

## Public sources and credit

- Anbalagan, Huang, Lovett, Norin, Vetta and Wu, [*Large Supports are Required for Well-Supported Nash Equilibria*](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX-RANDOM.2015.78), published conference proceedings, 13 August 2015. [Preprint](https://arxiv.org/abs/1504.03602).
- *Combinatorics*, Oberwolfach Reports 8 (2011), no. 1, pp. 5–83; Alon's question at printed p. 74. [Publisher article](https://ems.press/journals/owr/articles/4791), [DOI](https://doi.org/10.4171/OWR/2011/01).

One mathematical approach was used: identifying and specializing this published theorem. Verification and publication do not count as additional proof attempts. The queue records `already_solved`, `1/5`, and a credited Findings link; all other queue bytes are preserved.

## Frozen packages

Both archives are published unchanged and unpacked byte-for-byte into their corresponding directories. The audit archive also contains the unchanged author archive.

| Archive | Bytes | SHA-256 | Inner manifest SHA-256 |
|---|---:|---|---|
| `archives/DOMINATING_DIGRAPH_30001669_AUTHOR_SAFE_FREEZE.zip` | 10114 | `15bb36b2d492b2ace008a6b851b31a3893ec0a559ccc3853a2d709f58f3ed96f` | `d1d79514b2851823f47345677bfa66f53152f1922562b1040f7dd8882028c620` |
| `archives/DOMINATING_DIGRAPH_30001669_INDEPENDENT_AUDIT_SAFE.zip` | 24877 | `637a9051786e69d9d2d12591d9e99fe76044076082ba1777c57e652430c3779b` | `cc8b4329029939eabb9f2c91e4a33e5c1345911e9e5e0417904f364c809352b1` |

Historical fields such as `publication_performed: false` and `remote_mutation_performed: false` describe the earlier author/audit stages and are deliberately unchanged.

## Replay

Python 3.10+ and its standard library suffice. Obtain the externally recorded `PUBLICATION_MANIFEST.json` SHA-256 from the draft PR and verify the wrapper's published SHA-256 before execution. From this directory, replace `EXTERNAL_PUBLICATION_MANIFEST_SHA256` with that pin:

```sh
python -I -B verify_publication.py --manifest-sha256 EXTERNAL_PUBLICATION_MANIFEST_SHA256 --full
python -I -B -O verify_publication.py --manifest-sha256 EXTERNAL_PUBLICATION_MANIFEST_SHA256 --full
python -I -B PUBLICATION_CONTROL_TESTS.py --manifest-sha256 EXTERNAL_PUBLICATION_MANIFEST_SHA256
python -I -B -O PUBLICATION_CONTROL_TESTS.py --manifest-sha256 EXTERNAL_PUBLICATION_MANIFEST_SHA256
```

The wrapper binds the exact regular-file and directory inventory, prohibits links and special files, verifies every payload byte, both archives and all their members, and checks the disposition and construction parameters before replaying any inner script. Its full mode replays both author and independent harnesses and checks their outputs against the frozen results. The publication harness adds original/relocated normal/optimized replays, 17 integrity controls, and 16 re-manifested semantic controls, with rejection required in both Python modes. Replacing the externally trusted manifest pin changes the trust boundary.

[PUBLICATION_TEST_RESULTS.json](PUBLICATION_TEST_RESULTS.json) records the local publication checks. The draft PR's subsequent verification receipt records checks against downloaded remote bytes. A zero count of remote CI checks or runs is not a CI pass.

## Limits and publication boundary

This is a published existence result, not a newly computed adjacency certificate. No exhaustive check of all 100-subsets, proof-assistant verification, new proof of the cited theorem or its additive-number-theory dependency, or exhaustive literature clearance is claimed. Source and corpus authenticity were inspected at the author/audit stages as documented in their public metadata; public replay does not re-fetch the omitted sources.

The package contains only authored reports, audit and acceptance, code, results, unchanged safe archives, and public verification metadata. No third-party PDFs, page images, source extracts, raw dataset records, private source contents, or private coordination files are included.
