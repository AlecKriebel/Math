# Independent local check of the N=3 complex critical point

This supplements the frozen real-geometry derivation without changing it. It does not assume the global divisor argument or any inherited reviewer verdict.

For primitive closure, 3v=2K is equivalent to (N,tau)=(3,1). The exact triple-angle values are dn(3v)=1 and cn(3v)=-1, so L0=Z and L1=-Z. The second denominator factor in (8) is Z(1-k sn(u)). At u*=K+iK', the standard quarter-shift identity gives sn(u*)=1/k. Therefore cn(u*)^2=-(1-k^2)/k^2 is nonzero, whereas dn(u*)=0.

The Jacobi derivative formulas give

    sn'(u*)=cn(u*)dn(u*)=0,
    sn''(u*)=-sn(u*)[dn(u*)^2+k^2 cn(u*)^2]=(1-k^2)/k != 0,
    dn'(u*)=-k^2 sn(u*)cn(u*)=-k cn(u*) != 0.

Writing epsilon=u-u*,

    1-k sn(u)=-(1-k^2)epsilon^2/2+O(epsilon^3),
    dn(u)=dn'(u*)epsilon+O(epsilon^2).

The other factors at u* are D(u*)=1-t=q>0 and d+kC sn(u*)=d+C>0. Thus (8) has exactly one simple pole here, with nonzero residue

    -2 C0 q dn'(u*) / [(1-k^2) Z (d+C)^2].

This independently verifies the claimed order reduction at the merged triple-angle roots. It is stronger than an unexamined assertion of two simple roots merging: the numerator zero cancels exactly one of the two denominator orders. No conclusion about the cyclic sum's divisor follows from this local calculation alone.
