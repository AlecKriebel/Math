# Acceptance: K3 support-genus partials

K3 Problem 3.45, catalogue 2843, rank 1045. Accepted as partial research on
2026-10-08. Queue disposition: **unsolved, 5/5**. Both parts remain unresolved.
No genus-two support example, unbounded-support-genus family, universal genus-one
upper bound, full solution, or novelty claim is certified.

## Accepted mathematics

The complete author report and independent audit establish, within their stated
hypotheses, the following useful partial conclusions:

- For the once-bordered boundary-twist family, first homology is free of rank 2g,
  connected-binding support genus is exactly g, and support norm is exactly 2g-1.
  Unrestricted support genus can still admit genus-one pages with growing binding
  count. The annulus control requires relative-arc relations.
- The horizontal-page lower bound is conditional on the fixed fiber projection
  and actual covering hypothesis. Conformal change of the contact form changes
  its Reeb field, so this is not a bound for arbitrary supporting open books.
- For the Euler-number -1 Boothby-Wang family, c1 is zero and
  d3 = -g^2+2g-1/2 in the stated normalization. The symplectic zero section gives
  nonplanarity through an imported theorem, hence 1 <= sg <= g. Formal plane-field
  invariants alone cannot supply a positive universal support-genus lower bound.
- Abstract U-module diagnostics distinguish finite depth, infinite depth, and
  annihilation by U. They neither realize the actual Floer module/contact class
  nor establish a genus-one obstruction.
- Weighted capping constraints bound positive allowable factorization length and
  fillings presented with one fixed genus-one boundary open book. A bound on all
  Stein fillings is not thereby established.

The five approaches remain five. Source searches, audit, regression tests,
packaging, and code correction count as no additional mathematical approach.

## Imported source qualification

Orbegozo Rodriguez and Stenhede, *The support genus does not increase under contact
connected sum*, [arXiv:2607.19892v1](https://arxiv.org/abs/2607.19892), submitted
2026-07-22, is an imported preprint. Its maximum upper bound prevents iterated
connected sums of genus-one summands from giving the desired higher genus. It is
not proved by this packet and does not settle either question. Its recorded
manuscript status and the original K3 page-163 problem identification are retained
as historical inspection metadata. Fresh publication-stage source downloads,
source-byte checks, literature updates, and imported-theorem verification are
**NOT_RUN**. A bounded historical search is not a proof that no resolution exists.

## Preserved original and minimal correction

The original nine-file freeze remains separate and unchanged in `original/`.
Original manifest SHA-256:
`9e290bec9d6ba40ec3a61a1c41b9e70381f75c3ab80db6e2a4ef55f83d3aa751`.

The corrected candidate is separately retained in `audit/candidate_public/`.
Candidate manifest SHA-256:
`daaf2d88de9272733ea1d674396ec2236cfe250d4796dc922e841890ff087b69`.

Audit pins SHA-256:
`e63e6135620d9bac3fa22abcfe0af22b61c5dfd4167513472711e5aab43c116f`.

The actual `audit/public/OPTIMIZATION_FIX.patch` replaces 23 arithmetic assertions
and six packet assertions by explicit require checks. Only these two scripts and
the separately re-pinned candidate manifest differ. The report, result, arithmetic
results, source metadata, README, and five-approach ledger remain byte-identical.

The original has **44 optimized false passes** in invalid integrity/arithmetic
controls. The corrected implementation rejects all 60 non-type-equivalence
negative case/mode combinations, including those failures. Both versions still
accept a saved JSON true changed to integer 1 when the local manifest is also
rehashed, in all five recorded modes. The native parser permits nonfinite tokens;
the tested NaN is rejected by result comparison, not by strict parsing. These
limitations are preserved and explicitly disclosed, not silently repaired.

## Publication wrapper and trust boundary

The separate publication wrapper authenticates exact files against externally
anchored bootstrap, manifest, original, candidate and audit pins before executing
packet code. It validates its own schema with exact types, rejects duplicate JSON
keys and nonfinite/overflow numbers, and compares replay results with exact types.
Thus a changed candidate with a self-rehashed local manifest is rejected by the
fixed external anchor. This does not make the native candidate a strict parser.

Execution requires actual UID/EUID 1000 and Python's isolated, no-site, no-bytecode
flags. Replays use permission-read-only packet copies and working directories,
with write-denial probes. Normal, -O, and -OO publication checks include the native
150-run audit (which also tests inherited optimization) and independent arithmetic.
Negative controls cover malformed schemas, modified/rehashed candidates, extra or
missing files/directories, links, FIFOs, wrong pins, hostile imports and relocation.
Main and independent arithmetic replay results are compared as exact-type JSON
objects rather than raw stdout bytes. For the native 150-run receipt comparison,
stdout_sha256, stderr_sha256 and last_error_line are omitted from each row, and the
last-error string is replaced by its error class. Every other row field (including
mode, runtime identity/optimization, status, exact result object and read-only
probes) is retained and compared with exact types. Temporary path-bearing errors
and their hashes can differ. No full byte-identical native-receipt claim is made;
the complete historical receipt remains unchanged. The native harness stages
writable disposable source copies because its copytree-based negative-control
generation preserves source modes; all actually executed native control copies
are made permission-read-only before execution and their source bytes are checked
again afterward.

Authentication depends on obtaining the bootstrap hash from an independently
trusted channel. No local manifest alone supplies authenticity, and these
read-only tests are not an OS sandbox or a defense against concurrent adversarial
filesystem replacement by another same-user process.

Only authored mathematics, audit/correction material, code, and public verification
metadata are included. No source PDFs, extracted source text, dataset contents,
private sources, private personal data, or private coordination material are
included. The existing queue is preserved except this target's Status, Turns,
and Findings cells. No merge, release, or outreach is part of this publication.
