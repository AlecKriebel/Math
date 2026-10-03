# Literal geometry family audit of immutable original PR42

Status: **scoped mathematics checked; one provenance correction required**.
This is this family's review of original head
`099ae5e4d06d8789214cfaaece87309c87e914f9`, actual base
`60292bed09f59236aa192cb17aa138f7b4750e1a`. It is not a review of any future
corrected head, a full solution, a novelty certificate, or historical runtime
attestation. The initial seal and its exposure disclosure remain unchanged.
No sibling-family verdict was read. No original scientific helper was executed
by this family. All new diagnostics are separately authored audit controls.

## Artifact and full source read

`candidate_inventory.json` records actual complete byte reads of all 17 files
in ROOT's immutable `source_snapshot_v2`, their SHA256 values, and verified
0444 permissions. Every JSON/JSONL was completely decoded; every key in the
1263-entry independent result dictionary was parsed and its PASS value checked.
The mathematical note, source audit, README, research log, two complete checker
sources and old review were read directly. The two author checker copies and
their receipt copies are byte-identical. The old-to-final mathematical note
diff is exactly the review-status header replacement, with body unchanged.
These are present-file facts; they do not verify past claimed model settings,
execution, timing, search breadth, priority, or independent review history.

The exact target matches the flat pinned id 2233/EP-653: maximize the number of
different integers among the pinned-distance counts. Trivial upper g(n)<=n-1
for n>=2 makes the question's asymptotic lower bound equivalent to g(n)/n->1.
Ordering the points does not change the spectrum. Distinct planar points are
an explicit assumption, and finite diagnostics are appropriately separated
from all-n claims. The candidate's main mathematical artifact is an elementary
construction-route obstruction note; the newer incidence preprints occur only
as attributed outside claims in the source audit, not as proof premises.

## Complete check of the generic gluing mechanism

For a pin p in block i and two comparison points u,v, the forbidden equality
is F=|p+t_i-u-t_j|^2-|p+t_i-v-t_l|^2=0, where j,l record blocks. Cases:

* If j=l is external, the squared translation terms cancel. The coefficient
  of t_j-t_i is twice the nonzero vector u-v. Thus F is a nonconstant affine
  polynomial, including for blocks with collinear or symmetric seed points.
* If j differs from l and at least one is external, hold all translations but
  that external block fixed. Only one comparison point moves, giving a
  nonzero quadratic coefficient. This includes one internal comparison point.
* If both comparison points are in i, the candidate deliberately allows the
  equality and imposes no forbidden polynomial. Each seed is a set, so internal
  point coincidences do not exist. Cross-block point coincidence is a proper
  closed polynomial condition.

There are finitely many proper zero loci. Their union has empty interior, and
its complement is open dense in the full independent translation space.
This argument requires the full translation space: constraining translation
directions can make an equality identically true. The candidate states the
full-space hypothesis, so that restricted-parameter pitfall is not a flaw.

At an admissible placement, external points supply n-m_i mutually different
new distances at a pin; internal lengths are translation-invariant. Hence
r_Q=n-m_i+r_{P_i} and

    (n-1)-r_Q = (m_i-1)-r_{P_i}.

The deficit spectrum is exactly the union of seed spectra. A singleton has
deficit zero. Seeds of sizes at most M>=2 have deficits in 0,...,M-2, including
zero from singleton seeds, so the union has at most M-1 values. All singleton
seeds give one value. Iterating this identity at every admissible hierarchy
step yields the leaf union and the o(n) conclusion when M(n)=o(n). Single-block
and singleton boundaries do not invalidate any conclusion.

The unit-square negative control is valid: each unit segment has deficit zero,
but the four square pins have deficit one. It refutes extension of the identity
to nongeneric gluing and identifies the exact unrestricted gap. The candidate
does not claim arbitrary or deliberately equal-distance gluing is blocked.

## Complete check of geometric support restrictions

For a supported pin on a line, a positive distance circle intersects the line
in at most two points. For a supported pin on a positive-radius circle, that
pin is not the supporting circle's center, so its distance circle and the
supporting circle have distinct centers and at most two intersections. Thus
r(p)>=ceil((n-1)/2); with r<=n-1 there are ceil(n/2) possible integer count
values. Arithmetic progression points attain all of them. The candidate's
circular arc also attains them: angular span below pi makes
2R sin(a theta/2) strictly increasing with a=1,...,n-1. Whole-circle wraparound
would break that strict monotonicity, but is explicitly excluded.

If m=n-t>=2 supported points are present, each of those pins has at least
a=ceil((m-1)/2) distances from the supported subset, and adding points cannot
reduce that count. Their full counts occupy at most n-a integers. The other t
pins add at most t values, while the universal trivial bound is n-1. Therefore

    sigma(P)<=min(n-1,n+t-ceil((n-t-1)/2)).

