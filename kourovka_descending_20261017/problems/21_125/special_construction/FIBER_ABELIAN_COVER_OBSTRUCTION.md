# Exact algebraic obstruction to fiber-abelian canonical covers

October24,2026 UTC. This is a supporting exclusion of a particular construction mechanism, not a negative answer about virtual specialness. The canonical square complex may be replaced by a different cubulation.

Let X_r be the established one-vertex Hydra square complex on s,u_1,...,u_r with squares s u_i=u_i u_(i-1), setting u_0=s. Its big immersed hyperplane has midpoint vertices of types s,u_1,...,u_(r-1). The remaining midpoint type u_r belongs to a separate hyperplane. The big hyperplane has a loop of transport u_1 at type s; a tree edge of transport u_(i+1) from type s to type u_i; and a loop of transport s at every type u_i (1≤i≤r−1). Therefore the subgroup of transport at its s-midpoint is
\[
P_r=\langle u_1,\ u_2 s u_2^{-1},\ldots,u_r s u_r^{-1}\rangle.
\]
This description follows directly by following the two pairs of opposite sides in each square; it does not assume that the base hyperplane is embedded.

For a regular finite cover defined by ρ:H_r→Q, two s-edges starting at g,h have the same lifted hyperplane exactly when their Q-coordinates lie in the same **left coset** gρ(P_r). Equivalently, their coordinates satisfy g^−1h∈ρ(P_r). The u_i-edge starting at1 is opposite to the s-edge starting at u_(i+1)^−1 in a square. Consequently, if ρ(u_(i+1)) belongs to ρ(P_r), the s and u_i sides of the square at1 belong to the same hyperplane: that cover has a self-crossing hyperplane.

**Proposition.** If r≥3 and ρ factors through the quotient obtained by abelianizing the original free fiber F_r, the canonical cover has a self-crossing hyperplane. In fact this occurs in each square i≤r−2.

**Proof.** Work first in the integral quotient M_r=Z^r⋊<t>. Write vectors in the original a_i basis, put s=t^−1, and write φ=I+J, where J e_i=e_(i−1) and J e_1=0. In normal form (v,k)=v t^k, multiplication is
\[
(v,k)(w,l)=(v+\varphi^{-k}w,k+l).
\]
Conjugating s by u=(v,k) gives
\[
u^{-1}s u=(\varphi^k Jv,-1).
\]
Start u_r=(e_r,0) and use u_(i−1)=u_i^-1 s u_i. Thus all u_i for i<r have t-height−1, lower-fiber support, and
\[
u_1=(e_1,-1),\qquad u_r s u_r^{-1}=(-e_(r−1),-1).
\]
Both elements U=(e_1,-1), V=(-e_(r−1),-1) belong to the image of P_r. Their commutator in the convention [x,y]=xyx^-1y^-1 is exactly
\[
[U,V]=(-e_(r−2),0).
\]
Conjugation by V acts on fiber vectors by φ, so repeated commutators [V,w] apply J to w. After r−3 such steps we obtain (-e_1,0). This puts a_1 and hence s=a_1^-1 U in the image of P_r. Since V s^-1=(-e_(r−1),0), the image also contains a_(r−1); successive commutators with s recover a_(r−2),...,a_1. It therefore contains every u_i for i<r, whose vector lies in these coordinates and whose height is−1.

Passing to any further quotient Q preserves these subgroup membership identities. In particular ρ(u_(i+1)) belongs to ρ(P_r) for i≤r−2, giving the asserted self-crossing. This proves the proposition.

The proposition covers all regular finite quotients with abelian original fiber image, not all finite metabelian quotients and not all finite covers. It rules out using only the explicit finite filiform quotients to clean the canonical complex. It says nothing about the reported existing rank3/4 virtual-specialness proofs, which can use different quotients or different cubulations. A successful arbitrary-rank construction requires a genuinely nonabelian fiber image or a different complex.
