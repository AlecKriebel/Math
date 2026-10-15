# PR883 verification tooling contract

These four standalone, standard-library Python scripts authenticate artifacts and replay finite diagnostics. They do not certify a mathematical proof, novelty, historical priority, current openness, human review, or publication readiness. Python 3.10 or newer is required. Run every entry point with `python3 -I -S -B`; optimized operation adds `-O`. The tools refuse ordinary startup without the three mandatory isolation flags.

Before executing a script, authenticate its bytes against a digest obtained independently of the directory being checked. Then supply the independently obtained package-index or current-manifest SHA-256 to the script. A matching manifest containing the already-running verifier is not, by itself, authentication of startup code. Replacing the external anchor or executing unauthenticated startup code defeats this trust model. No sandbox or defense against a concurrent malicious filesystem writer is claimed.

## Portable package

The parent constructs `package_index.json` as an object with exactly `schema`, `problem_id`, and `files`. Its schema is `diffuse-9900008-verification-v1`; `problem_id` is the string `9900008`. Each file row has exactly `path`, `bytes`, and `sha256`: a safe relative ASCII path, an actual nonnegative integer (never a boolean or float), and 64 lowercase hexadecimal digits. The index excludes itself. Its file list is the entire package membership; extra files, empty directories, symlinks, and other special entries are rejected.

Mandatory indexed files are `check_originals.py`, `verify_package.py`, `build_verification.py`, and `root_evidence/SOURCE_MANIFEST.json`. The last file must match SHA-256 `53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab`. All 26 files from its frozen head `af25d26e21945a1a132aace5e600485152777070` must occur byte-for-byte under `source/` (211,771 bytes total). Their original Git blob identifiers are checked too. Source files cannot be coordinated away by regenerating the portable index. Additional paper, metadata, and evidence files are the parent's explicit indexing decision; the tooling does not discover or select them.

Usage after independent startup authentication:

```text
python3 -I -S -B verify_package.py INDEX_SHA256 --root PACKAGE_DIRECTORY
python3 -I -S -B check_originals.py INDEX_SHA256 --root PACKAGE_DIRECTORY
```

Full replay is the default. It authenticates the entire closed package and both historical ZIPs, then executes authenticated private copies of the included author self-test/integrity and original publication self-test in normal and optimized modes. The precise contract is **6 direct archival subprocesses plus 16 nested author subprocesses**, 22 total. The author self-test contains 18 negative controls and 2 positive variants; its finite counters are 9 quotient cases, 530 exact unit-window samples, and 361 translation-pair samples. Outputs must match the pinned historical outputs exactly.

The immutable publication wrapper historically requests eight author runs using four flag combinations. A reviewed current interceptor executes its unchanged body, allows only these exact commands, and injects `-I -S -B` plus `-O` when requested. Nested receipts retain both requested and effective flags. The historical wrapper is therefore executed unchanged under current instrumentation, rather than represented as an uninstrumented historical execution. Archived modules are never imported into the current verifier. Relocated files are checked again for unchanged bytes and closed membership after replay.

`--verify-only` authenticates bytes and structure and omits all archival execution; receipts explicitly report zero direct and nested runs. The omitted historical executable audit is neither distributed nor replayed in either mode.

Optional source authentication requires all four explicit arguments together:

```text
--catalog CATALOG_JSON --problems PROBLEMS_JSON --reports REPORTS_JSON --pdf-dir PDF_DIRECTORY
```

