# Collared finite-shape quotients do not prove movability

Problem 30003527 / OWR-15575-006, queue row 1767. Authored 13 October 2026 within shared substantive pass 3. This is a structural obstruction to a proposed proof method, not a counterexample to the flow question. No novelty claim is made.

## Results and scope

1. For a tame isolating block N of a continuous flow, put E=N^i, D=N^+, L=n^+, and K=Inv(N). The inclusion L into D has a genuine collar and is an NDR cofibration. Moreover, D/L has the shape of the finite polyhedron N/E. The latter is a shape assertion, not a claim of actual finite homotopy type.
2. These facts do not prove that D or K is movable. There is a compact metric pair (D_*,L_*) with L_* a collared circle, D_*/L_* of circle shape, and D_* nonmovable. It even has a compact remainder K_* with D_* minus K_* homeomorphic to L_* times [0,infinity), and continuous translation toward K_* giving homeomorphic nested tails with intersection K_*.
3. The example is not realized inside a three-manifold isolating block. It therefore does not refute movability of all isolated invariant sets or the requested invariant-enlargement theorem. It identifies why the ambient three-dimensional geometry cannot be dropped from a proposed positive proof.

## 1. The actual stable trace is collared

Use the continuous signed entry-time function t^i:N to [-infinity,0] of a tame block. If p lies in D minus K, then p is not in N^-, so t^i(p) is finite. Its backward entry point lies in L. Consequently

F:L times [0,infinity) to D minus K, F(l,s)=phi(s,l)

is a homeomorphism. Its inverse is p mapped to (phi(t^i(p),p),-t^i(p)). Injectivity follows from the uniqueness of the entry point: a positive trajectory starting at entry cannot meet entry again while staying inside N. Continuity of the inverse follows from the block entry-time property.

For each finite a, F(L times [0,a]) is compact and disjoint from K. An open initial collar is given by -t^i<a in D; it contains L. Hence L is genuinely collared, even when L is a wild compact subset of E.

For completeness, let s denote the collar coordinate and set u=min(1,2s) on the collar, u=1 on K. Move s to s-r h(s), for r in [0,1], where h(s)=s for 0<=s<=1/2, h(s)=1-s for 1/2<=s<=1, and h(s)=0 for s>=1. Fix K. This continuous homotopy fixes L, is the identity outside a compact initial collar, and at r=1 sends every u<1 point to L. Thus (D,L) is an NDR pair. If L is empty, the collar assertion is vacuous.

## 2. The quotient really has finite-polyhedral shape

Assume first E is nonempty. On N define the stopped backward semiflow

psi_t(p)=phi(max(-t,t^i(p)),p), t>=0.

The convention at t^i=-infinity gives phi(-t,p). This semiflow fixes E pointwise and descends to the compact ANR Q=N/E. The pair (N,E) is triangulable, so Q has finite-polyhedral type. The argument also works using a finite-polyhedral model of that pair.

Write N_t^+ for the points whose trajectory remains in N throughout [0,t]. Directly from the stopped-flow formula,

psi_t(N)=E union N_t^+.

Indeed, a point not stopped on E stays in N for t units after its new position; conversely y in N_t^+ is the image of phi(t,y). Therefore the compact images M_t=psi_t(Q) are nested and their intersection is

C=(E union D)/E, homeomorphic to D/L.

If L is empty, this notation means D with a disjoint basepoint. The quotient statement then applies to that based disjoint union. If E is empty, use Q=N and C=D directly.

The image sets M_t are cofinal among neighborhoods of C in Q, by the nested-compact-set argument. Also psi_s(C)=C: backward-stopped motion preserves D, and every point of D has a forward preimage in D. Thus C is invariant under this semiflow.

Here is an explicit shape argument, rather than an inference from cohomology. Choose a decreasing cofinal sequence of ANR neighborhoods V_n of C in Q. Choose increasing times T_n with M_(T_n) contained in V_n. The maps

r_n=psi_(T_n):Q to V_n

are compatible up to homotopy: between times T_n and T_m, m>=n, every image lies in M_(T_n), hence in V_n. Their composites with V_n into Q are homotopic to id_Q through psi_t. Conversely, for each n, invariance of C and compactness of [0,T_n] allow an m so small that psi_[0,T_n](V_m) lies in V_n. On V_m the same time homotopy joins r_n to the neighborhood inclusion. These are the two inverse identities in the shape category. Hence inclusion C into Q is a shape equivalence.

This verifies the finite-shape quotient by explicit homotopies. It does not turn D into a finite polyhedron, and does not assert that C has the actual homotopy type of Q.

The block input is the continuous entry-time property and existence of tame blocks from J. J. Sanchez-Gabites, *Using an invariant knot of a flow to find additional invariant structure*, arXiv:2403.18805v1, sections 2.3 and 5.4. The stopped-flow construction occurs in the proof of Proposition 5(ii). The shape upgrade above is the authored argument, separate from that proposition's cohomology statement. Public source: https://arxiv.org/html/2403.18805v1 .

## 3. A proper self-embedding of the rank-two free group

Let G be a rose with oriented loops a,b based at v, and let f:G to G fix the a-circle pointwise and traverse

f(b)=b a b^(-1) a^(-1) b.

Choose the usual piecewise linear parametrization. It is onto G. On the free group F=pi_1(G,v), write alpha=f_*.

The subgroup alpha(F) is proper and alpha is injective. To see this without invoking an automorphism classification, subdivide the image of b into a five-edge circle spelling b a b^(-1) a^(-1) b and wedge it with the a-loop. This labeled graph is already folded: at its basepoint the outgoing labels are a,a^(-1),b,b^(-1); at every other vertex the two outgoing labels are different. Its map to G is therefore an immersion and injective on pi_1. The a-loop and the five-edge circle form a free basis of its rank-two fundamental group. The path labeled b from the basepoint is not closed, so b is not in its represented subgroup. This proves injectivity and properness.

