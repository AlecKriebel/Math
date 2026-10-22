# Pointed pseudotriangulation counts: a sufficient condition and a failed universal route

Problem: 5500040 / AMR-054-0040 (TOPP 40).

**Review status.** Accepted as an unresolved partial result by the accompanying independent AI-assisted mathematical audit. The manuscript and audit are unrefereed; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. No novelty or bibliographic priority is established.

This proof-only edition retains all analytic arguments. References below to finite computations, their named fixtures, enumeration counts, certificates, or normal/optimized agreement describe recorded checks from the proof review and independent audit on 10 October 2026. They are historical aggregate metadata, not a reproducibility package. No programs, detailed generated outputs, or fixture datasets are distributed. The six-point coordinates and determinant calculations below are the authored analytic example. Edition preparation reran no mathematical computation and performed no scholarly-source retrieval, source-file rehash, visual inspection, or literature search.

## 1. Exact target and result status

Let S be a finite set of n >= 3 planar points with no three collinear. Let H be its convex-hull vertices and I = S \ H. Triangulations and pointed pseudotriangulations below are straight-line subdivisions of conv(S), have vertex set exactly S, and use no Steiner vertices. Distinct edge sets are counted separately. Write t(S) and ppt(S) for their numbers.

The target is ppt(S) >= t(S) for every S. This document DOES NOT prove or disprove that target. It proves a geometric sufficient condition by an explicit injection, and gives a six-point certificate showing why a containment-only injection cannot work universally. No novelty is claimed for the sufficient condition, its structural input, or the general existence of the containment obstruction.

## 2. Structural input and its exact role

We use the following standard characterization: a noncrossing straight-line graph on S, pointed at every vertex and having exactly 2n-3 edges, is a pointed pseudotriangulation of S. This is Theorem 2.7, items (2) and (4), of Rote, Santos and Streinu, *Pseudo-Triangulations — a Survey*, arXiv:math/0612672v2, physical PDF page 9. In particular, it is a statement about the given embedding, not about some other realization of an abstract Laman graph.

For orientation, the edge count follows from Euler's formula and angle counting. The converse can be obtained by extending a noncrossing pointed graph to an inclusion-maximal pointed graph. The survey's Theorem 2.6 identifies such a maximal graph with a pointed pseudotriangulation, and its Theorem 2.5 gives 2n-3 edges; thus an extension of an already 2n-3-edge graph adds nothing. This use of the characterization handles connectivity and simple-face issues; neither is silently inferred from an edge count alone.

A triangulation on S has 3n-|H|-3 = 2n+|I|-3 edges. Each hull vertex is pointed in every plane graph on S. Each interior vertex of a triangulation is nonpointed, because the incident triangular angles fill a full turn and each is less than pi.

## 3. Exposure witnesses and forced edges

For p in I define

    E(p) = {q in H : p is a convex-hull vertex of S \ {q}},
    r_p = |E(p)|.

Calling q a witness only describes a geometric test; no point is removed from the objects being counted.

Lemma 1. If q is in E(p), every nonpointed straight-line graph vertex p on S must be adjacent to q. Moreover, deleting the edge pq makes p pointed.

Proof. Since p is an extreme point of S \ {q}, and the set is in general position, there is a line through p with every point of S \ {p,q} strictly on one side. Thus all rays from p to those other points lie in one open halfplane. A graph omitting pq is therefore pointed at p. This proves that pq is forced when p is nonpointed. After deleting pq, all remaining incident rays lie in that same open halfplane, so p is pointed. QED.

In particular, every triangulation contains every edge in

    F = {pq : p in I, q in E(p)}.

These are literal fixed geometric edges. Their simultaneous occurrence in a triangulation also ensures they do not cross.

Theorem 2 (explicit sufficient condition). If r_p >= 1 for every p in I, then

    ppt(S) >= (product over p in I of r_p) t(S) >= t(S).

The empty product is 1 when S is convex.

Proof. Let T be any triangulation. Independently choose one q_p in E(p) for each p in I. Put

    D = {p q_p : p in I},       P = T \ D.

