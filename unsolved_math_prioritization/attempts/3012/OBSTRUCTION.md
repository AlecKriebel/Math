# KP-5.5: the remaining pairwise straightening step

**Target:** 3012 / KP-5.5.
**Outcome:** unresolved after two approaches. The conditional isotopy argument
below is standard machinery, not a solution or a novelty claim.

## 1. Source and conventions

The [2026 K3 list](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf),
Problem 5.5, printed p.304, asks whether connected sum of locally flat pairs

\[
 (M_1^{n+k},N_1^n)\#(M_2^{n+k},N_2^n)
\]

is well-defined in the topological category. Its cited codimension-two theorem
is [Livingston (2024)](https://doi.org/10.1017/prm.2022.87).

We retain the intended connected, oriented, locally flat setting of that
theorem: both ambient manifolds and submanifolds are connected and oriented,
and the equivalence is an orientation-preserving homeomorphism of pairs.
Charts are chosen with the compatible ambient and submanifold orientation
conventions. The construction is an interior connected sum; boundary connected
sum is not under discussion. We do not exploit omissions in the abbreviated
question to produce an orientation or component-choice ambiguity.

Livingston proves the codimension-two result in every dimension in this scope.
The K3 remarks also credit Brown for codimension one and identify the unsettled
range as codimension greater than two with ambient dimension greater than four.
The present attempt supplies neither the general higher-codimension result nor
a counterexample in that range.

## 2. The actual connected-sum data

Put \(m=n+k\). A pair chart is an embedding

\[
 \phi:(\mathbb R^m,\mathbb R^n\times\{0\})\longrightarrow(M,N)
\]

whose inverse image of \(N\) is exactly the indicated coordinate subspace.
Remove the interior of a standard ball pair in each chosen chart and identify
boundary points with the same coordinates, using the orientation-reversing
chart convention on the second summand. A product ball
\(P=D^n\times D^k\), with its zero section, can replace the round ball by a
fixed radial homeomorphism of standard pairs.

An ambient connected-sum theorem alone does not compare the resulting embedded
submanifolds. Every ambient isotopy used in the argument must preserve the
distinguished submanifold as a set. Livingston's Lemmas 3.3–3.5 explicitly
separate moving/shrinking pair charts, aligning them by normal-bundle theory,
and removing the remaining fiber-preserving automorphism.

## 3. Approach 1: extend the fiber-preserving step to arbitrary codimension

The last of those steps is not the higher-codimension obstruction. Here is its
precise general version, with its hypotheses left visible.

**Lemma.** Let \(n,k\ge1\), and suppose

\[
 g:(D^n\times D^k,D^n\times\{0\})\longrightarrow
       (D^n\times D^k,D^n\times\{0\})
\]

is a homeomorphism of the form

\[
 g(x,y)=(a(x),b_x(y)),
 \tag{1}
\]

where \(a\) is orientation-preserving and each \(b_x\) is an
orientation-preserving homeomorphism of \(D^k\) fixing zero. Then \(g\) is
isotopic to the identity through homeomorphisms of this pair. It extends to a
compactly supported homeomorphism of
\((\mathbb R^{n+k},\mathbb R^n)\) which is itself pair-isotopic to the identity.

**Proof.** We use the established ordinary, unpaired theorem that every
orientation-preserving self-homeomorphism of a sphere is isotopic to the
identity. Livingston's preprint Theorem 1 recalls it, including the necessary
topological annulus/stability input. Together with the Alexander trick it
implies that \(\operatorname{Homeo}^+(D^j)\) is path connected for every
\(j\ge1\).

The pointed group \(\operatorname{Homeo}^+(D^j,0)\) is also path connected.
Indeed, for \(h\) in that group let \(c\) be the radial cone extension of
\(h|_{S^{j-1}}\). The map \(c^{-1}h\) fixes the boundary and zero. Its
Alexander isotopy fixes both. The boundary isotopy of \(h|_{S^{j-1}}\) to the
identity can then be coned, fixing zero throughout. For \(j=1\), the
orientation-preserving boundary map fixes both endpoints, so the same argument
applies.

First use a path of \(a\) to the identity, acting on the base coordinate,
to deform (1) to \((x,b_x(y))\). Next use

\[
 G_t(x,y)=(x,b_{(1-t)x}(y)),\qquad 0\le t\le1.
 \tag{2}
\]

Every \(G_t\) is a homeomorphism of the product pair. The parameterized
inverses are continuous: on the compact ball, inversion is continuous in the
homeomorphism group, and \((x,y)\mapsto b_x(y)\) is continuous. At \(t=1\)
the fiber map is independent of \(x\). Finally use a path from \(b_0\) to the
identity in \(\operatorname{Homeo}^+(D^k,0)\). Concatenating these paths proves
the first assertion. Notice that only path connectedness of the pointed fiber
group is used; no assertion that it has the homotopy type of \(SO(k)\) is made.

For the extension, reverse the resulting isotopy and denote it by \(h_s\),
where \(h_0=\mathrm{id}\) and \(h_1=g\). Use the homogeneous product gauge

\[
 p(x,y)=\max\{\|x\|,\|y\|\},\qquad P=\{p\le1\}.
\]

Every nonzero point is uniquely \(ru\) with \(r=p(x,y)>0\) and
\(u\in\partial P\). Define

\[
 E_s(z)=
 \begin{cases}
 h_s(z),&p(z)\le1,\\
 r\,h_{s(2-r)}(u),&z=ru,\quad1\le r\le2,\\
 z,&p(z)\ge2.
 \end{cases}
 \tag{3}
\]

At \(r=1\) the formulas agree, and at \(r=2\) the middle formula is the
identity. A homeomorphism of \(P\) preserves its boundary, so the middle
formula preserves \(r\) and is a homeomorphism on each radial shell. Its inverse
uses the inverse boundary homeomorphism with the same parameter. This proves
joint continuity and invertibility, including the two seams. At the origin the
inside formula applies. The zero-section subspace is preserved in all three
regions because its intersection with \(\partial P\) is preserved by every
\(h_s\). Thus \(E_s\) is an ambient isotopy of pairs supported in \(2P\),
with \(E_1|_P=g\). \(\square\)

### Precisely what this handles in a connected sum

Suppose two pair charts \(\phi,\phi'\) have already been arranged to have
the same product-ball image, and their transition
\(g=\phi^{-1}\phi'|_P\) satisfies (1). Transport the compact extension (3)
through \(\phi\), and set it to the identity outside \(\phi(2P)\). The
resulting ambient pair homeomorphism \(E\) has \(E\phi=\phi'\) on \(P\).
Its inverse on that punctured summand, together with the identity on the other
summand, descends to a homeomorphism between the two connected sums: a boundary
point \(\phi'(u)\) is sent to \(\phi(u)\), with its matching point on the
other side unchanged.

This proves independence for those **already aligned, fiber-preserving** chart
changes. It does not show that arbitrary topological pair charts can be brought
to this form. In the cited codimension-two proof that is exactly the prior
normal-bundle alignment step, Lemma 3.4. Replacing 2 by \(k\) in the final
fiber contraction (2) does not extend that earlier theorem.

**Gap after Approach 1.** No relative straightening theorem was obtained for
an arbitrary nested pair chart in higher codimension. Assuming the existence
of a compatible bundle structure and its needed ambient uniqueness simply
assumes away the unresolved step.

## 4. Approach 2: an ambient annulus or an Alexander trick

The ordinary annulus theorem gives a product description of the ambient region
between nested locally flat sphere boundaries. It does not assert that the
submanifold in that region is simultaneously a product with the required
boundary matching. Livingston formulates this additional assertion as the
**Relative Annulus Conjecture**, Problem 4.2 in the published paper.

An Alexander trick cannot supply the missing hypothesis. If a homeomorphism
\(q:P\to P\) preserves the standard subspace and fixes \(\partial P\)
pointwise, the formula

\[
 A_t(z)=
 \begin{cases}
 t q(z/t),&p(z)\le t,\quad t>0,\\
 z,&p(z)\ge t,
 \end{cases}
 \qquad A_0(z)=z
 \tag{4}
\]

does give an isotopy of pairs from the identity to \(q\). The seam agrees
because \(q\) fixes the boundary, and the displacement is at most \(2t\)
in the product gauge, proving continuity at \(t=0\). Inverses use the same
formula with \(q^{-1}\). But a general chart transition is not a
boundary-fixing self-homeomorphism of one fixed product ball. Even after its
image is aligned, an arbitrary boundary isotopy would have to preserve the
equatorial submanifold. The ordinary sphere isotopy theorem used in Section 3
does not imply that stronger statement for a pair.

Similarly, coning a homeomorphism of a sphere pair extends it over a disk pair,
but extension across a missing disk is not extension over the punctured
summand. Such an argument would need the same relative boundary compatibility.
No actual pair of connected-sum choices with inequivalent outputs is produced
by observing this gap.

**Gap after Approach 2.** Neither a product of the relevant annular pair nor a
compactly supported localization of every orientation-compatible pair germ was
proved. No counterexample to either condition, and no counterexample to the
source question, was constructed. The ordinary theorem cannot be used with
the distinguished submanifold forgotten.

## 5. Status, source correction, and validation

The full codimension-two theorem is existing work. The higher-codimension
fiber-preserving lemma above isolates a conditional step and supplies its
explicit collar extension; it does not settle the unrestricted target.
The two approaches stop at relative straightening/localization, so the attempt
remains **unsolved**.

The source cross-reference was checked rather than followed by identifier
alone. The published Livingston reference [17] labels an earlier version of
this paper but gives arXiv:2110.03502, which is actually his different paper
*Intrinsic symmetry groups of links*. The title-matched earlier version is
[arXiv:2104.03930v1](https://arxiv.org/abs/2104.03930), whose Appendix C contains
the higher-codimension discussion referenced by K3. Both that preprint and the
full published paper were inspected. This bibliographic correction does not
invalidate the published codimension-two theorem.

The artifact is a proof-level conditional argument and source audit; numerical
sampling would not certify its topological localization gap. No computational
test is presented as doing so. Separate adversarial review is required before
publication. No historical novelty or general resolution is claimed.
