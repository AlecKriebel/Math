# Independent acceptance report

Problem 30000801 / OWR-1591-003 / catalog rank 816.
Audit date: 2026-10-06 UTC.

## Decision

**ACCEPT_CONDITIONAL_RESULT_ONLY_FULL_TARGET_UNRESOLVED.**

The frozen author's local Pohozaev identity, conditional mass relation
n₀=m²/(16π²), and positive finite-weight one-bubble deduction are correct.
The associated defect formula and objections to the other proposed reductions
are also correct. No mandatory mathematical correction or source correction
was found. The author's five approaches constitute five bounded attempts;
they do not establish the original strong-quantization conjecture.

The untouched author archive is 22,361 bytes, SHA-256
`45ab3bf6abaa90e865cba7899a509de3a8343ab44b32bb09dbbad7ccd9f46434`.
Its 11-member inventory and the author receipt's manifest digest match exactly.
This audit was performed on an extraction of that frozen archive, not on an
unfrozen working copy. It does not modify the author proof or retroactively
change the status of the original problem.

`MATHEMATICAL_AUDIT.md` records the independent derivation, including all
boundary terms, nonradial regular-part bounds, derivative regularity, and the
order of limits. The finite verification code supports that written audit;
it is not an analytic proof or proof assistant certification.

## Reproduction and adversarial checks

- Author verifier: normal and optimized Python each pass 17 exact controls
  with all three full supplied corpora.
- Author advertised adversarial suite: all 24 mutation runs are rejected;
  baseline and relocated normal/optimized runs pass.
- Independently written verifier: normal and optimized Python each pass 26
  exact controls, complete corpus replay, and all four supplied PDF identities.
- Independently written adversarial suite: 36 additional resealed-claim and
  structural mutation runs are rejected by the author verifier.
- Independent relocation: the independent and author checkers pass from
  unrelated temporary directories in normal and optimized Python.
- External freeze protection: four altered/truncated/wrong ZIP cases fail
  the independently pinned original archive identity.
- Source corruption: same-length single-byte changes to each of the three
  corpora and four PDFs are rejected by the independently checked hashes.

`RESULTS.json` preserves the detailed outputs. The counts describe finite
software checks, not the number of analytic statements proved.

## Two nonblocking verifier-scope observations

The author's metadata validator does not semantically pin every descriptive
field. With a deliberately resealed manifest, changing only the public catalog
rank to 999 or one PDF digest to another well-formed 64-character hexadecimal
string is accepted by the author checker, in both Python modes.

This does not invalidate the original frozen bytes or the mathematics. The
README promises explicit mathematical-metadata tests and an externally frozen
ZIP, not an exhaustive semantic validator for every descriptive field. These
mutations change the external ZIP identity and therefore fail this audit's
externally pinned freeze check. The genuine rank and all four genuine PDF hashes
were separately verified in this audit. Users should not treat a newly resealed
manifest as the same accepted artifact, nor treat an offline PASS as live
verification of the cited PDFs. No author-file patch is required for acceptance
of this exact freeze.

## Full-record verification

The three full byte streams, JSON cardinalities, unique target rows, catalog
rank, complete record/report review, and corrected statement all reproduce the
public metadata pins. Review serialization uses the entire problem record and
an absent report represented by {}, with default json.dumps separators and
sort_keys=True. The serialized review is 4,537 bytes with SHA-256
`6c5a284146c34349fd290aa03fea676c2fcd00352dec31988d7a5376d638fe3e`.
The corrected statement hash is
`e240b1b64786f66238f5efc7e10d42b166b7de5c2962733213161c6ba79c7c36`.

The original/legacy statement and background use incompatible nonlinearities.
The cleaned statement agrees with the official report. No corpus contents or
source text are redistributed in this audit.

## Primary-source verification and limits

The official [Oberwolfach report](https://ems.press/content/serial-article-files/46122)
was independently inspected, including locally rendered visual checks of
printed pages 2071–2072. They confirm the squared exponent, linear prefactor,
Navier data, scaling 96, quantum 16π², relative-scale separation, integer
quantization, and the stronger L=I question. The workshop is July 22–28, 2007.

[Struwe's author paper](https://people.math.ethz.ch/~struwe/CV/papers/ConcEner.pdf)
was checked at Theorems 1.1–1.2 and the introduction. It gives integer energy
quantization and raises the stronger question. It does not justify silently
replacing the selected-center index by the count of distinct limiting locations.

[Robert's revised author paper](https://iecl.univ-lorraine.fr/wp-content/uploads/2021/04/RobertExpQuanti.pdf)
was checked at Theorem 1.2: it concerns a different exponential equation,
uses the opposite second-order Laplacian sign, and assumes explicit Laplacian
integrability controls. Its multiplicities are positive integers, not
necessarily one.

[Martinazzi–Struwe](https://people.math.ethz.ch/~struwe/CV/papers/Quantization-2m.pdf)
was checked at its boundary conditions, Theorems 1–2, and subsequent discussion.
Its conditions are clamped Dirichlet; it cannot be treated as the Navier theorem.
Its discussion of a simpler exponential equation also retains the convexity
condition for the cited Navier result.

[Druet–Thizy](https://arxiv.org/pdf/1710.08811) was checked in the introduction
and Theorem 1.2. Its strong concentration theorem is two-dimensional and
second order. [Chen–Deng](https://arxiv.org/abs/2608.03321) was checked only at
the primary abstract/version metadata: it is a different nonlocal Choquard
problem, not a verified resolution here. Its manuscript is v1, August 4, 2026;
no journal reference was displayed. The source-audit scope distinctions stand.

The four supplied PDF byte streams were independently rehashed and matched.
Official URLs were independently opened through the web tool; those web reads
are not claimed as separately downloaded byte streams. The web screenshot
endpoint failed for the OWR pages; local rendering from the verified PDF
provided the visual inspection instead. Primary-source inspection was targeted,
not a line-by-line independent audit of the cited papers' entire proofs.

A fresh bounded search found no verified exact-target resolution. This is not
a proof of worldwide literature completeness or of the conjecture's current
open status. The author's prior GitHub search/history claims were not rerun;
they remain historical author-reported checks. This audit made no remote
repository mutation, publication, or external outreach.

## Promotion blockers

Strong quantization would still require deriving comparable positive finite
normalized heights, the exterior logarithmic profile, finite primitive-mass
limits, and both weighted exhaustion statements from the original assumptions.
Boundary regimes, distinct spatial locations, selected centers, and all bubble
tree levels must also be handled without interchanging their counts.
Ordinary energy no-neck does not automatically supply weighted no-neck.
Those are analytic gaps, not defects that additional finite tests can repair.
