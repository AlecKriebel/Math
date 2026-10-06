# Independent geometry derivation before candidate exposure

Only the explicit claim has been received. No candidate proof, checker, reviews, sibling findings or priority conclusions were read. This is an independent geometry mechanism, subject to adversarial checking and source correspondence; no publication acceptance is made.

Let q=F_n>=2, p=F_{n-1}, F1=F2=1. Use only k=0,...,q-1. Each square root is its nonnegative real branch. The coordinates have norm1 by the identity 4t(1-t)+(1-2t)²=1 for0<=t<=1. For0<=i<j<q write d=j-i, h=d/q, delta=2pi pd/q, c=cos(delta), and

 s=(i+j)/q-1, A=1+h²-s².

The latitude constraints imply |s|<=1-h and hence A>=2h. Expanding the chord and using the cosine addition identity gives exactly

 |z_i-z_j|² = 4/q²[q(i+j)-2ij-2sqrt(ij(q-i)(q-j))c]
             = 2[A-c sqrt(A²-4h²)].                                      (1)

The radicand identity follows from
 16ij(q-i)(q-j)/q⁴=(1-(s-h)²)(1-(s+h)²)=A²-4h².
All radicands are nonnegative from the original latitude range. No signed square-root substitution occurs.

For fixed d, the actual discrete latitude centers are s=(2i+d)/q-1 for0<=i<=q-d-1. Relaxing to the continuous closed interval |s|<=1-h only lowers the minimum. It includes an unused south-pole limit, which is harmless for a lower bound and must not be treated as an actual extra point.

If c<=0 then (1)>=2A>=4h. If0<c<1, minimize f(A)=A-c sqrt(A²-4h²) on A>=2h. Its derivative is1-cA/sqrt(A²-4h²), zero uniquely at A*=2h/sqrt(1-c²), with f(A*)=2h sqrt(1-c²). The derivative is negative before and positive after this point, so

 |z_i-z_j|² >=4h |sin(delta)|.                                           (2)

The exact relaxed physical-latitude minimum when c>0 is4h|sin(delta)| if A*<=1+h²; otherwise it is the equatorial endpoint value2[(1+h²)-c(1-h²)]. At c<=0 the relaxed minimum is4h at a pole. Our proof only needs the universally valid weaker bound (2), regardless of whether A* is an allowed latitude center. Because gcd(p,q)=1, c=1 is impossible for1<=d<q. The antipodal-longitude case c=-1 is already included in c<=0.

It remains to earn d|sin(delta)|>=1 when c>0. This is the actual uniform arithmetic gap, not something assumed from a picture or stationary/packing claim. The following elementary integer argument closes it.

First Cassini gives

 p²+pq-q²=(-1)^n.                                                        (3)

It follows by induction: replacing (p,q) with (q,p+q) reverses the sign, and the initial (p,q)=(1,2) has value-1. Also p/q<=2/3: this holds at q2 and q3, and the ratios alternate under t->1/(1+t) in [1/2,2/3]. Equation(3) implies gcd(p,q)=1.

Replace d by t=min(d,q-d), so1<=t<=q/2, with the same cosine and absolute sine. Let m be a nearest integer to pt/q, rho=pt-qm, r=|rho|. Coprimality ensures r>0. Positive cosine is exactly r<q/4. The integer

 M=m²+mt-t²

is nonzero: if it vanished, (2m+t)²=5t², impossible for positive integer t (the5-adic exponents have different parity). Multiplying by q² and expanding gives

 q²M = (p²+pq-q²)t²-(2p+q)t rho+rho².                                   (4)

If tr<q/4, (3),(4), t<=q/2, r<q/4 and2p+q<=7q/3 imply

 q²<=|q²M|<=t²+(2p+q)tr+r²
       <q²(1/4+7/12+1/16)=43q²/48<q²,

a contradiction. Therefore tr>=q/4 whenever c>0. Concavity of sin on[0,pi/2] gives sin(2pi r/q)>=4r/q. Hence

 d|sin(delta)|>=t sin(2pi r/q)>=4tr/q>=1.

Combined with (2), every positive-cosine pair has squared distance>=4/q; every nonpositive-cosine pair has squared distance>=4d/q>=4/q. Independently, z0 is the north pole and |z0-z1|²=2-2(1-2/q)=4/q. Thus the claimed all-pair minimum is2/sqrt(q). This establishes the exact claim mathematically within its specified construction, still requiring independent audit and source confirmation; it is not a priority claim.

Boundary checks: q2 yields the north pole and an equatorial point with chord sqrt2. q3 has all nontrivial longitude cosines negative. The complement d->q-d preserves c and absolute sine but only improves the sufficient arithmetic bound since d>=t. No geodesic conversion, height shift or irrational longitude replacement is used. The alternative index set1,...,q is exactly congruent: k->q-k sends z_k to (X,-Y,-Z), the half-turn about the X axis, because p is integral. This is an independent congruence deduction; attribution to a printed source remains pending.

Certified finite controls will check (1), the arithmetic inequality, exact pole equality and all pair lower bounds for small Fibonacci denominators. These are finite corroboration, not the reason the theorem holds for unbounded n. No empirical claim of packing optimality or novelty is made.
