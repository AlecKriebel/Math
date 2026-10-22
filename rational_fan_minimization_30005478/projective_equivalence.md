# Arbitrary rational fan minimization and projective rational points

Status: accepted partial reduction; see independent_reduction_audit.md. This is not a terminating algorithm and not an undecidability theorem. Scope is arbitrary finite rational fans, with no purity, balancing, or connectedness imposed.

## 1. From a loopless quiver to one Grassmannian incidence problem

Let a finite loopless quiver representation over Q have vector spaces M_v and rational arrow maps T_a:M_s -> M_t. Prescribe subrepresentation dimensions e_v. Set H=direct_sum_v M_v, h=dim H, and r=sum_v e_v. Seek an r-dimensional rational A subset H satisfying:

(a) dim(A intersection M_v)>=e_v for every vertex v;
(b) dim(A intersection G_a)>=e_s for every arrow a:s->t, where G_a={(x,T_a x):x in M_s} inside M_s direct_sum M_t subset H.

The coordinate intersections in (a) are disjoint and their lower bounds sum to dim A=r. Thus each has dimension exactly e_v and A=direct_sum_v A_v with A_v=A intersection M_v. Since s differs from t, projection of G_a to M_s is an isomorphism. Consequently A intersection G_a identifies with {x in A_s:T_a x in A_t}. Its dimension is at most e_s, and (b) holds if and only if T_a(A_s) subset A_t. This proves equivalence over Q and every extension field, using explicit rational linear algebra only.

## 2. Grassmann incidence to the minimum objective

Input: H=Q^h, 0<=r<=h, rational P_i subset H of dimensions p_i, integers k_i, and the question whether there is rational A in Gr(r,H) with dim(A intersection P_i)>=k_i. Handle k_i>min(r,p_i) as an immediate no instance, and discard constraints k_i<=max(0,r+p_i-h) as automatic. The nontrivial constraints have

t_i=h-p_i-r+k_i, with 0<=t_i<=h-r.

Let E and F be disjoint rational spaces, each of dimension h-r, and put W=H direct_sum E direct_sum F. Choose coordinate subspaces F_{t_i} subset F of dimension t_i. Form the finite family of rational spaces

H, E, F, V_i=P_i direct_sum F_{t_i}.

Set m=2h-r and f(U)=2 max_V dim(U+V)-dim U.

Claim: min over rational U subset W of f(U) equals m if and only if the incidence problem has a rational solution; it is always at least m.

Proof: write s=dim U, a=dim(U intersection H), b=dim(U intersection E). The individual objective terms for H and E are s+2h-2a and s+2(h-r)-2b. Their sum is 2m+2(s-a-b)>=2m. Thus f(U)>=m. If f(U)<=m, equality forces s=a+b and each anchor term=m. Hence U=A direct_sum B subset H direct_sum E and a-b=r. Since U misses F, its F term is s+2(h-r)<=m, giving s<=r. Combining s=a+b with a-b=r yields b=0,a=s=r. Therefore U=A subset H has exactly dimension r.

For such A, the H/E/F terms are all m. Moreover dim V_i=p_i+t_i=h-r+k_i, and A intersection V_i=A intersection P_i. Its individual objective term is r+2(h-r+k_i)-2 dim(A intersection P_i), which is <=m precisely when dim(A intersection P_i)>=k_i. This establishes both implications.

The boundary r=h is harmless: all incidence conditions are automatic or immediately impossible, and can be handled before the construction. Likewise r=0 can be decided immediately.

## 3. Projective universality: field issue explicitly addressed

Reineke's constructive proof realizes a projective zero locus as a quiver Grassmannian for a three-vertex acyclic quiver. It uses a Veronese embedding, linear forms obtained from the input equations, and monomial-deletion maps with 0/1 coefficients; the desired dimension vector is (0,1,1). Thus rational input equations give rational matrices. The construction and the Veronese inverse are defined over Q, so the correspondence preserves Q-points, rather than merely geometric points. Source inspected in full: Markus Reineke, Every projective variety is a quiver Grassmannian, https://arxiv.org/html/1204.5730 , especially the proof preceding the Schurian calculation. The Schurian property is not needed here.

A direct rational-point check avoids extracting d-th roots: the Veronese rank-one flattening has entries x_{n+e_i}, with n of total degree d-1. For a nonzero rank-one solution, choose any nonzero row. Its projective row coordinates give the preimage point of the Veronese embedding. If the flattened coordinates are rational, this row is rational, so its preimage is a Q-point. Thus a geometric isomorphism alone is not being used to infer arithmetic equivalence.

Combining this explicitly rational construction with Sections 1 and 2 gives an effective reduction from deciding whether a projective algebraic set over Q (not necessarily irreducible) has a Q-point to computing the rational-subspace minimum for arbitrary rational arrangements. This does not invoke or prove undecidability of rational-point decision.

## 4. Realizing arrangements as genuine rational fans

Given the finite rational spaces V, choose finitely many rational linear forms whose kernels intersect to give each V, and adjoin a basis of the ambient dual. The central hyperplane arrangement of all these forms defines a finite rational pointed fan. Take the subfan of its cones contained in the union of the V. Every V is a union of cones of this arrangement, with full-dimensional cones relative to V; the retained set is closed under faces and intersections. Its support is exactly the union of the V, and

dim(U+support)=max_V dim(U+V).

The fan need not be pure. This is essential to the stated scope; no reduction for the pure balanced case is asserted.

## 5. Reverse reduction

For each candidate r in {0,...,N} and integer m, define X_{r,m} subset Gr(r,N) over Q by dim(U+V_i)<=floor((m+r)/2) for every input span V_i. These are determinantal closed conditions, hence give an explicit projective incidence scheme. Its Q-points are exactly the rational witnesses with dim U=r and objective<=m. Emptiness over Q is unchanged on taking the reduced closed variety. A decision oracle for projective Q-points therefore tests finitely many r,m and computes the minimum. The possible value range is finite, for example 0 through N using U=ambient.

## Conclusion

Computing this arbitrary-fan rational minimum is equivalent, under effective finite reductions, to deciding Q-point existence for projective algebraic sets over Q (not necessarily irreducible). This is an obstruction classification, not a solution to the requested general algorithm. The reduction also explains why real quantifier elimination is insufficient in this generality. A separate explicit example gives rational minimum 7 and real minimum 6.

## Proof dependency and arithmetic completion

Section 3 is to be read together with Section 3 of independent_reduction_audit.md, which supplies the complete monomial recurrence, degree homogenization, and explicit rational Veronese inverse. The complex-source theorem alone is not the arithmetic justification. Sections 1, 2, 4, and 5 are elementary rational linear algebra, hyperplane-arrangement, and projective determinantal arguments; the independent audit checks their edge cases.
