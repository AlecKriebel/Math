# Independent final package audit

Checkpoint: 2026-09-23 04:05 UTC. Completion estimate for this bounded package
audit: **100%**. This review inspects the final source, publication archives,
metadata, build script, and generated site. It is independent of the earlier
mathematical proof reviews; it is not an additional external referee report.

## Verdict

**PASS after correction of the citation-file type.** No unresolved packaging,
claim-consistency, or reproduction defect was found. This audit made no
canonical build-output changes, deposits, releases, git operations, or outreach.

The original `CITATION.cff` used `type: article` at the top level, which is not
permitted by the [official CFF 1.2.0 schema](https://raw.githubusercontent.com/citation-file-format/citation-file-format/1.2.0/schema.json).
The corrected file describes the source/verification package as software under
MIT and gives the article, preprint status, author, date, version, URL, and
CC BY 4.0 license under `preferred-citation`. This reviewer checked the repaired
fields against the schema. The parent separately reports successful full JSON
Schema validation with YAML dates converted to strings as the schema requires.

## Independently reproduced checks

- Both ZIP files pass ZIP integrity checks, contain unique relative paths,
  contain regular files only, and have no path-traversal entries.
- Every source-manifest entry agrees with its SHA-256 digest; the manifest
  covers precisely every source archive member except the manifest itself.
  Every packaged source file agrees byte-for-byte with its canonical local file.
- The upload kit contains the PDF, nested source ZIP, payload checksum file,
  upload instructions, both metadata forms, and licenses. Its nested source ZIP
  is byte-identical to the standalone source ZIP. Its PDF is byte-identical to
  the canonical PDF and the PDF inside the source ZIP. Payload checksums agree.
- The API metadata is exactly the JSON object `{"metadata": metadata}`. Kit,
  source-archive, and canonical metadata and instructions agree.
- Generated-site download bytes agree with the canonical PDF and both ZIPs.
  Its checksum manifest covers all eight non-manifest files and all hashes
  agree. Every relative link in its HTML, including the fragment link, resolves
  within the generated site.
- A temporary extraction of the distributed source archive, placed under an
  unrelated temporary directory name, runs `python3 verification/verify.py`
  successfully. It reproduces all **7,016 checks**, **1,312 certified box/index
  cases**, and **three detected negative controls**, and produces byte-identical
  `verification/results.json`.
- Running `python3 build_package.py` inside that extracted package reconstructs
  **both ZIPs byte-for-byte**. This uses the distributed PDF; rebuilding the PDF
  is separately documented to require Tectonic and may change PDF metadata.
- The source ZIP contains only the project's own PDF, with no third-party PDF,
  source-page PNG/JPEG/GIF, or downloaded original AmSTeX file. The nested source
  ZIP is the same audited payload. Source URLs and source-file hashes remain
  available as provenance without redistributing the downloaded works.
- The PDF reports exactly **three pages**, has no embedded JavaScript, and is
  not encrypted. The TeX/PDF digests agree with the closure recorded in
  `final-manuscript-audit.md`.

Temporary extraction and build files were removed after these checks. The
archive comparison was performed before incorporating this audit itself;
including this report and subsequent delivery notes necessarily changes archive
digests. The builder includes those reports when present and regenerates all
dependent manifests and download copies.

## Claim, boundary-case, and metadata consistency

The manuscript, README, site, and Zenodo description use the same corrected
quantity: `D=((n+2)/n mean(E))^2-(n+4)/n mean(E^2)` and the same strict conclusion
`D>(E_(J+1)-E_J)^2/4`. The assumptions are a nonempty bounded open Euclidean
domain, integer dimension at least one, Dirichlet eigenvalues counted with
multiplicity, and finite positive integer index. The stronger strict Yang claim
is restricted to real thresholds strictly above the ground eigenvalue.

The final manuscript explicitly uses real eigenfunctions in the coordinate
identity and support lemma, incorporating the earlier wording repair. It treats
repeated ground eigenvalues directly and does not claim strictness at the ground
threshold. Rough boundaries, disconnected sets, and other eigenvalue
multiplicities are consistently included. The original source's missing square
and exclusion of the neighboring growth question are disclosed throughout.

The numerical counts agree across the results, verifier README, main README,
verification report, site, and Zenodo metadata: 7,016 checks, 1,312 box/index
cases, 600 zero gaps, 12 repeated-ground cases, and three negative controls.
The computation is consistently described as finite algebra/model verification,
not a formal proof of the general analytic theorem. Independent AI reviews are
not presented as external peer review. Priority is consistently limited to the
inspected literature, with no exhaustive novelty guarantee.

Author, ORCID, version 1.0.0, and September 23, 2026 UTC agree. The priority audit's
September 22 date is explicitly in America/Los_Angeles and is consistent with
the UTC date; the PDF creation time has the same timezone explanation.
Documentation states that Zenodo metadata is prepared locally, no DOI is minted
or reserved, and server validation/deposition has not occurred. Citation and
metadata files contain no invented project DOI.

## Portability and remaining scope

The distributed verifier uses only the Python 3.10+ standard library, resolves
its output relative to its own location, and its documented invocation uses
package-relative paths. The build script resolves paths relative to itself;
normal builds require neither this machine's home directory nor a git checkout.
The repository-only `--deploy-copy` mode is explicitly optional and guarded.
The extracted archive contains everything required for the documented normal
verification and archive build. Download links to generated ZIPs in the source
README become available after that documented build; recursive ZIP inclusion is
intentionally avoided.

This review checked local generated-site links and payloads. Live deployment is
the parent's separate delivery check. Zenodo server acceptance and publication
remain outside this prepared upload kit. No claim of machine formalization or
exhaustive priority certification follows from this packaging pass.
