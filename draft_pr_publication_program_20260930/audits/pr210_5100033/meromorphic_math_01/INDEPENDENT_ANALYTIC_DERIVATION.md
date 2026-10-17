# Independent analytic reconstruction

This derivation was written from the frozen claim map, standard Jacobi identities and independent algebra. No old mathematical acceptance report has been read. The optional bicentric and transfer derivations were subsequently read as mathematical claims, not as acceptance evidence.

## Canonical chords and physical geometry
Set S=sn(v), C=cn(v), d=dn(v), and at a midpoint t use s=sn(t), h=cn(t), e=dn(t). Jacobi addition gives the endpoints P(t+-v). Their common chord has equation -s*x/alpha+h*y/beta=1: substituting either endpoint reduces its numerator to s²*d²+h²=1-k²*s²*S², exactly its addition-formula denominator. Hence that chord is tangent to the caustic at (-alpha*s,beta*h). This derivation is valid for every0<v<K and every real midpoint, with a positive addition denominator. It does not assume convex orbit order. The source canonical theorem supplies physical reflection; independent Euclidean checks below also test it at all sampled vertices.

## Complete divisor and residues
The denominator a-c*sn(w) is nonzero at every real w. At a sn/cn common pole, use reciprocal local coordinate1/sn(w); cn/sn extends holomorphically there, so both coordinates of Q extend. On C/(4K,2p), sn has two simple poles, hence degree2. Its finite value a/c>1 has exactly the two preimages r+-v, because the displayed quarter identities give those values and both derivatives are nonzero. There is no canceled denominator branch at a common Jacobi pole.
For alpha>0,k in(0,1), S,C,d>0,kprime²=1-k², the denominator derivative at r-v is +alpha*kprime²*S/C² and at r+v is its negative. The common numerator is -alpha²*d*kprime²/(k*C³)*(1,i), so
Res(Q,r-v)=-alpha*d/(k*C*S)*(1,i),
Res(Q,r+v)=+alpha*d/(k*C*S)*(1,i).
These are explicitly nonzero and collinear. On the true vector torus4K,4p, there are exactly the two additional J-reflected poles in the other row.

## Collision count, including N3 and cyclic cut
Divide real coordinates by L=4K/N. Pole sites differ bytau, and the orbit acts by j*tau moduloN. For any phase where a vertex lands on r-v, exactly one adjacent vertex (j+1 moduloN) lands on r+v; multiplication bytau permutes Z/N. No third vertex can be singular, and the other imaginary row cannot coincide because the phase increment is real. N3 leaves exactly one regular vertex, but its two incident determinant terms still have only a single singular endpoint. For the cyclic adjacent pair the two leading residues have zero determinant; all possible double coefficients therefore vanish. No assumption of nonzero area, simple polygon or tau1 is present.

## Reflection and constant product without divisor counting
For the trace, direct reindexing j -> -j-1 in each edge shows T(2K-w)=T(w): the orientation reversal minus sign cancels det(J)=-1. Since2v is a true trace period, F(z)=T(K-v+z) is even. The true vector imaginary shift gives F(z+2p)=-F(z). On C/(L,4p) the only potential poles are p,3p, and are at most simple. At p+L/2 the function is regular; evenness, L periodicity, and2p antiperiod imply F=-F, hence a zero. Translation gives the other complementary zero. Thus F(z)*F(z+L/2) has no poles, without needing a nonzero residue or an exact zero count. Compactness makes it constant, even if the area trace is zero. For oddN,2K congruentL/2 moduloL, so this is the physical two-focus product.
The boundary of the method for evenprimitiveN is exact:2K is then an integerL period, so it proves Bminus=Bplus, not constancy of their common square.

## Independent inversion transfer
Let U=(c-a*sn(w),b*cn(w)), D=a-c*sn(w), and R=U/D², the translated unit inverse about the opposite focus. The exact identity U.U=D² implies that at either of its paired double poles U0 is nonzero isotropic and U0.U1=0. In two complex dimensions the orthogonal complement of a nonzero isotropic vector is its own span. Thus the order-2 and order-1 vector Laurent coefficients are collinear withU0. At the adjacent poleU0 is identical. In the determinant of the paired double-pole vertices, orders4and3 consequently cancel, and every other incident edge has order at most2. The area trace initially has pole order<=2.
The same real reflection and imaginary antiperiod as above make its reduced trace even aboutb and odd aboutb+p; the latter removes every even Laurent coefficient at either pole. Consequently its area has at most simple poles at exactly the same two allowed sites as Bplus. For forward physical orbits, the opposite focus lies strictly inside the caustic, so each directed inverse-edge determinant is positive; the inverse area is not identically zero.
The vector space of traces with those two allowed simple poles and antiperiod2p has dimension at most1: the antiperiod ties their residues with opposite sign; matching one residue makes the difference holomorphic, and the antiperiod kills its constant. Hence Bplus=gamma*Dminus, with a phase-independent scalar, without division by either area at zero. The samegamma serves the other focus by shift2K. This independently verifies the manuscript's transfer mechanism and excludes the false shortcut that pointwise projectivity or u-dependent point scaling alone transports area.

