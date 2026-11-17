# Private independent adversarial review: record 23204212

Date: 2026-11-17 UTC. Original-first INITIAL remains immutable.
Disposition for root consideration: **PASS, bounded manual scientific review**.
No material defect or unresolved central written inference was identified in
the consumed proof chain. This is not publication authority, a fresh formal
certificate, a first-priority finding, or human refereeing. Root alone handles
catalogue disposition. Follow-up: null.

The authorized continuation is complete at sealing (100%). Best estimate of
complete independently reproducible verification is 95%; a fresh Lean kernel
build was not performed. The written proof was checked directly and does not
need that build to fill an omitted mathematical argument.

## Precisely reviewed claim

The original note applies the nonamenability theorem for the standard dyadic
PL Thompson F to the established Le Boudec--Matte Bon reductions, then the
discrete-group trace theorem of Breuillard--Kalantar--Kennedy--Ozawa. For each
of F, T, full abstract Aut(F) and full abstract Comm(F), all given the discrete
topology, the reduced group algebra is simple and has its coefficient-at-identity
trace as its only tracial state. The countable subgroup-of-Homeo(S^1) consequence
requires containment of the specified standard circle action of F. Arbitrary
abstract embeddings and arbitrary topological-group C*-algebras are excluded.

The original note expressly attributes the new nonamenability input to OpenAI,
attributes the reductions to the older sources, and keeps the same dependency
on validity of the new input. It does not prove the nonamenability theorem
inside its four pages. The present review therefore checked the actual imported
proof rather than accepting that attribution as evidence of truth.

## Central imported proof: actual bodies and reconstruction

The actual 13-page pinned OpenAI PDF was fetched from commit
adc7f1241b42e322a6451854ab7e4b4c146bf78a, authenticated against the exact
pinned directory's byte count and Git-blob identity, extracted and read in full.
Its SHA256 is a474b04a7e94e172d4260fc42c3643f1f9a4924d7383e12448f4ba8d636175e5.
The complete hand reconstruction and attempted failure cases are recorded in
INDEPENDENT_RECONSTRUCTION.md, written before packaged agent_notes scientific
opinions were opened; those opinions remain unopened.

The proof uses a fixed-point-free Lipschitz map of an infinite-dimensional real
Hilbert ball with uniform positive displacement, a recursively defined color of
actual finite dyadic partitions, and finitely many actual affine pair transports
in standard F. It then derives a uniform positive boundary ratio for one fixed
finite translation set. I checked the following central inferences explicitly:

- The induction parameter is the actual number of partition cells. Restriction
  to an internal parent removes at least one outside cell and hence strictly
  decreases it. The recursion is total with zero outside its valid branch.
- A single sufficiently fine uniform partition level works for the finite set
  A union SA. Slopes and offsets are dyadic and finite in number for each g;
  the selected level may depend on A. S is chosen earlier and never depends on
  A. No level uniform over the whole group is asserted or required.
- The normalized restriction covariance uses actual affine transport on the
  selected interval and admissibility at both g and hg. No transport is assumed
  to preserve the other chosen intervals. Group multiplication is h*g=h composed
  with g, matching the left-translation boundary convention.
- The scalar correlations are globally defined and bounded in [-1,1], so finite
  cancellation on hA intersection A works for the function selected at the
  level n(A). This avoids a forbidden exchange between limits and a mean.
- The parent/sibling expansions have D diagonal and D(D-1) separated ordered
  terms. The mixed sum has exactly D uncontrolled nested terms and D(D-1)
  separated ones. Signed alpha cancels; no positivity of the common correlation
  is used. Fresh pixels of upstream pages6 and7 confirmed the formulas and
  schematic figure after extraction.
- All averages use 1/D, and quadratic expansions use 1/D^2. Full symmetric
  difference is used, with both residual pieces counted. The resulting bound is
  eta >= (delta^2/L^2-4/D)/(4(1-1/D)); D>=2 and D>4L^2/delta^2 make every
  rearranged denominator and the final numerator positive. For delta=1/2 the
  sufficient branching condition is D>16L^2. No finite test at small D certifies
  this analytic choice.
- Jensen is applied to the mean of f(z_i)-f(m), using x_i=f(z_i), rather than
  silently replacing f of a mean by the mean of f. This is the necessary
  nonlinear step, and its displayed use is valid.

I also checked the actual analytic appendix instead of treating a theorem
headline or geometric certificate as proof. The oscillator lives in actual
L2 of restricted Lebesgue measure of mass one with a Euclidean R^2 fiber.
Its parameter derivative contains w, and integration yields the speed factor
1/3 from the integral of w^2. The angular parameter is in radians; no missing
2*pi normalization is introduced. Uniform trigonometric remainders justify
L2 differentiation, including the piecewise scalar-profile junctions.

