# Direct implication of prior work for PR 1114

Audit target: problem 30003952 / OWR-16415-015; frozen head `e1a11feef98ed0fde22375c983e30b72b268d265`.
Independent priority analysis, 2026-10-17. This document proves a consequence of prior work; it does not claim a new theorem.

## Exact implication to establish

For every oriented smooth surface S and each prescribed pair of essential simple closed curves alpha,beta meeting transversely once, construct orientation-preserving smooth diffeomorphisms A,B with smooth inverses, [A]=t_alpha, [B]=t_beta, ABA=BAB as maps, and compact support inside any chosen sufficiently small compact regular neighborhood of the pair. The maps must be identity on a boundary collar of that neighborhood. The ambient mapping-class image need not be split if it has additional relations.

## Prior input, with the necessary local information

Mann–Tshishiku, Theorem 4.1, gives a section s:B3 -> Diff-infinity_boundary(D,{p1,p2,p3}). Its proof gives a common external identity collar and, in fixed coordinates on small equal disks around the marked points, translations on the filled disks. These properties hold for words and inverses. The source uses generators x,y with x^2=y^3; the Artin generators can be taken as y^(-1)x and x^(-1)y^2. Consequently the two Artin images have the same local properties.

Primary source: [arXiv v1](https://arxiv.org/pdf/1802.00490v1), dated 1 February 2018, physical/printed pp.18–19; [Mann author PDF](https://pi.math.cornell.edu/~mann/papers/RealizationProblems.pdf), same pages. A [proceedings-formatted author version](https://bena-tshishiku.github.io/files/papers/nielsen-survey.pdf), physical/printed pp.19–20, contains the same relevant assertions. In particular this argument does not apply the even-branch statement of Theorem 4.2 at an inadmissible parameter.

The rest is an explicit deduction and local covering calculation.

## 1. The odd branched cover is a one-holed torus

Let D*=D minus {p1,p2,p3}. Define a homomorphism pi1(D*) -> Z/2 by sending each small meridian to 1. Take its connected double cover and fill in a single ramification point over each pi, with local model z=w^2. Call the resulting compact oriented surface N and its branched covering p:N -> D.

The boundary meridian has image 1+1+1=1 in Z/2. Hence the preimage of the external boundary is connected and covers that boundary with degree two. The branched Euler-characteristic calculation gives chi(N)=2 chi(D)-3=-1. Thus 2-2g-1=-1, so g=1 and N has exactly one boundary component.

Choose the smooth structure near each ramification point using the same translated disk coordinates as in the prior action: p(w)=pi+w^2. Away from these points use the ordinary lifted smooth structure. These structures agree on punctured branch charts.

## 2. Boundary normalization gives an exact homomorphism of actual maps

Any orientation-preserving homeomorphism f of D that preserves the three branch points permutes their meridians, up to conjugacy. It therefore preserves the kernel of the above mod-two homomorphism and lifts to the unbranched double cover. Both lifts extend uniquely across the three missing ramification points; their only ambiguity is the deck involution iota.

If f is identity on a collar C of the external boundary, p^(-1)(C) is a connected annulus. Each lift restricts there either to identity or to iota. Exactly one is identity there. Denote this normalized lift by L(f).

For two such maps f,g, L(f)L(g) covers fg and is identity on the lifted external collar. Uniqueness gives L(fg)=L(f)L(g); likewise L(f^(-1))=L(f)^(-1). Thus a relation downstairs lifts as an equality of actual maps, with no unresolved deck sign.

For the finitely many generators of s(B3), intersect their identity collars once. Every group word is identity on this same collar.

## 3. Smoothness at the branch points is checked, not assumed

For f in the image of s, suppose f sends pi to pj. The local translation property means

f(pi+z)=pj+z

for small z, in the selected compatible coordinates. Write the normalized lift in the corresponding branch charts as w -> v. The covering identity gives

v^2 = w^2.

On a punctured connected branch disk, continuity forces one constant choice v=w or v=-w. Either choice extends linearly over w=0 and is a smooth local diffeomorphism. The inverse has the same property. Away from ramification the covering is a local diffeomorphism, so the lift is smooth there as well.

This proves that L(s(B3)) consists of orientation-preserving C-infinity diffeomorphisms of N, with C-infinity inverses, identity on a common boundary collar. It is false in general that every smooth map of the base has a smooth lift in the w^2 branch charts; only the verified local translations are used here.

## 4. Exact mapping classes, handedness, and absence of a central offset

Take adjacent embedded arcs e1 from p1 to p2 and e2 from p2 to p3 in D, with disjoint interiors and the usual chain configuration. Their inverse images c1,c2 are simple closed curves in N. In a branch chart at p2, the inverse images of the opposite real rays are the real and imaginary axes; hence c1 and c2 meet transversely once. In particular both are essential.

A half twist h_i about e_i lifts, with the boundary normalization, to a single Dehn twist about c_i. Here is a local annulus model that verifies the power exactly. On an annulus with coordinates (theta,t) in R/2pi Z times [-1,1], take the involution

iota(theta,t)=(-theta,-t).

Its quotient is a disk with two branch points, the images of (0,0) and (pi,0). Choose a smooth rho with rho=0 near -1, rho=1 near 1, and rho(-t)=1-rho(t). The map

tau(theta,t)=(theta+2pi rho(t),t)

is one full annular twist and commutes with iota. At t=0 it interchanges the two branch points. Its quotient is the half twist about their connecting arc. The support boundary is fixed. In the three-branch disk, the preimage of the complement of the two-point support disk is connected because it still contains the third branch point; thus the lift that fixes the external collar is identity on that complement. No boundary twist can be inserted outside the annulus.

Choose the common sign of the two disk half twists so their annular lifts are right Dehn twists in the orientation of N. If another source calls its standard twists left, simultaneously invert both generators; the braid relation survives inversion. Thus write H1,H2 for the disk classes whose normalized lifts are precisely t_c1,t_c2.

Mapping classes also lift without ambiguity. An isotopy in the branch-point-preserving, boundary-fixed homeomorphism group lifts, starting with the normalized lift, through boundary-fixed homeomorphisms of N. This is the covering homotopy property on D*, extended over ramification. Normalization prevents the terminal lift from acquiring a deck involution. Therefore [L(s(H_i))]=[L(h_i)]=t_ci exactly, rather than merely after capping or on homology.

The classical correspondence and the specific three-point example are also recorded in Farb–Margalit, §9.4.1–9.4.2, printed pp.265–268, especially Figures 9.14–9.15 ([university-hosted draft](https://pagine.dm.unipi.it/~a019210/Farb%20Magalit_Primer%20on%20Teichmuller%20theory.pdf)). The annulus calculation above supplies the needed local proof independently.

As a center check, let z=(H1 H2)^3 be the disk full twist, with the compatible handedness. The boundary map has degree two, so its normalized lift turns by pi across the lifted boundary collar and acts as the deck involution on the interior. Its square turns by 2pi across that collar and is identity in the interior: it is one boundary twist delta_N. Thus

L_*(z)=(t_c1 t_c2)^3,  L_*(z^2)=delta_N=(t_c1 t_c2)^6.

In particular one must not identify z itself with delta_N. The twist-class identification above was local and isotopy-theoretic; it did not leave an unknown central correction to be guessed from homology.

## 5. Exact braid relation

Put F=s(H1), G=s(H2), A0=L(F), B0=L(G). Since s is a homomorphism, FGF=GFG. By uniqueness of the boundary-normalized lift,

A0 B0 A0=L(FGF)=L(GFG)=B0 A0 B0.

All maps and inverses are smooth and identity on the same external collar.

## 6. Transfer to the prescribed surface and pair

A compact regular neighborhood M of alpha union beta is an oriented one-holed torus: it is the thickening of the alternating one-vertex, two-loop ribbon graph. The same holds for c1 union c2. There is an orientation-preserving diffeomorphism j:N -> M carrying the two model curve classes, in order, to those of alpha and beta. The curves are unoriented; their auxiliary orientations can be reversed to match the ribbon-graph orientation.

Set A=j A0 j^(-1) and B=j B0 j^(-1) on M and take both to be identity off M. Because the model maps already equal identity on a whole boundary collar, these formulas glue to smooth diffeomorphisms with smooth inverses. Their supports are compact subsets of the interior of M. The relation holds on M and on its complement. Orientation-preserving conjugacy and extension carry right twists to the corresponding prescribed right twists.

This works for every chosen sufficiently small compact regular neighborhood, and it avoids any punctures, marked points, or original boundary disjoint from the pair. It applies in particular to all the negative-Euler-characteristic oriented surfaces in the target. The homeomorphism, C1, every finite Cr, and C-infinity conclusions all follow.

## Scope and historical conclusion

The maps realize the prescribed homomorphism B3 -> Mod(S). If the ambient surface makes an additional word trivial in Mod(S), this construction need not make its actual-map image identity. For example a peripheral boundary twist may vanish after inclusion into a once-punctured torus. No section for every possible ambient image, and no higher-genus full mapping-class section, has been inferred.

Every assertion in the frozen theorem, including the support and boundary improvements, follows by this chain from the prior input. The earliest verified public smooth input is the arXiv posting of 1 February 2018, before the Oberwolfach workshop of 2–8 September 2018. The 2019 publication is also far earlier than the current manuscript. This is a complete prior-consequence certificate for the exact target; an additional later explicit answer is unnecessary for the priority disposition.

