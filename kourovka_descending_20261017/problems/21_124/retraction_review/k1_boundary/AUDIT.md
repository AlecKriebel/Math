# Independent k=1 boundary audit

UTC: 2026-10-24T22:33:18.867587+00:00. Audit completion estimate: 100%. Mathematical scope: **PASS for k=1 only**. This is not a resolution of Kourovka 21.124 and no originality claim is made.

Only `negative_geometric/FINITE_HOLONOMY_FILTER.md` and its cellular checker `check_covers.py` were read. In particular the all-k retraction delta and other approach families were not read.

Let G_1 have the exact presentation

G_1 = <a,b,c,t | tat^-1=a, tbt^-1=ba, tct^-1=caba^-1b^-1>.

Put V=Z^4, let P(v)_i=v_(i+1 mod4), A=(1,0,-1,0), and T=(0,0,1,1). Use the semidirect multiplication

(v,P^j)(w,P^l)=(v+P^j w,P^(j+l)).

Define the proposed images

rho(a)=(A,1), rho(t)=(T,1), rho(b)=(0,P), rho(c)=(0,P^2).

The first relation holds because translations commute. The exact vector equations for the other two relations are

T-PT=(0,-1,0,1)=PA,

T-P^2T=(-1,-1,1,1)=P^2A-P^3A.

Indeed rho(tbt^-1)=(T-PT,P)=rho(ba), and rho(tct^-1)=(T-P^2T,P^2)=rho(caba^-1b^-1). Thus these images define a homomorphism G_1 -> Z^4 semidirect C_4, with finite holonomy. This derives the affine model directly, independently of any cellular sign convention.

Let q:G_1 -> C_4 be a,t -> 0, b -> 1, c -> 2 and put H=ker q. The map is onto because q(b)=1, so H is an index-four normal subgroup and a belongs to H. On H, rho has trivial linear part. Therefore, writing rho(h)=(v(h),1), the map

f:H -> Z, f(h)=v(h)_0

is a group homomorphism. It satisfies f(a)=A_0=1, not merely a nonzero multiple. Consequently

r:H -> <a>, r(h)=a^{f(h)}

is a retraction onto the **exact subgroup <a>**, since r(a^n)=a^n for every integer n. Also a has infinite order because rho(a)^n=(nA,1) is nonidentity for n!=0; no independent free-by-cyclic assertion is needed for this fact.

No finite-index rescaling or replacement of <a> by <a^e> is required. Even a merely nonzero integer character evaluation would be enough after passing to the preimage of its value subgroup, but this construction already gives evaluation one.

The independent checker uses exact integer semidirect multiplication and verifies the three presentation relators. It also checks a bounded collection of kernel-word character products and powers a^n. The complete proof is the group law and kernel argument above; the bounded checks alone are not claimed to prove the universal assertion.

This validates the k=1 finite-cover cocycle as well as the stronger exact cyclic virtual-retraction conclusion. It provides no conclusion for k>=2, no RAAG embedding, and no virtual-specialness theorem. No objection remains in the audited k=1 scope.
