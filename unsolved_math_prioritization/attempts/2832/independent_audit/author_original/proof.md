# Common stabilization at height 2g: exact reductions and the remaining gap

Problem: KP-3.34, public problem ID 2832. Date: 2026-10-06.

## Outcome and conventions

This is a stopped partial investigation, not a solution or refutation. The results below are elementary structural reductions; no novelty is claimed.

Fix a connected, closed, orientable 3-manifold M. An ordered splitting P consists of a Heegaard surface and a labeling of its two handlebodies. Equivalence means ambient isotopy of M preserving those labels. Write g(P) for its genus. Orientability of M does not by itself specify whether equivalence must preserve the handlebody order.

The target assertion is: for every integer g and every two ordered genus-g splittings P,Q of every such M, there is an ordered common stabilization of genus at most 2g. This means at most g stabilizations of each initial splitting. The genus g is the given splitting genus, not necessarily the minimum Heegaard genus of M. No irreducibility, non-Haken, or hyperbolicity hypothesis is imposed.

K3, Problem 3.34, printed p.156, states the genus-g stabilization question without spelling out the ordering convention in that paragraph. Its cited sharpness theorem [HTT] uses ordered handlebodies and isotopy. We therefore analyze that stronger ordered interpretation and explicitly keep the unordered version separate. Ordered upper bounds imply unordered upper bounds. The sharp ordered lower examples do not automatically transfer to unordered equivalence.

## Standard input

Ordinary stabilization is well-defined on ordered ambient-isotopy classes. For each P and each integer h >= g(P), denote by P[h] its stabilization to genus h. Two stabilizations of the same ordered splitting with the same final genus are isotopic, and P[h][k] = P[k] for k >= h. These standard facts can be seen by using disjoint small balls meeting the surface in disks to perform the connected sums with the standard genus-one splitting of S^3; moving the balls and permuting the local summands preserves the resulting ordered isotopy class. The standard uniqueness statement is also recorded in [JF], Section 4, immediately after Definition 10. Reidemeister-Singer ensures that any pair eventually has a common stabilization.

Define c(P,Q) to be the least h for which P[h] and Q[h] are ordered-isotopic. It exists, and c(P,Q) >= max(g(P),g(Q)). All statements below also hold if unordered isotopy is used consistently throughout.

## Proposition 1: exact truncation of stabilization towers

For a >= g(P) and b >= g(Q),

    c(P[a], Q[b]) = max(c(P,Q), a, b).

Proof. Every common stabilization T of P[a] and Q[b] is also a stabilization of P and Q. Thus g(T) is at least c(P,Q), a, and b. Conversely, put h = max(c(P,Q),a,b). Stabilize a minimal common stabilization of P and Q to genus h. By uniqueness at a fixed genus, it is both P[h] = P[a][h] and Q[h] = Q[b][h]. This gives the matching upper bound. QED.

For equal initial genus g, define the stabilization deficit d(P,Q)=c(P,Q)-g. If each input is stabilized r times, Proposition 1 gives the exact law

    d(P[g+r], Q[g+r]) = max(d(P,Q)-r, 0).

Thus stabilizing both inputs consumes the existing deficit one unit at a time. This law gives no independent upper bound on the initial deficit.

## Proposition 2: an ultrametric inequality

For any three splittings of the same M,

    c(P,R) <= max(c(P,Q), c(Q,R)).

Proof. Let h be the maximum on the right. At genus h, uniqueness of stabilization gives P[h] = Q[h] and Q[h] = R[h] as ordered isotopy classes. Hence P[h] = R[h]. QED.

On the set of ordered genus-g splitting classes, d=c-g is consequently an integer-valued ultrametric: it is symmetric, nonnegative, vanishes exactly for equal classes, and satisfies d(P,R) <= max(d(P,Q),d(Q,R)). In particular, a chain of genus-g splittings with adjacent common genus at most 2g proves the same bound for the endpoints; the number of links does not accumulate a stabilization cost. This is a sufficient local-to-global strategy, not a construction of such chains.

## Proposition 3: the correct reduction to unstabilized cores

Call a splitting unstabilized if it is not the ordinary stabilization of a lower-genus splitting. Repeated destabilization terminates because genus decreases. Choose unstabilized cores P0,Q0 for P,Q, with genera p,q. The cores need not be unique.

If g(P)=g(Q)=g, then Proposition 1 yields

    c(P,Q) = max(c(P0,Q0), g).

Consequently the universal equal-genus target is equivalent to the following assertion about possibly unequal-genus unstabilized cores:

    c(P0,Q0) <= 2 max(p,q)
    for every pair of unstabilized cores in the same M.

Proof of sufficiency. Put k=max(p,q)<=g. The asserted core bound gives c(P,Q)<=max(2k,g)<=2g.

