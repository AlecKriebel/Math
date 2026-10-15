# PR164 independent direct-cochain adversarial review

The candidate's ordinary graded Lie answer is supported for the source's
specified nontrivial module, over every characteristic-two field. No
mathematical contradiction was found. This verdict is scoped to the precise
bracket claim, not novelty, priority, a full restricted/strict Gerstenhaber
presentation, or any publication authorization.

The authenticated manuscript is PROOF.md, SHA256
439bb5ac541dcc7cb0e6fbf5b30a22501f23f330b4f970fe641fb54234bd46be, at original
PR head 7c8acab3ff84c6c8caadec8998296936a156e0bd. The original source record
and source manifest were read, and the original file manifest was the
provenance anchor. The literal claimed-solved score 2/5 is inherited frozen
case metadata, not a mathematical validation score assigned by this family.

## Independent mechanism and initial seal

The family reconstructed multiplication on f,x,y,xy,e,m,xm and used the
normalized E-relative Hochschild complex. It did not start from the printed
Poisson expression or from another family's image calculation. Its decisive
mechanism is the explicit mixed module-bar complex. The coefficient
subcomplex for I=BeB is K in degree zero followed by shifted module-bar
cochains, with c↦c Id_M at the first boundary. The connecting cochain is
theta(f)(a₁,…,a_n,m)=f(a₁,…,a_n)m. Comparison of the y-periodic resolution
of M with the module bar evaluates theta on [y|…|y]⊗1, proving in all
degrees that the characteristic map kills u and y and sends v to eta.

Consequently gamma is injective, its positive-degree image is (y,u)R, and
its degree-zero image is K+yA. The full argument, including bar projectivity,
coordinates, every-degree comparison, actual original gamma, insertion
preservation and arbitrary-field extension, is in UNIVERSAL_DERIVATION.md.
This route does not transfer the central image problem to an unsupported
equivalent assertion: it gives the actual connecting cochain and evaluates
a stated chain comparison.

FIRST_ASSESSMENT.md and FIRST_ASSESSMENT_SEAL.json were sealed at
2026-10-12T08:18:41.125687+00:00, mode 0444. At that point this family had
read no supplied verify.py, verification.json, README, research logs,
independent_review material, or root/sibling conclusion. The seal hashes the
then-fixed independent source and primary receipt. Initial mathematical
evidence already contained the cohomology, image/boundary checks and actual
insertions below. The seal has not been revised.

## Actual cochains, brackets and cup products

The independent exact binary elimination gives:

| Degree | Cochain dimension | Differential rank | Cocycle dimension | Boundary dimension | HH dimension |
|---:|---:|---:|---:|---:|---:|
| 0 | 5 | 2 | 3 | 0 | 3 |
| 1 | 16 | 8 | 8 | 2 | 6 |
| 2 | 48 | 30 | 18 | 8 | 10 |
| 3 | 144 | 100 | 44 | 30 | 14 |
| 4 | 432 | 314 | 118 | 100 | 18 |

In each tested degree, every actual cocycle has its shuffle coordinate in
the claimed image. Every allowed coordinate has an actual cocycle lift.
Every zero-coordinate cocycle is reduced to an actual boundary, with no
dimension-only inference. The extended receipt exports the exact cocycle
bit vectors and their documented basis order for independent replay.

The primary code calculates actual normalized insertion on these cocycles,
not the candidate bracket applied to itself. It checks 618 basis pairs
with left degrees 0–3 and right degrees 0–2, apart from degree-zero versus
degree-zero, and 345 actual cup pairs with total degree at most 3. Each
actual bracket is checked to be a cocycle before its shuffle coordinates
are compared. Actual cochain brackets include:

| Left | Right | Actual class |
|---|---|---|
| u²v | y | u² |
| u³ | xy | yu² |
| xuv² | u | uv² |
| xuv² | yv | 0 |
| xuv | y | xu |
| xuv | yv² | xuv² |
| xu³ | xyv² | xyu²v² |

These include degree-three versus degree-two and degree-zero interactions.
The shuffle boundary identity is independently checked through degree nine.
The derivative-cup representatives' all-degree shuffle evaluation is also
proved combinatorially in the universal derivation, so no divided-power,
factorial or unrecorded coordinate normalization is used.

There are 96 further actual insertion checks over
F₄=F₂[alpha]/(alpha²+alpha+1), using non-prime-field coefficients. They
agree. Universal validity over arbitrary K comes from the all-degree
construction and flat scalar extension, not from these finite samples.

## Characteristic-two boundary and source module

The ordinary shifted graded Lie bracket is symmetric in characteristic two
and alternating. A zero self bracket does not imply zero squaring. Actual
degree-one insertion gives (xu)^[2]=xu and (yv)^[2]=yv; actual even-degree
divided squares give sq(xuv)=xuv² and sq(yuv)=yu²v. The manuscript explicitly
excludes a complete answer for these extra structures. Its ordinary bracket
answer is therefore not falsified by them, but describing this artifact as
a full restricted or strict Gerstenhaber computation would overstate it.

The [original OWR question](https://ems.press/content/serial-article-files/46571?nt=1),
printed p.1363, Question 5, confirms the target bracket and coefficient
sequence. [Hermann v2](https://arxiv.org/pdf/1411.0836v2), printed p.45,
Section 9.6 and Lemma 9.7, and [Xu](https://arxiv.org/pdf/0805.3295), printed
p.15, Section 3.1, confirm the two-arrow permutation action. g interchanges
the arrows and h fixes them, yielding M=A/(y) after x=g−1, y=h−1 and the
documented opposite-side convention. The downloaded primary PDFs have
exactly the three hashes recorded in the immutable source manifest. Their
bodies stay in private/; only locators and metadata are allowlisted.

The trivial-module substitution is not harmless. It produces a degree-zero
cohomology dimension of four instead of three in the independent model and
is rejected by the negative control. The degree-zero exception and the
source's module convention have therefore been checked independently.

## Fail-closed validation and remaining limitations

Both independent programs run successfully in ordinary and optimized modes.
They use explicit exception gates rather than assertions. Negative controls
exit with code 1 and status FAIL in both modes:

| Mutation | Rejection |
|---|---|
| Make the x action on M trivial | HH⁰ dimension is 4, expected 3 |
| Delete the right Hochschild boundary term | HH⁰ dimension is 1, expected 3 |
| Delete the final insertion slot | [y,yv] disagrees with actual expected y |
| Delete the final insertion slot only in outer arity ≥2 | The computed bracket is not a cocycle |

The last mutation leaves degree-one insertion intact and still fails on the
positive-degree cochain operation. Mutation receipts do not report PASS.
The initial driver had expected a coordinate mismatch for that final
mutation; its earlier cocycle rejection was correctly recorded instead.

After the first seal, verify.py was read only as an adversarial implementation
inspection. Its gate is Python `assert`, so its validation checks disappear
under `python -O` while counters still increment. That is a reproducibility
and fail-closed validation defect in the original diagnostic implementation,
not a counterexample to the manuscript's mathematics. No supplied checker
output or supplied independent review was used to establish this family's
mathematical verdict. The root family's separate repair was not imported.

The strongest verified result is the complete ordinary graded Lie and cup
identification for the specified B, with the original coefficient gamma
injective in every degree and image K+(y,u)R. Exact remaining gaps for a
broader claim are priority/novelty research and a complete additional
squaring/brace presentation. Neither is claimed here. No external person
was contacted, and no repository/publication action was performed by this
family.

Research-project author metadata: Alec Kriebel,
[ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).
This is an automated adversarial research audit, not a claim of human peer
review or external endorsement.
