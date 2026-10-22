# Independent derivation freeze before candidate comparison

2026-10-16 05:46 UTC (approximate persistence; exact tool timestamp recorded subsequently). Candidate proof/results/reviews remain unread.

Let D=diag(a^-2,b^-2), p_i=(a cos t_i,b sin t_i), n_i=Dp_i, k_i=|n_i|, u_i=n_i/k_i, h_i=1/k_i. Put Delta_i=arg u_{i+1}-arg u_i modulo2pi. Feet satisfy q_i-M=(h_i-M·u_i)u_i. Signed shoelace gives

A'_m(M)=1/2 sum(h_i-M·u_i)(h_{i+1}-M·u_{i+1})sin Delta_i.

For paired opposite tangents (even primitive periods), linear terms cancel. Quadratic anisotropy telescopes using
cos theta_i cos theta_{i+1} sin Delta_i = (sin2Delta_i + sin2theta_{i+1}-sin2theta_i)/4.
Thus A'_m(M)=A'_m(0)+|M|²/8 sum sin2Delta_i.

For t_j-t_i=2v and (t_i+t_j)/2=u, confocal chord tangency gives sin²v=lambda*(b² cos²u+a² sin²u)/(a²b²). Outer vertices are (a cosu,b sinu)/cosv; their locus is x²*(a²-lambda)/a^4+y²*(b²-lambda)/b^4=1. For finite consecutive intersections, A'=ab sum tan((t_{i+1}-t_i)/2) with coherent lifts; formula extends signed stars.

An independently derived invariant density for boundary phase: write P=a²b², c²=a²-b², alpha=P-lambda c², beta=P+lambda c², gamma=P-lambda(a²+b²). Adjacent phases satisfy alpha cos t cos s+beta sin t sin s=gamma. Implicit differentiation gives ds/dt=sqrt(D(s))/sqrt(D(t)) where D(t)=4lambda P*(b²-lambda+c²sin²t)>0. Therefore dt/sqrt(b²-lambda+c²sin²t) is invariant and pi-periodic. The orientation-preserving billiard map is translation in its cumulative measure; primitive even period implies antipodal pairing at half period. No named elliptic-function identities are used.

Numerical N6 direct-collision checks, a=2,b=1, lambda=4/9, show A'_m(0)/A=9/8 and (sum sin2Delta_i)/A=1 at all phases tested. General a,b numerical checks suggest A'_m(0)/A=(a+b)²/(4ab) and sum sin2Delta_i/A=2/(ab). This is evidence, not proof.

For the axis-start N6 orbit, lambda=a²b²/(a+b)² and p0=(a,0), p1=(a²/(a+b),b sqrt[b(2a+b)]/(a+b)), p2=(-p1x,p1y), then antipodes. Exact axis evaluation gives A'A=4a²b²(2a+b)(a+2b)/(a+b)², and conjectured full N6 product A'A'_m=ab(2a+b)(a+2b)*(1+|M|²/(a+b)²). The axis evaluation alone does not establish phase invariance.

Strongest rigorous all-period result so far: arbitrary-M reduction under opposite tangent pairing; central symmetry from elementary invariant measure for primitive even elliptic-caustic orbits; explicit circle formula for every admissible winding and repeated traversal. Exact gap: prove both scalar products A'A'_m(0) and A' sum sin2Delta_i constant for general N=2mod4.
