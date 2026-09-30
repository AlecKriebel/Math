# Genus-two Floer-rank mutation: source hold and elementary topological reductions

**ID2859 / KP3.61. Status:** original target unresolved,2/5 substantive approaches. Independent review pending. No new Floer-rank theorem or counterexample is claimed.

## Exact target and literature qualification

[K3, Problem3.61](https://aimath.org/pastworkshops/kirbylistrep.pdf), pp174–175, asks about total Heegaard Floer dimension. Its broad formulation is balanced sutured Floer homology over F2, including closed hat-HF and knot-hat-HFK specializations. Spin-c-graded or delta-graded noninvariance does not imply unequal total dimension. The text does not impose a separating-surface hypothesis on this broad formulation.

A [December2022 Nantes–Orsay seminar](https://www.imo.universite-paris-saclay.fr/~frederic.bourgeois/seminar/NO12-22.html) announced a closed-manifold rank-invariance argument by Paolo Ghiggini. The [February2023 Uppsala abstract](https://www.uu.se/en/department/mathematics/research/geometry-and-physics/seminar-series-in-geometry-and-topology-/archive/2023-02-16-gt-seminar-with-paolo-ghiggini-institut-fourier-grenoble) explicitly calls the Ghiggini–Petkova project work in progress. No retrievable complete proof was located in this audit, and the announcements do not specify the full sutured/nonseparating scope. They must be credited as prior announcements, without being treated as a reviewed general theorem or silently dismissed as absent.

[Moore–Starkston](https://arxiv.org/abs/1204.2524) give known infinite families whose total knot-Floer dimensions agree while finer gradings differ. Their examples do not refute total-rank invariance. Their Section2 also distinguishes mutations of a handlebody containing the knot from trivial changes supported away from the knot. These established results are cited, not re-proved here.

## 1. Extension criterion for a trivial mutation

Let a compact oriented three-manifold be written X union_f Y along a connected closed genus-two boundary component. Let h be the hyperelliptic involution of that component and define the mutant by attaching x=f(h(y)) instead of x=f(y). Suppose h extends to an orientation-preserving diffeomorphism H of Y which fixes every other boundary component and all distinguished data there, including sutures. Then the map which is the identity on X and H on Y descends to a diffeomorphism from the mutant to the original: the mutant identification x=f(h(y)) becomes the original identification of x with H(y)=h(y). It preserves the remaining boundary and data.

Consequently all diffeomorphism-invariant Floer groups in the stated category agree in this extension case. This uses their ordinary invariance, not a general mutation theorem.

In particular, if Sigma bounds a genus-two handlebody B in the interior, with no distinguished knot or sutures in B, the hyperelliptic boundary involution extends over B. One can model B as the double cover of a three-ball branched over three disjoint boundary-parallel arcs. Its deck involution is orientation-preserving, and its boundary is the double cover of a sphere with six branch points, hence a genus-two surface with the hyperelliptic deck involution. Any isotopic representative of the boundary map extends by a collar isotopy. The criterion therefore applies, with the complement left fixed.

The requirement on the location of distinguished data is essential. If a knot lies inside B, its image under the extension can be a different knot. A diffeomorphism of the underlying unmarked three-manifold does not then identify the original marked knot with its mutant. Thus this argument does not dispose of Moore–Starkston's nontrivial handlebody mutants.

## 2. Separating integral-homology invariance and the nonseparating caveat

The genus-two hyperelliptic involution acts as minus the identity on H1(Sigma;Z). One way to see this is to represent it by the standard half-turn on the two-handled surface, which reverses each generator in a symplectic homology basis; equivalently its quotient has genus zero, so the invariant rational first-homology subspace is zero, and an order-two integral action with no +1 eigenspace is -I.

For a separating surface with connected sides X,Y, the Mayer–Vietoris sequence identifies H1(M;Z) with the cokernel of

    H1(Sigma;Z) -> H1(X;Z) direct-sum H1(Y;Z),
    u -> (i_X(u),-i_Y(u)).

There is no following kernel term because H0(Sigma) maps injectively to H0(X) direct-sum H0(Y). Mutation replaces one inclusion by its composition with -I. Multiplying the corresponding target summand by -1 intertwines the two presentation maps. Their cokernels are isomorphic, including torsion. This proof works for arbitrary finitely generated target homology groups, not only free groups. It is a classical homological observation, not a Floer-rank calculation.

The separating hypothesis cannot be dropped from that assertion. Take M=Sigma_2 times S1 and cut along a fiber. Regluing by h gives the mapping torus T_h. The Wang exact sequence, split over the free H0 kernel, gives

    H1(T_f;Z) = Z direct-sum coker(f_*-I on H1(Sigma_2;Z)).

Therefore

    H1(M;Z)=Z5,
    H1(T_h;Z)=Z direct-sum (Z/2)^4.

Over F2, however, -I=I, and both first-homology dimensions are5. This is not a Floer-rank counterexample. It simply prevents importing a separating integral-homology statement into the source's broader wording. Neither integral H1 nor its rank determines total hat-HF dimension in the general class under discussion.

## 3. Exact remaining gap

The extension criterion leaves mutations where no data-preserving extension over a side is available. The Mayer–Vietoris calculation leaves the Floer differential entirely uncontrolled. A proof needs a genuine Floer pairing/categorical symmetry or another rank argument in the exact coefficient and sutured scope; a counterexample needs actual Floer computations for a geometric mutant pair. No such general comparison is supplied. The announced Ghiggini–Petkova work merits source follow-up, but without an accessible complete argument it is not certified here; no outreach is initiated.

`verify.py` checks finite presentation-matrix sign identities over integers and mod2, and the fiber-action presentation matrices. These are controls on the homological calculation only. The extension argument is a written topological proof and is not represented as executable geometry.

No novelty or human peer review is claimed. Work used the inherited native runtime without model/reasoning changes; its exact model identifier was not exposed. Source PDFs remain outside the publication package.