Let H_n=alpha^n(F), n>=0. Injectivity and properness imply H_(n+1) is a proper subgroup of H_n for every n. All H_n have rank two.

## 4. Nonmovability, including unbased homotopies

Set X=lim(G <-f- G <-f- ...). This inverse sequence of finite polyhedra is a shape expansion of its compact metric inverse limit.

We use the following classical free-group fact: every ascending sequence of finitely generated subgroups of a free group whose ranks have a common finite bound eventually stabilizes (Takahasi-Higman). A full proof is Theorem 14.1 of I. Kapovich and A. Myasnikov, *Stallings foldings and the subgroup structure of free groups*, J. Algebra 248 (2002), 608-668. Public primary-author version: https://arxiv.org/abs/math/0202285 . Author-hosted PDF: https://web.stevens.edu/algebraic/alexeim/Teaching/GroupTheory626/graph5.pdf .

An immediate consequence is that no finitely generated subgroup H of a free group is properly contained in a conjugate gHg^(-1). Otherwise iteration of that conjugation gives an infinite strictly ascending chain of subgroups all of rank rank(H).

Suppose X were movable. Apply the unbased inverse-system movability criterion at stage zero. Some j would have the following property: for every k>=j there is r:G_j to G_k for which f^j is homotopic to f^k composed with r. Take k>j. On fundamental groups an unbased homotopy allows a conjugating element g, so it forces

H_j contained in g H_k g^(-1).

Since H_k is properly contained in H_j, this gives H_k properly contained in g H_k g^(-1), contradicting the preceding consequence of Takahasi-Higman. Thus X is not movable. This argument does not silently replace unbased movability by pointed movability.

The abelianization of alpha is the identity. In particular the integral first Cech cohomology of X is Z^2, and its ordinary first homology bonding maps are identities. These algebraic facts do not imply movability.

## 5. Add a genuine collar before taking the quotient

Because f fixes the a-circle pointwise, X contains its constant inverse-limit copy A, homeomorphic to S^1. Form

D_*=X union_A (A times [0,1]),

where (a,1) is identified with a in X. Let L_*=A times {0}. This is a compact metrizable adjunction space. The outer end L_* has an actual product collar; it is a movable circle and its inclusion is an NDR cofibration. Collapsing the cylinder toward height 1 strongly deformation retracts D_* onto X. As movability is a shape invariant, D_* is not movable.

The quotient must be analyzed after this collar attachment. It is the mapping cone of A into X, and cannot be replaced without proof by X/A.

At finite stage attach the same cylinder to the a-circle of G, obtaining P_n=G union_A (A times [0,1]), with bonding map f on G and the identity on the cylinder. Their inverse limit is exactly D_*: a sequence in the interior of the cylinder has that same cylinder coordinate at every stage; all remaining sequences give X. This compact-to-Hausdorff identification is a homeomorphism.

Collapsing all copies of L_* commutes with this inverse limit. To check directly, a sequence in the quotient system that is non-basepoint at one stage is non-basepoint at every later stage, has unique compatible lifts there, and hence a unique inverse-limit lift. The all-basepoint sequence corresponds exactly to L_*. Compactness then makes the induced bijection a homeomorphism.

Each P_n/L_* is G with a disk attached along the a-circle. It is the wedge of a disk and the b-circle, so has homotopy type S^1. The induced bonding map has degree one on that circle, because the exponent sum of b in f(b) is one. Each quotient bonding map is therefore a homotopy equivalence. The quotient inverse limit, D_*/L_*, has shape S^1.

We have proved all three asserted abstract properties: collared movable L_*, finite-circle quotient shape, and nonmovable D_*.

## 6. Even the internal stable-tail pattern is present

Put K_*=X inside D_*. Then D_* minus K_*=A times [0,1), homeomorphic to L_* times [0,infinity). Use the age coordinate s=-log(1-t), where t is cylinder height. Positive translation s mapped to s+r extends continuously to D_* by fixing X pointwise: as s tends to infinity, the cylinder point tends to the corresponding point of A in X, and a finite translation has the same limit.

At time r>=0 the map is an embedding of D_* onto the compact tail

D_r=X union (A times [1-exp(-r),1]).

The tails are nested, homeomorphic to D_*, cofinal at X, and have intersection X. This is the same abstract compactification/positive-semiflow pattern available in a stable set. A full flow exists on the locally compact space obtained by extending the collar age to all real numbers and retaining X as its limiting end, but that space is not asserted to be a manifold.

Thus the internal stable-tail pattern does not repair the failed abstract implication either. In an actual three-dimensional flow the entry/exit embedding and the geometry of the rest of the block must supply an additional essential condition.

## 7. What this does and does not settle

This report rules out the proof shortcut

movable entry trace + collar/cofibration + finite-shape quotient (+ internal stable tails) implies movable invariant set.

It does not rule out a theorem with the full three-dimensional isolating-block hypotheses. In fact X has finite H^0 and H^1, so the accepted finite-cohomology isolated-flow theorem already excludes its realization as an isolated invariant compactum in R^3. No flow, compact invariant A, and prescribed open U excluding all movable invariant supersets is constructed here. Nor is a movable enlargement supplied for an arbitrary flow. The unrestricted row-1767 target remains unresolved.

No source text, dataset, private notes, or external correspondence is included. The two external mathematical inputs are the standard inverse-system characterization of shape movability and the explicitly cited Takahasi-Higman theorem; all quotient and flow-collar claims are proved above. Independent audit is still required before importing the new assertions as accepted results.
