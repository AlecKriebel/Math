# Root scientific disposition: Thompson-family reduced C*-algebras

Record 23204212, inventory row 192. Review completed 17 November 2026 UTC.
**PASS within the substantive ordinary written-proof review described below.**
No material defect or unresolved central written inference was identified. This
is an automated research review, not human refereeing or a fresh formal proof
certificate. Review completion is 100% of this bounded task. Follow-up: none.

## Edition and exact conclusion

The controlling published manuscript is the four-page `paper.pdf`, 56917 bytes,
SHA256 `527ac7feb6f2c889998559122296dd8caab2def0cf7aeac00f79c1f8b0c8a978`,
DOI https://doi.org/10.5281/zenodo.23204212. Its original declared publication
date is 6 October 2026. The native API has no version field; Zenodo's displayed
`v1` is a host edition label, not an author-supplied version. The record was
created 7 October 2026 at 05:35:37.608378 UTC and updated 10 October at
21:24:52.833389 UTC. Preserve these distinctions rather than substituting the
review date or inventing a version. Native order is verification ZIP, source
ZIP, PDF. SOURCE_METADATA.json records their exact identities and rights.

All groups are discrete. Assuming the pinned nonamenability theorem for the
standard dyadic piecewise-linear Thompson group F, the reduced group
C*-algebras of F, T, full abstract Aut(F), and full abstract Comm(F) are simple
and have their canonical coefficient-at-identity traces as their unique
tracial states. The same conclusion holds for each countable subgroup of
Homeo(S¹) containing the specified standard circle action of F. The note
collects attributed consequences of existing reductions. It supplies neither
a new C*-simplicity criterion nor an independent discovery of nonamenability.

The essential dependency is OpenAI's pinned source commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`, specifically its actual 13-page
nonamenability proof. The dependent conclusions retain exactly that dependency.
Unique trace for T was already unconditional. No exclusive priority follows.

## Independent root reasoning and primary-source checks

The original-only INITIAL namespace was frozen and checkpointed before support
or primary-source continuation. Root personally read the complete native
95-line TeX, fresh four-page extracted text, all four rendered manuscript
pages and native metadata. The independent initial reconstruction checked
the countability and reduced/full-algebra controls before seeing current peer
conclusions. The later ROOT_INDEPENDENT_PRIMARY_CHECKPOINT_88.json was saved
before either current family's mathematical report was opened.

Root then read all 690 extracted lines of the complete pinned 13-page upstream
proof, including its analytic appendix and the unused companion-consequence
section. Its PDF is 354266 bytes, SHA256
`a474b04a7e94e172d4260fc42c3643f1f9a4924d7383e12448f4ba8d636175e5`.
The following actual inferences were checked independently, rather than
accepting an announcement or treating finite experiments as proof:

1. The recursive color of a finite dyadic partition is well founded because
   restriction to a proper internal parent strictly reduces its number of
   cells. The relevant averages stay in the Hilbert unit ball by convexity.
   Ordered separated interval pairs admit actual standard-F affine transports:
   split each of the three complementary dyadic gaps until the two cell counts
   agree, then map corresponding basic dyadic cells affinely.
2. The finite transport set S is chosen before the arbitrary finite group set
   A. A sufficiently fine common level n(A) works for A union SA because each
   element has finitely many dyadic pieces. Dependence of that level and of the
   bounded scalar test functions on A is legitimate in the finite cancellation
   argument. No uniform mesh over all of F or illicit invariant-mean limit is
   assumed.
3. Normalized restriction is covariant when the selected transport is affine
   on the selected interval. Both g and hg are admissible separately; h need
   not preserve all the other selected intervals. Multiplication is h after
   g, matching the left-boundary convention.
