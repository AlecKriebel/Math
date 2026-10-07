# Package v2 reference portability receipt

Finished: 2026-10-07T04:46:26.336533+00:00. Completion estimate: 100% of this packaging-reference audit.

**PASS_WITH_ADVISORIES: 12/12 checks passed; no broken current supplied-file promises identified.**

The audit read the immutable package tree/ZIP, every supplied Markdown document and standalone TeX file, the map, source/provenance/priority receipts, and the current builder without executing it. Candidate bytes remained unchanged. No Git, network, publication, or external communication occurred.

All 24 original-project mappings identify existing supplied files and match the original bytes after the builder's documented Markdown normalization. ARCHIVE_MAP.json and SHA256SUMS.json are generated archive metadata, with no original project counterpart. ZIP contains the same 26 flat files with identical bytes. All 207 formal module hashes correspond to the pinned external manifest; those external modules are intentionally absent.

128 Markdown/TeX file-reference occurrences were classified; all current supplied references resolve directly, by precise map entry, or by enclosing upload-kit scope. Upstream manuscript/Lean references denote excluded pinned inputs. main.tex has no local input/include/graphics/bibliography dependency and its internal labels resolve.

## Exact remaining concerns (advisories)

**R-A1** (FORMAL_SCOPE_AUDIT.md:1, FORMAL_SCOPE_AUDIT.md:69, FORMAL_SCOPE_AUDIT.md:73, FORMAL_SCOPE_AUDIT.md:79): Historical formal report says local configurations/logs are retained and reproduce.sh is supplied. These files are absent from ZIP; the leading archive note explicitly excludes the reproduction script and Lean checkout, so this is qualified historical wording rather than a current supplied-file promise.

Recommendation: Optionally add these local artifacts to omitted_inputs and label the historical Reproduction paragraph as project-only. Fetching upstream does not recreate the altered minimal configuration or Audit.lean byte-for-byte.

**R-A2** (PRIORITY_AUDIT.md:17, PRIORITY_AUDIT.md:117, README.md:17, ARCHIVE_MAP.json:28): Seven project-owned priority retrieval/hash receipts are cited but neither supplied nor individually listed as omitted. README locates review receipts in the public project repository, but gives no project repository URL. Supplied PRIORITY_SEARCH_LOG.json does resolve the historical SEARCH_LOG.json context.

Recommendation: Optionally record these seven omitted project receipts and provide a stable project repository URL; preserve the report's explicit v1 scope rather than presenting its v1 hashes as v2 identities.

**R-A3** (ARCHIVE_MAP.json:31, PRELIMINARY_PRIORITY_AUDIT.md:78, PRIORITY_AUDIT.md:51, PRIMARY_REFERENCE_PROVENANCE.md:5): omitted_inputs says PDF source URLs/hashes are in priority/provenance records. The supplied provenance table contains hashes for Glassey 1996, Bouchut-Golse-Pallard, and Luk-Strain; no exact Glassey-Schaeffer 1988 PDF digest or preliminary GitHub API response digest is in the supplied records, although historical reports describe hash checks/source-manifest hashes.

Recommendation: Optionally narrow the hash-availability wording or include the permitted project-owned digest/retrieval records; the third-party PDFs themselves remain intentionally omitted.

The historical priority audit expressly covers package v1 and retains its v1 hashes; this audit does not promote it to approval of v2. External URLs were recorded but not fetched. The receipt establishes packaging reference integrity, not mathematical correctness, novelty/priority, formal certification, or readiness to publish.

The JSON receipt contains exact per-reference classifications, all mapping comparisons and candidate SHA256 hashes. The accompanying script is rerunnable and writes only in this reference_check folder.
