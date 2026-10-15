# Independent public readback — PASS

Checkpoint: 2026-10-07T16:07:41.455687+00:00. Public observation window: 2026-10-07T16:05:14.909534+00:00 through 2026-10-07T16:06:15.314759+00:00. Best-guess completion: **100% of this public publication-verification task**.

Unauthenticated public HTTPS GETs independently verify [production Zenodo record 23217863](https://zenodo.org/records/23217863) and its [public API response](https://zenodo.org/api/records/23217863). The API reports `status: published`, `state: done`, `submitted: true`, and open access. [DOI 10.5281/zenodo.23217863](https://doi.org/10.5281/zenodo.23217863) resolves via HTTP 302 → 302 → 200 to the correct public record.

Exact title: **Ordinary Banach–Mazur rigidity of von Neumann algebras**. Publication date: **2026-10-07**. The sole creator is **Kriebel, Alec**, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). The public license ID is `cc-by-4.0`; the landing page visibly names **Creative Commons Attribution 4.0 International** and links to its [license](https://creativecommons.org/licenses/by/4.0/legalcode). Title, date, complete description, keywords, access right, and publication/preprint type match `zenodo-deposit.json`. The creator comparison permits only the documented omitted-affiliation → `null` normalization. No description or Unicode/HTML normalization was needed, and no other discrepancy was found.

The public record contains exactly these two files. Each unauthenticated download returned HTTP 200, matches the local upload artifact in a full byte comparison, and matches its public MD5 checksum:

| Public file | Bytes | SHA-256 |
| --- | ---: | --- |
| [paper.pdf](https://zenodo.org/api/records/23217863/files/paper.pdf/content) | 83877 | `64ef84935aa6b3d327e30d26719927ce603aa75116a6aefa70589342bafe1c0b` |
| [source-and-verification.zip](https://zenodo.org/api/records/23217863/files/source-and-verification.zip/content) | 617532 | `c237465073726cf0da83abfa3e0251f15a30541dac693f35885694df632c7bb0` |

The downloaded PDF has its PDF 1.5 header and the downloaded ZIP is recognized as a ZIP. Repeated local hashing confirms that both upload artifacts, the deposit manifest, and the root published-inspection receipt remain unchanged. Downloads occupy only the agent's ignored `tmp/published_public_independent_readback_20261007/` directory. All **33** recorded checks pass; the nonsecret public response snapshot, safe response headers, redirect evidence, and expected/actual comparisons are preserved in `receipts/published_public_independent_readback_20261007.json`.

Limitations: this is a timestamped verification of public metadata, DOI resolution, and exact uploaded bytes, not a new mathematical review or a guarantee of future persistence. The web browsing tool could not access the API/DOI URLs; direct unauthenticated Python HTTPS requests succeeded. DOI and landing metadata were additionally checked by a separate read-only subagent. No credentials, publication operations, external communications, Google operations, or edits to manuscript/PDF/ZIP/manifest/curated inputs were used. The immutable uploaded artifacts and root-owned reports/state/logs were not edited.
