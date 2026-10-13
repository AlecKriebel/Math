Independent construction and convention derivations

Write N=F_n and A=F_(n-1). For nontrivial sizes N>=2, use the companion's F_1=F_2=1, F_n=F_(n-1)+F_(n-2); thus n>=3. Distinguish the report's labels r_k from the companion's labels c_j throughout.

1. Lambert map, sphere and measure

Both primary bodies display Phi(alpha,tau)=(2*sqrt(tau*(1-tau))*cos(2*pi*alpha),2*sqrt(tau*(1-tau))*sin(2*pi*alpha),1-2*tau), with alpha,tau in [0,1]. Alpha is the angular coordinate, tau is latitude parameter. Its squared norm is 4*tau*(1-tau)+(1-2*tau)^2=1. Tau=0 is the north pole, tau=1 the south pole, and tau=1/2 the equator. Alpha is periodic modulo1, while tau=0 and1 are different points. Longitude is immaterial at either pole. For 0<tau<1 let theta=2*pi*alpha and h=1-2*tau. Unit-sphere surface area in these coordinates is dtheta*dh in absolute value, so dA=4*pi*dalpha*dtau. The companion's probability surface measure sigma=dA/(4*pi) therefore corresponds to planar area. Equal area does not mean equal pair distances; planar least-distance formulas do not transfer through Phi as isometries.

2. Chord and endpoint

For p=Phi(alpha,t) and q=Phi(beta,u), expansion of their Euclidean dot product gives

|p-q|^2=4*(t+u-2*t*u-2*sqrt(t*(1-t)*u*(1-u))*cos(2*pi*(alpha-beta))).

The report's displayed construction is r_k=Phi({k*A/N},k/N), 0<=k<N. Fractional parts can be omitted inside cosine/sine. The north-pole endpoint r_0=(0,0,1) gives |r_0-r_k|^2=4*k/N, hence |r_0-r_1|=2/sqrt(N). This proves only the distance of that pair. It does not prove |r_i-r_j|^2>=4/N for every pair. The source conjecture asks for exactly that additional inequality, under its displayed unshifted construction.

Unit-sphere geodesic distance is 2*arcsin(|p-q|/2), so this endpoint has geodesic distance 2*arcsin(1/sqrt(N)), not 2/sqrt(N). The function is strictly increasing: the minimizing pair is unchanged but the claimed numerical value changes. Sphere radius R multiplies the chord and arc by R. Both sources explicitly use radius1.

3. Companion coordinate order and exact relabeling

Companion §5.2 prints the lattice point as (j/N,{j*A/N}) and c_j=Phi(j/N,{j*A/N}), 0<=j<N, before setting its spherical point set to {c_0,...,c_(N-1)}. Its vector definition has a subscript m although j (printed n) varies; the subsequent lattice and z_n labels identify the intended varying point index. This notation slip does not authorize swapping Phi's arguments without proof. In particular, for N>=2 its same-labeled endpoint pair satisfies |c_0-c_1|^2=4*A/N.

Consecutive Fibonacci numbers are coprime by the Euclidean algorithm. Set D_n=F_n*F_(n-2)-F_(n-1)^2 for n>=3. D_3=1 and the recurrence gives D_(n+1)=-D_n, so D_n=(-1)^(n-1). Reducing modulo N yields A^2=(-1)^n mod N. Put s=(-1)^n. The multiplication map j -> k=j*A mod N is a bijection of 0,...,N-1, with inverse k -> j=s*k*A mod N. For that k, k*A=s*j mod N. It follows exactly that

r_k = T_s(c_j), where T_s(x,y,z)=(x,s*y,z).

T_s is an isometry (identity for even n, reflection for odd n). Consequently the unordered sets have the same pair-distance multiset. The label r_1 corresponds to c_(s*A mod N), not usually c_1. For n=5, N=5,A=3, it corresponds to c_2; the squared chords of the report and companion same-labeled pairs are respectively4/5 and12/5. This resolves construction correspondence without conflating labels or asserting a minimum theorem.

4. Source endpoint set slip and possible extension

The report displays k=0,...,N-1, then prints its set as {z_1,...,z_N}, then explicitly asks about z_0,z_1. The coherent convention for its displayed definition and question is {r_0,...,r_(N-1)}. Literal z_N is not defined in the stated range. If the displayed formula is deliberately extended to k=N, it is the south pole, and the set {r_1,...,r_N} lacks the north pole used in the question. This extension happens to give an isometric unordered set: for 1<=k<=N,

r_(N-k)=(r_k.x,-r_k.y,-r_k.z),

since A is integer and the cosine/sine angle at N-k is the negative angle at k modulo2*pi. This rotation preserves all pair distances but cannot justify the literal statement that r_0 belongs to {r_1,...,r_N}. Including both endpoints gives N+1 distinct latitudes/points; omitting both gives N-1. Neither is the source's N-point construction. The midpoint shift tau=(k+1/2)/N is different again: it removes both poles and destroys the indicated pole-pair identity. The report mentions shifted configurations separately for numerical integration, not as its least-distance conjecture's definition.

5. Degenerate sizes and limited checks

The original contribution does not state an n-range or Fibonacci seeds. The companion supplies F_1=F_2=1 and the recurrence for m>2. For n=2 the construction has N=1 and one north-pole point; no distinct pair or r_1 exists. For n=1 the report's A=F_0 additionally requires a seed not supplied there; setting F_0=0 would still give a singleton. A least-pair theorem must restrict to N>=2, equivalently n>=3 under these seeds, or explicitly qualify the singleton. At n=3,N=2 there is exactly one pair; its distance is sqrt(2)=2/sqrt(N). No all-size minimum assertion follows from this boundary observation.

CONVENTION_CONTROLS.json records exact integer/Fraction permutation and pair-value checks for n=3..20. Floating coordinate/norm/reflection diagnostics use tolerance3e-14 and observed isometry error1.191874962812805e-15. They are finite floating diagnostics, not validated intervals or a universal proof. Negative controls reject changing the midpoint latitude, rational rotation to an irrational golden-ratio angle, chord to arc, radius1 to2, point count and endpoint labels. The pole-pair distance alone fails to detect changed longitude, because a pole's distance is independent of longitude; an explicit coordinate check is retained to expose that failure model.
