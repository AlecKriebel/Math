# SIRSN publication verification

Problem 9700033 / AMR-096-0033, rank 935. Verification date: 2026-10-06 UTC.

## Accepted scope and limits

The accepted result is the separately corrected derivative at [audit/corrected/RESULT.md](audit/corrected/RESULT.md), bound by [audit/ACCEPTANCE.json](audit/ACCEPTANCE.json). Disposition remains **UNSOLVED, scoped partial result, 3/5 substantive approaches**. The original submission is preserved without alteration. The measurable witness count H_r bounds the number of components needed for exterior coverage and satisfies E[H_r] <= 8p(1). No expectation of an unformalized exact topological-component count is claimed. General uniqueness remains unproved.

The mathematical acceptance is independent AI review, not human peer review, a machine-checked proof, or a novelty certificate. Byte checks, source matching, and finite diagnostics do not prove the continuous geometric argument. Existing source provenance and inspection history are preserved; this publication verification does not claim fresh remote PDF byte identity or a fresh literature-openness determination.

## Frozen archive anchors

These four original files are preserved byte-for-byte under archives/:

- SIRSN_UNBOUNDED_9700033_AUTHOR_SAFE_FREEZE.zip: 10,738 bytes; SHA-256 5bd8726384871fa1f3f97543db1a88d7340d2474287f8e90feb4509a73746523.
- SIRSN_UNBOUNDED_9700033_AUTHOR_EXTERNAL_MANIFEST.json: 999 bytes; SHA-256 47cf2deb9dc39191fe5a7ff78aa2cef3bf245f4e9e47eae3092583e6735ea5c9.
- SIRSN_UNBOUNDED_9700033_INDEPENDENT_AUDIT_SAFE.zip: 59,373 bytes; SHA-256 303460b01cfc4a01aa7c44e9fa6787a8326eadfa4b20f89e708495acc9616df8.
- SIRSN_UNBOUNDED_9700033_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json: 4,039 bytes; SHA-256 03bae1e769cbbd8ce9d7ae2f9b4dc8e340856528d1367192e9be0b0a475b27b6.

Every ZIP member was checked before extraction. The public author/ tree matches all five original archive members. The public audit/ tree matches all 22 audit archive members, including its nested original ZIP, external manifest, original files, corrected files, correction patch, and exact acceptance. No archive or external manifest was rebuilt. The audit's original/ files equal the author archive member bytes.

The accepted corrected proof is 15,591 bytes, SHA-256 6dce990127314a48057675ab0506a0144bfc36734c815360601ebc19c4f0093c. The correction patch is 16,693 bytes, SHA-256 1cd19374bb8d7d2dc52f669604136e67c9d14dda35543972bdc6e0a5664fb801. Applying that patch with zero fuzz to a verified copy of the original reproduces all five corrected files exactly, including the unchanged verifier.

## Mandatory full-input validation

The publication bootstrap requires the complete local problems file, research-results map, catalog, and source directory. Missing arguments, missing files, or mismatched bytes fail; there is no package-only mode silently substituted for full validation.

Recomputed corpus bindings:

- Problems: 68,931,837 bytes; 15,458 records; SHA-256 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf.
- Research results: 80,334,822 bytes; 6,701 entries; SHA-256 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b.
- Catalog: 21,735,099 bytes; 15,458 records; SHA-256 891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566.

The complete exact-ID problem record and its report were selected from those full inputs, serialized as json.dumps(pair, sort_keys=True) with Python's default separators and ensure_ascii, and compared with the saved canonical pair. The result is 4,823 bytes, SHA-256 21b8f492c3e9bbdc7d788b8dde10d0d0d9ea6b46a947b1bf4f9447507155d8f0. The saved catalog record equals the independently selected full-catalog record; its review hash, rank, ID, and problem number match.

All three supplied PDF files were rehashed, and fresh pdftotext -layout output matched both the saved extraction and the audit's extraction metadata:

- Aldous, published 2014 paper: PDF 595,604 bytes / fd5b785da34c7ca81c6165b11f85f2bd521c728aeb6fb8bbb3af9b6ead455298; text 145,537 bytes / 190eccba6dc64fde50a325665fbcdf7ce18c5e8d0b5d1611e6fd1596fea05b9d.
- Aldous, long 2012 preprint: PDF 455,350 bytes / 708c3d0161e6f3929f9bb57f07a838781a1f2efc3b94ca6c7c4665dbff478433; text 128,291 bytes / ef25a9b3a1bd344dc0f45f40bce03b110de0895c1cdb45d00e9b4ccb17b2517a.
- Kahn, 2016 paper: PDF 673,770 bytes / 84af8a3084755d70c20a16f5de08e06129542058a88ff7d2f16399e5bfafe18c; text 88,801 bytes / 19a04d26679eed0aa879654071bd1e96e47161d9c1b093453829829ac9303f96.

