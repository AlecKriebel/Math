# Official archival evidence addendum

This addendum follows the independent mathematical PASS and original bounded priority audit. It preserves the original report, mathematical freeze, manifest and research log unchanged. Only materially new official evidence supplied by the root reviewer is assessed here. No credentials were accessed, operational kit executed, external individual contacted, or provider/Git state changed by this auditor.

## Changed conclusion

The evidence is now stronger than an earlier DOI announcement. **The official published, public Zenodo version contains completed file entries whose MD5 checksums and byte sizes exactly match all three files in the independently validated manuscript package.** Official record and per-file creation/update timestamps precede our first recorded target checkpoint and full candidate.

The previously missing official archive-file checksum/time association is closed. **Direct archived-body comparison is still unverified:** the root's main.pdf content request timed out without a captured body, and its separate documented versioned-file request returned 406. I did not relabel the already downloaded EulerSolve PDF as a downloaded Zenodo body or assign its SHA-256 to an unseen archive body.

At ordinary repository checksum standards, this is strong evidence of an earlier archived complete proof of our exact target. It is appropriate to treat the manuscript as an externally archived same-target proof predating our recorded campaign and to acknowledge it. An assertion that our campaign first resolved or disclosed this target is unsupported. This conclusion does not establish absolute priority against all literature, who first discovered the result, plagiarism, or independence.

## Official source authentication

Root's [native record receipt](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr261_5100021/initial_review_20261012/competing_preprint_priority_adversary/archival_addendum_20261012/ZENODO_NATIVE_READONLY_RECEIPT.json) records a single read-only GET completed on October 12 at 10:18:00.476882 UTC, with no retries or mutations and no credential output. I independently read and pinned the 14,104-byte official response:

- Source URL: [Zenodo record API](https://zenodo.org/api/records/23079799).
- Response SHA-256: `766a2c2157f05b5323563d2ee6005486a9fb08636c727a1b46f601b62afd3777`.
- DOI: `10.5281/zenodo.23079799`; title/author and v1.0 match the validated preprint.
- `status=published`, `is_published=true`, `is_draft=false`; record/files public, open, no active embargo, not deleted.
- Version index 1 and latest; three enabled files, all nonhidden.
- Record created **2026-10-01T10:00:33.366348Z**, last updated **10:00:56.046398Z**.

The public file-metadata responses identify completed file objects in the same bucket and match the native record's IDs, checksums, sizes and content links. `CHECKSUM_BINDING.json` is my independent comparison; it does not rely on the root's comparison output. The separately pinned root comparison agrees.

| Archived key | Size | Official MD5, independently matched | Official file created UTC | Official file last updated UTC |
|---|---:|---|---|---|
| main.pdf | 84,383 | c7a628028184e8486bb8b766b2dc808d | Oct1 10:00:33.406393 | Oct1 10:00:33.426116 |
| arxiv_source.zip | 75,954 | ad07cefd26da2344d1e5c6adb2726be2 | Oct1 10:00:33.451779 | Oct1 10:00:33.466466 |
| verification_report.md | 3,344 | 420cae154ce86dec9e6065e250a9669a | Oct1 10:00:33.433285 | Oct1 10:00:33.445259 |

The independent website-download SHA-256 values remain:

- PDF: `34ff068237a7ebbd6ffa063f89717aae946bc4d27df6db23d4468b5bb52d3582`.
- ZIP: `6680bf0a3fd4cade6fabaf2061f88941c9d57776fe65f28bfb9e69acb8b39876`.
- Verification: `c84cf16d7a46801a6a438228924d069f93bda9a7c8242875435fa777c6afd8f5`.

Each is a hash of actual local bytes read and validated in the earlier audit. The new linkage is through the official archive's matching MD5 and size; a directly downloaded archive SHA-256 is not available. MD5 matching is the authentication method reported, not a claim of cryptographic byte identity stronger than the available evidence.

## Precise temporal assessment

Do not rename file creation time or record creation time as the exact first instant a public HTTP reader could access the proof. These are official repository object events. The reported record last update and all three file last updates are still on October 1, preceding our campaign. The public version is associated with those unchanged server-reported dates.

The official [Zenodo DOI guidance](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/) says registration occurs on publication and distinguishes reserving an identifier beforehand. The independently recovered DataCite version DOI reports created/registered **October 1 at 10:01:22.000 UTC**, with last update one second later. Combined with the completed file entries, archive checksum binding and published/public record state, this supplies a conservative **publication-associated** timestamp earlier than our work. It is stronger than the previously available date-only landing assertion. It is not a claim of a logged first public HTTP access at that exact second.

The official [record-management guidance](https://help.zenodo.org/docs/deposit/manage-records/) distinguishes editable metadata/file visibility from postpublication file changes requiring support. Thus “immutable” should refer to the identified archived file version in the ordinary repository sense, not an assumption that no administrative modification is possible. No post-October-1 update appears in the retrieved record or file metadata. These policy pages and their read-only retrieval receipts are preserved in this addendum folder.

| Our verified event | UTC | After conservative DOI publication-associated time |
|---|---|---:|
| First authored target checkpoint 210161f… | Oct1 11:31:06 | 1h29m44s |
| First full candidate-file commit 8f29c19… | Oct1 11:46:29 | 1h45m07s |
| Reviewed checkpoint b85ec990… | Oct1 12:11:52 | 2h10m30s |
| PR261 service creation | Oct1 12:12:30 | 2h11m08s |

Git author/committer dates are still authored events, not independently measured public push times. The service-created PR event is distinct. The native record/file events precede each of these, and `EVENT_TIME_COMPARISON.json` preserves the microsecond differences without equating event types.

## Remaining limits and mathematical status

The root preserved the content timeout and HTTP406 receipts. A direct archived-body/SHA-256 comparison remains unavailable. The record/file checksum association is now verified, so the old broad statement that no archive file binding was available has been superseded by this addendum. The old frozen report correctly records what was known before this new retrieval and must not be silently rewritten.

No additional proof search or numerical rerun was needed: the actual website manuscript had already passed an independent reconstruction, exact symbolic checks and geometric corroboration, and the official checksum/size match associates its complete-proof artifact with the earlier archive. The mathematical verdict remains PASS for primitive least period divisible by four, strict confocal elliptical caustic, ordered signed same-focus product, including stars and zero antipedal area, using the correctly matched published Chávez-Caliz theorem. Our distinct compact-torus proof remains subject to the parent review; this addendum is not a promotion action.

This completes **100% of the assigned bounded archival addendum**, with the direct-download limitation retained explicitly. Strongest verified result: an official earlier public published file-bearing archive, with exact matching repository checksums/sizes for the independently validated complete-proof package. Exact first HTTP visibility, absolute global priority, discovery chronology and causal relationships remain unverified.
