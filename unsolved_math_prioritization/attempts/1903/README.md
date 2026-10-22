# Least totient preimages: audited partial result (EP-51 / 1903)

This unrefereed, AI-assisted exposition and independent internal AI audit
establish an explicit partial result, not the requested divergence of least
totient-preimage ratios. “Accepted” refers only to the internal audit scope;
no external human peer review, journal acceptance of these authored documents,
formal proof-assistant certification, novelty, or global record is claimed.

For F(a)={n≥1:φ(n)=a}, m(a)=min F(a), and R(a)=m(a)/a, the full nine-element
fiber at D=575651577856 has minimum M=1177105133055. Thus
R(D)=4580175615/2239889408=2.044822212490233… . The result concerns the
least preimage, not a freely chosen large preimage.

The full proof in PROOF.md applies the classical Erdős whole-fiber theorem
to obtain infinitely many totients whose ratios exceed this constant and
converge to it from above. Every attained ratio is similarly approached at
arbitrarily large arguments; the global supremum equals the limsup at
infinity and is strictly greater than each attained value. A separate
published counting lemma of Pollack–Pomerance–Treviño proves positive lower
relative density among totients above the fixed threshold. No density limit,
positive natural density among integers, or seed-uniform constant is asserted.

The elementary finite proof uses the complete divisor-plus-one classification:
144 cases for D and 68 for the older seed. Those classifications were
independently verified locally. Full factor tables, JSON certificates,
detailed outputs, and executable code are excluded from this prose edition.
They can be reconstructed from the explicitly stated divisor formulas by
deterministic trial division. The classifications remain genuine finite
proof dependencies; this edition does not distribute all computational
certificates. AUDIT.md retains the substantive review and explains why its
preferred embedded-table presentation was not used. ACCEPTANCE.json expressly
records the permitted honest-disclosure alternative.

The older seed is credited to the August 2026 SciNet claim page, whose recorded
status was partial and awaiting independent review. Its ratio-2 theorem and
census are not accepted dependencies. Both seed fibers were established
independently. The cited analytic inputs retain their exact scope and are
not independently reproved here. See SOURCE_METADATA.json and
SOURCE_VERIFICATION.json for public URLs, PDF identities and recorded
retrieval/inspection history; this edition performed no new source inspection.

Repeated transport alone gives no uniform control of usable primes as the
seed changes and does not prove that the reciprocal increments diverge.
No sequence of seed ratios tending to infinity is established. The exact
least-preimage divergence target remains unresolved by this work.

This eight-file edition contains authored proof, audit, acceptance, and public
verification/source metadata only. It excludes copied third-party source
text/documents/images, computational certificate/table contents, raw data,
private sources, private personal data, and private coordination material.
MANIFEST.json lists every member and hashes the other seven; its independent
digest is recorded in the proposed draft description. No executable
reproduction package is distributed.
