# Independent universal reconstruction

This is a mathematical reconstruction of the published claims, not an adoption of a prior PASS. The primary manuscript was read in full before the claim freeze; the freeze preceded reading any review/adoption conclusions. The supplementary derivations were then read as mathematical objects and the calculations below checked independently. No computation proves the universal theorem by sampling.

## 1. Parameters, actual geometry, and completeness

Write alpha²=a²-lambda, beta²=b²-lambda, c²=a²-b². Strict a>b>0 and 0<lambda<b² give alpha>c>0, beta>0, k=c/alpha in (0,1), k'=beta/alpha, and a unique v in (0,K) with cn(v)=beta/b. The identities dn²(v)=1-k² sn²(v) give dn(v)=a beta/(alpha b), hence a=alpha dn(v)/cn(v), b=beta/cn(v).

Set P(w)=(-a sn(w),b cn(w)) and delta=2v. This is injective on the real boundary modulo 4K. The endpoints P(z-v),P(z+v) lie on the tangent to the caustic at C(z)=(-alpha sn(z),beta cn(z)): its normal is (-sn(z)/alpha,cn(z)/beta). The addition formulas give

    [dn(v) sn(z) sn(z±v)+cn(z) cn(z±v)]/cn(v)=1.

For example, putting s=sn(z), t=cn(z), d=dn(z), S=sn(v), C=cn(v), D=dn(v), both sides reduce to C[D²s²+t²]/[C(1-k²s²S²)]=1; the mixed terms cancel. Thus every constructed edge is a genuine tangent segment to the proper confocal caustic.

The confocal reflection assertion also has a direct check: for any unit direction e of a line through P=(a cos(theta),b sin(theta)), let m be its unit perpendicular. Tangency to the caustic is equivalent to

    lambda = a²m_x²+b²m_y²-(m·P)² = a²b² (e·n_E)²,
    n_E=(P_x/a²,P_y/b²).

Consequently the two chord directions have equal absolute normal component, with inbound/outbound signs, and equal directed tangential component on the chosen branch. They satisfy ordinary specular reflection. At any boundary point there are exactly two tangents to the strict inner ellipse, so there is no omitted forward branch with that caustic beyond orientation reversal. This verifies the geometry behind Stachel's full parametrization; his published Theorem 4.3 (PDF p.13, printed p.1614), including (4.9), expressly states this canonical parametrization and the coprime turning-number closure.

Closure with least N is N delta=4K tau, gcd(tau,N)=1. Choosing orientation gives 0<tau<N/2. No assumption tau=1 entered the construction. Since 0<delta<2K, successive boundary points are distinct and nonantipodal, so successive tangents meet finitely. Three distinct conic tangents cannot concur: their dual points would give three collinear points on a nondegenerate dual conic. Hence V_j=ell_j intersect ell_{j+1} are genuine vertices and the ordered outer side V_{j-1}V_j is exactly ell_j, including for a star.

For n(w)=(-sn(w)/a,cn(w)/b), projection of F+=(c,0) to n·X=1 gives

    Q(w)=(a(c-a sn(w))/(a-c sn(w)), ab cn(w)/(a-c sn(w))).

This follows by cancellation of (a+c sn(w)) in F+ +(1-n·F+)n/(n·n); n·n=(a-cs)(a+cs)/(a²b²). For real w the remaining denominator is at least a-c>0. Direct expansion gives Q·Q=a². The foot on the actual outer side is therefore this Q, without clipping to segments. Central negation and a shift by 2K give Q_-(w)=-Q(w+2K), so signed areas satisfy B_+=T(w), B_-=T(w+2K).

## 2. Full vector periods, exhaustive singularities, and local cancellation

Use p=iK' and r=K+p. On the sn torus with periods 4K,2p, sn has degree two. The standard quarter-shift identities are

    sn(r+z)=dn(z)/(k cn(z)),
    cn(r+z)=-i k'/(k cn(z)),
    dn(r+z)=i k' sn(z)/cn(z).

At a common Jacobi pole, numerator and denominator of Q are at most simple with nonzero leading denominator, so Q is removable. All remaining possible poles solve sn(w)=a/c=dn(v)/(k cn(v)). Their two roots on the sn torus are r-v,r+v. They are distinct and simple because sn(v),cn(v),dn(v) are strictly positive for 0<v<K; the displayed cn,dn and hence the denominator derivative -c cn(w)dn(w) are nonzero there. Degree two excludes further roots.

The vector Q has periods 4K,4p, not 4K,2p: translation by 2p preserves sn and negates cn, giving Q(w+2p)=JQ(w), J=diag(1,-1). The full vector torus has four possible poles, the two roots and their 2p translates. At r±v, cn=-ib/c and sn=a/c, so both numerator vectors are (-ab²/c,-iab²/c). The denominator derivatives are opposite. Thus the two simple residue vectors are R,-R. Translated-row residues are JR,-JR.