4. The separated parent and sibling correlations share a common scalar alpha
   up to the boundary error. The D diagonal or nested terms have fraction
   1/D among D² terms. In the variance expansion alpha cancels without a sign
   assumption, giving the bound 4/D + 4(1-1/D) eta. Jensen and the Lipschitz
   bound apply to f(z_i)-f(m), not an invalid assertion that f commutes with
   averaging. Uniform displacement delta then gives a positive uniform
   boundary bound when D > 4 L²/delta².
5. The analytic appendix supplies the actual infinite-dimensional map used in
   this argument. For its L²([0,1];R²) curve, speed squared is a'²+a² theta'²/3;
   the factor 1/3 is the integral of the squared coordinate. Speed is bounded
   below by 1/8. The bounded positive tail has uniform separation through the
   sinc correlation; the negative branch is straight and unbounded. This is
   stronger than injectivity and does not assume compact Hilbert balls.
6. Separation confines a near-curve minimizing sequence to a compact real
   parameter interval, so the nearest point exists. The local derivative
   projection and orthogonality prove uniqueness and the parameter Lipschitz
   bound 16. The rank-two rotation R=Id+A+A²/(1+kappa) has kappa >= 0,
   includes u=v without division by zero, and maps the tangent to the radial
   direction. The cutoff correction is globally Lipschitz, including pairs
   crossing the open tube boundary. Its norm is at least rho/4 in every cutoff
   region. Normalization is therefore legitimate. The correction equals the
   identity for norm at least 1/2, and its negative normalization displaces
   every unit-ball point by at least 1/2. Junctions t=1,2,3, tube radii
   rho/4,rho/2,rho and norm 1/2 were included. This written construction
   discharges the central analytic input without an unsupported certificate.

Root additionally read actual LMB v3 Theorem 3.7 and its supporting
Proposition 3.8/Lemma 3.9 proof, Theorems 4.1 and 4.3, Corollaries 4.2 and 4.4
with their proofs; BKKO's published Theorem 4.1 and Corollary 4.3 proofs;
Brin's definitions and Theorem 1; BCR v2 definitions, Proposition 2.1 and the
full Theorem 3.1 proof; the BCR addendum's exact subnormal chain; CFP Corollary
2.6 and Lemma 4.4 proof; and the actual published HO 5.5/5.6 discussion.
These supply the following consequence interfaces:

- Every nonempty open arc contains a smaller basic dyadic interval supporting
  an affine copy of F. Its rigid stabilizer is nonamenable, so LMB's criterion
  applies to the actual standard action. The fixed glued endpoint is harmless;
  minimality and orientation preservation are not extra hypotheses of that
  criterion.
- Brin and BCR provide faithful full Aut(F) and Comm(F) line realizations,
  including decreasing homeomorphisms. LMB's full Homeo(R) theorem applies.
  Positive-slope neighboring notation in the source does not justify replacing
  the full groups by their index-two subgroups. The unused reverse Comm
  equivalence uses F' normal in K normal in Comm+(F) normal in Comm(F), from
  the later addendum, rather than falsely asserting that F is normal in Comm.
- F and T have finite dyadic descriptions. CFP gives two generators for F,
  so automorphisms are determined by two images. Finite-index subgroups are
  countable in number, have finite generating sets by Schreier, and have only
  countably many homomorphisms to one another. Taking the commensuration
  quotient therefore gives a countable group. All LMB countability hypotheses
  are met.
- BKKO's boundary/multiplicative-domain argument forces a trace coefficient
  to vanish outside the amenable radical. A C*-simple discrete group has
  trivial radical. Norm density of its group algebra then identifies every
  tracial state with its canonical trace.
- Published HO theorem/remark 5.5/5.6 correspond to arXiv 4.5/4.6. The note's
  attribution of T's already known unique trace, including Dudko--Medynets
  credit, is faithful. The original bibliography's BCR article and the
  transitive later addendum are distinguished in the review evidence.

