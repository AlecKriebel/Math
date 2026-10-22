# Independent adversarial review: the pentagon marked-lifting problem

**Verdict: PASS_SCOPED_GEOMETRY_AND_UNRESOLVED_MARKED_LIFT.** The finite geometry,
affine/projective nonrealizability statement, realizable square, explicit
Falk–Sturmfels identification and source-scope distinctions are correct. The
specified order-four action is still not lifted or obstructed at the fundamental
group or integral E∞ level. Recommended status remains **unsolved, 2/5**.
No mandatory mathematical correction was identified.

Reviewed on 30 September 2026 by a separate AI reviewer, gpt-6-astra at xhigh
reasoning effort. This is not human peer review. The frozen `OBSTRUCTION.md`
has SHA-256 `a71569494de781df442ebf8b43fdf6075f396e91a443456cdb740b4f32a89402`.
Historical novelty is not established.

## 1. Original target and arrangement

I inspected the full Problem 3 and neighboring context on printed p.2978 of the
[OWR 49/2012 report](https://ems.press/content/serial-article-files/46421), including
the rendered page, and read Rybnikov's complete pp.2966–2968 contribution. The
problem specifies the eight affine lines AB, CE, AC, DE, AD, BC, AE, BD and the
vertex cycle B→C→E→D→B, fixing A. It asks for lifts of that specified homology
action, rather than an unmarked equivalence of complements. The separate
realization-space question is Problem 4.

Adding the line at infinity produces nine projective lines. Adding all ten
pentagon joins and then infinity would produce a different eleven-line
arrangement. The frozen artifact and both checkers consistently use the correct
eight/nine-line configuration.

I reconstructed all eight affine equations directly from the displayed vertices,
using exact arithmetic in Q(a), a²=a+1. The Gram matrix with diagonal entries one
and off-diagonal entry (1−a)/2 has determinant (2+a)/4>0. In this metric the five
successive sides have squared length one and the five diagonals have squared
length a². Thus the coordinates really are an affine normalization of the
regular pentagon, not merely an arbitrary five-point realization.

The incidence calculation gives one quadruple, four finite triple points, six
finite double points and four parallel pairs. After projectivization there are
eight triple points and six double points, in addition to the quadruple. Counting
the pairs of lines at these flats gives exactly 36=binom(9,2); deleting infinity
recovers all 28 affine line pairs, including the four parallel pairs. The order-four
permutation σ=(0 2 6 4)(1 3 7 5) preserves every flat.

## 2. The projective-to-affine reduction is justified

The triple and quadruple intersections force any alleged affine realization of
σ to send A,B,E to A,C,D. These three input points form an affine frame, so the
map is forced to be T(x,y)=(ax+y,x+ay). It is invertible, with determinant a,
but sends C to (a+2,2a), which is not E. This contradiction works over C; it is
not merely an exclusion of real or Euclidean isometries.

There is also no missed projective realization. The intersection of lines 0,1
and that of lines 2,3 are distinct points of infinity. Under σ they must map to
the intersections of 2,3 and 6,7 respectively, again two distinct points of
infinity. Any projective transformation with this line action therefore preserves
the line through them, namely infinity. It consequently restricts to an affine
map, already excluded. This argument remains valid even if fixing infinity is
not separately included in the requested permutation.

As a further finite check, infinity is the unique line containing four triple
points. The unique quadruple point fixes a four-line class. I tested all 4!·4!=576
permutations of that class and its four remaining affine lines, rather than
presupposing how parallel partners must move. Exactly the four powers of σ
preserve all incidence data. This confirms the cited C₄ combinatorial group,
without turning it into a group of geometric or topological automorphisms.

## 3. The square really has the claimed marked lifts

The coordinate swap R(x,y)=(y,x) takes the eight lines to their σ² images and
fixes (2,2), which is on none of them. It is a complex-linear involution of the
ambient affine plane, so its restriction is an actual based homeomorphism of the
complex complement. It therefore induces an automorphism of the full discrete
fundamental group; no completion or quotient is needed for this assertion.

The normal map to a complex line is multiplication by a nonzero complex number.
Such a map preserves the orientation of a small positively oriented normal circle.
Thus R takes the positive meridian class of line i to the positive class of line
σ²(i). Choices of paths to a fixed basepoint can introduce conjugations in the
fundamental group, but not signs or changes in the stated H₁ permutation.

The E∞ claim is correct in the precise category used by the source. OWR Theorems
1–3 give the natural singular-chain structure, the functor from the homotopy
category of spaces, and transport to free integral homology. In the more detailed
[2014 manuscript](https://arxiv.org/abs/1402.6272v1), Theorem 13 supplies the
strong-deformation-retraction transfer and Proposition 14 its uniqueness up to
isomorphism. The morphisms are universal-bimodule morphisms modulo chain
homotopy, not necessarily strict coalgebra maps on a chosen presentation.

Concretely, choose the transfer equivalence i:H→C and its inverse p:C→H with the
usual identification on homology. The composite p·C(R)·i is an automorphism in
that category, with inverse p·C(R⁻¹)·i, and induces exactly H(R). Integral
arrangement-complement homology is free, as the original contribution explicitly
recalls. The cohomology algebra is generated in degree one, so the meridian action
also fixes the intended induced action on the full ordinary homology coalgebra.
There is no rationalization or change of coefficient ring here.

These arguments apply to σ² only. Neither a square lift nor the existence of a
C₄ action on combinatorial data supplies a square root of that lift. Conversely,
a hypothetical lift of σ need not itself have order four; its fourth power could
be a nontrivial automorphism acting identically on H₁. The artifact correctly
avoids that extra constraint.

## 4. Galois and Falk–Sturmfels comparisons preserve the marking issue

The relations a+a′=1 and aa′=−1, with a′=1−a, verify every displayed vertex
image for the map from the a′ realization to the a realization. It has the
nontrivial line permutation σ. This is not a self-map of the fixed realization.
The two parameters are real, so ordinary complex conjugation does not exchange
them. A continuous automorphism of C fixes Q, hence all real numbers by density;
coefficient-field conjugation cannot be inserted as a continuous map.

An additional check gives T_a·T_a′=R: composing the two concrete cross-realization
maps produces the already-realized square. It does not manufacture the missing
order-four marked self-map.

I read the published [Nazir–Yoshinaga Example 5.2](https://www.numdam.org/item/ASNSP_2012_5_11_4_921_0.pdf),
pp.933–934. The affine substitution (X,Y)=(y,1−x+(a−1)y) has determinant one
and carries the source lines, in order, to
(L₁,K₁,L₄,K₄,L₃,K₃,L₂,K₂,H₉). All nine linear-form substitutions were checked
independently. Hence the identification with the Falk–Sturmfels type is explicit,
not just a match of an informal arrangement name.

That example gives a projective equivalence of the two Galois-conjugate
arrangements with a label permutation. It does not assert the particular
label-preserving equivalence which, when combined with a cross-realization map,
would resolve the present self-action. [Amram et al., Proposition 6.1 and
Remark 6.2](https://arxiv.org/abs/1310.0700v1) give C₄ and a C₂ subgroup whose
realization-space action is trivial, precisely as the artifact reports. Different
choices of the generator may invert the displayed four-cycle, with no effect on
this conclusion. Those statements are not assertions that every combinatorial
automorphism lifts to the marked fundamental group.

## 5. The exploratory truncations are not evidence of a lift

The archive contains 24 records, covering three permutations, two half-twist
sign conventions and four prime fields, each reporting a consistent formal linear
system. Its README, script header and main artifact all expressly disclaim a
certified arrangement-group presentation or nilpotent-quotient interpretation.
I checked the recorded coverage and these disclaimers; I did not certify the
presentation-to-topology or truncation-to-group identifications and did not use
those records in this verdict's mathematical deductions.

Even a correctly realized finite quotient would not by itself establish an
integral automorphism of the full discrete group. Nor would one low-degree
obstruction calculation certify all E∞ coherences. Rybnikov's Theorem 12 concerns
the augmentation-ideal/dimension completion, and the artifact does not identify
that completion with the full group. Its distinction between rational formality,
ordinary coproduct preservation, finite truncations and the required integral
marked lift is sound.

## 6. Reproduction and recommendation

The submitted 111-assertion geometry checker reproduced its receipt byte for byte.
All five cited primary PDF hashes match the source manifest.

The independent checker imports no author code and uses only the Python standard
library. It constructs the lines from their endpoint pairs in the quadratic field,
recomputes intersection partitions, tests all 576 candidate incidence permutations,
verifies the projective infinity argument, checks the Galois maps and their
composition, and matches the published Falk–Sturmfels equations. All **703 exact
controls** pass. These finite checks support the geometry; the functorial square
lift is justified by the written topological argument above.

Run `python3 independent_checks.py` and `python3 author_replay/verify.py` from the
review directory. Compare stdout with their respective JSON receipts. The author
checker requires SymPy and the exact frozen artifact adjacent to it.

Recommended publication status is **unsolved, 2/5**. The precise remaining problem
is a lift of σ with the fixed positive-meridian action, or a rigorous obstruction
to that lift, separately at the discrete group and natural integral E∞ levels.
No unmarked equivalence, geometry of the square, or uncertified Magnus system
settles either question. Preserve these limits and the absence of a novelty claim.