This mode authenticates the three complete frozen corpora by streaming SHA-256, boundedly parses the authenticated files sequentially, and verifies the entire canonical record/report serialization (5,255 bytes; SHA-256 `5ccf640125437cbff98966972b50bc5f73f19e1ae1735dff8a49829cfbcdc42a`), actual catalog review binding, and complete statement hash `85140471a18e2a6974b1e984ead6f94e6954f1d619201d414dc8be50244c8c54`. It also authenticates exactly these five original PDFs and checks their PDF magic: `some-open-probability-problems.pdf`, `0906.2062.pdf`, `1405.7566.pdf`, `2112.13053.pdf`, and `2303.05137.pdf`. It does not automatically authenticate later sources, including the 2025 final publication, or claim coverage of every source in the parent's ledger. No historical source-checker executable exists in this portable bundle. Source authentication can accompany `--verify-only`; that remains authentication without archival replay. No corpus or PDF copy, write, chmod, or truncate is performed by source mode.

## Deterministic builder

```text
python3 -I -S -B build_verification.py PACKAGE_DIRECTORY INDEX_SHA256 VERIFIER_SHA256 OUTPUT_DIRECTORY
```

The verifier digest is separately supplied and checked before its authenticated copied bytes execute. Authenticate the builder startup independently too. The builder validates the complete closed input and runs the full default verification before producing an archive. The output must be fresh or empty, outside the assembly and its ancestors, with an existing parent directory. Validation failure creates no output archive. ZIP creation takes place in a small temporary staging directory; the verified result is renamed into place only after validation.

Members use sorted names, no directory entries or comments, fixed Unix regular-file mode 0644, fixed 2026-10-15 00:00:00 timestamps, and DEFLATE level 9. Reproducibility means identical input bytes on the same Python ZIP implementation and zlib; no cross-version compressed-byte promise is made. The ZIP verifier checks the complete local/central/end representation, member bytes, and closed membership, including prefix/trailer, gap, metadata, and declared-size rejection. No archive extraction occurs.

## Current outer root

The parent builds an independent `CURRENT_PUBLICATION_MANIFEST.json`, preserving the historical `PUBLICATION_MANIFEST.json` unchanged. The current manifest has the portable row format, schema `diffuse-9900008-current-publication-v1`, string `problem_id` `9900008`, and indexes all outer files except itself. Mandatory files include `verify_current_publication.py` and `CURRENT_PUBLICATION.json`. The outer index is supplied by its independent digest:

```text
python3 -I -S -B verify_current_publication.py MANIFEST_SHA256 --root CURRENT_ROOT
```

The JSON object `CURRENT_PUBLICATION.json` may carry the parent's other metadata. Its `tooling_layout` member must have exactly these keys:

```json
{
  "portable_prefix": "preprint/verification_package",
  "zip_path": "preprint/verification.zip",
  "copy_pairs": [
    {"outer_path": "preprint/check_originals.py", "portable_path": "check_originals.py"}
  ],
  "preserved_source_paths": ["all 24 frozen relative paths except README.md and RESEARCH_LOG.md"],
  "json_equal_groups": []
}
```

The example preserved-source list is descriptive: the actual list must enumerate the 24 exact paths. Every listed path is validated and already covered by the current closed inventory. All 26 originals remain mandatory inside the portable `source/` directory; the outer root additionally preserves the 24 originals other than its new README and research log. `copy_pairs` must enumerate every outer/portable duplication the parent intends to bind. `json_equal_groups` optionally lists groups of outer JSON paths whose entire parsed JSON values must match in canonical serialization; it does not compare selected nested metadata fields. The root verifier validates these explicit copy contracts, checks the complete generated ZIP against every portable byte, and invokes the authenticated portable verifier with full replay by default. `--verify-only` and source arguments have the same meaning as for the portable verifier.

Root/ancestor aliases outside a selected tree may resolve normally. The selected root itself, every directory within a selected tree, and every opened file leaf must be ordinary entries. Reads and expanded ZIP members are bounded. File size, identity, and modification time are checked around reads. These checks reduce accidental ambiguity; they are not a sandbox or a claim of race-proof hostile-environment execution.

## Status

The separate engineering report records actual test results and limitations. A parent's assembled paper/metadata package requires its own freshly pinned inventory, startup digest distribution, complete read, independent adversarial audit, and final disposition review. Passing these tools supplies artifact evidence only.
