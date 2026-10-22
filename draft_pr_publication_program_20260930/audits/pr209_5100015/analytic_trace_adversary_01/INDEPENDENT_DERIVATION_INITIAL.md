# Independent initial derivation

Written before source inspection.

Put P(u)=(a sn(u,k),b cn(u,k)), with real modulus 0<k<1. Write K=K(k), v=2K*tau/N, and choose b>0, a/b=dn(v)/sqrt(1-k^2), lambda=b^2 sn(v)^2. Then lambda is proper, a>b, k^2=(a^2-b^2)/(a^2-lambda), and u_j=u_0+2jv is the closed torsion orbit. Direct Jacobi addition gives its chord equation at endpoints u+/-v as (dn(v) sn(u)/cn(v))*x/a + (cn(u)/cn(v))*y/b=1; the tangency condition to the proper confocal caustic follows immediately.

The boundary tangent intersections are exactly

R_j=(a dn(v)/cn(v) sn(u_j+v), b/cn(v) cn(u_j+v)).

Thus, writing S_l(u)=1/2 sum_j det((sn(u_j),cn(u_j)),(sn(u_j+l),cn(u_j+l))),

A(R)=a b dn(v)/cn(v)^2 * S_{2v}(u+v).

For an eccentric-angle parametrization P(t)=(a cos t,b sin t), a second independent direct formula is

A(R)=ab sum_j tan((t_{j+1}-t_j)/2),

and orthogonal feet satisfy

Q(t)=(a b^2 cos(t)/D(t), a^2 b sin(t)/D(t)), D(t)=b^2 cos(t)^2+a^2 sin(t)^2,
A(Q)=(a^3 b^3/2) sum_j sin(t_{j+1}-t_j)/(D(t_j)D(t_{j+1})).

These are signed formulas; the orientation in the chosen u parameter is clockwise.

Set w=K-v. With C=cn(w), D=dn(w)=b/a, the Jacobi sums yield

Q_j=diag(b^2/(2a C D), b/(2C)) * (V_j-V_{j-1}),
V_j=(sn(u_j-w),cn(u_j-w)).

The minus sign follows from V(u+2K)=-V(u) and 2w=2K-2v. Consequently

A(Q)=b^3/(4a C^2 D) * (2 S_{2v}(u-w)-S_{4v}(u-w)).

This converts the problem to a universal identity between finite traces of elliptic functions. It also exposes that a proof based merely on cancellation of all trace poles would be suspicious: the trace summand h_l(z)=sn(z)cn(z+l)-cn(z)sn(z+l) has nontrivial complex poles. The real area formulas have no denominators zero for real phase in the proper regime (C,cn(v)>0; D(t)>0).

Parity to attack: the normalized polygon area trace has real periods 2K and 2v. For odd N its reduced real period is 2K/N, and v is an integer multiple of it; for even N=2M its reduced period is 2K/M, with v an odd half-period. The difference construction also changes at divisibility by 4. This is a mechanism to test, not yet a proof of the product identity.
