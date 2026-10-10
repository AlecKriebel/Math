# Independent adversarial audit: normalized schlicht minimum spherical area

## Verdict and exact binding

**PASS. The exact target is a complete classical consequence. Classify this
target as `already_solved = 1`, with no novelty claim. No blocking
mathematical or source-applicability defect was found.**

Target: rank 686, ID 2306078, Hayman--Lingham Problem 6.78. The reviewed
package consists of exactly nine files and 33,785 bytes. Its original
`MANIFEST.json` is 1,571 bytes with SHA-256
`91f186baae524ac606084115d2f9ed946f71693c737dbc7e759e17c881e47953`.
`FROZEN_BINDING.json` independently pins every file, including that manifest.
The package was treated as read-only throughout the review. Its controls
were copied into a separate replay directory before execution, because
the original control script writes its results beside itself.

The answer is an attained minimum of one half of the standard Riemann
sphere, uniquely attained by `f(z)=z` in the class
`f(0)=0, f'(0)=1`. With density `4/(1+|w|^2)^2` this is `2*pi`; with
density `1/(1+|w|^2)^2` it is `pi/2`.

This audit supplies the previously pending independent mathematical gate.
The frozen package's statements that its audit was pending accurately
record its earlier state and have deliberately not been edited. This
separate audit and its binding establish the subsequent result.

## 1. Governing problem, not an inferred surrogate

The governing primary source is Hayman and Lingham, *Research Problems in
Function Theory (New Edition)*, arXiv:1809.07200v2. I inspected the rendered
class definition on printed page 114 and the complete target on printed
page 145. The class is holomorphic and injective on the unit disk, with
Taylor expansion beginning `z`. The requested quantity is the spherical
area of the image region, and the extremal function is also requested.

There is no coefficient-reality, convexity, polynomial-degree, boundedness,
or boundary-extension assumption. The candidate matches this full scope.
The neighboring editorial update reports no progress received; that does
not invalidate a verified implication of an earlier theorem. No conclusion
about how the historical discrepancy arose is needed or claimed.

Primary reference: <https://arxiv.org/abs/1809.07200v2>.

## 2. Independent classical-source verification

The load-bearing antecedent is Jacques Dufresnoy, *Sur les domaines
couverts par les valeurs d'une fonction meromorphe ou algebroide*,
Annales scientifiques de l'Ecole Normale Superieure, series 3, volume 58
(1941), pp. 179-259, DOI 10.24033/asens.889.

I independently downloaded the complete PDF from the public NUMDAM URL.
The response was HTTP 200, 6,222,006 bytes, SHA-256
`d0736cd82cf1c6bec0a251ee589a1312d9a42a6bb6e93803c055a938df06c0ff`,
exactly matching the reviewed source file. The public archive's
bibliographic record was independently accessible as well.

Inspection included:

- Unit-sphere and covering-sheet definitions on printed pages 181 and 184
  by extracted text.
- The cap/isoperimetric discussion on printed page 186, text and rendering.
- Section 19 on printed page 208, text and rendering, including the
  pullback area, spherical length and Cauchy--Schwarz constants used later.
- All of Section 27 on printed pages 218-220, text and independently
  generated renderings, including the statement, local proof and equality
  formula. The nearby spherical-rotation remark was also read.

In modern notation its endpoint assertion is

`q(0)^2 <= s0 / (r0^2 * (1-s0))`,

where `q=|f'|/(1+|f|^2)` and the spherical covering area is `4*pi*s0<4*pi`.
The proof uses `L^2 <= 8*pi^2*r*s'`, the spherical isoperimetric lower
bound `L^2 >= 16*pi^2*s*(1-s)`, and integration of the resulting logistic
inequality. The small-radius normalization is exactly `s(r)~q(0)^2*r^2`.
Neither the lemma nor its relevant derivation assumes spherical convexity.

The equality family printed at the end of Section 27 is

`f(z) = (b + lambda*z)/(1-lambda*conjugate(b)*z)`.

