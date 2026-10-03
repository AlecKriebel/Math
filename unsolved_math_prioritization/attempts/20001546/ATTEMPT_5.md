# Attempt 5: a proper Helly action and the exact cocompactness gap

Recorded 2026-10-03 UTC. Outcome: a proper action on a locally finite Helly
graph follows from established hull results; cocompactness is not proved or
refuted. The original AIM problem remains unresolved after five attempts.
Budget: 5/5. No sixth proof attempt is undertaken in this pass.

## Construction

Let Q=Cay(A,S) be the finite-degree graph explicitly specified in Attempt 1.
Haettel–Huang's cyclic-type construction and their weakly modular quotient
result give that Q is weakly modular. Let E(Q) be its injective hull, with the
canonical isometric embedding of Q, and let H(Q) be its integer-valued Helly
hull. Graph automorphisms of Q extend canonically to both hulls, so left
multiplication induces A-actions.

**Exact weak-modularity citation and identification.** Haettel–Huang,
*Lattices, Garside structures and weakly modular graphs*, Theorem 5.7,
https://arxiv.org/html/2211.03257v2, proves weak modularity of the weak Cayley
graph of a weak Garside group and of its quotient by the Garside automorphism.
Apply this to the constructed Garside structure on A x Z. Its Garside element
is (1,1), so quotienting by that element removes exactly the central Z factor.
The proof of Corollary 4.5 in *New Garside structures and applications to Artin
groups*, https://arxiv.org/html/2305.11622v2, identifies the resulting Bestvina
complex with the flag Cayley complex on the lifted union of dual intervals.
That union is precisely {1,a,b,c,d,e,f,p,q,r} from Attempt 1. Consequently its
1-skeleton is the particular Q used here, which is therefore weakly modular.

The following inputs are established results, not new theorems of this pass:

1. Every weakly modular graph has 1-stable intervals: Chalopin–Chepoi–Genevois–
   Hirai–Osajda, *Helly groups*, Geometry & Topology 29 (2025), Lemma 6.5.
2. A locally finite graph with stable intervals has a proper injective hull:
   Lang's theorem, quoted there as Theorem 6.4.
3. The integer-valued hull is a Helly graph, has its supremum metric equal to
   its graph metric, and embeds in E(Q). Its distinct vertices are at least
   distance 1 apart. Therefore properness of E(Q) implies local finiteness
   of H(Q).

Primary sources: https://msp.org/gt/2025/29-1/gt-v29-n1-p01-p.pdf and
https://arxiv.org/abs/1107.5971. Q is locally finite because S is finite.
Thus all three inputs apply.

## Properness of the extended action: explicit proof

Choose the identity vertex o in Q. The action of A on Q is proper, since
only finitely many group elements lie in any fixed word ball. Let y be any
point of E(Q), and write D=d(y,o). If d(y,gy)<=R, then

    d(o,go) <= d(o,y)+d(y,gy)+d(gy,go) <= 2D+R.

Only finitely many g satisfy this bound. To obtain properness on compact
sets, enclose a compact K in B(y,M). If gK meets K, then d(y,gy)<=2M.
The preceding bound gives finitely many such g. Hence A acts properly on
E(Q), and therefore properly on H(Q).

In particular, this produces a locally finite Helly graph with a proper
A-action, overcoming the properness failure of the extended Deligne model.
It is a deduction of published results, and no novelty is claimed. It does
not show cocompactness. Since A is torsion-free (for example, because A x Z
is Garside), the proper action also has trivial vertex stabilizers.

## Cocompactness is exactly the bounded-hull question

The vertex orbit A.o is precisely the embedded copy of Q. Therefore the
following are equivalent for this particular canonical construction:

    (i) A acts cocompactly on H(Q);
    (ii) there is a constant C such that every vertex of H(Q) is within C of Q;
    (iii) Q is coarsely Helly.

For (i)->(ii), choose finitely many vertex-orbit representatives in the locally
finite graph. Each has finite distance to o, giving a uniform bound. For
(ii)->(i), translate the nearby point of Q to o. Every orbit then meets the
finite ball B_H(o,C), giving finitely many vertex orbits and hence finitely
many edge orbits by local finiteness.

For the equivalence with (iii), use the bounded-distance characterization of
Helly hulls (Chalopin et al., Proposition 3.12; also Haettel's lecture notes,
Proposition 9.14). One direction can be seen directly: intersect the pairwise
compatible balls in H(Q), then choose a Q-vertex within C of their common
vertex. It lies in all original balls after enlarging their radii by C.
The reverse direction follows by applying coarse Hellyness to the radii given
by distances from a hull vertex and using the hull's extremal-distance-function
characterization. This standard theorem is cited rather than silently assumed.

Equivalently, the missing statement is the existence of a single integer C>=0
such that for every finite collection of centers g_i in A and integer radii r_i
with d_Q(g_i,g_j)<=r_i+r_j, some x in A satisfies

    d_Q(x,g_i)<=r_i+C for every i.

Finite families suffice because Q is locally finite: once one enlarged ball
is fixed, its finite vertex set turns the finite-intersection property into
a common vertex for any larger family.

## Final effort and obstruction audit

The original triangle test implies C cannot be 0. The certified tests of Q^2
and Q^3 do not exclude C=1 or any other fixed C. The exact all-scale family of
Attempt 2 gives a concrete candidate for proving unbounded defect, but the
necessary distance/intersection control is still missing. Neither the
non-Helly Coxeter quotient nor the tree-fiber obstruction supplies it.

Thus this attempt establishes properness and local finiteness of a canonical
Helly completion, and removes stable intervals as an additional unknown.
The only undecided condition for THIS completion is coarse Hellyness of Q.
A positive answer would solve AIM 4.2; a negative answer would only exclude
this hull construction and would still not rule out unrelated geometric
Helly actions of A.

## Final verdict

No proper cocompact Helly action of A has been constructed, and no obstruction
to all such actions has been proved. The original problem is UNSOLVED in this
five-attempt pass. The deliverable contains scoped partial results and exact
finite certificates, with no claim of full resolution or historical priority.
