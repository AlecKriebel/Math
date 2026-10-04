# PR65 whole-package adversarial review, new round 1

Reviewed immutable scientific head: `5cc1602c05d79502defb07cec7027963149494d2`.

Reviewed public package: `publication_package_v1/`, exactly the 33 regular files
pinned in `INITIAL_PINS.json`. The closing comparison in
`PUBLIC_PACKAGE_FINAL_PIN_CHECK.json` found no changed member. The package is
unpublished. This report supplies neither publication permission nor a PR65
exception, novelty certification, historical-priority clearance, human peer
review, or formal proof-system verification.

## Verdict

**Bounded mathematical adversarial review: PASS; whole-package round 1:
MINOR TRACEABILITY REPAIR REQUESTED, then a new round 2.**

I found no substantive mathematical failure, unsupported central transfer,
circularity, missing boundary case, incorrect global derivative constant, or
misleading novelty/human-review claim in the final note. I found one minor
historical-runner custody omission, described below. The current public runner
and unchanged diagnostic scripts independently replay successfully; the
omission does not invalidate that replay or the analytic proof.

Historical priority and the historical meaning of “explicit” remain unresolved.
The package says so prominently and credits the old mechanisms. Passing this
bounded correctness review does not resolve those questions or authorize
publication under the parent task's policy.

## Independence and exact scope

The first scientific conclusion was recorded at 2026-10-04
06:25:01.293654 UTC in `FIRST_INDEPENDENT_CONCLUSION.md`, after reading the
entire `note.tex` and before reading package provenance, priority notes, or
prior reviewer/root opinions. That conclusion was provisional and already
found no proof failure. I did not read sibling mathematical/priority reports
to decide this verdict. Later I checked the bytes and hashes of the five
exposition-input reports without consuming their opinions. A parent message
reported concurrent root preflight checks after my first conclusion; none of
those operations is credited as my own verification.

I read the complete final TeX manuscript, including both appendices and all
references; the complete preserved historical `CANDIDATE.md`; all four
diagnostic scripts; the current runner and manifest code; README, priority
note, bibliography, provenance, verification summary, deposit metadata, and
both licenses. I checked every archive member and every stored output/receipt
by bytes or parsed fields. I rendered and visually inspected **all ten** pages
of the supplied `note.pdf`, at 120 dpi. No clipping, overlapping equations,
unresolved citation, broken glyph, or inconsistent title/date/ORCID was found.
The native compiler separately returned success for a disposable copy of the
source; no editor tab was opened or changed and no compiler PID is claimed,
because its API response exposes none.

Primary-source inspection in this review was bounded as follows:

| Source | Actual inspected material | Purpose |
|---|---|---|
| Hayman–Lingham 2018 v2 | Printed pp. 104–105 in retained full-source extraction, including complete Problem 5.51/update and surrounding context | Exact target, known existence, dated no-progress statement |
| Kahane 1969 | Complete retained OCR body, printed pp. 185–192; close inspection of construction pp. 189–191 and bibliography p. 192 | Fixed absorbed unit rule, strict-neighbor variant, constant-step admissibility, general-interval estimate, Piranian/DSS trail |
| Cantón 1998 | Introduction p. 211 and construction hypotheses/rule pp. 214–215 | Decreasing steps, positive barriers, directed transitions; impossibility of claiming the unit/zero rule as a literal theorem specialization |
| AAN 1999 | Theorem 2 on p. 320, covering proof pp. 326–327, explicit Cayley application pp. 328–329, criterion on p. 333 | Stronger pre-existing construction and precise attribution |
| Carmona–Donaire 1999 | Complete printed pp. 207–208 and ancillary p. 210 | Weighted positive-measure class, ordinary versus symmetric derivative definitions, exact finite NT Loomis statement |

These were private retained lawful source copies/extractions; source paths,
sizes and SHA-256 values are pinned in `SOURCE_PINS.json`. No full primary
body or source image was copied into this audit or the public package. I did
not conduct a new worldwide literature search or read the original Loomis
1943 body, Piranian/DSS 1966 bodies, or relevant 2019 book update. I have not
independently certified the package's statements that earlier agents read
other complete papers. Its attribution limits are qualifications, not novelty
evidence. I do not infer lack of prior publication from those limits.

## Mathematical adversarial assessment

**Claim and success criteria.** The construction must prescribe a holomorphic
disk Blaschke product, with no singular canonical factor, normalized at zero,
whose complex Cayley derivative has a global Bloch bound. The effective
interpretation additionally needs finite algebraic rational-inner stages and a
computable compact error modulus. An a.e. singularity statement, a radial-only
argument, or mere compact convergence of finite Blaschke products would not
meet those criteria. The final note explicitly supplies the missing stronger
ingredients, and the target itself does not formally define “explicit.”

