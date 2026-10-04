# Corrections and proof clarifications

Problem 30006276 / OWR-14299284-004. These amendments apply to the author
packet identified in `AUDITED_INPUTS.json`. The original files are unchanged.
They do not change the result: **unsolved**.

## C1. Restrict the annihilator lemma to g >= 2

In PROOF.md, Section 4, immediately before “Set lambda=lambda_(g-1)”, insert:

> In the following annihilator calculation assume g >= 2. For g=1 the
> nonsimple locus is empty and this route is vacuous; multiplicativity is
> already covered by the small-genus case.

The assertions Ann_R(lambda_(g-1))=lambda_(g-1)R and
lambda_(g-1)^2=0 hold exactly as argued for g>=2. They are false for g=1,
where lambda_0=1, R=Q, Ann_R(1)=0, and 1^2=1. All supplied computational
annihilator checks already begin at g=2. This is a scope correction to the
lemma, not an exception to the intended multiplicativity conclusion.

## C2. Justify cohomological vanishing on the entire singular boundary

PROOF.md, Section 3.1 reaches the correct conclusion. The transition from
Chow vanishing on the boundary to ordinary cohomological vanishing can be
made explicit, without treating a singular boundary as smooth.

Pass to a smooth finite level cover U of A_g and a smooth proper toroidal
compactification X with simple normal-crossing boundary D. The Hodge bundle
is pulled back throughout. Each smooth proper boundary component D_i has
lambda_g|D_i=0 in Chow, hence also in ordinary cohomology. Let
D_tilde be the disjoint union of the D_i and let q:D_tilde -> D be the
normalization. Deligne's Proposition 8.2.7 identifies the kernels of

    H*(X,Q) -> H*(D,Q),
    H*(X,Q) -> H*(D_tilde,Q).

Its hypotheses hold: X is smooth, D is proper, D_tilde is proper and smooth,
and q is surjective. Thus cl(lambda_g)|D=0. The exact sequence of (X,D)
then supplies u in H_c^(2g)(U,Q) mapping to cl(lambda_g) in H^(2g)(X,Q).
Relative cup product gives, whenever the degrees are complementary,

    integral_X cl(bar(a)) cl(bar(r)) cl(lambda_g)
      = integral_U cl(a) cl(r) u.

If cl(a)=0, the right side is zero. Divide by the level-cover degree and
use the tautological perfect pairing to obtain P(a)=0. This proves the
factorization through algebraic cohomology used in the packet. No uniqueness
of u is required.

Reference: Pierre Deligne, *Théorie de Hodge III*, Proposition 8.2.7,
printed p. 40, with Proposition 8.2.5 and its weight argument on p. 39:
https://www.numdam.org/articles/10.1007/BF02685881/ .
This clarification is not a newly discovered obstruction or an added
conjectural hypothesis.

## C3. Specify the compactification in the Torelli integral

At PROOF.md, Section 5, before the displayed integral over bar(M_g), add:

> For this formula choose a toroidal compactification to which the Torelli
> map extends, and interpret pullbacks in a smooth neighborhood of its
> image, or on a compatible resolution. Arbitrary smooth compactifications
> need not themselves carry an extension from bar(M_g).

The second Voronoi or perfect-cone compactification supplies the usual
extension, with the image in its nonsingular locus, as explained in
arXiv:2601.04353v3, Section 1.9. Equivalently, extend the pullback classes
from M_g^ct to bar(M_g); lambda_g kills ambiguity supported outside compact
type. The formula and the five scalar tests do not change.
