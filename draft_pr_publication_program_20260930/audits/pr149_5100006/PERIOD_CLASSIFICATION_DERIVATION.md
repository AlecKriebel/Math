# ROOT derivation: complete least-period classification for focal products

This is a new proof candidate, not an accepted result. It strengthens the submitted k114 theorem and addresses the unqualified return-period wording rather than silently narrowing it.

Assumptions: a>b>0, c^2=a^2-b^2>0; a strictly nested confocal elliptical caustic with semiaxes alpha>beta>0 and c^2=alpha^2-beta^2. Stachel's canonical coordinate gives P(u)=(-a sn(u,k),b cn(u,k)), k=c/alpha in (0,1), and step delta=2v with 0<v<K, a=alpha dn(v)/cn(v), b=beta/cn(v). A real primitive n-periodic family has v=2K tau/n, gcd(tau,n)=1 and 0<tau<n/2. Circular boundaries are treated separately.

Claim: On every such noncircular family, the product of ordinary distances to either one fixed boundary focus is phase-independent if and only if the least period n is 2 modulo 4. For every positive integer r, the r-fold repeated product is constant if and only if the primitive product is constant. Thus for listed return length N=2 modulo 4 the assertion holds when its least period is 2 modulo 4 and fails when its least period is odd. This is a complete classification within the original nondegenerate elliptical-caustic setting.

Let g_+(u)=a+c sn(u,k) and g_-(u)=a-c sn(u,k). These equal the ordinary distances to (c,0) and (-c,0), respectively, and are strictly positive on the real axis because a>c. Set D_n^+(u)=product over j=0,...,n-1 of g_+(u+j delta), and similarly for g_-.

1. Odd primitive n.
Use the full sn lattice Lambda0=4K Z+2iK' Z. The only poles of each g are simple at p=iK' and p+2K. The zeros of g_- are p+K+v and p+K-v, from sn(K+iK' +/- v)=dn(v)/(k cn(v))=a/c. The zeros of g_+ are p-K+v and p-K-v, by the 2K antiperiod. These exhaust the zero divisors: the two zeros are distinct, nonpolar, and each g has exactly two simple poles.

Translation by delta=4K tau/n has order n. For odd n the pole orbits p+H and p+2K+H are disjoint: 2K=j delta mod4K would require n=2 tau j mod2n, impossible by parity. No zero orbit meets either pole orbit: a congruence +/- K +/- v = 2K epsilon+j delta modulo4K implies +/- n +/-2 tau =2n epsilon+4 tau j modulo4n; its left side is odd and its right side even. Therefore D_n^+ and D_n^- each have 2n uncancelled simple poles. They are nonconstant meromorphic functions. Since no real point is a pole, real-axis constancy would force complex constancy by the identity theorem, a contradiction.

2. Even primitive n=2m.
Primitivity implies tau odd and gcd(tau,m)=1. Opposite vertices pair because m delta=2K tau. Consequently the one-focus products are equal and both are
R_m(u)=product over j=0,...,m-1 of F(u+j delta), F(u)=a^2-c^2 sn(u,k)^2.

On Lambda=2K Z+2iK' Z, F has one double pole p and exactly two simple zeros p+K+v and p+K-v. Here delta=2K tau/m has order m. If m is odd, K is congruent to m v modulo2K, so K +/-v is h_+/- delta with h_+=(m+1)/2 and h_-=(m-1)/2. Both zero orbits coincide with the pole orbit, cancelling its double poles. Hence div(R_m)=0 and compact-torus holomorphy makes R_m constant and positive.

If m is even, neither zero orbit can meet the pole orbit: K +/-v =j delta modulo2K would require m +/-tau=2 tau j modulo2m; the left side is odd and the right side even. Hence R_m has m uncancelled double poles and is nonconstant, also on its real phase line by the identity theorem.

3. Repetition and circles.
The r-fold product is (D_n^+/-)^r. Because the real product is strictly positive, the map x -> x^r is injective; repetition preserves constancy exactly and cannot repair nonconstancy. For a circle the two foci coincide with the center, every focal distance equals a, and every listed product is a^N.

Boundary cases: n=2 is excluded by 0<v<K and a nondegenerate strictly nested elliptic caustic. Hyperbolic and degenerate caustics are outside the actual source setting. Orientation reversal changes only the order of the factors.

Priority: unresolved until the literature audit is complete. Standard Stachel parametrization, Jacobi identities and compact-torus arguments are credited. The odd/even nonconstancy extension is ROOT's current derivation and requires independent adversarial verification.
