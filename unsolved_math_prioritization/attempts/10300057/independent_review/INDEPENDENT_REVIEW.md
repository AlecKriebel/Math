# Independent review: 10300057 / Calegari Question 13.4

**Disposition: scoped partials pass after the versioned source-hypothesis correction identified below; original question remains unsolved, 5/5 author turns.**

This is a separate AI-assisted mathematical audit, not human peer review or a
novelty certification. The reviewer did not contribute to the five author
mechanisms. The review challenged their exact source scope, proofs and checks;
it did not supply a sixth author search turn or an example of the original
phenomenon.

## 1. Target and one required source correction

I independently read Calegari's complete Question 13.4 on printed p.30 of
*Problems in foliations and laminations of 3-manifolds*, and visually inspected
that page. It asks for taut foliations on a hyperbolic manifold with a geometric
isotopy-orbit limit after a finite cover but no corresponding limit downstairs.
It does not say that plane-field homotopy or contact isotopy is sufficient.
The companion norm paper's Theorem 3.1.2 explicitly uses tangent-plane
convergence. Its displayed inequality is norm(limit) >= limsup norm(sequence).
The author correctly follows that formula rather than its inconsistent nearby
semicontinuity terminology.

The initial frozen TURN_5.md abbreviated Vogel Theorem 1.4(i) as absence of
torus leaves. The published statement actually excludes **all closed leaves
of genus at most one**, including spheres. I requested that literal source
condition be restored. The hyperbolic taut subclass had already excluded
both types in the subsequent paragraph, so this is a source-hypothesis
correction, not a new proof or a change of the retained hyperbolic conclusion.
The binding corrected hashes and exact diff are recorded in REVIEW_BINDING.json.
The initial author freeze and correction history must remain available.

The source question's possible nonclosed, unoriented or lower-regularity
interpretations are not answered by imposing the extra hypotheses of the
scoped theorems. The final author status correctly remains unsolved.

## 2. Transfer and plane-field necessary conditions

The chain-level transfer argument is valid in ordinary real singular homology.
Each simplex has exactly d lifts; affine transversality is local and survives
both lifting and projection. The two chain norm inequalities and p_*Tr=d id
prove exact degree scaling for the transferred class. This argument does not
assume a minimizing chain or a regular cover. Extended infinite values cause
no exception, because projection rules out a finite representative upstairs
when the downstairs seminorm is infinite.

Identity isotopies act trivially on homology, so the upstairs semicontinuity
premise implies precisely the downstairs norm inequality, in the stated
source setting. The universal-cover leaf space is unchanged by passing to
an intermediate finite cover; ordinary branching cannot distinguish them.

For closed manifolds, uniformly close unoriented distributions are joined
by a short Grassmannian homotopy. Composing this with the ambient isotopy
proves homotopy of the lifted fields. Transfer on H^1(-; Z/2) gives the
odd-degree orientability restriction. For cooriented fields, the relative
normal lift has one global sign on connected N, and transfer gives
`d(e(F)-sigma e(G))=0`. Rational equality, torsion annihilation and integral
equality in the torsion-free case are correctly separated. The argument does
not confuse equality of Euler classes with full plane-field homotopy.

## 3. Regularization and the controlled-flow theorem

The normal core of a finite-index subgroup gives a finite regular cover.
An entire identity isotopy lifts from time zero by the covering homotopy
property. The inverse path lifts as well, so the lifted maps are
homeomorphisms/diffeomorphisms. This is sufficient even when a single
arbitrary self-map might not preserve the chosen subgroup. The displayed
naturality of pushed distributions follows from q h_tilde = h q.
Regularization does not assert equivariance under the new full deck group.

The controlled descent theorem is analytically correct under its explicit
integrated spatial C2 bound and integrated C1 deck defect tending to zero.
For a fixed invariant metric, deck averaging preserves the relevant norm
bound. Both flows exist globally on compact N. The position estimate is
Gronwall with the integrated Lipschitz coefficient; the derivative estimate
adds the term D2V times the position error. Thus its constant depends on the
uniform integral bound, rather than on a pointwise-in-time bound that was
not assumed. The variational equations give uniform first, inverse-first
and second derivative bounds. Comparing pushforwards at h^{-1}(y) and
k^{-1}(y) then uses those bounds and the modulus of continuity of the original
distribution. This proves uniform Grassmannian convergence without silently
assuming that the distribution is differentiable.

The averaged vector fields, and hence their flows, commute with every deck
map and descend along the whole isotopy. Conversely the proof never extracts
its generator assumptions from endpoint convergence. The local Pfaff-form
calculation correctly shows why averaging defining forms is insufficient;
it is not presented as a global foliation counterexample.

## 4. The torsion plane-field example

I checked the full primary classification inputs and Thurston's actual
figure-eight filling statement. Positive integral 15-surgery lies outside
the exceptional slopes. The surgery relation yields H_1=Z/15, H^1(Z)=0,
and H^2(Z)=Z/15. The Bockstein of the abelianization character is a generator;
pulling back to its connected kernel cover kills that character and hence
that generator. No computation of the cover's first Betti number is needed.

