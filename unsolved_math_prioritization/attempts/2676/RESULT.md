# KP-1.17: mixed alternation and common double-branched covers

**Problem 2676, rank 264. Original unresolved after five substantive author
turns.** This is a frozen partial-results packet for independent adversarial
review. No affirmative or negative answer to the unrestricted source question
is claimed, and no novelty or priority is certified.

## Exact original problem and edition

Can an alternating link and a nonalternating link in (S^3\) have homeomorphic
branched double covers?

The source is *K3*, the 2026 preliminary Kirby-problem book, Problem 1.17,
printed p. 26, scribed by J. Greene. Its numbering must not be identified
with the 1997 Kirby list's Problem 1.17. The source cites Greene's published
Conjecture 1.4; the accessed arXiv v1 has the same question as Conjecture 1.3.
The catalog's AIM link was only a workshop report; the full actual K3 source
was recovered and inspected. See `SOURCE_GATE.md`.

The question concerns all tame links, not just prime knots or hyperbolic
branched covers. Alternation is a property of the link type, not the displayed
diagram. An orientation-reversing cover homeomorphism can be accommodated by
reflecting one branch link, which preserves alternation. The prior-Alec and
campaign checks found no exact earlier attempt; those checks are provenance
evidence, not a novelty certificate.

## 1. Hyperbolic-cover restrictions and a failed homology-sphere route

`TURN_1.md` gives a finite-group reduction when the common closed cover is
hyperbolic. Its branch involutions can be geometrized in the finite group
of orientation-preserving isometries. Conjugate involutions have equivalent
branch links. If a branching involution is the only involution in its
centralizer, Sylow theory implies that every involution is conjugate to it;
a mixed pair is impossible in that case. Thus a mixed hyperbolic-cover pair
requires nonconjugate branching classes and a distinct commuting involution
for each branch involution. The commuting partner is not thereby known to
have quotient (S^3\).

The dihedral 2-group reduction and an explicit (D_8\) negative control keep
that distinction visible: two nonconjugate branching candidates need not have
commuting representatives just because each has a commuting partner. The
argument does not replace the global branching problem by a (V_4\) action
without proving its quotient hypotheses.

A separate determinant argument shows that an alternating link with integral
homology-sphere double cover must be the unknot, with cover (S^3\). Split
links contribute free cover homology, and a nonempty reduced alternating Tait
graph has at least two spanning trees. Consequently nontrivial integral
homology-sphere common-cover constructions, including the cited numerator-one
surgeries in Mecchia's examples, cannot supply a mixed pair. This is a
construction exclusion, not a resolution for arbitrary covers.

## 2. Definite surfaces require the actual involution

`TURN_2.md` proves integrally that every (S^3\)-link double-cover deck
involution acts by (-I\) on (H_1\). A branched Wirtinger/Schreier
presentation proves this without division by 2 and includes torsion and free
homology. The abstract action alone therefore cannot distinguish branch
descriptions.

The relevant classical positive certificate is precise: opposite definite
fillings must carry extensions of the specified branch involution, their
quotients must be standard four-balls, and their branch surfaces must be
isotopic relative to boundary to push-ins of embedded spanning surfaces in
(S^3\). Greene's definite-spanning-surface theorem then gives alternation.
Nonequivariant definite fillings or a merely algebraic lattice involution do
not supply these hypotheses.

