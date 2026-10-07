# VMRT normality: credited prior negative resolution

Problem **30001917 / OWR-11139-010**, queue rank **982**. Queue status: **already_solved**. Answer: **negative, from credited prior literature**. New mathematical research turns: **0/5**.

Casagrande–Druel (2015) provide an irreducible sextic VMRT with smooth genus-seven normalization. Its arithmetic genus is ten, so its normalization defect is three. This fits the original Oberwolfach report's locally unsplit definition and codimension-one scope. Their family is explicitly not degree-minimal for any ample polarization. Hwang–Kim (2015), with `n=6,d=3`, separately provide a genuinely degree-minimal unsplit Picard-number-one example; that example has codimension two.

Read [the unchanged authored report](original/REPORT.md), [the independent acceptance audit](independent_audit/INDEPENDENT_AUDIT.md), and [publication acceptance](ACCEPTANCE.md). Both constructions are credited prior results. No new counterexample, novelty, numerical general-polynomial witness, or formal proof of the cited geometric theorems is claimed.

## Portable verification

Python 3 standard library only; no network, third-party packages, PDFs, or datasets are needed. Obtain the publication manifest SHA-256 independently from the draft PR receipt. From this directory run:

```
python -B verify_publication.py --expected-manifest-sha256 TRUSTED_SHA256
python -B -O verify_publication.py --expected-manifest-sha256 TRUSTED_SHA256
python -B -OO verify_publication.py --expected-manifest-sha256 TRUSTED_SHA256
python -B mutation_tests.py --expected-manifest-sha256 TRUSTED_SHA256
```

Use a trusted checkout or independently verify the manifest's SHA-256 and the verifier's recorded SHA-256 before executing it. An executable cannot establish its own authenticity after arbitrary replacement. Do not derive the trusted digest from a potentially modified packet and treat that as an independent integrity anchor.

The publication wrapper requires an external manifest digest, enforces exact file and directory inventories, rejects symbolic links and special files, checks all sizes and hashes, enforces the independently pinned original and audit manifests, compares the preserved ZIP to the original, and replays all 28 frozen arithmetic/metadata checks. It rechecks every byte after execution. It runs correctly from an unrelated working directory, under relocation, and under normal, `-O`, and `-OO` Python. The corruption controls use disposable relocated copies.

The original checker reports its manifest digest but does not independently enforce it. The wrapper supplies that missing enforcement without altering the original. These checks establish arithmetic consistency and artifact identity; they do not replace the source-based mathematical audit or prove the cited geometric existence theorems.

## Preserved evidence

- `original/`: complete ten-file frozen author packet, unchanged.
- `independent_audit/`: complete six-file independent acceptance packet, unchanged.
- `archives/original_frozen_v1.zip`: original 16,237-byte archive, unchanged.
- `PUBLIC_MANIFEST.json`: exact publication inventory, excluding only itself.
- `PUBLICATION_METADATA.json`: public source/provenance and queue-edit verification metadata.

Historical `publication_performed: false` and similar fields in the frozen records describe their creation-time state and are intentionally preserved. The current publication-level disposition is recorded separately. The publication contains authored exposition and public verification metadata only. No copied third-party source documents, extracts, dataset records, private sources, or private coordination files are included.

## Public sources

- [Hwang's contribution, Oberwolfach Report 47/2011](https://doi.org/10.4171/owr/2011/47), pp. 2690–2692.
- [Casagrande–Druel, IMRN 2015](https://doi.org/10.1093/imrn/rnv011), Theorems 1.9–1.10, Remark 5.4 and Example 5.8.
- [Hwang–Kim, Algebraic Geometry 2015](https://doi.org/10.14231/AG-2015-008), Theorem 1.3 and final proof.
- [Hwang–Mok, Asian Journal of Mathematics 2004](https://doi.org/10.4310/AJM.2004.v8.n1.a6), Theorem 1 and Corollary 1.
