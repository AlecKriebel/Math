# Independent algebra derivation

This derivation was completed before reading the PR proof, checkers, or historical audit. Set J=[[0,-1],[1,0]], A_u=J⊕uE12 and 0<u<1/2. Changing the sign convention of J by orthogonal conjugacy changes none of the conclusions.

## Curvature from the connection

For the bracket [e0,v]=Av on an orthonormal abelian four-plane n, put S=(A+Aᵀ)/2 and K=(A−Aᵀ)/2. Koszul gives ∇₀₀=0, ∇₀v=Kv, ∇v₀=−Sv, and ∇vw=⟨Sv,w⟩e0. Contracting the curvature gives Ric=diag(−tr S², [A,Aᵀ]/2−(tr A)S), with zero mixed block. The independent code contracts the full Koszul formula for sixteen independent matrix entries and checks this polynomial identity exactly. In the trace-zero case Scal=−q, q=tr S², and

F=q²/(q²+||[A,Aᵀ]||²/4).

At A_u, q=u²/2 and Ric=diag(−u²/2,0,0,u²/2,−u²/2); hence F=1/3. The denominator is nonzero whenever u>0.

## Exact Hessian and its flat directions

Define G(A)=||[A,Aᵀ]||²−8q². Then F−1/3=−G/[12(q²+||[A,Aᵀ]||²/4)]. Thus proving G≥0 is equivalent to the desired local inequality. Along A(t)=exp(tX)A_u exp(−tX), take

X=[[a,b,p,q1],[b,−a,r,t1],[p,r,c,d],[q1,t1,d,−c]].

The scalar block traces commute with A and can be omitted. Exact expansion gives G'=0 and

G''=128(2−u²)(a²+b²)+16(p²+q1²+r²+t1²+4u p t1−4u q1 r).

The crossblock eigenvalues are 16(1+2u) and 16(1−2u), each twice. The six transverse variables (a,b,p,q1,r,t1) therefore have positive G Hessian for 0<u<1/2. The F Hessian is −G''/(9u⁴), with precisely two zero directions among these eight symmetric coordinates: c,d. The c direction changes u; the d tangent equals an infinitesimal orthogonal action on the nilpotent block. More strongly, every conjugate of a two-dimensional nonzero rank-one nilpotent block has F=1/3 when paired orthogonally with normal J: it is orthogonally equivalent to vE12. This identifies actual constant-value directions, rather than relying only on Hessian degeneracy.

## A complete local chart and Taylor proof

Let Z(z) have only the first trace-free symmetric block [[a,b],[b,−a]] and the arbitrary symmetric crossblock [[p,q1],[r,t1]], with zero second diagonal block. Consider

Φ(Q,z,v)=Q exp(Z(z)) A_v exp(−Z(z)) Qᵀ,

where Q lies in a local five-dimensional orthogonal section obtained by excluding the first-block rotation stabilizer. At z=0,v=u, the five orthogonal tangent directions, six Z directions, and ∂v A_v form a basis of the twelve-dimensional conjugacy orbit. A direct symbolic rank check gives 12. There are no exceptional parameters u>0: the crossblock orthogonal and symmetric generators jointly cover all eight off-diagonal generator entries; their commutator map has trivial kernel because J and vE12 have disjoint spectra. The first-block trace-free symmetric commutators have rank two. The second-block rotation and ∂v span its two-dimensional rank-one nilpotent orbit. The centralizer dimension is 2+2=4, since the crossblock commuting equations have only the zero solution. Thus the conjugacy orbit has dimension 16−4=12 and the inverse function theorem makes Φ a complete local chart.

G is invariant under Q. For every v near u, G(A_v)=0 and ∂zG(exp Z A_v exp−Z)|z=0=0. Choose a compact small interval of v inside (0,1/2). The six-variable Hessian at z=0 is uniformly positive there by the displayed eigenvalues. Continuity makes the Hessian positive in a product neighborhood. The integral Taylor formula then gives G(exp Z A_v exp−Z)≥κ||z||² for some κ>0. This is a proof of local maximality, including the flat v family.

Every nearby inner product on the fixed Lie algebra has an orthonormal basis consisting of a basis of the fixed abelian codimension-one n and its unit normal e0'=h e0+w. In that basis its bracket matrix is h P A_u P⁻¹, where h≠0 and P is invertible. The shift w makes no contribution because n is abelian. F is invariant under nonzero scalar multiplication of A. Local maximality on the conjugacy orbit therefore proves local maximality among all left-invariant metrics on the fixed simply connected group.

## Solvsoliton obstruction and larger same-group metric

If Ric=λI+D for a derivation D, its displayed block form gives [D_n,A_u]=d0 A_u. The J block has zero commutator, so d0=0 and λ=−u²/2. In the nilpotent block [D_n,uE12]=u³E12≠0. Thus the metric is not a solvsoliton.

For P=diag(2,1,2/u,1), its exact conjugate B=P A_u P⁻¹ is [[0,−2],[1/2,0]]⊕2E12. The independent calculation gives F(B)=625/1587 and F(B)−1/3=32/529>0. This is an explicit inner product on the same fixed Lie group.

## Boundary checks and limits

At u=0 the metric is flat and F is undefined; the argument explicitly excludes that endpoint. At u=1/2 the two eigenvalues 16(1−2u) vanish and this transverse Taylor proof does not decide local maximality. For u>1/2 those eigenvalues turn negative for G, giving directions of increasing F. The claimed open interval is consequently material. Orthogonal symmetry, scalar multiplication, and changes of bracket basis have been accounted for explicitly.

Strongest independent result: the exact claimed family, all-metrics local maximum, non-solvsoliton property, and strict same-group comparison are proved. No mathematical gap remains for this claim. Original-author proof and checker coverage have not yet been inspected at this checkpoint.