The conjugation and the placement of `lambda` were checked visually.
Under the target normalization, `b=0` and then `lambda=1`. Thus the
source resolves both the value and uniqueness, not merely a lower bound.
The general meromorphic equality family may have poles; the normalized
target specialization is holomorphic and has no pole.

Public archive: <https://www.numdam.org/item/ASENS_1941_3_58__179_0/>.
Primary PDF: <https://numdam.org/item/10.24033/asens.889.pdf>.

## 3. Covering area, image area and the full-sphere endpoint

The distinction between covering area and image-set area is essential.
For a holomorphic injective map the real Jacobian is `|f'|^2`, so the
pullback integral counts each image point exactly once. Consequently the
classical covering-area hypothesis is the requested image-area quantity
for every admissible function.

Without injectivity this identification fails. The added exact controls
use `z^m` for `m=2,3,4`: its image is the same unit disk, but its covering
area is `m` times the disk's area. This is a countercontrol against silently
using image area in the general meromorphic lemma.

Every injective planar image has spherical area at most `4*pi`; an
unbounded image can have exactly that area, since a omitted set may have
zero area. The proof handles `A=4*pi` separately and never divides by
`1-A/(4*pi)` at that endpoint. When `A<4*pi`, normalization gives
`1 <= s0/(1-s0)`, hence `s0>=1/2`. The identity attains equality.

## 4. Independent audit of the geometric derivation

The candidate also proves the required univalent specialization directly.
Fix `0<r<1`. A slightly larger closed disk remains inside the domain of
holomorphy and injectivity. Hence `f(rD)` has a smooth Jordan boundary,
`f'` does not vanish there, and the compact image of the closed disk is
bounded. This validates all length and area formulas and ensures
`0<A(r)<4*pi` at every radius where the differential argument is used.

For `q=|f'|/(1+|f|^2)`,

`A'(r)=4*r*integral(q^2 dt)`,
`L(r)=2*r*integral(q dt)`.

Cauchy--Schwarz yields `L(r)^2 <= 2*pi*r*A'(r)`. The general spherical
isoperimetric theorem yields `A(r)*(4*pi-A(r)) <= L(r)^2`. The direction
of both inequalities is correct. With `a=A/(4*pi)`, they give

`r*a' >= 2*a*(1-a)`.

Therefore `Q=a/(r^2*(1-a))` is nondecreasing. Since `q(0)=1`, continuity
of the density gives `a(r)=r^2+o(r^2)` and `Q(r)->1` at the origin.
Rearranging `Q>=1` gives `A(r)>=4*pi*r^2/(1+r^2)`.

As `r` increases to one, the image domains increase to `f(D)` exactly.
Continuity from below of a finite spherical measure supplies the boundary
limit. No global boundary parametrization, finite Euclidean area,
rectifiable limiting boundary, or extension to the unit circle is used.
This handles slit domains and other irregular boundary behavior.

The isoperimetric theorem is a standard geometric dependency, not a claim
that finite algebraic tests prove an analytic theorem. As a modern
crosscheck, Kourou and Roth's equation (2.10), printed page 1788, explicitly
applies to a smooth simply connected spherical domain. I inspected its
rendering and the metric definition on printed page 1781. Their metric
has curvature four, so `L_unit=2*L_paper` and `A_unit=4*A_paper`; the
converted inequality is exactly the one above. Their separate
convexity-dependent function theorems are not used.

Crosscheck: <https://doi.org/10.4153/S0008414X22000529>.

## 5. Equality, rotations and possible normalization escapes

Assume the global area equals `2*pi`. Then the two endpoint limits of
the nondecreasing `Q` are both one. Thus it is identically one on the
open interval, giving the exact identity-model area for every inner disk.
The upper and lower bounds surrounding `L(r)^2` now coincide. In
particular, equality in Cauchy--Schwarz makes the continuous function
`q(r*exp(i*t))` constant in `t` for each `r`.

If `f` differs from the identity, analyticity supplies a least nonzero
coefficient `c` of order `n>=2`. Its contribution to `|f'|` appears at
order `r^(n-1)`, whereas the first angular contribution to `|f|^2` appears
at order `r^(n+1)`. The leading angular contribution to `q` is therefore
`n*r^(n-1)*Re(c*exp(i*(n-1)*t))`. The uniform remainder is `O(r^n)`;
the potentially troublesome quadratic derivative error satisfies
`2*n-2>=n`, including `n=2`. Opposite phases of the leading harmonic
contradict circular constancy for sufficiently small `r`.