**Recursion and seams.** The asymmetric left/right tie choices and ordered
middle pair produce exactly two positive and two negative unit increments at
each positive integer height; zero is absorbing. Parent mass, positivity and
the height bound follow without looking at new children asynchronously.
Across unequal positive parents the facing difference is `d-2 sign(d)`;
across equal positive parents it has modulus two; a zero neighbor forces the
positive facing child down by one. These are all seam/tie cases, including
the one-cell initial cyclic list. The actual first two lists and `B0=-z`,
`B1=-i z^2` are consistent. A new independently written exact checker tested
10,048 cyclic configurations/high translates of lengths 1–6, including
heights shifted by 1,000,001, as a finite falsification attempt.

**Weak limit and singularity.** The proof establishes atomlessness before
using half-open grid cells as continuity sets. For each fixed level, an open
neighborhood has mass at most `2(n+1)4^-n` in every later approximant;
Portmanteau's open-set inequality has the direction used in the paper. The
bound tends to zero and removes endpoint ambiguity. Consistent cell masses
then identify every subsequential weak limit. Absorption under Lebesgue
measure follows from the bounded stopped walk and exit argument. Its union
of zero-mass cells gives singularity directly, so no uniform-integrability
assumption or illicit passage of a martingale limit's total mass is needed.

**All-point obstruction.** Each specified nested path is eventually zero or
has unit successive changes forever. Thus it cannot have a finite positive
limit. The paper uses ordinary density over arbitrary intervals with the
point strictly inside, not just centered density or an a.e. assertion.
For grid endpoints the comparison `(x-h^2,x+h)` to `(x,x+h)`, with the
extra mass bounded by the centered `O(h^2)` interval, legitimately obtains
the one-sided ratio. Atomlessness and local periodic lifting cover every
grid endpoint and the circle seam. No exceptional point is discarded.

**Global Zygmund and full Bloch derivative.** The uniform primitive tail is
valid since every old cell's increment has integral zero and modulus at
most one. At the selected scale the length-`2h` interval meets at most nine
cells; their chained slope range is at most 16 and the stated looser 18
is safe. The tail contributes at most `16h/3`, below the stated constant
24 together with 18. The large-scale bound and periodic lifting handle
all arcs. My new exact primitive controls examined both the submitted and
Kahane fixed rule through generation 4, including the line-arrangement
lattice where all finite piecewise-linear ratio extrema can occur.

Appendix A has the correct normalized Stieltjes formula and factor `6/pi`
after pairing the even zero-integral kernel against second differences.
The bounds `D>=delta^2+(2/pi^2)t^2`, `|D'|<=2|t|`, `|D''|<=2`, and
`1-r^2<=2delta` give the displayed second-kernel estimate. Its two elementary
integrals evaluate to `(2pi^4+2pi^2)/delta`. Crucially, bounding
`v=Im(zF')=-u_theta` is followed by an interior harmonic gradient estimate,
the Cauchy–Riemann equations, and radial integration of the other component
from `Re(zF')(0)=0`. This controls the **full complex** derivative; it does
not stop at the tangential real-part derivative. The resulting
`240pi(pi^2+1)<8196` is a valid deliberately loose global constant; the
small-radius probability-kernel bound covers zero and the central disk.

**Innerness and canonical purity.** Positivity prevents the Cayley
denominator from vanishing and yields the defect identity. The singular
Poisson measure's a.e. radial limit plus the bounded analytic boundary
theorem establishes innerness, but the proof does not mistake that for
purity. A nonzero singular canonical measure has infinite centered density
at its own a.e. points; the cone-dependent Poisson lower bound then forces
the singular factor, and hence B, to tend to zero **nontangentially**.
Consequently the positive Poisson integral tends to one NT. Carmona–Donaire
pp. 207–208 state exactly the finite-NT/ordinary-density Loomis theorem
being used. The disk-to-half-plane map and weight `pi(1+t^2)` have the
claimed identity and integrability; normalized angle has derivative
`1/pi` at the rotated point. Therefore the forced circle density is one,
contradicting the all-point obstruction. The proof is not using the weaker
radial/symmetric converse. The origin order/Jensen argument checks the
actual Blaschke sum; the finite boundary-pole argument correctly makes the
product infinite. The singular compact-limit negative control correctly
explains why finite-stage innerness alone is insufficient.

**Finite stages and effectivity.** The positive atomic Herglotz function
has only the specified simple boundary poles. At each atom the stated
polynomial numerator is nonzero, so the Cayley point is removable and
equal to one; away from atoms its denominator cannot vanish on the circle.
The disk denominator is excluded by positivity. Factoring the disk zeros
therefore leaves an analytic zero-free quotient continuous on the closed
disk, whose quotient and inverse maximum principles give a unimodular
constant. This validates finite rational-inner, hence finite Blaschke,
stages. Weights are rational and specified midpoints are roots of unity.
Midpoint transport gives both compact error bounds with the displayed
angular factors; the derivative kernel bound is also correctly normalized.
The Cayley difference identity, compact `|1-B|>=1-r`, and rational
majorant `13r/(1-r)^2` justify finite precision selection and effective
evaluation for the stated input model. No numerical root search, unknown
measure selection, or unproved global denominator bound is being hidden.
The individual atomic stages remain non-Bloch, as correctly disclosed.

