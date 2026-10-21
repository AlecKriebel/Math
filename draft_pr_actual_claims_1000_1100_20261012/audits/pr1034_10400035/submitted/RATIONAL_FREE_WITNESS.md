# A rational free-exterior two-string link with a trefoil plat

## Lemma

Fix the ordinary unframed ordered two-string-link category in the rounded
cylinder `C = D^2 x [0,1]`, with endpoints `(p_i,0),(p_i,1)` and component
orientations from bottom to top. Let `c(K)` be the coefficient of `z^2` in
the normalized Conway polynomial. Set

`a_i(L) = c(the standard individual closure of L_i)` and

`w(L) = c(the standard two-string plat of L) - a_1(L) - a_2(L)`.

There is a smooth string link `R` in this category such that its actual compact
three-dimensional exterior is a genus-two handlebody and

`(a_1(R), a_2(R), w(R)) = (0,0,1)`.

One may take the rational tangle `[1] + 1/[2]` in the
Kauffman--Lambropoulou convention, using the vertical endpoint marking and the
cap-preserving identification specified below. This is a theorem-level
geometric certification, not a machine-verified Wirtinger computation.

## Primary inputs and their exact roles

1. Louis H. Kauffman and Sofia Lambropoulou, *From Tangle Fractions to DNA*,
   author-hosted PDF, p.30, Figure 20 and its preceding paragraph:
   https://homepages.math.uic.edu/~kauffman/Dresden.pdf . The displayed tangle
   `[1]+1/[2]` has fraction `3/2`; its numerator is the left-handed trefoil.
   Both complete tangle drawings and their crossing information were visually
   inspected. The authors explicitly distinguish the tangles from their
   isotopic numerator closures.
2. The same authors, *On the Classification of Rational Knots*,
   arXiv:math/0212011v2, 27 November 2003:
   https://arxiv.org/pdf/math/0212011v2 . Section 2, p.6, defines rationality by
   a ball-pair homeomorphism to the trivial two-tangle, equivalently finite
   endpoint twists. Figure 2, p.7, fixes the elementary tangle convention;
   Figure 5, p.9, fixes the numerator caps. Section 5, pp.39--41, Theorem 6,
   identifies odd/even fractions with vertical connectivity. The same trefoil
   example occurs at pp.20--21, Figure 15.

The argument below is the category, cap, and exterior verification needed to
use these inputs here. It does not use a claim about arbitrary gluing or
stacking of free tangles.

## 1. The specified tangle really has vertical connectivity

Use `NW,NE,SW,SE` for the four diagram endpoints. The reduced fraction of
`T = [1] + 1/[2]` is `1 + 1/2 = 3/2`. Theorem 6 therefore gives connectivity
type `[infinity]`, namely the pairs

`{NW,SW}` and `{NE,SE}`.

There is also a direct endpoint check which does not require the general
parity theorem. The one-crossing tangle `[1]` has diagonal pairs
`NW--SE` and `NE--SW`. The two-crossing integer tangle `[2]` has horizontal
pairs, so its inverse `1/[2]` has vertical pairs. Form the horizontal sum of
`A=[1]` and `B=1/[2]` by identifying `NE_A` with `NW_B` and `SE_A` with
`SW_B`. The first outer arc runs

`NW_A -> SE_A = SW_B -> NW_B = NE_A -> SW_A`.

The second is `NE_B -> SE_B`. Thus the outer endpoints are paired vertically,
with no additional circle component. This matches the complete primary
drawing.

The horizontal sum in this definition is only a specification of this one
finite rational-tangle diagram. We are not assuming that the sum of arbitrary
rational tangles is rational, nor that stacking arbitrary free-exterior
string links preserves freeness. Here `1/[2]` is rational and adjoining the
single boundary twist `[1]` is one of its defining rational-tangle operations.

## 2. Smooth ordinary marking, with the plat caps fixed

Realize the finite crossing diagram as a smooth proper two-arc system in a
ball `B`, using small over/under displacements near its three crossings and
straight terminal collars. Equivalently, use the finite smooth endpoint-twist
construction of this rational tangle. Label its `SW--NW` arc as component 1
and its `SE--NE` arc as component 2.

Let `c_+` and `c_-` be the two disjoint boundary arcs used for the numerator:
`c_+` joins `NW` to `NE` above the diagram, and `c_-` joins `SW` to `SE`
below it. Interpret the outside planar caps as small outward pushes of these
boundary arcs. We now choose a marking of the entire cap system, not merely
the four endpoint positions.

Let `beta_+` and `beta_-` be the fixed short top and bottom cap paths in the
definition of the standard string-link plat. Choose an orientation-preserving
smooth ball identification `g:B -> C` which sends

`SW -> (p_1,0)`, `SE -> (p_2,0)`,

`NW -> (p_1,1)`, `NE -> (p_2,1)`,

and sends `c_-` to `beta_-` and `c_+` to `beta_+`.

Such an identification exists. On the boundary sphere the two disjoint
embedded cap arcs have disjoint disk neighborhoods. The target cap arcs have
the same property. Identify the two pairs of disk neighborhoods preserving
the labeled endpoints and the sphere orientation, and extend across their
complementary annulus. Equivalently, move the two boundary arcs by a smooth
sphere isotopy. Extend this boundary identification over the ball, or extend
the sphere isotopy through a boundary collar after a fixed ball
identification. This is an identification of smooth balls with marked cap
arcs; it is not a requirement that the rational tangle become a braid.

