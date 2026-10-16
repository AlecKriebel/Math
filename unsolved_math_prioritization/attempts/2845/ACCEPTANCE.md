# Acceptance: elliptic Reeb-orbit partial results

K3 Problem 3.47, record 2845, rank 1046. Accepted as corrected partial research
on 2026-10-08. Queue disposition: **unsolved, 5/5**. Both universal questions
remain unresolved. No universal ellipticity theorem, counterexample, realized
all-hyperbolic flow, or novelty claim is established.

## Accepted mathematical scope

The five mathematical approaches are ECH filtered-chain counting, disk-section
Lefschetz indices, Hamiltonian index growth and pinching, uniform hyperbolicity
and S3 topology, and approximation with bounded-period compactness. Source
inspection, correction, independent audit, and publication add zero approaches.

The corrected report establishes the all-hyperbolic reduction under inclusive
spectral ellipticity; excludes the finite-simple-orbit case using established
results; obtains the ECH logarithmic lower bound for the number of simple
orbits of action below L in a hypothetical all-hyperbolic flow; and proves a
conditional dyadic-period recurrence and bounded-period closure lemma.

The ECH lower bound is one-sided. Infinite hyperbolic spectra remain compatible
with it. The all-iterate dyadic index assignment is an abstract solution of the
Lefschetz identities, with no disk-map or Reeb-flow realization claimed. The
positive Hamiltonian matrix example is a transverse linear-system obstruction,
not an all-hyperbolic convex hypersurface. Pointwise hyperbolicity supplies
neither uniform rates nor transversality. The closed-disk extension and boundary
conditions in the Lefschetz argument remain explicit additional assumptions.
Generic ellipticity without a uniform period bound does not settle either
universal question.

The September 2026 Shibata manuscript is reported as a preprint. Its positive
hyperbolic-orbit statement does not exclude mixed all-hyperbolic spectra, and
none of the completed elementary deductions depends on its proof.

## Exact correction and evidence preservation

The original eight-file author slice remains byte-for-byte intact in `author/`.
The separately accepted eight-file slice in `corrected/` applies only the
source-attribution correction in `audit/SOURCE_ATTRIBUTION_CORRECTION.patch`.
The ten-file independent audit slice remains intact in `audit/`.

K3 itself defines inclusive ellipticity in section 3.5 on printed/PDF page 160.
The original mathematical convention was already correct. The patch attributes
it directly to K3 and changes only `AUDIT.md`, `REPORT.md`, `SOURCE_PINS.json`,
and the resulting `MANIFEST.json`. Mathematical conclusions, code, recorded
exact output, status, and the original README are unchanged. The public wrapper
applies the exact unified patch in memory without offsets or fuzz and compares
every reconstructed file byte-for-byte with `corrected/`.

Frozen manifest SHA-256 anchors:

- Original: e807c15d1bcd72e46389a6f9955a9a8c6ce73e764b036ae2a08aa356d9b9c4a1
- Corrected: 7beb5ce3cb8b294c18ab9256c896a79cd8fe8920e46bd253c30a02bbe849407f
- Independent audit: 2d8e417f2921ba7eae8e8500a6d0680292abc50725ba93e6f001fc335ccfe559

## Reproducibility boundary

The native audit requires Linux bubblewrap and actual UID/EUID 1000. It mounts
the entire visible filesystem read-only with `bwrap --ro-bind / /` and no
writable rebind. Actual write-open probes return EROFS for original, corrected,
and independent scripts in normal Python, -O, and -OO. Its six mathematical
mutations are rejected for the intended reasons in all three modes, giving
18 native negative-control executions per wrapper run. No network-namespace
isolation is claimed.

The publication wrapper authenticates the exact recursive inventory and all
26 accepted evidence files before any payload code runs, verifies all nested
manifests and the correction patch, and reproduces the complete historical
native receipt byte-for-byte. Separate publication controls cover malformed
JSON, exact types, path and link boundaries, coordinated repinning, correction
and patch tampering, hostile imports, and relocation. The externally recorded
bootstrap SHA-256 is the trust anchor; a hash read solely from an untrusted
packet does not authenticate that packet.

Seven PDF hash/size matches and source inspections in the accepted audit are
historical observations. Fresh source/PDF checks in this publication replay
are **NOT_RUN**, since source documents are omitted. The replay does not prove
imported ECH results, universal dynamics, or source currency, and it does not
independently certify the September preprint. Finite rational checks support
the separately reviewed written deductions; they are not universal proofs.

Only authored mathematics, authored checking code, arithmetic receipts, the
attribution patch, and public verification metadata are included. No copied
third-party documents, source-body excerpts, dataset contents, private sources,
private personal data, or private coordination material are included.
