# Independent packaging-helper review

Checkpoint: 2026-10-06 22:57 PDT. Assigned packaging QA: 100% complete for the inspected helper and proposed inputs. This is a scoped engineering review, not a mathematical, priority, PDF-layout, or publication approval.

## Scope and inspected version

Reviewed `reproducibility/build_publication_package.py`, the proposed metadata/selection/licenses, and the static deposit README. Compared the generated manifest contract directly with `zenodo_deposit_tool/zenodo.py::load_manifest`. The final inspected helper has SHA-256:

```text
b83a38cb75d02e8384cbb209f56b79127dda7f51ac1669883166e5b48a936597
```

All build-branch exercises used synthetic data and a memory-only replacement for the write function. No actual packaging was run. The actual proposed inputs were inspected only with `--plan`. No network, credential read, deposit operation, tracker update, Git mutation, or manuscript/PDF edit was performed.

## Findings and checks

No blocking packaging defect remains in this inspected version.

- Repeated synthetic builds produced identical bytes for every output. ZIP entries are sorted, stored without compression, timestamped 1980-01-01, marked as regular Unix files with mode 0644, and contain no generated directory entries. Archive construction is independent of dictionary insertion order.
- The generated deposit manifest has exactly `metadata` and `files` as top-level keys. A memory-only invocation of the repository tool's actual `load_manifest` accepted it. Its two entries are separately downloadable `paper.pdf` and `source-and-verification.zip`; the outer convenience ZIP is not a deposit payload.
- The output PDF is byte-identical to the selected input. The source archive does not duplicate the PDF. Its generated top-level `README.md` exactly matches the selected, hash-frozen `publication/README_FOR_DEPOSIT.md`.
- `SOURCE_SHA256SUMS.txt` covers every other source-archive member, including the generated metadata, frozen selection, and generated README. All synthetic member checksums matched. The checksum manifest excludes itself explicitly.
- Changing a frozen source rejects the build before any write. Metadata is canonically serialized and its SHA-256 is part of the frozen input map. Missing inputs, non-final filenames, and a non-frozen selection prevent building.
- Tests rejected traversal, absolute paths, third-party `references/` caches, `sources/pinned/` sources, hidden credential paths, the checkpoint/push helper, the original request, proposed package members, the live root README, and filenames containing newline or DEL. Symlink inputs are rejected by inspection of each path component.
- Proposed metadata names only Alec Kriebel with the supplied ORCID, omits affiliation, uses publication/preprint and open CC BY 4.0, and records the correct local manuscript date of October 6, 2026. It attributes the external gap input and established complex comparison, states the proposed additional scope, and discloses extensive AI use and absence of conventional human peer review. The proposed license separates rights in original prose/code from rights in cited third-party material.

Three defects found in the initial version were reported and repaired before this final check: malformed creator metadata could pass; the plan could call non-PDF bytes build-ready; and control characters could make source checksum filenames ambiguous. Memory-only regression checks now reject malformed creators, mark non-PDF input as not build-ready, and reject the tested control characters.

## Exact remaining work

The actual proposed plan correctly reports `build_ready=false`. The deliberately missing final inputs are `publication/LICENSES.md` and `publication/SOURCE_PROVENANCE.json`; the selection remains proposed and has no frozen hash map. The project lead must finalize all source/provenance/metadata, freeze the final selection, perform the required fresh complete-package mathematical and priority reviews, and run the local build and repository-tool check on the exact resulting payloads. Those release-stage facts are not certified here.

The source allowlist is explicit and prevents the named operational and third-party paths. It is not a semantic copyright or secret-content detector for arbitrary newly authored files placed in otherwise permitted directories; the final selected contents and provenance still require human/project-lead review. Reproducibility here means identical payload bytes for identical selected inputs and selection/metadata semantics, not byte-identical recompilation of a PDF by different LaTeX engines.

## Scope-change checkpoint: 2026-10-06 23:02 PDT

Assigned packaging QA remains 100% complete for the updated scope. This checkpoint supersedes the inspected helper version above. Reviewed helper SHA-256:

```text
b4f14af0a0cdb4ebaffe506e27279a119073395585900e8985064eaeb4ed3c40
```

The live top-level `CURRENT_THEOREM.md`, `DEPENDENCY_LEDGER.md`, `APPROACH_TABLE.md`, `RESEARCH_LOG.md`, and `README.md` are absent from the selected source inputs and are rejected by the helper. The generated archive README remains the exact selected static deposit README. The required static `publication/THEOREMS_AND_DEPENDENCIES.md` and required `reproducibility/build_paper.py` are present in the proposed selection and synthetic source archive. The static scope record states the positive-dimensional hypothesis `m>=1`, attributes its external inputs, distinguishes the cubic metric boundary application from arbitrary weak KE completions, and makes no live deposit-status assertion. Reading it does not substitute for the project's independent mathematical reviews. The PDF build script was read but not executed.

Reran the complete synthetic packaging exercise entirely in memory against the updated selection. Repeated outputs were byte-identical; archive timestamps, modes, compression policy, source checksum coverage, static README copying, unchanged PDF copying, and acceptance by the actual repository `load_manifest` function all passed. The manifest still specifies exactly the separately downloadable `paper.pdf` and `source-and-verification.zip`. Mutation of either the new static theorem record or metadata was rejected by the frozen-hash check. Non-PDF bytes remained not build-ready. All five live root status documents, control characters, traversal, caches, credentials, the Git helper, original prompt, and proposed files were rejected as tested.

The actual read-only `--plan` still correctly reports `build_ready=false`, with final license/provenance records absent and a proposed, unfrozen selection. No blocking packaging defect was found in this updated helper. No actual package, PDF export, network operation, credential read, Git mutation, deposit, or tracker update was performed. Final payload freezing, actual local build/tool checks, and the external complete-package acceptance reports remain the project lead's release-stage work.