All these edges are present by Lemma 1. They are distinct: every one joins its designated interior point to a hull point, so edges designated for different interior points cannot coincide. Hence |D|=|I| and P has exactly 2n-3 edges. P is noncrossing as a subgraph of T. At each interior p, precisely one incident witness edge is removed and Lemma 1 makes p pointed. Deletions for other interior vertices have only their own interior endpoint and a hull endpoint, so this argument is unaffected. Hull vertices remain pointed. The standard characterization in Section 2 therefore says that P is a pointed pseudotriangulation on exactly S.

It remains to prove injectivity, including the witness choices. The fixed set F is contained in every input T, and D is a subset of F. Consequently

    T = P union F,       D = F \ P.

Thus P uniquely determines T, and D uniquely determines the one chosen q_p for each p. This is an injection from the disjoint union of all t(S) triangulations, each with product(r_p) choices, into the pointed pseudotriangulations. QED.

This is a full proof for the stated geometric class, with arbitrarily many points and possibly many interior points. It is not a proof that every S belongs to that class. The predicate r_p >= 1 can fail even with only one interior point.

The exact computational fixture called `two_ear_chains` has four hull vertices, four interior points, and one witness per interior point. Its counts are t=80 and ppt=1476. The theorem proves its inequality without needing those counts. Finite computations do not establish a new infinite-family theorem beyond the condition explicitly proved above.

## 4. A certified obstruction to any universal containment map

Take these five hull vertices in counterclockwise order:

    q0=(-2,0), q1=(-1,-2), q2=(2,-1), q3=(3,2), q4=(-1,3),

and the sole interior point p=(0,0). Let T0 consist of the five hull edges and all five spokes p qi.

All 20 orientation determinants of triples of these six points are nonzero; the recorded independent audit checked them. The coordinates and determinant formulas suffice to check this claim directly. For the five hull edges, every other point is strictly to their left, so the hull is the indicated strictly convex pentagon and p is interior. T0 is its wheel triangulation.

Here is a short exact certificate that T0 contains no pointed pseudotriangulation. A pointed pseudotriangulation has 2*6-3=9 edges, whereas T0 has 10. A contained one would have to retain all five hull edges and delete precisely one spoke. For i=0,...,4, in cyclic order,

    det(q_i,q_(i+1)) = 4, 5, 7, 11, 6,
    det(q_(i-1),q_(i+1)) = 5, 2, 4, 5, 4.

Every original gap between adjacent spokes is in (0,pi). On deleting spoke p qi the only merged gap is the counterclockwise angle from q_(i-1) to q_(i+1). It is less than 2pi, and its positive determinant proves it is less than pi. All gaps therefore remain below pi, so p is still nonpointed. No spoke deletion works. QED.

Consequences:

1. The assertion that every triangulation contains a pointed pseudotriangulation is false.
2. There cannot be a universal injection T -> P with P a subgraph of its input T. Indeed T0 has no eligible output at all.
3. A Hall-matching argument whose only allowable pairs are edge containments already fails on the singleton {T0}.
4. This is NOT a counterexample to the requested counting inequality. Exact enumeration gives t(S)=11 and ppt(S)=25. Of the eleven triangulations, one contains zero PPTs, five contain two, and five contain three. Every PPT here has a unique triangulation refinement, so 25=0+5*2+5*3.

The phenomenon of triangulations without contained PPTs is already acknowledged by TOPP 50, with a reference to O'Rourke's 2002 computational geometry column. This note supplies a compact analytic coordinate certificate; recorded verification is supporting metadata, not a claim to first discovery.

## 5. One interior point: exact fibers and the known formula

Suppose p is the sole interior point. In a PPT every hull vertex has its reflex angle outside conv(S), while p has exactly one reflex angle in the subdivision. Hence there is exactly one nontriangular face: a concave quadrilateral with reflex vertex p. All other faces are triangles. That concave quadrilateral has a unique interior diagonal, so every PPT has exactly one triangulation refinement.

