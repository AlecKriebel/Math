# PR786 production metadata adapter: independent integration review

**PASS: zero actionable issues found in the exact case-only adapter.**

This is an administrative production-integration check for known record23418581, not another mathematical or whole-preprint review. The previously reviewed213-file source and six release artifacts are unchanged. No new agent session or extra whole-paper review is claimed.

## Exact scope and mechanism

The parent supplied one readonly reconciliation receipt showing that the stored draft description differs only by the literal substring n>=2 becoming n&gt;=2. These represent the same paragraph text under HTML entity interpretation. I independently read the full receipt, adapter and relevant original repository tool implementation.

The adapter pins the complete original tool bytes, complete frozen metadata bytes and a single integer record ID. It checks that the original verifier comes from the expected module/file. At installation it requires exactly one normalization locus in the frozen description. At verification it requires the full supplied local metadata to equal the frozen metadata.

It accepts no general HTML rewriting. Only when the entire remote description equals the exact one-locus replacement does it deep-copy the response, restore that one field on the copy and pass the complete copy, metadata and files to the original verifier. All other metadata/file checks are retained. A returned normalization record names the exact locus, visible-text equivalence, metadata digest and ID. The original exact description still follows the original verifier with no spurious normalization.

The adapter performs no API action, file upload, state/auth read, metadata update, new deposit creation or publication. Assignment of tool.verify is an in-memory integration hook; the shared repository file is unchanged.

## Independent offline reproduction

test_adapter.py authenticates adapter/tool source hashes before importing either and derives its synthetic response from tool.load_manifest on the frozen local deposit manifest and public-safe metadata. It never loads auth configuration or private state. Before installation, all network-client/auth/state integration entry points are replaced with raising sentinels.

Python3.14.6 normal and Python3.12.14 optimized each passed60 verification cases and6 installation/code-pin guards. Every verification case checks that response, metadata and file arguments are unchanged after either acceptance or rejection.

Positive cases:
- Exact frozen description, no normalization record.
- Exactly one observed n&gt;=2 description, with an explicit normalization record.
- Existing repository file aliases/uppercase MD5/string-size conventions, retained from the original verifier.

Negative coverage:
- Wrong/missing/noninteger/bool IDs.
- Every specified local and remote metadata field changed, including author/ORCID, title, math-bearing description, dates, license, references and keywords; missing/extra supplied local fields.
- Changed mathematical r or rank inequality, numerical/double-encoded greater-than entities, whole-HTML escaping, another entity elsewhere, apostrophe encoding, removed tags or whitespace additions.
- Changed remote filename, checksum or size for each expected file; missing/extra/duplicate/invalid file lists or entries.
- Changed frozen metadata bytes, changed repository tool bytes, copied-tool/function filename mismatch, nonoriginal verifier, modified adapter rejected before import, and a second installation.

The original verifier rejects the observed paragraph encoding before adapter installation, demonstrating that the exception is real rather than redundant. After installation, invalid other fields still fail through the original verifier; the exception never short-circuits them.

A first run of my own unsealed harness failed because tool.load_manifest returns Path objects that the harness's JSON comparison had not serialized. I corrected only the harness to serialize those known path values and reran successfully. No adapter/source change was made or defect inferred from that harness error.

## Interface boundaries

The underlying repository verifier compares the expected filenames and each file's MD5/size; the adapter retains those exact checks. It does not add a new SHA256 guarantee or defend against a trusted caller coherently replacing its own expected file list. The production caller must continue loading the unchanged pinned local manifest/artifacts, and the parent separately validates release/public-download SHA256. This review's INPUTS.json binds all eight frozen artifacts plus their receipt, both code files and the readonly reconciliation.

The repository run path independently checks record/publication state and preserves its single-known-ID/no-repeat-publication reconciliation behavior. The adapter's verifier is valid for the known record's draft and later published responses; it is not an API client or standalone publication-state validator. Server-added unrelated fields retain the original verifier's treatment. No broader equality or stronger security property is claimed.

The review does not change the paper, metadata bytes, source ZIP, upload kit, original tool, draft metadata or accounts. It does not authorize another create or another publication POST. Parent retains production decisions and unknown-outcome reconciliation.

## Delivery

The strict flat authored packet is staged under metadata-adapter-review, with an externally supplied manifest and checker pin, optimization-safe custody and meaningful physical negative controls. Input files are checked read-only. Parent handles canonical persistence. Prior sealed whole-review01 files were not changed.
