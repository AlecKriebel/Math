# Recovering layers for central toric arrangements with at most two connected hypertori

**ID 30003709 / OWR-15987-020. Status:** original target unresolved, 2/5 substantive approaches. Independent review pending. This is a restricted recovery theorem, not a general cohomological reconstruction.

## Source scope

Roberto Pagaria's Question 3 in [Oberwolfach Report 2/2018](https://ems.press/content/serial-article-files/46724?nt=1), printed p114, explicitly uses rational cohomology. It asks whether the graded algebra of the complement of a central toric arrangement determines its abstract layer poset. No preserved ambient-torus subalgebra, distinguished generators, characters or Leray filtration is required in the question. Layers are connected components of intersections, ordered by reverse inclusion; they retain more information than the ordinary matroid or arithmetic multiplicities alone.

[Pagaria, Two Examples of Toric Arrangements](https://arxiv.org/abs/1804.05767v3), gives the failure of the reverse implication for integral cohomology, and rational examples with the same arithmetic matroid but different cohomology. Neither is a pair of isomorphic rational cohomology algebras with nonisomorphic layer posets. Those examples therefore do not refute the source question. We do not replace rational graded algebra by an integral ring or by its associated graded algebra.

## Restricted theorem

Within the class of central arrangements consisting of at most two **distinct connected** codimension-one hypertori in a complex torus T=(C*)^d, the graded rational cohomology algebra of the complement determines the abstract layer poset. In fact its graded dimensions suffice. No identification of ambient classes or meridian generators is needed.

Connectedness means the defining character is primitive in the integer character lattice. This extra hypothesis is part of the restricted theorem. Two nonprimitive equations may have many connected components and are not covered merely because there are two equations. No claim is made that arbitrary arrangements can be recognized as members of this restricted class from the abstract algebra alone.

### Two-hypertorus normal form

Suppose there are two distinct connected central hypertori. Send the first primitive character to the first coordinate by an integral change of torus coordinates. Using integer operations on the remaining coordinates, write the second as x^a y^m, where m>=1 and gcd(a,m)=1. Distinctness ensures the second character is not rationally proportional to the first: otherwise primitiveness would make the kernels equal. Thus d>=2. The coordinate operations are torus automorphisms, and the complement is

    X_(a,m) times (C*)^(d-2),
    X_(a,m)={(x,y) in (C*)^2 : x!=1, x^a y^m!=1}.             (1)

The common intersection has m connected components, given by x=1 and y in the m-th roots of unity, with the remaining torus coordinates arbitrary. Its layer poset consists of the ambient torus, two incomparable hypertori above it, and m incomparable codimension-two layers above both. Hence the poset in this class depends only on m, not on a or d.

### Direct cohomology calculation

Project X_(a,m) to B=C* minus {1} by (x,y)->x. This is a locally trivial bundle with fiber C* minus m distinct points. Indeed a local branch of x^(a/m) identifies the fiber with C* minus the m-th roots of unity. Both base and fiber have the homotopy type of finite graphs. The base is a wedge of two circles; the fiber has first rational cohomology of dimension m+1.

Choose fiber meridians around 0 and the m removed roots. Around a loop in B encircling 0, the roots are cyclically permuted by the step -a modulo m; gcd(a,m)=1 makes this a single m-cycle. The meridian around 0 is fixed. A loop around 1 has zero winding around 0 and trivial monodromy on these meridians. Possible motion of based loops changes conjugacy, not their first homology classes. Thus the cohomology local system V=H1(fiber;Q) has one trivial coordinate and one cyclic permutation block (up to taking the dual, which has the same ranks).

On a two-circle graph, local-system cohomology is computed by

    V -> V direct-sum V,       v -> ((P-I)v,0),               (2)

where P is that permutation. Since rank(P-I)=m-1, we obtain

    dim H0(B;V)=2,       dim H1(B;V)=m+3.

The Serre spectral sequence for the bundle has only columns p=0,1 and rows q=0,1, so every differential vanishes for degree reasons. This is a statement about graded dimensions and does not require splitting the cohomology ring. The constant q=0 row gives dimensions 1 and 2. Therefore

    P_X(t)=1+4t+(m+3)t^2,
    P_M(t)=(1+t)^(d-2) [1+4t+(m+3)t^2].                     (3)

In particular the top nonzero cohomological degree is d, b1=d+2, and

    m=b2-binomial(d,2)-2(d-1).                               (4)

These integers can be read from an abstract graded-algebra isomorphism. Recovering m recovers the layer poset described above.

### Zero or one hypertorus

The empty arrangement has complement T and polynomial (1+t)^d, and its poset has one element. A single primitive hypertorus can be sent to x=1, so the complement is (C* minus {1}) times (C*)^(d-1), with polynomial

    (1+2t)(1+t)^(d-1).

Again the top degree is d, and b1-d equals the number of hypertori (0,1 or2) throughout our restricted class. Thus the three cases can be distinguished without being given d separately. For d=0 only the empty case occurs. This completes the restricted recovery proof.

## What this does not recover

The theorem recovers an abstract poset, not a labeled arrangement, its character matrix, an arithmetic representation or its embedding in T. For two hypertori the rational dimensions do not distinguish the residue a modulo m, and the theorem does not claim that the full cohomology rings are isomorphic for all such residues.

With three or more distinct connected hypertori, or disconnected character kernels, the above two-circle fibration and single-cycle calculation no longer provide the general incidence information. No arbitrary ring-to-poset reconstruction, or pair contradicting it, has been produced. The original question remains unresolved.

## Verification and attribution

The proof is a direct elementary normal-form and bundle computation. The checker verifies the character arithmetic, cyclic monodromy ranks, spectral-sequence dimension arithmetic and recovery formula for finite parameter ranges. Those finite ranges are controls, not the proof of the unbounded theorem. No topological bundle theorem is represented as executable geometry. No novelty or human peer review is claimed.

Work used the inherited native runtime without model or reasoning-setting changes; its exact model identifier was not exposed. Primary PDFs are retained outside the publication package.