For a triangulation T, let the cyclic angles between its k spokes at p be alpha_1,...,alpha_k. Each alpha_j lies in (0,pi), and their sum is 2pi. Define

    d_p(T) = #{j : alpha_(j-1) + alpha_j > pi}.

Deleting spoke j gives a PPT exactly in this case. The two triangles merge into a quadrilateral; it has a reflex corner at p precisely when the sum exceeds pi. Thus

    ppt(S) = sum over T of d_p(T),
    ppt(S)-t(S) = sum over T of (d_p(T)-1).

For k=3, d_p(T)=3. For k=4, d_p(T)=2, since opposite pair-sums add to 2pi and no pair-sum equals pi. For k>=5, d_p(T) can be zero, as the certificate above shows. A termwise proof d_p(T)>=1 therefore fails.

The global compensation is nevertheless known: Randall, Rote, Santos and Snoeyink, *Counting triangulations and pseudo-triangulations of wheels* (CCCG 2001), prove

    ppt(S)-t(S) = C_(n-2),       C_m = binomial(2m,m)/(m+1).

This theorem is credited to that paper, not claimed as a result of this note. The six-point counts have difference 25-11=14=C_4. The sufficient-condition theorem above does not cover this central wheel; the known wheel theorem does.

## 6. General exact identity and the remaining gap

For an arbitrary S, let R(P) be the number of triangulation refinements of a PPT P. It is positive, since each simple pseudotriangle can be triangulated using its existing vertices. Counting each P with total weight one over its refinements gives the exact identity

    ppt(S) = sum over triangulations T of
             sum over PPTs P contained in T of 1/R(P).

This double-counting identity is not a solution: the inner sum can vanish, as T0 shows. The required assertion is that its average over all T is at least one. No global compensation inequality establishing that assertion has been proved here.

The fixed-edge route applies when all r_p are positive; it stops as soon as a needed interior point has no exposure witness. The exact `two_deep_interior_pentagon` fixture has two interior points with r_p=0 for both. Its finite inequality is verified computationally, but the construction in Section 3 provides no map for it. Even proving the finite samples and citing the already known one-interior-point case leaves arbitrary larger configurations open.

The stronger layer-by-layer monotonicity conjecture of Aichholzer, Orden, Santos and Speckmann has not been used as an assumption. Convex-position minimization across different point sets, upper bounds on ppt(S), and Carpenter's-rule results do not fill this gap.

## 7. Credit, scope, and recorded checks

- TOPP 40 supplies the per-set problem and records it as open. Its equality-only-in-convex-position companion is stronger than the target here.
- Aichholzer, Orden, Santos and Speckmann, arXiv:math/0601747v2 (2007; JCTA 115 (2008), 254-278), establish special-family results including almost-convex sets/double circles and single/double chains. Those are prior work.
- The arXiv:1210.7126 source is by Moria Ben-Ner, Andre Schulz, and Adam Sheffer, **not** Sharir and Sheffer. Its Section 5, physical page 14, restates the comparison conjecture; its upper bounds do not prove it.
- Rote, Santos and Streinu, arXiv:math/0612672v2, Theorem 2.7, supplies the embedding-specific characterization used in Theorem 2.
- The one-interior-point identity belongs to Randall, Rote, Santos and Snoeyink (2001).
- The recorded original enumeration used exhaustive edge-subset enumeration and exact integer determinants, rather than a floating-point drawing or a random search. It covered only the named coordinate fixtures. Its normal and optimized Python outputs agreed exactly. Those detailed outputs are not distributed in this proof-only edition.

Final classification: **ACCEPTED UNRESOLVED PARTIAL; rigorous sufficient condition and an analytic obstruction to a stronger proof route.** The accompanying mathematical audit found no defect or required mathematical correction. The universal per-set inequality remains unresolved by this work. Acceptance does not certify novelty, bibliographic priority, or exhaustive worldwide current-openness research. All analytic conclusions are independent of omitted programs and detailed generated outputs.