## Bicentric/Landen route: independent check of the affirmative auxiliary claims

Put A=alpha², B=beta² and lambda=l. The projectivity matrix is
[[a²,0,a²c],[0,a²,0],[c,0,a²]].
Its determinant a⁴b² is positive; its denominator a²+cx is positive throughout the closed original ellipse. It carries the boundary to the radius-a circle. With line coordinates (X,Y,-a²), the dual of its caustic image is proportional to
B*(X²+Y²)+2c*l*X+A*c²-a⁴.
Completing the square gives exactly d=-c*l/B and R²=A*b⁴/B². This computation fixes the sign in the polarity. The original outer vertex at midpoint phasez is V=(-a²*sn(z)/alpha,b²*cn(z)/beta); its projective denominator a²*(1-k*sn(z)) is positive on the real axis, so the derived R vertices are finite.

The caustic contains the original focus (-c,0), because c<alpha; its projective image therefore contains the auxiliary-circle center. A directed original chord with the caustic to its left maps to a circle chord with the center to its left. Its positively oriented angle is in(0,pi), including every admitted star. Tangents to the radius-r circle at the two contacts meet with positive tangent length t_j=r*tan(epsilon_j). Direct signed determinant summation gives area(R)=r*sum(t_j) and Bplus=r³*sum(t_j/(r²+t_j²)); no unsigned star-face decomposition is involved.

For the dn parametrization, independently differentiate
f(z)=sqrt((1-k)/(1+k))*dn(z)/(1-k*sn(z)).
Then f'=sqrt((1-k)/(1+k))*k*cn(z)/(1-k*sn(z)) and
f''=((1+k)²/4)*[(2-m_b)*f-2*f³],
where m_b=4k/(1+k)². Also f(K)=1 and f'(K)=0. Uniqueness of the real analytic ODE solution yields f(z)=dn((1+k)*(z-K)/2,m_b), where m_b is a parameter. The normalized circumcircle coordinate has value-1 atz=K and angular derivative(1+k)*f; this identifies it with minus(cn(u)+i*sn(u))², including its sign and phase origin.
Writing d0=-d>0, the elementary relations
t_M²=lambda*b²/(alpha-c)² and 4R*d0/t_M²=4k/(1+k)²
then give t_j=t_M*dn(u_j,m_b), with positivity selecting the positive square root. The interval and sign selection are essential for star orbits.

The classical quadratic Gauss identities, checked against the old primary author text, give
cn(sigma,m_b)=r/(R+d0),
dn(sigma,m_b)=(R-d0)/(R+d0),
sigma=(1+k)*v.
The ordinary dn addition formula gives
dn(u+sigma)+dn(u-sigma)
=2*dn(u)*dn(sigma)/(1-m_b*sn²(u)*sn²(sigma)).
Since N*sigma=2K_b*tau is a true dn period, its cyclic sum reindexes exactly. Substitution in the contact-area sum gives
Bplus=[r³*t_M/(R²-d0²)]*sum_j dn(u+2j*K_b*tau/N,m_b),
and Bplus/area(R)=r²/(R²-d0²), exactly the manuscript coefficient. Every real denominator is positive because R>d0+r.

For completeness, the arbitrary-order dn reduction also follows directly from the absolutely convergent real Fourier series: summing shifts2j*K_b/N annihilates Fourier modes not divisible byN. Coprimality permits anytau to reorder those shifts. The surviving coefficients have nome q_b^N and normalization N*K_N/K_b, giving the scaled dn formula. For oddN the original opposite-focus shift u->u+K_b becomes a real half-period after reduction, so the old dn half-period identity gives the same constant product. These are mathematical verifications of the auxiliary route; they do not establish a historical priority claim.
