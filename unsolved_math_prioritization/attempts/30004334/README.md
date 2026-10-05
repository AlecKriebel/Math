# Root-of-unity blowups: audited partial-results checkpoint

Problem 30004334 / OWR-17296-019, rank 747. **Unsolved, 5/5 substantive approaches.** The general fixed-order complex problem for m >= 4 remains unresolved by this packet. No novelty, priority, full solution, or complex counterexample is claimed.

## Results and limits

The signed optimal bounds for m=1,2,3 are -1,-1,-2. The packet proves the vertical-curve classification, equal-multiplicity obstruction, and several divisibility/cover implications. Its infinite numerical family on X_4 is **not** a family of realized integral curves: two exact interpolation minors exclude its first two cases; Hao's genus-dependent result excludes every remaining case. Positive-characteristic unbounded-negativity examples do not supply complex counterexamples.

The author and independent-audit trees are preserved exactly under `author/` and `audit/`. Their historical preparation-time statements, including the author's pending-audit wording, are frozen provenance. The completed independent audit is PASS within the stated partial-results scope with no mandatory correction. Mathematical certificates do not formalize every geometric proof or certify global literature completeness.

## Reproduce

Python 3 standard library only; no downloads or source PDFs are required. From any working directory:

```sh
python3 /path/to/verify_publication.py /path/to/package PUBLICATION_MANIFEST_SHA256 --queue /path/to/QUEUE.md --replay
python3 -O /path/to/verify_publication.py /path/to/package PUBLICATION_MANIFEST_SHA256 --queue /path/to/QUEUE.md --replay
python3 /path/to/test_publication.py /path/to/package PUBLICATION_MANIFEST_SHA256 --queue /path/to/QUEUE.md
```

Use the publication-manifest SHA-256 recorded in the draft PR as the external pin. The publication gate rejects symlinks, unexpected files/directories, duplicate JSON keys, missing or changed bytes, and replacement manifests. It checks both immutable inner manifest hashes. The author verifier alone accepts a manifest-only symlink to identical pinned bytes; the stricter independent and publication gates reject that case.

The replay invokes both independent arithmetic reconstruction and the original/relocated, normal/optimized suite: eight full runs, seven author mathematical negative controls, and thirty integrity rejections. Publication-specific mutation controls are separately reproducible.

## Queue and publication scope

The exact live-base queue blob is bound in QUEUE_PATCH.json. Only this target's Status and Turns change to `unsolved` and `5/5`. Findings, Chat, DOI, every other row and byte, and the existing stale embedded header are preserved. A supplied queue file is verified against the updated hash and reverse-patched to the actual original Git blob.

Only authored proof, code, audit analysis, and public-source/verification metadata are included. No PDFs, source extracts, raw external datasets, or private coordination files are distributed. No GitHub release, merge, or outreach is authorized by this checkpoint.
