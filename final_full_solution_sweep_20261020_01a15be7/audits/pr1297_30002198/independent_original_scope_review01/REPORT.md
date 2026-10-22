# PR1297 / problem 30002198 — independent original-scope adjudication

**Verdict: valid literal scope correction; not a resolution of the intended
absolutely irreducible Yetter–Drinfeld conjecture. No complete-solution
publication row is proposed.**

The standard Cartan A3 counterexample and its universal polynomial
obstruction are correct. The frozen PR already states the essential
limitation clearly; this review finds no mathematical overclaim in that
qualified manuscript. The exact remaining obstacle is that its defining
module is a direct sum of three nonzero Yetter–Drinfeld submodules.

## Original statement and intended scope

The official [OWR report](https://ems.press/content/serial-article-files/46419?nt=1),
printed pp.2901–2902, was independently downloaded, extracted, and the
two pages visually read. Lochmann's contribution puts its classification
and factorization discussion in the setting of indecomposable racks and
explicitly requires an absolutely irreducible module and support-generated
group in its labeled conjecture. Its closing sentence is literally
unrestricted: it does not repeat those conditions. That textual fact
should be preserved, not rewritten as an explicitly qualified sentence.

[Vendramin's 2014 notes](https://leandrovendramin.org/notes/rauischholzhausen2014.pdf),
p.6, Conjecture 4.4, explicitly require absolute simplicity for the
degree-1/2 factorization and attribute the conjecture to the October 2012
meeting. Definition 5.2 on p.7 clarifies simplicity after every field
extension. This coauthor's formulation supports the contextual intended
reading. It is not a hypothesis invented to evade the counterexample.

There are consequently two precise adjudications:

| Target | Result |
| --- | --- |
| Standalone cached universal statement, or isolated closing sentence, covering every finite-dimensional Nichols algebra | Fully disproved by the displayed example. |
| Historical conjecture with absolute irreducibility in its stated surrounding setting | This example is outside the class and establishes no proof or counterexample. |

The first result is not grounds to mark the second solved. Conversely,
the contextual restriction does not erase the genuine counterexample to
the literal standalone text. This review recommends retaining the PR as
a scope correction and recording the original-scope failure explicitly.
The intended conjecture's current open/closed status is not determined.
No nonabelian-group hypothesis or other unstated restriction is needed
for this decision: failure of the explicit simplicity condition suffices.

The read-only original cache record binds to the compact catalog through
statement SHA-256
`01b3d81ece1aa18419f6916a72891b9fdb6153ddcccb5e34b9f1d81568d6b104`.
The corpus's broad formulation is therefore a verified input, not a
reconstruction based on the PR's description.

## Mathematical finding

The complete independently written [argument](UNIVERSAL_ARGUMENT.md)
checks the braiding, group realization, theorem assumptions, ordinary
grading, finite dimension, and obstruction. The primary PBW theorem
applies at a fifth root; no prime-larger-than-seven classification
restriction belongs to this theorem. It supplies six root vectors with
degrees 1,1,1,2,2,3 and exponents zero through four. Hence

\[
H(t)=(5)_t^3(5)_{t^2}^2(5)_{t^3}
     =\Phi_5(t)^6\Phi_{10}(t)^2\Phi_{15}(t),
\quad H(1)=15625,\quad\deg H=40.
\]

Every permitted factor contributing Φ15 contributes Φ3, but H has no Φ3.
The proof excludes arbitrarily many factors of arbitrary positive integer
length, including harmless unit factors. It is a universal argument,
not a bounded computational search. The group support generates the
chosen group of order 125, while each coordinate line remains a proper
submodule and subcomodule. Diagram connectedness does not repair this.

No blocking defect was found in the PR's qualified mathematical claim.
Minor index and dimension slips in the cited primary proof are identified
and explicitly repaired in the independent argument. These are source
proof-reading corrections, not a new theorem or an enlargement of the PR.

## Verification, prior attribution, and limits

The newly authored exact checker runs without third-party libraries or
downloaded programs. Its three outputs are byte-identical. Checks include
all 15,625 bounded PBW exponent tuples, all 46,875 character identities,
the A3 root orbit, full polynomial factorization, and exact quantum
symmetrizer ranks 8,17,33 over Q(ζ5) in degrees two through four. All
fifteen mathematical controls pass in every mode, for 45 control passes.
The finite checks do not mechanically certify the imported PBW theorem
or resolve historical source interpretation.

The algebra and PBW formula belong to established work of
Andruskiewitsch–Schneider, [2001 v1](https://arxiv.org/abs/math/0110136v1),
published in 2002; the [actual book chapter PDF](https://library.slmath.org/books/Book43/files/andrus.pdf)
was also retrieved and its essential proof read. Cambridge authenticates
chapter DOI [10.1017/9781009701396.002](https://doi.org/10.1017/9781009701396.002).
The later [Andruskiewitsch–Angiono survey](https://arxiv.org/abs/1707.08387v1)
corroborates the root/PBW data; its journal identity is
[10.1007/s13373-017-0113-x](https://doi.org/10.1007/s13373-017-0113-x).
These are dependencies for the literal negative, not authenticated
solutions of the intended conjecture. No novelty claim is supported.
The 2001 and 2002 items are versions of one work; the 2017 preprint and
journal article form another family. The OWR DOI identifies the original
report, not a solution publication.

Before substantive mathematics, a new read-only numeric-gid duplicate
query returned 191 nonempty response rows, with no target, Nichols,
Yetter–Drinfeld, or source-family alias match. A subsequent alias pass
also checked the authenticated chapter and journal DOIs in that same
fresh snapshot. Local catalog/queue and packet searches found the
existing target and source references, not an independently authenticated
publication resolving the intended conjecture. This is bounded duplicate
and provenance evidence, not a comprehensive current-status or priority
proof. No existing-paper row or new-publication row is warranted for
full original-target coverage on this evidence.

## Exact inputs and read scope

The full PR body and all eight added files were read at immutable head
`a3082b458bb4bfb55b4efcb0bda98e4c137ab9a9`, compared against base
`5c5d4c9d7a2ea547fdf8a35cf874f604cec27bed`. All eight Git blob identities
and all seven payload entries of its nested manifest match. No QUEUE
path occurs. The historical candidate/checker/raw receipts behind the PR
were not supplied in its eight-file payload; this review neither executes
nor claims to reproduce them. Its finite checks and receipts are new.

The own source packet retains five independently downloaded PDFs:
OWR, Vendramin 2014, the 2001 preprint, the actual 2002 chapter, and the
2017 v1 survey. Relevant full contribution and essential proof locations
were read; none of the 182-page survey or whole workshop is claimed as
fully audited. Source-read locations and authenticating metadata are
listed in SOURCE_READ_SCOPE.json and PRIOR_ALIASES.json. Springer
metadata/introduction and Cambridge metadata were accessed; no uninspected
publisher text is passed off as a full body review. All third-party texts,
ledger data, and full PR copies remain in the ignored private directory.

This is an AI-assisted independent audit packet. It makes no external
publication, merge, readiness, current-status, or novelty decision. It
does not change the original catalog or any shared state. All nine earlier
own review seals, including completed PR1296, are independently rechecked
without modification. The closing directory seal covers every own file,
including the retained PR's nested MANIFEST.json, and excludes only the
exact closing seal itself.