The proof establishes uniform separation of the entire bounded positive tail,
not merely injectivity. Its nearest-point argument minimizes over a compact
real parameter interval supplied by that separation; it does not assume compact
balls in infinite-dimensional Hilbert space. Orthogonality is derived at an
attained minimum, and the nearby-parameter estimate supplies uniqueness. The
rank-two rotation is defined by a denominator 1+<u,v>>=1 and covers u=v without
a singular choice of a two-plane. The lower bound for the correction G handles
all four cutoff regions and the tube exterior. Its global Lipschitz estimate
includes the actual open-tube boundary. Only after ||G||>=rho/4 is proved is
normalization performed. The outer-annulus identity and reverse triangle
inequality then give displacement at least1/2. Boundary values r=rho/4,rho/2,rho,
t=1,2,3 and norm x=1/2 were included in the hand checks.

These steps provide a written proof, rather than shifting the central task to
an unsupported analytic certificate. The cited Benyamini--Sternfeld existence
theorem is not an unfilled central gap here because the actual appendix gives
and proves the concrete Hilbert-space instance used.

As a dimensional control, a bounded uniformly separated infinite sequence
cannot occur in a finite-dimensional Hilbert ball, by total boundedness. The
actual L2 space is infinite-dimensional: the integer-frequency sine/cosine
pairs give infinitely many mutually orthogonal unit vectors. Thus the bounded
oscillating tail uses the intended infinite-dimensional setting and does not
silently claim a fixed-point-free map of a finite-dimensional compact ball.

## Actual Lean semantics and limits

All68 actual Thompson Lean files, totaling9457 lines /372798 bytes, were
personally read completely. PRIMARY_COVERAGE.json records their exact hashes,
imports and actual Main-reachable internal closure, also68 files. Every file
matches its pinned GitHub directory byte count/Git-blob SHA1 and the deposited
author hash manifest independently. This match authenticates edition identity;
it is not used as a proof of correctness.

The formal carrier F is a subtype of actual increasing interval homeomorphisms
with an existential finite strictly ordered dyadic PL witness. A chosen witness
does not add data to group-element identity. Coverage follows from endpoints;
there is no extra uniform-grid, free-action, transport or expansion assumption
hidden in the definition. The group operation is actual function composition.
StandardCharacterization supplies the ordinary PL carrier equivalence, and
StandardF supplies the compatible multiplication formula.

The mean's domain is lp-infinity of all bounded real functions on the group,
not finitely supported functions or a smaller test algebra. Positivity,
normalization and left invariance are its defining fields; norm continuity is
derived. MeanApproximation uses separation of a convex finite-probability
defect set in actual l1 on S times G; FiniteCoarea uses exact finite scalar
level sets to obtain a nonempty finite Folner set. No countability or finite
generation is silently added in that mean-to-Folner bridge.

The formal analytic carrier uses measure-theoretic Lp with exponent2, distinct
from the discrete lp-infinity mean domain. Actual representatives are used only
through a.e. identities. RegularCurveData and CorrectionData are intermediate
structures whose geometric fields are concretely instantiated and proved in
AnalyticConstruction; the final theorem does not take one of these certificates
as a hypothesis. Main proves its boundary theorem and negates Nonempty of the
defined invariant-mean structure without a remaining nonamenability premise.

I found no actual local axiom/sorry/admit proof hole in these68 files. The
literal lexical scan has one `admit` hit in the English documentation sentence
about positive dyadic gaps admitting equal-length chains; it is not a Lean
admission. Manual source reading, not that scan count, supports this statement.

The actual fetched toolchain pins Lean4.34.1 and the actual lake file/manifest
pins Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612. I read their saved
contents. The shared lake configuration has unrelated dependency provisioning
and compatibility-patch actions, so loading/building it would not be a passive
operation. No Lean/Lake command, import, compiler or kernel build was executed.
Only5.7GiB available disk was observed, and no dependency installation or
interpreter/toolchain switch was attempted. I do not claim that all external
Mathlib/kernel proof bodies were reread or freshly validated. Fresh formal
reproduction remains a limit, not an identified written-proof defect and not
an asserted formalization of the C*-algebra follow-on note.

## Classical consequence interfaces

The actual arXiv1605.01651v3 LMB PDF (2016-12-23 version, separate from the
2018 journal citation) was retained. I read Theorem3.7, the complete supporting
Theorem3.5/Proposition3.8 proof and its lemmas, and Theorems4.1/4.3 plus
Corollaries4.2/4.4 and their proof bodies. The rigid-stabilizer criterion requires
a countable faithful group of homeomorphisms of a Hausdorff space and
nonamenability of every nonempty open set's rigid stabilizer. It does not
add minimality, extreme proximality or orientation preservation. A circle or
line open set contains a proper local dyadic copy of standard F, supplying the
rigid stabilizer hypothesis from N. Faithfulness is supplied by subgroup
containment in the actual homeomorphism group.