The full-group-algebra negative control is decisive: for any nontrivial group
the augmentation is a character, its kernel is proper and nonzero because
lambda_g-1 is nonzero in the regular representation, and its trace differs
from the pulled-back regular trace. Thus none of the reduced conclusions
silently becomes a full-algebra claim. C*-simplicity is not abstract group
simplicity. Nor does an arbitrary abstract overgroup inherit C*-simplicity:
adjoining a central C2 supplies a control and does not realize the specified
faithful local action.

## Independent families, corroboration and remaining limits

Both current families were withheld until root's original and primary
checkpoints were saved. Root then read their actual complete FINAL_REPORT.md
files, seals and the scope family's SCIENTIFIC_REVIEW.md. Both recommend PASS
within ordinary written-proof scope, with no material central gap identified.
The adversarial route explicitly tested the infinite-dimensional geometry,
all cutoff and covariance boundaries and actual formal carrier semantics;
the scope route reconstructed theorem interfaces and full-group identifications.
Their original-only gates and exposure disclosures remain separate.

Each family personally read and ran the unmodified 7192-byte documented native
finite checker once in an isolated copy. Both exited 0 in about 2.18 seconds,
with literal inputs and streams retained. The checks cover 1969 transports,
31504 covariance cells, 17 recursive identities and one 1024-cell image at
level 10. Its scalar map has a fixed point. It corroborates finite dyadic
algebra only; it certifies neither nonamenability nor analytic displacement,
C*-simplicity or a Lean kernel result. Root executed no scientific program.

The adversarial family personally read all 68 Main-reachable Lean files,
9457 lines and 372798 bytes. Root personally read Main, Model, StandardF,
StandardCharacterization, FiniteBoundary, AnalyticConstruction and MeanToFolner.
The actual formal F is the finite dyadic PL subgroup, not an abstract group
with a nonamenability or geometry axiom. The invariant mean is defined on all
bounded real group functions. The actual analytic construction instantiates
its intermediate geometric structures. The final Main theorem negates
Nonempty(InvariantMean F) without a remaining nonamenability premise.
Root does not claim to have read every Lean body. No reviewer performed a
fresh Lean/Lake/kernel build, dependency installation or compiler run; the
shared configuration has provisioning/compatibility actions. No formalization
of this C*-algebra consequence note is claimed. The complete ordinary written
proof, rather than a missing build, supplies the reviewed argument.

Established classical foundations are accepted at their checked primary
interfaces. Manual/automated reviews remain fallible. Historical assertions
about earliest repository visibility and failed priority searches were not
independently certified and must not become a new priority claim. This is
an attributed consequence note whose value is a transparent synthesis;
its page should state that plainly and preserve the upstream dependency.

Custody was freshly authenticated across 491 files and 33 child directories:
source, root INITIAL and both current continuation packets. Exact terminal
pins are in FINAL_EVIDENCE_AUTHENTICATION.json. The source55/14 is unchanged.
Both family native attempts succeeded. The scope family retained a separate
HTTP-200 HTML response at an intended PDF filename as an unusable retrieval;
a distinct valid CFP scan supplied its primary. A text-diff exit 1 records
frontmatter differences, not a scientific failure. Root's first raw-copy
selector and a dependent absent-destination check failed before copying;
both are retained, followed by a distinct explicit68-file-closure copy.
No scientific failure was repaired or concealed.

## Public disposition

Prepare a straightforward, searchable research page with the full native
abstract, original date and qualified host edition, unchanged PDF and both
native support ZIPs. Credit OpenAI, LMB, BKKO and the group-realization sources
prominently. Explain reduced algebras, standard-action containment, countability,
the upstream dependency and T's already known trace. Keep internal review
steps, counts, dates and error histories off the page. Retain AI-use disclosure,
unrefereed status and a contribution-based passive collaboration invitation.
No follow-up clears the required bar. No outreach or manuscript edit is
authorized. Website/actual UI/tracker publication checks remain separate.

Scientific inventory after this disposition: **143/203 reviewed**, comprising
135 passes and 8 deferred; 60 remain, approximately 70.44335% complete.
The native Sheet remains at 142 until its explicit later transition.
