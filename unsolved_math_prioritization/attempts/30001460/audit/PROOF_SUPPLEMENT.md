# Scheme-level supplement to the K-sheet gluing criterion

This is an independently authored clarification of the frozen proof for problem 30001460. It does not change the author archive. All schemes are over an algebraically closed field of characteristic zero unless a base change is expressly made. The quotient is allowed to be nonseparated.

## 1. Exact hypotheses and source interface

Let G be the connected adjoint group, and let K be the connected subgroup with Lie algebra ad_g(kappa), where kappa is the fixed Lie subalgebra. For each chosen nilpotent e_i in the reduced sheet S, set T_i = S intersect (e_i + p^{f_i}) with its reduced locally closed scheme structure. Put U_i = K.T_i.

The proof needs these precise inputs:

- The U_i form a finite open cover, and the action a_i: K x T_i -> U_i is smooth and surjective. Bulois–Hivert supplies the open-cover and smooth-action statements in Propositions 2.4(v), 2.5(ii), 2.8 of the inspected v2 manuscript.
- S lies in a single G-sheet. Its Slodowy slice Q_i admits a G-invariant morphism psi_i: S_G -> Q_i with psi_i restricted to Q_i equal to the identity. Bulois's Lemma 3.6 and Theorem 3.7 give this when the adjoint centralizer G^{e_i} is connected.

These are stronger than density of U_i or finite intersection with G-orbits. The original OWR Question 1 does not explicitly impose separatedness; the present convention must remain visible.

## 2. Factoring the morphism through the reduced slice

A general elementary fact is useful. Suppose X is a reduced finite-type k-scheme, Z is a reduced locally closed subscheme of Y, and a morphism f:X->Y has set-theoretic image in Z. Write Z as a closed subscheme of an open W in Y. First f factors through W. Locally on W, any function in the ideal of Z pulls back to a function zero at every point of X, hence zero because X is reduced. Thus f factors uniquely through Z.

It is enough here to check the image on closed k-points: by constructibility, a nonempty image outside Z would contain a closed k-point. Every such x in U_i is k.t for some t in T_i. G-invariance gives psi_i(x)=psi_i(t)=t. The elementary fact therefore gives a scheme morphism q_i:U_i->T_i and q_i s_i=id, where s_i is the inclusion. The identity q_i a_i=pr_2 is scheme-theoretic: compose both sides with the immersion T_i->Q_i and use G-invariance of psi_i.

Notice the restriction to U_i. If two K-orbits in S lie in the same G-orbit, they need not belong to the same U_i. For any x,y in U_i with equal q_i-value t, however, both are K-conjugate to t. This is exactly why the restriction is safe.

## 3. Fibers, openness, and invariant functions

The fiber claim extends to every algebraically closed field extension Omega/k without assuming a new theorem about base-changed sheets. Given x in U_i(Omega), smooth surjectivity of a_i supplies (g,t) in K(Omega) x T_i(Omega) mapping to x. The equality q_i a_i=pr_2 forces t=q_i(x). Thus the geometric fiber over t consists precisely of K(Omega).t.

For an arbitrary base change B->T_i, the map a_{i,B}:K x B->U_i x_{T_i} B is still smooth and surjective. Its composite with q_{i,B} is projection to B. For every open W in the base-changed U_i,

    q_{i,B}(W) = pr_B(a_{i,B}^{-1}(W)).

The projection is smooth, hence open. Therefore q_i is universally open and surjective.

On an open V in T_i, let F be an invariant regular function on q_i^{-1}(V), and put f=s_i^*F. Invariance and q_i a_i=pr_2 give a_i^*F=a_i^*q_i^*f. The restricted action cover K x V->q_i^{-1}(V) is faithfully flat, so F=q_i^*f. Conversely q_i^*f is invariant, and the section proves injectivity. This proves the equality of sheaves O_{T_i}=(q_{i*}O_{U_i})^K on all opens. No affineness of U_i or unjustified exactness of an invariant functor is involved.