At a phase at which Q(w+j delta) has a pole, exactly two indices are singular, j and j+1 modulo N. Distinctness of the N residues modulo 4K follows from gcd(tau,N)=1; the two roots differ by exactly delta. There is no collision with the other imaginary row, since the real grid cannot shift by 2p modulo 4p. The singular edge has expansions

    Q_j=R/epsilon+A+O(epsilon),
    Q_{j+1}=-R/epsilon+B+O(epsilon).

Its double coefficient is det(R,-R)=0. Every other edge has at most one singular endpoint, hence at most a simple pole. N=3 shares one regular vertex between the other two edges; that does not create an extra singular factor. The closing edge is the same local argument because N delta=4K tau is an actual vector period. This proves a global upper bound, rather than merely cancelling a selected pole.

Cyclic reindexing gives a period delta for T; 4K is also a period, so Bezout gives L=4K/N. All root translates reduce to b0+p and b0+3p on X=C/(L Z+4p Z), b0=K-v. The two points are distinct. The proof only needs “at most simple”; it does not assume any residue is nonzero.

## 3. Reduced-torus characters, zeros, and the product

Q(2K-w)=JQ(w). Reflection and reversal of cyclic order each negate signed area, hence T(2K-w)=T(w). Also T(w+2p)=-T(w). With F(z)=T(b0+z), the reflection center shifts by delta, a period, so F is even. Its periods are L,4p, its antiperiod is 2p, and its only possible poles are simple at p,3p.

The points p+L/2 and 3p+L/2 are regular and distinct from the pole set. Evenness plus period L gives F(-p+L/2)=F(p+L/2); the 2p antiperiod gives the negative equality, so F(p+L/2)=0. Translation gives the second zero. These zeros cancel every possible simple pole of F(z)F(z+L/2), in both factors. The product is a holomorphic function on the compact torus and therefore constant. If F has no poles, compactness makes F constant and its antiperiod forces F=0. No division through an area or a residue is used.

For odd N, 2K=N L/2 equals L/2 modulo L. Thus B_+B_-=T(w)T(w+2K) is exactly that constant. This applies to every admitted coprime star winding. For even primitive N the shift is a full reduced real period and only gives B_+=B_-, without constancy of the square. The verified D,C fixtures give products 16 and 25 on one four-periodic family. A fixed s-fold traversal multiplies each shoelace sum by s, hence the product by s²; reversal negates each area. The circle is handled separately by rigid rotation of the regular-star vertices, which are the feet from the coincident center focus to its tangent lines. Hyperbolic/collapsed/grazing caustics are not proved here.

## 4. Independent check of the alternative bicentric/contact/Landen route

The projectivity T_+(x,y)=(a²(x+c)/(a²+cx),a²y/(a²+cx)) has positive denominator throughout the closed ellipse interior and positive homogeneous determinant a⁴b². It takes E to the circle S of radius r_b=a and agrees there with the focal-foot map. Substitution into the caustic equation gives

    A X²+B Y²-2D X+C0=0,
    A=a⁴/alpha²-c², B=b⁴/beta²,
    D=c a² lambda/alpha², C0=-a⁴ beta²/alpha²,
    A-B=-c² lambda²/(alpha² beta²), D²=-C0(B-A).

This ellipse contains O (its inverse image is (-c,0), inside the caustic) and has a focus at O. Its polarity q·R=a² gives an outer circle with center d=-c lambda/beta² and radius R=alpha b²/beta². In particular the polar line uses homogeneous coordinate -a²; the opposite sign gives a false center. Because the caustic image is strictly inside S and contains O, its polar circle is strictly outside S.

Intersections of the two original tangents at z-v,z+v give

    V(z)=(-a² sn(z)/alpha, b² cn(z)/beta),
    (R_x(z)-d)/R=(k-sn(z))/(1-k sn(z)),
    R_y(z)/R=k' cn(z)/(1-k sn(z)), R(z)=T_+(V(z)).

The transformed chords leave O on their left: the projectivity preserves the relevant side relation because its denominator stays positive. Each forward circle angular step is strictly between 0 and pi, including stars. Hence its tangent length t_j=r_b tan(epsilon_j)>0. Signed shoelace, in the trajectory order, gives

    Area(R)=r_b sum_j t_j,
    B_+=r_b³ sum_j t_j/(r_b²+t_j²).

No filled-star region area is substituted.

Set m_b=4k/(1+k)², K_b=(1+k)K, K_b'=(1+k)K'/2, and u=(1+k)(z-K)/2. To verify the quadratic shift without relying on a remembered convention, put

    f(z)=sqrt((1-k)/(1+k)) dn(z)/(1-k sn(z)).

Differentiation gives f'=sqrt((1-k)/(1+k)) k cn(z)/(1-k sn(z)) and

    f''=((1+k)²/4)[(2-m_b)f-2f³], f(K)=1, f'(K)=0.