Straighten the four tangle germs in disjoint endpoint collars without
changing the cap isotopy classes, and orient each image arc from bottom to
top. Denote the resulting ordered string link by `R`. Once this choice is
made, all string-link isotopies are relative to the cylinder boundary.
Bottom-to-top orientation does not require the height coordinate to be
monotone along a strand.

No framing is retained. The over/under picture defines ordinary embedded
arcs, and the smoothing and collars add no framing variable.

It is important that `g` preserves the two cap arcs. An arbitrary
four-endpoint marking could change the two-string plat, and is not used to
assert its knot type here. The different ball-pair homeomorphism witnessing
rationality below need not preserve these caps or the pointwise boundary.

## 3. The actual exterior is a genus-two handlebody

Rationality supplies a homeomorphism of pairs from `(B,T)` to a trivial
two-arc ball tangle. One can take the inverse of the smooth endpoint-twist
construction in this particular case. Hence the compact exterior of `T` is
homeomorphic to

`(D^2 minus the interiors of two disjoint small disks) x [0,1]`.

The surface factor is a pair of pants. Its product with an interval is a
genus-two handlebody: represent the pair of pants as one disk with two
two-dimensional 1-handles and thicken this handle decomposition by an
interval. The result is a three-ball with two three-dimensional 1-handles.

The marking `g` and endpoint-collar isotopies preserve the exterior
homeomorphism type. Therefore the compact exterior of `R` is a genus-two
handlebody. In particular its actual fundamental group is the free group
of rank two. The open complement of the arcs has the same fundamental
group by the regular-neighborhood deformation. No pro-nilpotent or other
completion replaces this actual group, and no assertion about the standard
bottom meridians being a free basis is needed.

## 4. Both individual closures are unknotted

In the trivial two-tangle each arc cobounds a disk with an arc of the ball
boundary. Transporting such a disk by the inverse rationality homeomorphism
shows that each arc of `T`, considered individually, is boundary-parallel.
After applying `g`, the same holds for each arc of `R`.

After discarding the other component, any two simple arcs on the unpunctured
boundary sphere joining the two surviving endpoints are isotopic relative
to those endpoints. A standard bigon-removal argument, or the disk
neighborhood classification of sphere arcs, proves this. Thus a standard
outside individual closing arc may be replaced by a small outward push of
the boundary arc from the boundary-parallelism disk. The resulting knot
bounds the corresponding disk and is the unknot.

The other two endpoints are not retained as punctures in this argument:
the other strand has first been forgotten. We make no claim that arbitrary
two-cap systems on a four-punctured sphere are isotopic.

Consequently each standard individual closure has Conway polynomial `1`,
so `a_1(R)=a_2(R)=0`.

## 5. The standard plat is the trefoil

The cap-preserving marking in Section 2 identifies the standard plat of `R`
with the numerator closure of the specified tangle `T`. The primary example
therefore identifies this plat as a left-handed trefoil. This uses the
complete diagram and its stated numerator, not an inference that tangle
fractions classify string links without their boundary marking.

For either trefoil chirality, the normalized symmetric Alexander polynomial
is `t - 1 + t^(-1) = 1 + (t^(1/2)-t^(-1/2))^2`; equivalently its Conway
polynomial is `1+z^2`. Reversing the orientation of the resulting knot does
not change it. Thus its Conway coefficient is `1`, and

`w(R) = 1 - 0 - 0 = 1`.

This proves the lemma.

## Certification limits and permitted use

- The certified output is existence of this one ordinarily marked smooth
  unframed ordered two-string link, with actual handlebody exterior and the
  displayed three invariant values.
- No numerical linking number or Milnor invariant is assigned. These may be
  left symbolic in the main evaluation matrix.
- No complete marked Wirtinger presentation, machine-checked knot isotopy,
  or algorithmic fundamental-group certificate is claimed. The proof uses
  the explicit finite rational construction and verified primary inputs.
- No arbitrary boundary re-marking is asserted to preserve the plat;
  the explicit two-cap marking is part of the witness.
- No closure property for free exteriors under arbitrary stacking, tangle
  sum, or gluing is used.
- The lemma alone neither classifies finite-type invariants nor proves a
  statement about higher orders or other numbers of strings.

## Retention and verification metadata

The complete author PDF `Dresden.pdf` is 1,388,506 bytes, SHA256
`53cd49ea0448fe796c3baa07e2246f89d16352398293cb0e2b1d9019dbfa5fd1`.
The original `www.math.uic.edu` request resolved to the same author's
`homepages.math.uic.edu` host and returned HTTP 200; an independent direct
HTTPS retrieval at the latter URL returned identical bytes.

The complete classification PDF `math0212011v2.pdf` is 459,279 bytes,
SHA256 `de77c7cf69cd5464ed7b9044dc4842004c23c5c2820f334c30b5ecbd8cf4fc10`.
It returned HTTP 200 and contains 58 PDF pages. The arXiv landing-page
comment says 56 pages; the observed PDF page count is reported rather than
silently copying that comment.

SOURCES.json records public PDF identities and the historical source-inspection
summary. The underlying retrieval records and source/inspection artifacts are
not included in this edition. The relevant pages were rendered with Poppler and
opened as images: Dresden p.30; Classification pp.6, 7, 9, 21, 39, 40, 41.
The relevant text on Classification p.20 was inspected in its extracted
layout text, and the complete drawing on p.21 was visually inspected.

Copied PDF bodies, extracted text, and source-page images are private
supporting evidence, not authored publication material. This proof and
public verification metadata are separate. The accepted preceding proof and its audit were not edited.
