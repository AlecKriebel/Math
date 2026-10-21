# A two-pole proof of the centered pedal-area invariant

Alec Kriebel · ORCID 0009-0001-9320-500X · 16 October 2026

This is an attributed alternative research note. Alper Ferudun's
*Center-Pedal Area Products in Elliptic Billiards*, version 1.0,
DOI 10.5281/zenodo.23085904, proves the same qualified theorem.
The manuscript credits that result and related methods; no theorem,
formula or method novelty, firstness, independent discovery, or literal
simultaneity is claimed. The dated GitHub and Zenodo records do not
establish discovery chronology or historical visibility.

## Exact claim

For a noncircular ellipse and a proper strictly nested confocal elliptical
caustic, multiply the signed shoelace area of a physical billiard orbit
by the signed shoelace area of its ordered origin-pedal polygon, using
orthogonal feet on the complete original sidelines. The product is
phase independent for **least physical periods** that are odd or divisible
by four, including admitted primitive stars and reversal. The original
experimental table does not literally say least period; a doubled
six-period counterexample explains this qualification. The proof makes
no arbitrary-point, hyperbolic-caustic, clipped-foot or filled-star-area
claim. Absolute values of the signed shoelace areas also give the same
product.

The six-page paper, rather than computational agreement, supplies the
universal meromorphic argument. The current manuscript governs these
claims. Original submission files and dated audit records are preserved
unchanged as historical evidence, including their earlier limitations.

## Files and provenance

The three intended Zenodo uploads are centered_pedal_dn.pdf,
centered_pedal_dn.tex and verification-package.zip. The archive contains
this README, license, intended metadata snapshot, portable verification
entrypoint/evidence, and materials in the original A204-relative layout.
PUBLIC_MATERIALS_MANIFEST.json is the authoritative list of included
archive files and their SHA-256/size pins. It separately identifies the
two external manuscript uploads; they need not be duplicated in the ZIP.

The materials preserve all20 original submitted files, independent source,
complex, direct-geometry and Euclidean-shooting records, hardening repairs,
positive priority evidence, and Root's dated acceptance ledgers. They also
preserve the original GitHub custody and native-tree evidence. These
ledgers are stage-specific records: an earlier false publication-readiness
flag is not rewritten after a later stage.

Some upstream authored manifests describe a larger original local
collection. In particular the direct-geometry manifest pins a private
512477-byte runtime-cache inventory, SHA-256
a68a3f8b1fa83bc1a40818dc61f0ca3deb6bc45e8927a565085dc9b1d3aa7a5b,
which is intentionally excluded. The resolved incident concerned
regenerable bytecode outside that auditor's assigned folder; source and
scientific results were retained, cleanup was separately checked, and
later runs disable bytecode. Upstream manifests remain byte-exact
provenance records, not completeness claims about this archive.
No mathematical premise depends on that private inventory. Primary
third-party PDFs, dependencies, credentials, UI data and operational tree
caches are excluded; primary-source URLs, hashes and reading scopes are
recorded instead.

The source-analytic and complex families verified the universal Jacobi
argument after exposure to the candidate proof. The direct-geometry
family independently proved low-period cases; its general scalar route
remains partial. Euclidean shooting is independent finite physical
evidence. Root's pre-candidate flag route also remains incomplete. No
independent-discovery or multiple-independent-universal-discovery
certification is inferred from these activities.

## Run the finite controls

Use Python with existing SymPy1.14.0 and mpmath1.3.0. From the extracted
archive root:

    python3 -B portable_verification_01/verify_portable.py \
      --materials materials --work-dir verification-work \
      --output verification-receipt.json

An optional PR204_RUNTIME_PACKAGES environment variable may name an
existing directory containing those two packages. Otherwise existing
PYTHONPATH or installed packages are used. The driver installs or
downloads nothing. It checks142 material pins and runs28 expected
outcomes:14 valid ordinary/optimized executions and14 intended false
identity/NaN rejections. Correct failure identities and finite data are
required; an arbitrary nonzero exit does not count as successful rejection.
Seven valid mode pairs must agree. Default concurrency is two; use
--jobs 1 to reduce concurrent work. Writes use new owned receipt files
and disposable layouts outside immutable material families. See the
portable README for exact runtime, raw-evidence and path rules.

Historical bare-assert scripts lose their correctness enforcement under
Python optimization. They are archived records, **not live entrypoints**.
Explicit-exception derivatives reproduce their valid JSON byte-for-byte
and reject genuine false identities in both modes. The portable driver
runs those derivatives and current independent checks, never the
historical bare-assert programs or fixed-runtime audit wrappers. The
historical PROOF.md copied into one temporary layout is only a legacy
hash-binding input, not the present manuscript.

PORTABLE_RUN_RECEIPT_02.json and its gzip companion preserve the successful
28-case run, code/flag/raw-output bindings, software versions, immutable
input snapshots and unchanged dependency-cache inventories. The exact
first failed run is also retained:13 cases completed as expected, then15
temporary-layout setups failed with ENOSPC. It is explicitly FAIL.
Per-case cleanup was then improved and a distinct complete run passed.
No scientific failure was hidden. The local dependency path and temporary
paths in historical receipts record actual past execution; they are not
requirements for a new machine.

These are finite exact checks and noninterval numerical diagnostics.
PASS certifies those controls, not universal phase constancy or novelty.
The physical audit sampled63 primitive shape/winding configurations and
378 phase/direction orbits. Exact radical controls cover two phases each
for periods three and four and the primitive-six/repeated-twelve boundary.
The full theorem is proved analytically in the manuscript.

## Disclosure and reuse

AI tools were used extensively in derivation, auditing, computation,
software and drafting. Internal adversarial AI reviews do not constitute
conventional human peer review. This is an unrefereed preprint without
proof-assistant certification. The author is responsible for its claims.
No outside person was contacted for this project.

The author's paper and supporting materials are offered under CC BY4.0.
Third-party sources are cited, not relicensed or redistributed here.