For an invariant morphism h:U_i->Y to an arbitrary scheme, take h_i=h s_i. Then h and h_i q_i agree after the same smooth surjection. Morphisms of schemes form an fpqc sheaf, so they agree before pullback. This applies to nonseparated Y as well. Only faithfulness is needed here; one is not descending an unspecified scheme. See [Stacks, Tag 023Q](https://stacks.math.columbia.edu/tag/023Q).

## 4. Explicit scheme-theoretic inverse and cocycle argument

Set U_{ij}=U_i intersect U_j and T_{ij}=s_i^{-1}(U_j). These are open. The equality q_i^{-1}(T_{ij})=U_{ij} follows because U_j is K-stable and every q_i-fiber is one orbit. The map phi_{ij}=q_j s_i restricted to T_{ij} has image in the open T_{ji}, again by K-stability.

Here is a direct cover on which the inverse identity can be checked. Pull the smooth surjection a_j:K x T_j->U_j back along s_i:T_{ij}->U_j. The resulting scheme E->T_{ij} is a smooth surjection. On E there are universal elements g,t_j,t_i with

    g.t_j = t_i,       t_i in T_{ij},       t_j in T_{ji}.

The last membership follows as a scheme-theoretic open factorization from K-stability of U_i. Pulling phi_{ij} back to E gives t_j because q_j(g.t_j)=t_j. Pulling phi_{ji} phi_{ij} back gives q_i(t_j)=q_i(g.t_j)=q_i(t_i)=t_i. Faithfulness of pullback along E->T_{ij} proves phi_{ji} phi_{ij}=id as morphisms.

For a triple overlap, use the same cover, now restricted to t_i in T_{ij} intersect T_{il}. K-stability of U_l puts t_j in U_l. On this cover,

    q_l(t_j)=q_l(g.t_j)=q_l(t_i).

This is phi_{jl} phi_{ij}=phi_{il}. It also proves the required equality of overlap domains: membership in U_l is preserved under the transition. Thus the full gluing data, including domains and cocycle, hold schematically, not only on k-points.

Ordinary open gluing gives a scheme Q with charts T_i; no algebraic-space-to-scheme shortcut is used. See [Stacks, Section 26.14](https://stacks.math.columbia.edu/tag/01JA). Its chart preimages are exactly U_i. Since there are finitely many finite-type charts, Q is finite type. The local quotient properties and the categorical factorizations glue. No step claims Q is separated.

## 5. Type A: avoid both central-cover and center-sign ambiguities

For a nilpotent matrix e, its commutant algebra A={M:Me=eM} is a vector space. The invertible matrices in A form the nonempty principal open det(M)!=0, so GL_n^e is irreducible. Its surjective image PGL_n^e is connected. This establishes the centralizer condition for the adjoint group of either gl_n or sl_n.

This statement would be false with SL_n substituted for the adjoint group. For a regular nilpotent N, the commutant consists of polynomials d_0 I+d_1 N+...+d_{n-1}N^{n-1}; invertibility means d_0!=0, and determinant one means d_0^n=1. Over the stated field, the SL_n-centralizer has n components. In particular SL_2 already has two. The frozen proof avoids this error.

There is also an intrinsic proof of ambient-sheet containment which avoids worrying whether a chosen extension to the scalar center is one of the customary AI/AII/AIII formulas. On gl_n, the trace form pairs the two eigenspaces nondegenerately and orthogonally. For x in p, the maps ad(x):kappa->p and ad(x):p->kappa are transposes up to sign, so their ranks agree. Hence dim(G.x)=2 dim(K.x). The irreducible K-sheet S lies in g^{(2m)}. Distinct G-sheets of gl_n are disjoint; as the finitely many irreducible components of g^{(2m)}, they are consequently also open in that stratum. The irreducible S must lie in one of them. This is the type-A containment argument used in Bulois's proof of Theorem 13.2.

Every Lie algebra involution of gl_n preserves sl_n and the scalar center, and its center action is plus or minus the identity. Equivalently p=p_0 direct-sum z^-, and K acts trivially on z^-. Thus p^{(m)}=p_0^{(m)} x z^- and its sheets are S_0 x z^-. The slice also acquires exactly the z^- factor. This verifies that changing the center sign creates no missing quotient case. For sl_n, either the same rank argument or extension by a trivially acted-on scalar center yields the identical quotient problem; the group remains PGL_n. The trivial rank-zero case has the identity quotient.

## 6. Separation and the rank-one control

For the diagonal torus acting effectively by (a,b)->(ta,t^{-1}b), let S=A^2 minus the origin. The punctured axes are distinct K-orbits. The charts a!=0 and b!=0 have quotient coordinate c=ab and sections (1,c),(c,1). Their overlaps are c!=0, so their quotient is the doubled-origin line.

The morphisms alpha(z)=(1,z) and beta(z)=(z,1) are conjugate on z!=0 with conjugating parameter t=z. Any K-invariant morphism to a separated scheme or separated algebraic space therefore identifies alpha(0) and beta(0), by its closed diagonal. It cannot be an orbit-separating quotient. This proves exactly the separated obstruction.

The opening summary should say “K-invariant orbit-separating morphism” explicitly. Without invariance, the identity map of the separated scheme S would of course distinguish different orbits. The detailed frozen proof already assumes invariance; the accompanying one-line patch only makes the summary unambiguous.

## 7. Boundary of the result

The criterion and its gl_n/sl_n application pass this audit. In arbitrary type, disconnected adjoint centralizers obstruct this particular section argument; the audit does not claim that geometric quotients then fail. Hameister–Morrissey's Theorem 3.16 concerns the entire regular locus and cannot be promoted to all nonregular K-sheets. Constant orbit dimension, finite computations, or a quotient stack alone do not settle the missing cases.