The source's Corollary4.4 uses unqualified full Aut(F) and abstract Comm(F).
To check the orientation interface directly, I additionally read Brin's actual
published definitions, Theorem1 and its part(i) proof via Theorem2.3, and the
actual BCR arXiv0711.0919v2 definitions and full Theorem3.1 proof. Brin explicitly
distinguishes N(F) from its index-two orientation-preserving subgroup N+(F).
His normalizer-to-Aut(F) isomorphism uses all self-homeomorphisms of R. BCR
constructs an injective commensurator-to-Homeo(R) homomorphism by uniqueness of
the conjugating homeomorphism, treating orientation reversal explicitly. Thus
the faithful line-action interface is not established by quietly replacing the
full abstract groups with their positive subgroups. Some text extractions lose
bars over the extended PL-group notation; the explicit index-two distinctions
and unrestricted Homeo(R) formulation fix the meaning needed here.

For the reverse Comm(F) equivalence, the 2013 BCR addendum was read completely.
Its corrected structure has F' normal in K, K normal in Comm+(F), and Comm+(F)
normal of index two in Comm(F). This is the required subnormality, and I do
not rely on the older original paper's different unused structural sequence.
BKKO's actual published Theorem1.4 proof of normal-subgroup inheritance was
also read. This supplies the inheritance used in LMB's reverse direction.

The actual published BKKO PDF, pages35-71, was retained. I read the actual
Theorem4.1 vanishing proof, Corollary4.3 proof and needed boundary-kernel,
injectivity and rigidity propositions. Fresh pixels of printed page49 confirmed
the non-equalities dropped by text extraction. In the proof, a trace extends
to the boundary crossed product, rigidity fixes the boundary algebra, and the
multiplicative-domain identity forces its constant coefficient for a moving
element to vanish. Its statement applies to discrete groups and reduced GROUP
algebras. The final norm-density passage to uniqueness is explicitly proved in
INITIAL.md. The converse trace construction can use the conjugation-invariant
unit character of the amenable normal subgroup; no arbitrary non-invariant
trace extension is needed. Established Furstenberg/Rubin/standard operator
algebra results appearing in these classical proofs are treated as classical
inputs, not new independent research claims.

Finite generation is now checked against the actual CFP primary article:
Theorem2.5 and its complete induction, with fresh personally viewed printed
pages223-224 including the tree rotation figure, imply Corollary2.6 that F is
generated by A,B. Each X_n is a conjugate of B by a power of A. The elementary
Aut/Comm countability reconstruction in INITIAL.md therefore has its finite
generation interface discharged. Full Aut and Comm remain countable despite
including their orientation-reversing coset.

The independent initial controls continue to apply: H times a central C2
refutes an arbitrary-abstract-overgroup transfer rule, but its extra central
factor cannot act faithfully while centralizing the specified local F action.
The full group algebra augmentation kernel is explicitly nonzero for every
nontrivial target group. Endpoint slopes give a nontrivial proper normal kernel
inside F, so group simplicity is not confused with reduced-algebra simplicity.
Trivial and finite group controls do not satisfy the new nonamenability premise.

## One native route and its exact role

After personally reading all7192 bytes of the native finite checker and all
its called project functions, I ran exactly once:
`python3 upstream_finite_checks.py`, from the fresh native-once directory.
No upstream Lean or additional local project module was imported or executed
by this route. Its original
MIT license is retained alongside the unmodified program. NATIVE_RECEIPT.json
and the literal stdout/stderr files retain command, cwd, start/end UTC,
elapsed2.1838160420011263s, exit0 and complete matching copied-input guards.
Stdout reports1969 transports,31504 covariance cells,17 recursion identities,
and one1024-cell image enumeration at level10. Stderr is empty.

This checker uses exact rational endpoints and a bounded scalar Lipschitz
color with a fixed point. Its dyadic family uses a smaller allowed grid depth
than the formal implementation's depth2D. It corroborates finite geometry,
covariance and restriction recursion on those instances. It does not evaluate
the actual infinite-dimensional displacement map, certify a uniform theorem
over F, or replace any written/Lean proof body. No further native route,
analytic numerical control, retry, repair, source modification, install or
formal build was undertaken.

## Exact limitations, custody and stop

No central written proof gap remains identified after the checks above.
Remaining limits are fresh kernel/dependency reproduction, ordinary trust in
the stated classical background results, and the inherent fallibility of manual
review. I did not repeat a priority search, endorse an author audit opinion,
audit unrelated OpenAI companion consequences, or obtain conventional human
refereeing. No general firstness or formal-validation claim follows.

The native record has no API version field; the host's v1 label is separate.
Native record rights are CC BY4.0. The finite checker has its separately retained
MIT license, and the acquired upstream Lean project has its separately retained
Apache2.0 license. Other primary PDFs retain their original bytes and notices;
no blanket relabeling or publication of third-party material is authorized.

The complete protected source55/14 and old INITIAL18/0 receive exact before/after
guards including all bytes, modes, hidden/empty topology and recorded timestamps.
Only this new sibling was written. The final finite manifest includes every
actual owned object, with precisely its already-created terminal manifest/seal
pair excluded from recursive CONTENT hashing. All other files are hashed; root
and child directories are frozen0555 and files0444. No source, Git, W, Sheet,
Zenodo, release, deployment or external-contact action was taken. Stop after
the final freeze. Root handles adoption and any subsequent disposition.