This validates the candidate's independent uniqueness proof without
requiring a fresh classification of equality in spherical isoperimetry.
The added symbolic controls verify the corresponding leading term in
`q^2` for orders two through ten, while the written argument applies to
every integer order, not just the tested ones.

Spherical rotations do not produce additional normalized minimizers.
The source equality formula forces the value at zero first and the full
complex derivative second. If the latter requirement were weakened to
`|f'(0)|=1`, ordinary rotations would remain; that is a different class.
The candidate correctly distinguishes these statements.

## 6. Secondary-family controls and rejected shortcuts

The normalized Mobius family is holomorphic and univalent for `|c|<=1`,
including its boundary-pole endpoint. Solving for its inverse yields
`(1-|c|^2)|w|^2-2*Re(c*w)<1`. For general complex `c=p+i*q`, the
stereographic plane normal is `(-2*p,2*q,2-|c|^2)`, of squared norm
`4+|c|^4`, with offset `|c|^2`. The cap area in the candidate has the
correct sign and includes more than a hemisphere for every nonzero `c`.

This family excludes no other univalent maps by itself; the candidate
does not misuse it as a universal proof. Likewise, the Koebe-quarter
inclusion gives only `4*pi/17`, and a Euclidean area lower bound cannot
simply be multiplied by a variable decreasing spherical density. The
candidate identifies both limitations correctly.

## 7. Replays, independent controls and artifact integrity

- The original verifier passed all eight self-manifested file entries.
- An independent exhaustive file inventory also checked the ninth file,
  the manifest itself, against the freeze receipt.
- All 46 original exact checks and six algebraic mutation rejections
  passed in a separate replay copy. The generated `EXACT_RESULTS.json`
  matched its frozen counterpart byte-for-byte.
- The independently written `independent_controls.py` passed 42 exact
  checks and rejected eight deliberately false algebraic variants.
- Four separate file-binding mutation tests were rejected: changed proof
  bytes, a missing file, an extra file inside `__pycache__`, and a symbolic
  link. These mutations were applied only to temporary copies.
- Added coverage includes arbitrary sphere radius and initial derivative,
  source metric conversion, complex Mobius geometry, exact spherical
  rotation identities, higher leading angular modes, and explicit
  multivalent covering/image counterexamples.

These controls are exact symbolic regression checks and falsification
controls, not proof-assistant formalization or whole-proof mutation
testing. The analytic limits, topology of inner images and standard
isoperimetry were assessed in the mathematical review above.

The separate `verify_frozen_binding.py` checks the exact frozen file set
and all nine hashes, refuses symbolic links, and makes no writes. The
original verifier ignores files under `__pycache__`; the independent
inventory does not, so that implementation choice leaves no unchecked
extra file in this audited snapshot.

## 8. Findings, limits and release recommendation

There are no required corrections to the frozen mathematical proof.
The three substantive approaches suffice because a full proof and a
verified classical antecedent have been reached; adding two inconclusive
routes would not strengthen the result.

The release should identify a classical consequence resolving the exact
stated target, retain both numerical conventions, and retain the explicit
absence of novelty. Do not describe the historical editorial update as a
verified present open status. Classification as `already_solved = 1` is
supported by the source theorem and exact specialization.

The complete 82-page Dufresnoy paper and the general theory of covering
surfaces were not audited globally. The standard isoperimetric theorem
was not re-proved from foundations. The Yamashita corroboration is not
needed. Repository search history and corpus metadata were inspected as
metadata in the frozen package, not independently replayed against live
repositories or full corpora during this mathematical audit. Those
limits are already non-load-bearing and do not affect the deduction.

This audit's safe files contain authored mathematical assessment, code,
results, hashes, source titles and public URLs only. No source PDF/text,
dataset contents, private sources, or private coordination records are
included. No remote writes were made in this review.
