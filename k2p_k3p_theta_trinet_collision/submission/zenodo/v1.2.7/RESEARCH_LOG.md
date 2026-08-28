# Research log

## 2026-08-27 -- Paper-first Zenodo v1.2.7 package

- Reframed the Zenodo deposit as a publication/preprint whose primary object
  is the complete manuscript, with the source, certificates, verifiers, and
  replay materials supplied in a canonical supporting archive.
- Rejected reuse of the v1.2.6 upload set because its embedded manuscript no
  longer matched the final production PDF.
- Froze annotated tag `k2p-k3p-theta-v1.2.7` at commit
  `19cf11f65ed448cf031842b666e4bfc7e02a9ab7`.
- Built the canonical archive from that tag in a clean extraction. The release
  builder passed the ordinary and optimized exact replay suites, hostile-input
  tests, PDF rebuild, manifest checks, and deterministic-archive checks.
- Collected exactly three intended upload files: the standalone manuscript,
  the matching canonical ZIP, and a checksum manifest covering both.
- Independently audited the metadata scope and archival-language claims. The
  guide describes the public record as documenting archival chronology and
  does not characterize Zenodo as conferring legal priority or peer review.
- Best-guess completion: 100% of package preparation. The remaining actions
  are the author's review of Zenodo's final preview and the irreversible
  Publish action.
