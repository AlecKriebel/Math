# Validation and diagnostic replay

## What has been checked

All eight unchanged accepted checker programs were executed in normal Python, `-O`, and `-OO`: 24 successful runs. A deliberately forced failure in each program's enforcement path was also rejected in all three modes: 24 successful negative controls. The replay evidence is in [REPLAY_EVIDENCE.json](REPLAY_EVIDENCE.json).

No program relies on Python `assert` for a check. Their explicit exceptions or nonzero exits remain active when optimization removes assertions and docstrings. The replay harness and bundle validator also use explicit checks. A fresh AST scan rejects any Python assert node in the shipped programs.

For the three Hardy programs, a temporary copy forces the final pass flag false immediately before its explicit exit. Its already printed formula report stays true, while its process correctly exits with code 1. For the other five programs, a temporary copy forces a runtime `require` condition false and verifies the expected rejection marker. These probes test active rejection paths; they do not purport to cover every possible software fault.

The original spectral-audit programs contain timestamps and optimization flags, so their raw output differs across modes. All replay outputs agree after removing **only** `checked_at_utc` and `optimization_flag`; the full raw report content is preserved in the evidence. No mathematical result field is normalized away.

## Check the packaged files

From this directory, using an existing Python 3 installation:

```sh
python verify_bundle.py
python -O verify_bundle.py
python -OO verify_bundle.py
```

This standard-library validator checks exact file membership, byte counts and SHA-256 hashes, the two primary manifest anchors plus the final source-scope and original-copy-map anchors, every original-copy pin, all 115 original JSON digest fields using exact-pointer mappings, including 100 local artifact references and 15 external PDF metadata references, all shipped checker coverage and recorded mode results, local Markdown links, absence of symlinks/unexpected file types, private-material markers in every file, with no filename exemption, and assertion-free Python checks. Citation-only PDF metadata is distinguished from bundled artifacts; no third-party PDF is present.

The external archive receipt pins `MANIFEST.json` and the archive itself. A hash is an identity check and is meaningful only in relation to the separately retained trusted receipt. Neither a valid manifest nor a successful diagnostic establishes a mathematical theorem.

## Rerun the accepted diagnostics

The existing diagnostic environment used Python 3 with SymPy, NumPy and SciPy. Exact versions are recorded in the replay reports. No package installation or network access is performed by these tools.

```sh
python replay_diagnostics.py --output ../fresh_replay.json
```

The harness runs all three modes itself. It makes isolated temporary copies so the two original spectral programs can write their normal sidecars without changing sealed evidence. The optional output must be outside the reader directory; omitting `--output` prints the full report to standard output. The bundle validator can then be rerun to confirm that the preserved reader did not change.

A missing dependency or failed subprocess is a failed or blocked replay, not a pass. Different numerical-library versions may change floating-point values. Fresh results should be compared on their merits; the accepted counterexamples use exact variational definitions, never rounded diagnostic eigenvalues.

## What validation does not establish

The checkers reproduce symbolic identities, rational comparisons, limited polynomial examples, and numerical smoke tests where stated. Compactness, positivity, spectral-gap arguments, full test-class convergence and universal inequalities are analytical claims established in the authored manuscripts and accepted audits. No automated formal proof verification, new mathematical pass, or extra source-scope conclusion is claimed.

## Reviewed edition evidence

The independent review reran the 24 successful diagnostic invocations and 24 active-failure controls; [fresh complete evidence](review/INDEPENDENT_REPLAY_EVIDENCE.json) is retained alongside the unchanged earlier record. The validator checks both records. All nested manifests are included; only the root manifest itself is excluded from its own inventory. Nonregular filesystem entries, duplicate JSON keys, disguised PDF bytes and inappropriate source-disposition or pass-count changes are rejected. [The integration report](review/INDEPENDENT_INTEGRATION_ACCEPTANCE.md) explains the two observed baseline packaging gaps and their editorial repairs. [Tamper-test evidence](review/INTEGRATION_EVIDENCE.json) and the external final archive receipt document failure detection and restoration.