For a concrete negative control, let (H=\Sigma_2(T(3,5))\) and (Y=H\#-H\).
The product of the punctured homology sphere with an interval is a homology
ball bounded by (Y\); interior sums with copies of (\pm\mathbb{CP}^2\)
give opposite diagonal definite fillings. Their correction-term inequalities
can achieve equality. Nevertheless (Y\neq S^3\) is an integral homology
sphere, so it has no alternating branch by Turn 1. The example has reducible
boundary and non-simply-connected fillings; these limitations are explicit.
It does not settle a stronger sharp-filling question with additional
hypotheses. Tubing a spanning surface also creates both signs in its
Gordon–Litherland form and is not a route to definiteness by itself.

## 3. Reduction to prime hyperbolic branch exteriors

`TURN_3.md` reduces any hypothetical mixed pair to one with both links prime,
nonsplit and nontrivial, and with a common irreducible rational-homology-sphere
L-space cover. It uses the connected-sum/split-union cover formulas, prime
cover irreducibility, uniqueness of three-manifold prime decomposition, and
the fact that the alternating factors can be chosen alternating.

The precise Boyer–Gordon–Hu inputs then exclude Seifert and toroidal
**exteriors of the nonalternating branch**. The Seifert-link theorem forces
an ADE case if the double cover is an L-space. Its nonalternating (D/E\)
cases have finite noncyclic covers and determinant at most 4. A complete
small-Tait-graph argument excludes an alternating description of those covers.
The degree-two toroidal theorem directly gives a non-L-space double cover
for a prime toroidal branch link. This is a proved degree-two statement, not
an invocation of the broader all-degree conjecture.

Thus both reduced branch exteriors are hyperbolic. **Their common cover has
not thereby been proved hyperbolic.**

Source editions matter: the Seifert file is arXiv:2402.15914v1 (2024), with
separately checked 2025 publication metadata; the toroidal file is
arXiv:2106.14378v5 (13 April 2026). The v1 Seifert table's odd-(D\) homology
entry is bypassed by an independent Cartan/Goeritz calculation giving order 4.
No assertion about an unaccessed published table is made. The exact source
details and access limitations are retained in the turn and source addendum.

## 4. Common-cover geometry and a concrete toroidal control

`TURN_4.md` uses the classical Seifert branching classification, already
explicit in K3's Remark (3), to exclude a Seifert **common cover** for the
reduced mixed pair. In the nonspherical case its hyperbolic-exterior branch
links must be Montesinos and are related by Conway mutations; alternation is
preserved. The spherical case has unique branching class. The remaining
common-cover sectors are therefore hyperbolic or toroidal non-Seifert.

A concrete toroidal control is obtained by gluing two right-trefoil exteriors
with meridian–longitude matrix

\[
 \begin{pmatrix}3&-5\\1&-2\end{pmatrix}.
\]

The resulting (Y_2\) is irreducible, toroidal, and an L-space with
(H_1(Y_2)=\mathbb Z/5\). The L-space gluing check treats the meridian as an
endpoint of the interior-slope complement, not as a non-L-space filling.
Standard trefoil strong inversions commute exactly with the linear gluing
map, producing an actual (S^3\) quotient and a prime hyperbolic branch knot.

Yet (Y_2\) has no alternating branch: a determinant-five alternating Tait
graph is a five-fold parallel pair, its dual five-cycle, or
(\Theta(1,1,2)\); the corresponding covers are lens spaces. An essential
torus excludes that possibility for (Y_2\). This control belongs to the
already known small toroidal L-space setting of
Hanselman–Rasmussen–Watson. It rules out a weak Floer-property sufficiency
route and is not a mixed-alternation counterexample.

## 5. Actual branching rigidity in an infinite toroidal family

`TURN_5.md` extends the control to

\[
 p_r=r(r+1)-1,\qquad
 A_r=\begin{pmatrix}r+1&-p_r\\1&-r\end{pmatrix},\qquad r\geq2.
\]

The two-trefoil splice (Y_r\) is an irreducible toroidal non-Seifert L-space
with (H_1(Y_r)=\mathbb Z/p_r\) and an actual branch quotient. Every branch
is a prime knot with hyperbolic exterior. The proof then addresses arbitrary
branching involutions, not just the constructed one:

1. Equivariant JSJ gives an invariant splitting torus. The marked piece
   homology inclusions and the deck action (-I\) exclude exchanging pieces.
   A separate peripheral-matrix argument reaches the same exclusion.
2. On a trefoil exterior, the homology kernel generated by the longitude and
   the characteristic central fiber force every orientation-preserving
   boundary matrix to be (\pm I\). Each restricted branch involution acts
   by (-I\) and extends meridionally to a trefoil strong inversion.
3. Sakuma's classical uniqueness theorem gives actual piece conjugacies.
   Their boundary discrepancy is not discarded: the resulting gluing
   difference lifts to (\pm I\) on the torus and therefore lies in the
   Klein-four kernel of the four-punctured-sphere mapping-class action.
   Its three nonidentity possibilities are precisely Conway mutations.

Consequently all branch knots of a fixed (Y_r\), up to mirroring to match
orientation, are mutants of its reference branch. No member of this family
can be a mixed common cover. There are at most four resulting branch classes,
without a claim that they are distinct. The (r=2\) case has only
nonalternating branches; no classification of alternation for every
(r\geq3\) is required or claimed.

This is an explicitly family-scoped consequence of classical theorems. It
does not classify actions on general graph manifolds, does not force a
hyperbolic piece to have a unique strong inversion, and does not transport
checkerboard surfaces through an arbitrary cover homeomorphism.

## Validation, limits, and final status

The five exact checker receipts have 29,858; 287,506; 11,505; 16,437; and
15,934 assertions, totaling 361,240. They check finite group controls,
presentation and lattice algebra, graph enumeration, family gluing algebra,
and the explicit pillowcase permutations. They are not implementations of
the deep topological classification inputs. The written proofs and exact
source hypotheses are indispensable.

The source gate and each of the five substantive turns are separately
preserved. `TARGET.json` is a historical source-gate record with its original
zero count; the current count and disposition are in `TURN_LEDGER.json` and
`FINAL_STATUS.json`. No attempt history is reset. One metadata-only correction
to earlier completion-estimate wording is documented separately and does not
change its mathematical claims.

The remaining original gap is alternation compatibility for arbitrary actual
(S^3\)-quotient involutions on a hyperbolic common cover or a toroidal
non-Seifert cover outside the proved family. Multiple local involutions,
piece permutations and general gluing data are not controlled by the present
arguments. The definite-filling approach still lacks the required equivariant
push-in certificate. No valid mixed pair has been produced.

**Original status: unsolved, five of five substantive author turns.** A
separate adversarial review is required before a final partial-result PR.
Reading PDFs, rendered pages and full extracted sources are excluded from
the portable public packet. No further author search is hidden in packaging
or review.