Its right side is at most n/2+3t/2+1/2, so t=o(n) gives the claimed half barrier.
An exceptional center of the circle can have count one; it is covered by the
t exceptions. m=2 and t=0 have correct rounding. The support is exact; the
candidate makes no claim for points merely close to a line/circle or for a
growing number of supports. Counts based on exact equalities do not vary
continuously under perturbation.

## Classical upper defect and scope

The pair-center circle argument and spectrum representative inequality were
already proved in this family's initial seal. The candidate uses the correct
representatives a_1,a_2, rather than counting multiplicity of a small count.
Distinct centers prevent coincident circles; positive radii follow from
distinct points. Its n-2<=2h(h+1) and square-root expression have the right
constant and rounding scope. The s=1 and n=2 cases are handled. It is credited
as classical, not presented as a novel discovery.

The strongest candidate result is the exact generic-gluing identity plus sharp
line/circle spectrum restriction and its exception extension. These do not
improve the conjecture's unrestricted asymptotic bounds. Exact remaining gap:
provide configurations for every sufficiently large n with n-o(n) different
counts, or prove a uniform linear-proportion defect. Generic seed replication
and exact line/circle concentration cannot supply this. A universal sublinear
defect with exponent below one, including the cited 5/7 or approximately .817
external claims, remains compatible with the target.

## Primary source verification and exact limits

Post-seal, freshly fetched E95 author manuscript is HTTP200, 190123 bytes,
SHA256 `a4c59e58e15fc7fa6d84a52da523e639b81697e61fc1095294690268b15708ce`.
It exactly matches the candidate's recorded source. I extracted all 20 pages
to a foreign-source derivative but proof-read only the relevant manuscript
pages 14-15, including rendered visual inspection of both entire pages. These
independently confirm the spectrum question, n-o(n) proposal, and Saldanha
credit. E95 uses g(n) earlier for unit-distance multiplicity; this local symbol
must not be confused with Bloom's g(n). The candidate correctly restates the
spectrum parameter rather than importing the earlier symbol's definition.

Fresh official 1997 publisher contents confirms the article title and pages
527-537, but the exact 1997 full text was not recovered. Fresh Janzer et al.
PDF is 269349 bytes, SHA256
`53426e6bd5df5b4eba401c3dc342bd62776932601fd37e3c524918269a8b6da2`,
matching the candidate's v1 source record. Relevant Corollary 1.12 was text-read:
for m planar points and n circles it states the exponents 2/3, 6/11, 9/11
recorded in the outside-claim discussion. Its complete proof was not read or
imported; the candidate elementary lemmas do not use it. Publisher DOI access
failed in the browser tool, so no independent journal-version certification is
made by this family. Full original Erdős--Fishburn and Csizmadia--Ismailescu
proof-reading limits remain as in the initial seal. No historical coefficient,
newer external preprint, absence-of-literature claim, or priority is certified.

Primary files, extracted text and rendered pages are separately inventoried
foreign material. Captures contain source excerpts as forensic evidence, not
as claims of first-party proof authorship. Initial accidental search-snippet
exposure is still disclosed; no erased or backdated independence claim is made.

## Required provenance correction

`SOURCE_AUDIT.md`, first section, says that the corresponding research-results
entry "is null". ROOT reports the raw prior key is **absent**, while the supplied
`pinned_prior_report.json` contains `{}` as an explicitly qualified SQL fallback.
These facts do not establish a fetched null-valued prior entry. The local
artifact must distinguish absent key, stored fallback, and dated triage text.
Suggested correction: "The raw source has no prior research-results key; the
audit's empty object is a SQL fallback rather than a fetched prior result. A
dated OPEN-TRIAGE note occurs in the pinned problem background."

No mathematical correction is required for the displayed scoped lemmas. The
SOURCE_AUDIT's old pending-review sentence can be dated explicitly or updated
for consistency, but is not evidence that the mathematical proofs fail.
Unverified historical model/runtime/search claims require ROOT's separate
provenance treatment; this report does not validate them by repetition.

## Own controls and completion

Full actual PID/UTC/command/source/stdout/stderr captures are in `controls/`.
The initial exact controls checked 6868 small integer-grid subsets and 1580
deterministic samples, the line formulas through n=200, and the exact g(4)
construction. The new adversarial control passed 3697 exact assertions,
including 762 admissible two-block placements, 534 rejected or coincident
placements, 152 support boundary cases, singleton and constrained-translation
pitfalls, and an exceptional circle-center pin. These are finite diagnostics,
not replacements for the proofs above or a replay of original helpers.

Scientific estimate toward solving literal EP-653: **5%**, unchanged.
Own audit completion: **100%** for the immutable original snapshot. There are
**zero new substantive attempts and zero additional original audit turns**.
Original two-attempt ledger and all budgets are preserved. No files outside
this family were edited, no Git/index/branch/native/canonical edits were made,
and no external human communication occurred. Final seal identifies exact
first-party and excluded foreign closures; it applies to this report and its
recorded original snapshot only.