**Older rule and attribution.** Kahane's fixed absorbed rule has the same
pointwise unit changes, positive mass, neighbor estimate and vanishing seam
cells. Applying the already proved analytic mechanism therefore gives the
same target and compact-rate type. The note correctly labels that final
application as a deduction, not proof that it had previously been printed.
The AAN theorem and printed rotated Cayley application justify the stronger
prior-work credit. The Canton qualification matches its actual step/barrier
hypotheses. No new measure mechanism, stronger existence, first solution,
or settled 2026 open-status claim is smuggled into title, abstract, metadata,
or current supporting prose.

## Reproduction, custody, and package consistency

The archive has 31 regular members, passes CRC inspection, has no member
different from its corresponding public file, and excludes the separate
PDF and archive itself as stated. The 29-member supporting-file manifest
and its own digest verify. Because my first disposable manifest check and
replay overlapped, I do not use that first manifest process as the decisive
custody check; a later strictly read-only verification of the untouched
public manifest independently passed. All original public hashes remained
unchanged. No shared Git/index/refs/status/queue/budget/PR/upload state was
mutated.

My actual current-launcher replay was process 10530, with diagnostic
children 10536, 10537, 10543, 10544; all exited zero. It independently
reproduced the author's 2,884 assertions, legacy independent 37,154,
factorization 4,534, and analytic generations 0–8 bounded outcome. The
four stdout hashes exactly match the archived diagnostic streams and each
stderr is empty. Original result JSONs agree with their respective stdout
JSON. An optimization negative control, process 16806, exited **one as
expected** with the assertion-preservation guard before running checkers.
This is an intentional rejection, not an unexplained failed verification.
The new adversary, process 14206, exited zero with 293,966 exact bounded
checks; its script is independently written and imports no package code.
No count here establishes a limiting analytic theorem or priority.

`execution/*/record.json`, exact `.bin` streams,
`REPRODUCIBILITY_EVIDENCE.json`, and the disposable package's new
`execution/EXECUTIONS.json` preserve genuine observed PIDs, UTC intervals,
exit codes, source hashes and stream hashes. Some initial read-only text
commands and source-pin calculations were invoked directly through the
tool, which exposes no shell child PID; I do not retroactively invent one.

The requested commit is absent from the current checkout's object database,
so I did not conflate workspace HEAD with the immutable scientific head.
I recomputed the retained 270-byte Git commit object to the requested SHA1,
independently serialized the root and each directory linking to the three
original package blobs, and recomputed the candidate and checker blob IDs.
All match. All five claimed unchanged source copies and all five exposition
input pins match declared SHA-256/size. This authenticates the selected
source chain; it is not a new audit of every unrelated tree or prior report.

Paper/PDF title, date, author ORCID, intended version, README and intended
deposit description are consistent. The metadata contains no DOI/deposit ID
or false publication completion. Its CC BY 4.0 manuscript/prose and MIT code
scope is disclosed consistently with the license files. No primary full
body, credential, request header, or outside correspondence occurs in the
public archive. The historical candidate's superseded prior-work discussion
and status are explicitly identified as historical in README. I did not
exercise a live Zenodo API or certify an upload schema accepted by it.

## Required minor repair: historical runner source custody

`execution/EXECUTIONS.json` truthfully preserves an earlier run from
`reviewable_note_v1`. Its recorded launcher hash is
`8456746a69b283b6bba43b6c125ba1994c616f739269e1c246b81eb85bc505f3`,
but the only packaged current `run_verification.py` hashes to
`4ea0462d8d1a28163e83630c3d994f27a87431975de2890696a0cb1dfb66dce2`.
The current launcher includes the assertion guard and `-E -B` child launch
flags, while those flags are absent from the archived argv arrays. README
already calls the receipts historical, so this is **not** evidence of fake
execution or changed diagnostic sources. Nevertheless, the exact historical
launcher body needed to complete the receipt's source custody is missing
from the public supporting archive.

I independently located and hashed the retained, 5,504-byte
`reviewable_note_v1/run_verification.py`: it matches the historical hash
exactly. I did not execute or mutate it. Preserve that exact file in an
explicitly historical, non-current location; add a short explanation that
the recorded old receipt belongs to that old launcher and that the current
launcher added assertion/environment guards. Keep the current runner and
four frozen diagnostic sources as they are. Regenerate the manifest and
archive, record the package revision, and have a **new** whole-package
adversary inspect the repaired package. Do not silently relabel the old
receipt as a run of the current source or overwrite its original PIDs/times.

That is the only repair requested by this round. It is minor package
traceability work; no mathematical rewrite is requested. The parent has
stated an intention to repair it, but this verdict applies to the pinned
unrepaired round-one package, not to a promised future state.

## Completion and boundary

This bounded whole-package round-one review is 100% complete. Its strongest
result is independent proof/source-step scrutiny with no substantive
mathematical defect found, complete PDF QA, selected immutable source-chain
authentication, successful finite replay, and a precisely identified minor
public custody omission. The exact remaining work is that repair followed
by a new whole-package round, alongside the separately unresolved priority
and policy questions. No outside individual was contacted, no new subagent
was spawned by this reviewer, and PR50's editor was untouched.