For a generator a of a cyclic nonsingular linking pairing, its self-pairing
is v/15 modulo integers with v a unit. Since 4²=1 modulo 15, the self-linking
values of links representing a and 4a differ by an integer. A framing twist
can make the rational values exactly equal. Transferring a rational bounding
chain multiplies intersections with the full lifted parallel by the degree,
so both lifted self-linking values become the same integer. The lifted primary
classes vanish; Pontryagin's primary-zero classification uses precisely that
integer even when the cover has nonzero H^1. This avoids an unjustified
rational-Hopf classification at a nonzero primary class.

The Euler classes are 2c and 8c, and these are unequal even up to sign in
Z/15. An unoriented homotopy would lift its normal line bundle on M x I,
contradicting that calculation. Hence the downstairs orbit-limit obstruction
for these plane fields is valid. Homotopic lifted fields are not asserted
to be isotopic foliations, and taut representatives are not asserted to exist.

## 5. Spin-c Floer obstruction to the proposed realization

I read Lin's nonvanishing proof in full at its decisive cap-and-pairing step.
The relative invariants use canonical Spin-c restrictions and the pairing
respects Spin-c summands. Small contact perturbations preserve the underlying
plane-field class. Therefore reduced Floer nonvanishing holds in the
foliation's summand; the conventional orientation/conjugation identifications
at the negative end do not allow a different arbitrary summand. Conjugation
symmetry in any case makes the zero-Euler conclusion below independent of
that sign convention. This is a consequence of the cited classical argument,
not an inference from the total dimension alone.

I visually checked Hendricks–Manolescu Figure 17 and read the ordinary
large-surgery statement and its effective range. The source square has its
displayed e shifted relative to the lower-left corner used in TURN_4;
the author explicitly accounts for that shift. In the quotient
`C{i>=0 or j>=s}`, a square is partial only at n=min(0,s). The two-generator
partial squares for nonzero s are acyclic. At s=0 the three-generator square
has one surviving homology class, killed by U. The isolated generator forms
a separate U-tower. Thus the extra copy of F is truly reduced, not an
extension hidden inside the tower. The proof covers every integer n,
whereas the checkers only test finite sections.

For labels -7<=s<=7, p=15 satisfies the exact sufficient surgery range
p>=g+|s|. Only s=0 has nonzero reduced homology, and the source labels it
as the spin structure. Odd-order H^2 gives its uniqueness and zero Chern
class. The coorientation obstruction H^1(M;Z/2) vanishes as claimed.
Therefore smooth cooriented taut representatives of the two nonzero Euler
classes are excluded. This does not rule out Euler-zero taut foliations or
other manifolds, and does not refute the original question.

## 6. Contact-approximation orbit and covering deductions

I visually checked the published Vogel Theorem 1.4, including the corrected
sphere condition and the plane/cylinder exceptions. Tautness gives Reeblessness;
closed torus leaves would inject Z² into the closed hyperbolic group. Reeb
stability excludes sphere leaves here. The stated classical plane-only and
cylinder-only alternatives cannot be closed hyperbolic. These facts also
hold in each finite cover.

The orbit-closure proof has the correct quantifier order: after fixing n,
choose a contact approximation sufficiently close to G that its h_n-image
lies in the uniqueness neighborhood of F. Continuity for each fixed h_n is
enough; no derivative bound uniform in n is being smuggled in. The whole
identity isotopy pushes that contact structure through contact structures.
The argument works separately for both contact signs. Coorientation reversal
leaves the contact sign unchanged and reverses the two coorientations
together. Passing to a constant-sign subsequence gives precisely the
correlated two-choice invariant, rather than four independent choices.

Pullback preserves contactness, sign, isotopy and C0 convergence. Approximations
chosen sufficiently close downstairs eventually enter the upstairs uniqueness
neighborhood, proving covering naturality. This uses no injectivity of
pullback on contact isotopy classes. Equality of contact data remains only
a necessary condition for the requested foliation orbit closure.

## 7. Reproducibility and disposition

The initial 16 author-file hashes and all nine primary PDF hashes matched.
The two author receipts replayed byte-for-byte, with 6 and 9,974 controls.
The versioned correction and final freeze are checked separately in the
binding receipt. My independently authored checker assembles entire finite
quotient complexes, computes kernels and U-power images in homology, and
checks the torsion/framing arithmetic and weighted Pfaff averages. It passes
40,570 exact assertions. It imports none of the author checker code.

These finite checks do not certify Pontryagin theory, Floer/contact theorems,
covering topology or the ODE proof; those were audited above using the pinned
sources and explicit analytic arguments. Each of the five author turns contains
a substantive deduction, including rejection of the proposed taut realization,
rather than administrative work counted as research.

After the recorded source correction, no remaining mandatory mathematical
revision is identified. The entire retained **scoped partial package** is
suitable for independent-review attribution. The original target remains
**unsolved, 5/5**, with no certified example, general descent theorem or
novelty assertion. Parent retains publication authority.