Proof of necessity. Given cores of genera p,q, stabilize both to k=max(p,q). The equal-genus target gives c(P0[k],Q0[k])<=2k. Proposition 1 then gives max(c(P0,Q0),k)<=2k. QED.

The unequal genera cannot be omitted: destabilizing an equal-genus pair can produce cores of different genera. This is the gap in a reduction that checks only equal-genus unstabilized pairs.

A further consequence is useful for a hypothetical counterexample. Choose the smallest initial genus g of any equal-genus counterexample. Its two splittings cannot both be stabilized. Otherwise write them as P0[g],Q0[g] for genus-(g-1) splittings. Proposition 1 and c(P,Q)>2g force c(P0,Q0)>2g>2(g-1), contradicting minimality. This conclusion says at least one input is unstabilized, not that both are.

## Proposition 4: bounded-height paths are equivalent certificates

For an integer H, form a graph whose vertices are ordered splitting classes of M of genus at most H. Join two classes by an edge when one is an ordinary one-step stabilization of the other. Isotopic splittings are the same vertex.

For any P,Q in this graph, they lie in the same component if and only if c(P,Q)<=H.

Proof. If c(P,Q)<=H, ascend from P and Q by ordinary stabilizations to a minimal common stabilization and traverse one ascent backwards. Conversely, take a finite path. Stabilize every vertex on it to genus H. The two endpoints of each edge become the same genus-H class by uniqueness of stabilization. Induction along the path gives P[H]=Q[H], hence c(P,Q)<=H. QED.

Therefore, a Cerf-theoretic or diagrammatic proof of the target must supply, for arbitrary genus-g endpoints, a stabilization/destabilization path with every vertex at genus at most 2g. Mere eventual connectivity is insufficient. A diagram move argument must also justify passage to the ordered ambient-isotopy classes used here.

## Geometric route and its precise missing step

[JU], Lemma 3, states a sweep-out construction: for genera p,q, a suitably positioned spine of the designated handlebody of the second splitting, with n locally maximal horizontal components relative to a sweep-out of the first, yields a common stabilization of genus at most p+q+n-1. The complement-handlebody argument and side convention are part of that lemma; counting graph cycles alone is insufficient.

For p=q=g this bound meets 2g when n=1. No proof was found that every pair admits that single-maximum position with the required spine and ordering conditions. This is a sufficient geometric hypothesis only, not a necessary characterization and not an established global normal form.

The same manuscript's Theorem 1 states a genus bound 3p/2+2q-1 for both equivalence conventions. Even if accepted, for g>=1 its equal-genus specialization permits floor(7g/2-1), rather than establishing 2g in general. We treat [JU] as an inspected preprint, not as a newly verified peer-reviewed theorem; the structural propositions above do not depend on its global bound.

## Why the known lower examples do not refute the target

[HTT], Theorem 1.1, supplies ordered genus-g pairs requiring g stabilizations for every g>1. Those examples meet the proposed upper bound. Their two initial surfaces are the same surface with opposite orderings, so forgetting order makes them identical from the start. [HTT] explicitly warns that its theorem does not directly establish the corresponding claim for unordered surfaces or equivalence by homeomorphism.

[JF], Theorem 1, bounds the final flip genus below by min(2g,d_H/2), where d_H is Hempel distance; its introduction also records the 2g flip upper bound. Thus this particular obstruction can force sharpness at 2g but cannot on its own force a flip genus greater than 2g. Final genus must not be confused with the number of added handles.

## Exact unresolved obligation

The missing global statement is c(P,Q)<=2g for arbitrary ordered genus-g pairs in an arbitrary connected closed orientable M. Equivalently, it is the unequal-core inequality of Proposition 3 or the bounded-height connectivity statement of Proposition 4. None of the formal reductions establishes it. No counterexample with c(P,Q)>2g was constructed. No mathematical computation or exhaustive search is claimed.

## References

- [K3] Baykur, Kirby, Ruberman (editors), K3: A New Problem List in Low-Dimensional Topology, author preliminary version, Problem 3.34, printed p.156. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [HTT] Joel Hass, Abigail Thompson, William Thurston, Stabilization of Heegaard splittings, Geometry & Topology 13 (2009), 2029-2050. https://msp.org/gt/2009/13-4/gt-v13-n4-p05-p.pdf
- [JF] Jesse Johnson, Flipping and stabilizing Heegaard splittings, arXiv:0805.4422v1 (2008), Theorem 1, introduction, and Section 4. https://arxiv.org/abs/0805.4422
- [JU] Jesse Johnson, An upper bound on common stabilizations of Heegaard splittings, arXiv:1107.2127v1 (2011), Theorem 1 and Lemmas 2-3. https://arxiv.org/abs/1107.2127
