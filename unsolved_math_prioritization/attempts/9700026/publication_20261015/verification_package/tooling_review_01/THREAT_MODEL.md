# Independent tooling threat model

Recorded 2026-10-15 09:49 UTC, before reading candidate tooling or engineering verdicts.

This review tests the publication-tooling claim for PR 880 / PID 9700026 at original head fba74a301786f9648e48722e76f440097b0746c2 and the externally specified source-manifest SHA-256 b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b. It does not certify a mathematical or priority claim or constitute the mandatory final whole-package review.

The intended trust boundary is that an external caller supplies startup pins and tools authenticate the candidate before executing candidate-controlled code. A byte-consistent package is insufficient if its self-described index or embedded wrapper can replace that external trust boundary. Startup-marker tampering must be rejected without executing the marker. The historical source wrapper must be authenticated and never executed.

Attack families, fixed before code inspection:

1. Filesystem closure: symlinks, FIFOs, devices/special files, missing files, unlisted files and empty directories, unsafe relative names, unexpected parents, and output paths inside input or colliding with inputs. Negative fixtures must never write through hard links or symlinks into authentic evidence.
2. Structural and typed parsing: duplicate JSON object keys, boolean/integer confusion, NaN/Infinity and overflow such as 1e999, unknown fields, inconsistent counts, and metadata that understates work or ZIP expansion.
3. Archive consistency: duplicate ZIP names, unsafe/absolute/dot paths, directories and special mode attributes, noncanonical compression/timestamps/flags/comments/extra fields, declared and actual byte limits, readable duplicate divergence, nested archive inconsistency, and exact tree/index membership.
4. Execution: proof of ordinary and optimized Python behavior, absence of security-critical asserts, pinned startup before imports/replays, malicious authenticated-looking markers never executing, no implicit execution of historical wrapper, deterministic reconstruction, and authentic positive controls.
5. Scope and truthfulness: eight finite original replays must really run; source-free execution must say NOT_RUN truthfully; verify-only must not claim full source/PDF replay; optional provenance arguments must be all-or-none and map each of three corpora and two PDFs to the correct role (especially 2012).
6. Assembly: explicit authored-file allowlist, exclusion of raw third-party files/private fixtures, fresh or controlled output paths, reproducibility, no unintended global changes, and resistance to absent final paper/index/ZIP.

Success requires concrete rejection evidence plus working positive controls, inspection of complete implementations, and exact labeling of untested final assembly boundaries. Synthetic paper bytes will be visibly labeled SYNTHETIC TOOLING FIXTURE, never represented as the real paper. Tests use only review-private disposable state. No corpus copying, final assembly, publication, external contact, or repeated PDF marker is authorized here.

Initial completion estimate: 5% of this independent tooling review. Central uncertainty: whether the implementation enforces the above boundaries end-to-end, rather than in unused helpers.
