# Version and public-availability chronology

Access date for all observations below: 2026-10-16 UTC. Raw unauthenticated provider JSON/HTML and HTTP receipts are in `private_reading/` and `SOURCE_ACCESS_RECEIPTS.json`. `SOURCE_BYTE_INVENTORY.json` hashes the archived files and source-archive members. Author dates, DOI registration, archive record creation, repository server events, and first public access are not interchangeable.

## Original authors' source

The current [arXiv record](https://arxiv.org/abs/2004.12497) reports v11 as latest and gives this complete history. Every version's actual PDF target passage was inspected; the target retains a question mark in its proof column throughout.

| Version | arXiv submission time UTC | Target location in PDF | Status there |
|---|---|---|---|
| 1 | 2020-04-26 23:01:52 | Table 3, p.4 | conjecture/question mark |
| 2 | 2020-04-28 09:32:25 | Table 3, p.4 | same |
| 3 | 2020-04-30 11:05:38 | Table 3, p.4 | same |
| 4 | 2020-05-04 18:29:59 | Table 3, p.4 | same |
| 5 | 2020-06-24 11:20:49 | Table 3, p.4 | same |
| 6 | 2020-07-05 20:52:20 | Table 3, p.4 | same |
| 7 | 2020-08-24 10:47:06 | Table 3, p.5 | same |
| 8 | 2020-10-10 21:17:15 | Table 3, p.5 | same |
| 9 | 2020-10-21 19:46:09 | Table 4, p.6 | same |
| 10 | 2020-10-25 20:13:18 | Table 4, p.6 | same |
| 11 | 2020-10-29 11:37:49 | Table 4, p.6 | same |

Thus the conjecture is already present in April 2020. The 2021 published edition is entitled *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Mathematical Journal 7, 341-355, DOI [10.1007/s40598-021-00174-y](https://doi.org/10.1007/s40598-021-00174-y); Table 4 p.346 retains the same product, parity, center and question mark. The publisher and [Crossref record](https://api.crossref.org/works/10.1007/s40598-021-00174-y) report first online 2021-02-18. Crossref creation is 2021-02-19T14:02:14Z. Crossref currently exposes neither an `update-to` entry nor a nonempty relation map for a correction. That bounded metadata observation does not prove that no later resolution exists.

The early table is numbered 3, not 4. This is a location change, not a different theorem or a newly discovered invariant. Referring to arXiv *Eighty* as the 2021 version of record obscures its distinct 2020 arXiv history; a 2021 proposed-year field may instead reflect the journal edition and is not automatically a false datum.

## Ferudun note0014: all provider-listed versions

The unauthenticated [Zenodo versions endpoint](https://zenodo.org/api/records/23088516/versions?size=25) returns exactly two entries, with no next-page link. A separate [all-version exact-title search](https://zenodo.org/api/records?q=%22Outer-Pedal%20Area%20Products%22&size=25&all_versions=true) returns the same two records. A title search of arXiv returns no result; a source ZIP called `arxiv_source.zip` therefore must not be called an actual arXiv posting.

| Field | Version 1.0 | Version 1.1 |
|---|---|---|
| Version DOI | [10.5281/zenodo.23087221](https://doi.org/10.5281/zenodo.23087221) | [10.5281/zenodo.23088516](https://doi.org/10.5281/zenodo.23088516) |
| Concept DOI | 10.5281/zenodo.23087220 | same |
| Zenodo creation UTC | 2026-10-01T16:56:14.316216+00:00 | 2026-10-01T18:12:36.529602+00:00 |
| Zenodo modification UTC | 2026-10-01T16:56:14.807727+00:00 | 2026-10-01T18:12:36.893358+00:00 |
| DataCite creation/registration/update UTC | 2026-10-01T16:56:15.000Z | 2026-10-01T18:12:37.000Z |
| DOI state on audit | findable | findable |
| Zenodo access/status on audit | open / published | open / published |
| Author-assigned publication date | 2026-10-01 | 2026-10-01 |
| PDF bytes | 90,127 | 100,311 |
| PDF SHA256 | 3c6791ae0099a49b9215844c506970806148f0ab568a5be2bd798616b0f1d0c9 | 5ff816c279e39f478e96ae5454779cc3b5280bc9eed1084429578540b3d352b6 |
| Source ZIP bytes | 76,259 | 138,800 |
| Source ZIP SHA256 | ec5d18a6e6aa959f8929bd848582887afece8a79efaca50384ebcf25d340cad6 | 58aff5d03ae61005f3aaeccc47ab3c520b0698353ab32ed13375040ed1470d5d |
| Exact coverage | Theorem 1 p.1, proof Sections 2-5: arbitrary point, primitive N=2 mod4; hence centered even primitive subset | Theorem 2 p.2, proof Section 6 p.6 plus dependencies Sections 2,4,5: complete centered target |

The v1.1 PDF was read in place to avoid duplication. Its local MD5 matches the independently fetched Zenodo file checksum and its SHA256 matches the current publisher metadata. Both source archives were actually downloaded, inventoried member by member and read as data. The v1.0 main source has one theorem environment and no k303,b occurrence. The v1.1 source has the added center theorem and its complete odd/repetition proof. No unpublished, private, future or nonexistent version is inferred.

The [current publisher page](https://eulersolve.org/papers/amr-050-0014/) and [metadata](https://eulersolve.org/papers/amr-050-0014/metadata.json) claim first online release on October 1 and explicitly describe v1.1 as an extension. These are author-controlled day-resolution claims. The metadata still contains `doi_archived_file_version: 1.0` alongside `version: 1.1`; that field is stale relative to the actual matching v1.1 archived PDF/source. It must not be used to classify the current bytes as v1.0. The version DOI 23088516 is not the concept DOI.

A read-only Internet Archive [CDX query](https://web.archive.org/cdx/search/cdx?url=eulersolve.org%2Fpapers%2Famr-050-0014%2F%2A&output=json&filter=statuscode%3A200&collapse=timestamp%3A8) returned an empty list. Public GitHub user/repository listings did not provide a versioned website source history in the inspected entries. Neither observation proves absence of an earlier website posting. No independent earlier website capture has been located. No individual was contacted.

## Candidate ordering: exact limit of this family's evidence

The candidate's local research log/commit chronology places the full mechanism earlier on October 1. This is evidence of claimed preparation time, not proof of first public availability. After this family froze its independent scope, root supplied separate observations of GitHub server-created check suites at 05:35:19Z and PR creation at 05:48:56Z on October 1, with the same complete proof blob. These raw GitHub receipts are maintained by root, not authenticated afresh by this family; root also expressly has not inferred historical public visibility solely from current public flags. This family does not convert those observations into an absolute priority decision.

The confirmed provider-record sequence is that Ferudun's archived even theorem and then its full centered extension have October 1 afternoon UTC creation/registration times. This is later than the candidate's claimed morning preparation and the server events communicated by root. First public ordering between the actual complete candidate proof and any earlier Ferudun website/repository version remains a separate historical question. A later exact proof does not retroactively anticipate a genuinely earlier public proof, and a current exact match does not establish who posted first. Conversely, the candidate's commit dates and an old source question mark cannot support a first-proof assertion.

The strongest safe classification is **confirmed exact contemporary full proof with a different proof organization; no earlier full exact anticipation located by this family; absolute first-public order and independent non-derivation not certified**.