The corpus contents, canonical source record text, PDFs, and extracted source text remain outside this public package. See [source metadata](audit/corrected/SOURCE_MANIFEST.json), [input bindings](audit/INPUT_BINDINGS.json), and [retrieval history](audit/SOURCE_RETRIEVAL_HISTORY.json) for public provenance information.

## Replayed controls

The external publication bootstrap was tested from a relocated directory containing spaces under ordinary, optimized (-O), isolated (-I), and isolated-optimized (-I -O) Python. Each complete run independently checked publication inventory, frozen archive/member bytes, all extracted bytes, mandatory full inputs, exact acceptance, and patch reproduction before reporting PASS.

Each run reproduced:

- **21 author controls:** four successful relocated execution modes; eight mutation types under normal and optimized Python; rejection of a coherently rewritten result and certificate against the external anchor.
- **17 fresh audit controls:** same-size body mutation; false canonical hash with certificate rebinding; the deliberately accepted internal-only false-corpus-metadata rewrite and its external-anchor rejection; duplicate JSON keys; traversal, duplicate-member, and symlink ZIP controls; exact patch reproduction; four corrected-package relocation modes.
- **Six audit-verifier controls total:** four successful relocation modes and two expected rejections (mutated corrected proof, wrong audit external-manifest pin). These are six controls, not six negative tests.

Every successful finite package verifier reported 625 scaling rectangles, 100 intensity tail sums, 9,841 last-exit controls, and three negative mathematical controls.

**Sixteen additional publication-gate rejection controls** checked a wrong publication pin; omission of each of the four mandatory input arguments; missing corpus/source paths; mutation of archived verifier code under all four Python modes; coherently rebound internal corpus metadata; an altered frozen author manifest even after a test-local outer reseal; an omitted mandatory PDF; mutated PDF bytes; and a symlink publication root. An injected sentinel in the mutated archived verifier never executed: rejection occurred at the pre-execution byte gate.

The original verifier intentionally accepts coherently rebound false corpus metadata internally: it does not read the full corpora and is not a standalone authenticity oracle. This behavior was reproduced as an expected diagnostic limitation, not hidden as a failure. The independently anchored freeze rejects such rewriting, and this publication bootstrap separately recomputes the real full-input bindings. No mechanism can authenticate content after an adversary replaces both the verifier and the independently trusted pins.

## Reusable fail-closed replay

Requirements: Python 3, GNU-compatible patch, Poppler pdftotext, and separately obtained local inputs whose bytes match the metadata above. Do not treat a hash downloaded alongside an untrusted package as an independent trust anchor.

1. Obtain the bootstrap SHA-256 and publication-manifest SHA-256 through a trusted channel or retain them independently from the reviewed publication. The bootstrap must be inspected or authenticated **before execution**. Its own manifest check cannot authenticate the code already executing.
2. Check the bootstrap with an independent hashing tool. For example, with PUB set to the local publication directory and TRUSTED_BOOTSTRAP_SHA256 set to the independently supplied digest:

```sh
printf '%s  %s\n' "$TRUSTED_BOOTSTRAP_SHA256" "$PUB/PUBLICATION_BOOTSTRAP.py" | sha256sum -c -
```

3. Only after that check succeeds, run the verified bootstrap with the independently supplied manifest pin:

```sh
python -I -B "$PUB/PUBLICATION_BOOTSTRAP.py" \
  --publication-root "$PUB" \
  --manifest-sha256 "$TRUSTED_PUBLICATION_MANIFEST_SHA256" \
  --problems /local/inputs/problems.json \
  --research-results /local/inputs/research_results.json \
  --catalog /local/inputs/catalog.json \
  --source-dir /local/source-inputs \
  --receipt /local/output/full-verification-receipt.json
```

The source directory must contain the three named PDFs and matching .txt extractions (aldous-published-2014, aldous-long-2012, and kahn2016), canonical_pair.private.json, and catalog_record.private.json. These input names describe caller-supplied local files, not public package members. An output receipt must be outside the publication tree. Run from any working directory; the publication root and all input locations are explicit. Repeat with ordinary, -O, and -I -O Python if desired.

The bootstrap uses explicit checks rather than assertions. It verifies the externally pinned publication manifest before parsing it, rejects symlinks/special nodes and unexpected inventory, checks each frozen archive and member against fixed independent author/audit anchors, compares every published extracted byte with the frozen members, validates all mandatory inputs, then writes verified snapshots to a fresh temporary directory before executing any archived verifier or control script. It applies the patch with zero fuzz and compares every resulting file, not only the proof text.

PUBLICATION_MANIFEST.json binds all other public files and excludes only itself. It does not include its own digest; that digest must be retained outside the package. If any publication file changes, the manifest and its independently retained pin must be updated and the full replay rerun. A verified local bootstrap may also be pointed at separately materialized remote bytes using --publication-root.