The real ODE initial value problem identifies f(z)=dn(u,m_b). The circle coordinates above and -exp(2i am(u,m_b)) agree at z=K and have the same angular derivative (1+k)f(z), establishing their equality. With d0=-d>0 and t_M²=(R+d0)²-r_b², direct geometry now gives

    t_j=t_M dn(u_j,m_b), u_j=u0+j sigma,
    sigma=(1+k)v=2K_b tau/N.

One checks 4R d0=m_b t_M²; explicitly t_M²=lambda b²/(alpha-c)². The quadratic identities, or substitution of sn²(v)=lambda/b² into the addition formulas, give

    cn(sigma,m_b)=r_b/(R+d0),
    dn(sigma,m_b)=(R-d0)/(R+d0)>0.

Since r_b²+t_M² dn²(u)=(R+d0)²[1-m_b sn²(u)sn²(sigma)], sum the local identity

    dn(u+sigma)+dn(u-sigma)
      =2dn(u)dn(sigma)/[1-m_b sn²(u)sn²(sigma)]

over the closed cyclic grid. Its two left sums both equal sum dn(u_j), since N sigma=2K_b tau is a true dn period. Therefore

    B_+=[r_b³ t_M/(R²-d0²)] sum_j dn(u_j,m_b),
    B_+/Area(R)=r_b²/(R²-d0²).

This independently supplies the contact-area step; generic projective equivalence alone would not preserve Euclidean area.

For nome q_b, the standard Fourier expansion of dn has constant pi/(2K_b) and coefficients (2pi/K_b) q_b^h/(1+q_b^(2h)) cos(h pi u/K_b). A finite sum over N equally spaced shifts kills exactly the modes not divisible by N. Absolute uniform convergence on the real axis justifies this operation. With m_N of nome q_b^N and K_N its complete integral,

    sum_j dn(u+2jK_b/N,m_b)
      =(N K_N/K_b) dn((N K_N/K_b)u,m_N).

Coprime tau merely permutes this sum. Opposite original focus means w→w+2K, hence u→u+K_b; odd N sends the reduced argument to its real half-period. The old identity dn(x,m_N)dn(x+K_N,m_N)=sqrt(1-m_N) proves the product. The finite exact controls separately confirm the actual bicentric circle, contacts, and area ratio 2/15 in both triangular phases. This route uses classical analytic identities and additional checked geometry; it does not certify a historical publication of that geometry.

## 5. Independent inverse-area function-space reduction

For the unit inversion about F_-=(-c,0), translate its image back by F_-:

    R_-(w)=(c-a sn(w),b cn(w))/(a-c sn(w))².

Its signed area D_- is unchanged by that translation. Q_+(w)=a(a-c sn(w))R_-(w), whose factor is phase dependent, so this pointwise relation alone is not an area multiplier.

The only possible poles of R_- are the same r±v and their 2p translates, of order at most two; at a Jacobi pole the inverse vector tends to zero. At either root the finite original vector U=P-F_- is isotropic and U·U=(a-c sn(w))², so U0·U0=U0·U1=0. In complex dimension two U0 is nonzero and its orthogonal complement is its own line, so U1 is parallel to U0. The two roots have the same P value because P(r+z) is even in z. Both negative Laurent coefficients at both singular vertices are therefore collinear, cancelling fourth- and third-order edge terms. The cyclic area has order at most two.

Evenness of P about r gives, at w*=r-v,

    R_f(w*-epsilon+j delta)=R_f(w*+epsilon+(1-j)delta)

for either focus label f. The index permutation reverses cyclic order, so D_f is odd in epsilon about w*. The possible even double Laurent term vanishes. Thus D_- has only possible simple poles at b0+p,b0+3p on the same reduced torus, and its 2p antiperiod follows from reflection of the translated vectors. These are the pole and character facts actually needed from the earlier inverse proof; its headline theorem alone would not imply them.

The space of such functions has dimension at most one: the antiperiod fixes opposite residues at the two possible points; cancelling one residue against a nonzero member cancels both, leaving a holomorphic constant forced to zero by the antiperiod. D_- is nonzero because for real forward trajectories both foci lie inside the caustic, so every original chord determinant relative to either focus is positive; inversion divides it by positive squared distances. Hence B_+=gamma D_- with phase-independent gamma. Focus exchange gives the same gamma in B_-=gamma D_+. This does not divide through complex zeros. The earlier odd inverse-product theorem then implies the present product once the additional foot-pole lemma is supplied. This reduction is valid, but its mere derivability does not establish earlier printing of the target application. The exact controls independently give gamma=2016/5 in both triangular phases.

## 6. What this does and does not establish

The universal primary proof and the two auxiliary applications have no remaining mathematical gap identified in this reconstruction. They are informal, checkable derivations using established identities, not proof-assistant certificates. The separate exact finite checks test the actual construction, signs, boundary/caustic/reflection conditions and published numerical distinctions. They neither enumerate all admissible N nor replace the arguments above. No priority, causal independence, simultaneity, exhaustive literature coverage, or human peer review is established by this work.
